import os
import csv
import pandas as pd
import re
from datetime import datetime, timedelta
from multiprocessing import Process
import multiprocessing as mp

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.db import IntegrityError, transaction
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.contrib.auth.models import User


# -----------------------------------------------------------------------------
# Helper Functions (findCVVar and findCVunit remain unchanged)
# -----------------------------------------------------------------------------
def findCVVar(var):
    varf = var.lower().title()
    cvvars = CvVariablename.objects.filter(name__icontains=varf)
    finalvar = None
    tmpvarfcum = ''
    tmpvarf = ''
    with open('varmap.csv', 'r') as mapfile:
        reader = csv.reader(mapfile)
        for row in reader:
            if var.upper() == row[0]:
                finalvar = CvVariablename.objects.filter(name=row[2])
                if finalvar.exists():
                    return finalvar.first()
    if cvvars.count() == 1:
        return cvvars.first()
    else:
        varfsubs = varf.split()
        for tmpvarf in varfsubs:
            cvvars = CvVariablename.objects.filter(name__icontains=tmpvarf)
            if cvvars.exists():
                return cvvars.first()
            else:
                tmpvarfcum += ' ' + tmpvarf
                cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)
                if cvvars.exists():
                    return cvvars.first()
        cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)
        if cvvars.count() == 1:
            return cvvars.first()
        varfsubs = varf.split()
        tmpvarfcum = ''
        for tmpvarf in varfsubs:
            cvvars = CvVariablename.objects.filter(name__icontains=tmpvarf)
            if cvvars.exists():
                return cvvars.first()
            else:
                tmpvarfcum += ' ' + tmpvarf
                cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)
                if cvvars.exists():
                    return cvvars.first()
    return None


def findCVunit(unit):
    unitf = unit.lower()
    cvunits = []
    with open('unitmap.csv', 'r') as mapfile:
        reader = csv.reader(mapfile)
        for row in reader:
            if unit == row[1]:
                cvunits = CvUnitstype.objects.filter(name__icontains=row[2])
                if cvunits.exists():
                    return cvunits.first()
    cvunits = CvUnitstype.objects.filter(name__icontains=unit)
    if cvunits.exists():
        return cvunits.first()
    return None


# -----------------------------------------------------------------------------
# Main function: loadtimeseries (uses Pandas, caching, bulk inserts, and duplicate checks)
# -----------------------------------------------------------------------------
def loadtimeseries(directory, filename):
    with transaction.atomic():
        with open('logtimeseriessampleNewPREP2025b.log', 'a') as lfile:
            lfile.writelines(f"Processing file: {filename}\n")

            # Caches for repeated lookups
            samplingfeature_cache = {}
            variable_cache = {}
            unit_cache = {}
            featureactions_cache = {}
            result_cache = {}
            # Cache for latest date per result (to avoid duplicates)
            result_last_date_cache = {}

            # Bulk list for Timeseriesresultvalues objects and batch size
            bulktimeseriesvalues = []
            bulk_batch_size = 5000
            bulkcount = 0

            # Pre-fetch common lookup objects
            try:
                censorcode = CvCensorcode.objects.get(name="Not censored")
                qualitycodegood = CvQualitycode.objects.get(name="Good")
                qualitycodebad = CvQualitycode.objects.get(name="Bad")
                annotationtypecv = CvAnnotationtype.objects.get(name="Time series result value annotation")
                annotator = People.objects.get(personid=1)
                newtimeunit = Units.objects.get(unitsname='minute')
                vt = CvVariabletype.objects.get(name='Water quality')
                sm = CvMedium.objects.get(name='Liquid aqueous')
                resulttype = CvResulttype.objects.get(name='Time series coverage')
                plevel = Processinglevels.objects.get(processinglevelid=1)
                aggstat = CvAggregationstatistic.objects.get(name='Average')
                actiontype = CvActiontype.objects.get(name='Equipment deployment')
                meth = Methods.objects.get(methodid=4)
            except Exception as e:
                lfile.writelines("Error in pre-fetch lookups: " + str(e) + "\n")
                return

            # Use Pandas to read CSV file
            if filename.endswith(".csv"):
                filepath = os.path.join(directory, filename)
                print(filepath)
                try:
                    df = pd.read_csv(filepath)
                except Exception as e:
                    lfile.writelines("Error reading CSV file: " + str(e) + "\n")
                    return

                # Expected CSV columns:
                # [2]: Sampling Feature Code, [3]: Date, [4]: Time, [5]: Variable,
                # [6]: Value, [7]: Unit, [8]: Valid, [9]: Result Comment
                for row in df.itertuples(index=False, name=None):
                    if len(row) < 10:
                        continue

                    # Parse datetime from Date and Time columns
                    try:
                        try:
                            datet = datetime.strptime(str(row[3])[:10] + ' ' + str(row[4])[11:], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                datet = datetime.strptime(str(row[3]) + ' ' + str(row[4]), '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                datet = datetime.strptime(str(row[3]) + ' ' + str(row[4]), '%Y-%m-%d %H:%M')
                    except Exception as e:
                        lfile.writelines('Bad date: ' + str(row[3]) + ' ' + str(row[4]) + '\n')
                        lfile.writelines(str(row) + '\n')
                        continue

                    # Retrieve or cache Sampling Feature (from column index 2)
                    sf_code = str(row[2]).strip()
                    if sf_code in samplingfeature_cache:
                        newsf = samplingfeature_cache[sf_code]
                    else:
                        sfs = Samplingfeatures.objects.filter(samplingfeaturecode__iexact=sf_code)
                        if sfs.exists():
                            newsf = sfs.first()
                            samplingfeature_cache[sf_code] = newsf
                        else:
                            lfile.writelines('No site match for: ' + sf_code.lower() + "\n")
                            continue

                    # Process Variable (column index 5)
                    var = str(row[5]).strip()
                    if var in variable_cache:
                        newvar = variable_cache[var]
                    else:
                        stdvar = findCVVar(var)
                        if not stdvar:
                            stdvar = CvVariablename(term=var, name=var, definition=' new cv variable for NH DES')
                            stdvar.save()
                            lfile.writelines('New cv variable created\n')
                            lfile.writelines(str(stdvar) + '\n')
                        newvars = Variables.objects.filter(variable_name=stdvar)
                        if newvars.exists():
                            newvar = newvars.first()
                        else:
                            newvar = Variables(
                                variable_type=vt,
                                variablecode=var.lower().title(),
                                variable_name=stdvar,
                                variabledefinition=var.lower().title() + ' from NHDES timeseries',
                                nodatavalue=-9999
                            )
                            newvar.save()
                            lfile.writelines('New variable created: ' + str(newvar) + '\n')
                            lfile.writelines(str(row) + '\n')
                        variable_cache[var] = newvar

                    # Process Unit (column index 7)
                    unit_val = str(row[7]).strip()
                    if unit_val in unit_cache:
                        newunit = unit_cache[unit_val]
                    else:
                        newunits = Units.objects.filter(unitsabbreviation=unit_val.lower())
                        if newunits.exists() and newunits.count() == 1:
                            newunit = newunits.first()
                        else:
                            ut = findCVunit(unit_val)
                            if not ut:
                                ut = CvUnitstype(name=unit_val, term=unit_val,
                                                 definition=' new cv unit type for NH DES')
                                ut.save()
                            newunit = Units(unit_type=ut, unitsabbreviation=unit_val.lower(),
                                            unitsname=unit_val.lower())
                            newunit.save()
                            lfile.writelines('New unit created: ' + str(newunit) + '\n')
                            lfile.writelines(str(row) + '\n')
                        unit_cache[unit_val] = newunit

                    # Retrieve or cache Feature Actions based on Sampling Feature
                    if newsf.pk in featureactions_cache:
                        newfa = featureactions_cache[newsf.pk]
                    else:
                        fas = Featureactions.objects.filter(samplingfeatureid=newsf, action__action_type=actiontype)
                        if fas.exists():
                            newfa = fas.first()
                        else:
                            actiondescription = var.lower().title() + ' imported from NHDES'
                            newaction = Actions(action_type=actiontype, method=meth,
                                                begindatetime=datet,
                                                actiondescription=actiondescription)
                            newaction.save()
                            newfa = Featureactions(samplingfeatureid=newsf, action=newaction)
                            newfa.save()
                        featureactions_cache[newsf.pk] = newfa

                    # Process Results and Timeseries Results using cache keyed on (featureaction, variable, unit)
                    key = (newfa.pk, newvar.pk, newunit.pk)
                    if key in result_cache:
                        r = result_cache[key]
                        try:
                            tsr = Timeseriesresults.objects.get(resultid=r)
                        except ObjectDoesNotExist:
                            lfile.writelines('No timeseries result for existing result: ' + str(r) + '\n')
                            lfile.writelines(str(row) + '\n')
                            continue
                    else:
                        rs = Results.objects.filter(featureactionid=newfa, variableid=newvar, unitsid=newunit)
                        if rs.exists():
                            r = rs.first()
                            try:
                                tsr = Timeseriesresults.objects.get(resultid=r)
                            except ObjectDoesNotExist:
                                lfile.writelines('No timeseries result for: ' + str(r) + '\n')
                                lfile.writelines(str(row) + '\n')
                                continue
                        else:
                            newresult = Results(
                                featureactionid=newfa,
                                result_type=resulttype,
                                variableid=newvar,
                                unitsid=newunit,
                                processing_level=plevel,
                                sampledmediumcv=sm,
                                valuecount=1
                            )
                            newresult.save()
                            tsr = Timeseriesresults(resultid=newresult, aggregationstatisticcv=aggstat)
                            tsr.save()
                            r = newresult
                        result_cache[key] = r

                    # --------- Duplicate Check Based on Latest Date ----------
                    # Use .pk to retrieve the primary key regardless of its field name.
                    result_id = r.pk
                    if result_id in result_last_date_cache:
                        last_date = result_last_date_cache[result_id]
                    else:
                        agg = Timeseriesresultvalues.objects.filter(resultid=tsr).aggregate(Max('valuedatetime'))
                        last_date = agg.get('valuedatetime__max')
                        result_last_date_cache[result_id] = last_date

                    if last_date is not None and datet <= last_date:
                        lfile.writelines(
                            f"Skipping row with datetime {datet} for resultid {result_id} (existing latest: {last_date})\n")
                        continue
                    # -------------------------------------------------------------

                    # Parse Value (column index 6) and check for annotation needs
                    annotate = False
                    detect = False
                    annotationtext = ''
                    annocode = ''
                    try:
                        if str(row[6]).strip() == '':
                            val = float('nan')
                        else:
                            if "<" in str(row[6]):
                                annotate = True
                                detect = True
                                annotationtext = "Below detection limit of " + str(row[6])
                                annocode = "Below detection limit"
                                val = float('nan')
                            elif ">" in str(row[6]):
                                annotate = True
                                detect = True
                                annotationtext = "Above method detection maximum of " + str(row[6])
                                annocode = "Above method detection maximum"
                                val = float('nan')
                            else:
                                val = float(row[6])
                    except ValueError as e:
                        lfile.writelines('Non-numeric value: ' + str(row[6]) + '\n')
                        lfile.writelines(str(row) + '\n')
                        continue

                    # Append result comment if present (column index 9)
                    if str(row[9]).strip():
                        annotate = True
                        if annotationtext:
                            annotationtext += " -- result comment: " + str(row[9]).strip()
                            annocode += " -- result comment"
                        else:
                            annotationtext = "Result comment: " + str(row[9]).strip()
                            annocode = "result comment"

                    # Set quality based on Valid (column index 8)
                    valid_field = str(row[8]).strip()
                    if valid_field == '':
                        quality = qualitycodegood
                    elif valid_field.upper() in ['N', 'NO']:
                        quality = qualitycodebad
                    else:
                        quality = qualitycodegood

                    # Create the Timeseriesresultvalues object
                    try:
                        tsrv = Timeseriesresultvalues(
                            resultid=tsr,
                            datavalue=val,
                            valuedatetime=datet,
                            valuedatetimeutcoffset=-5,
                            censorcodecv=censorcode,
                            qualitycodecv=quality,
                            timeaggregationinterval=1,
                            timeaggregationintervalunitsid=newtimeunit
                        )
                        if annotate and annotationtext:
                            tsrv.save()  # Immediate save to generate primary key for linking annotation
                            annotation = Annotations(
                                annotationtypecv=annotationtypecv,
                                annotationcode=annocode[:50],
                                annotationtext=annotationtext,
                                annotationdatetime=datetime.now(),
                                annotationutcoffset=4,
                                annotatorid=annotator
                            )
                            annotation.save()
                            Timeseriesresultvalueannotations(valueid=tsrv, annotationid=annotation).save()
                        else:
                            bulktimeseriesvalues.append(tsrv)
                            bulkcount += 1
                        # Update latest date cache
                        if (result_last_date_cache.get(result_id) is None) or (
                                datet > result_last_date_cache[result_id]):
                            result_last_date_cache[result_id] = datet
                        # Bulk create if threshold reached
                        if bulkcount >= bulk_batch_size:
                            print(f'Bulk creating {bulkcount} time series values')
                            Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)
                            bulktimeseriesvalues = []
                            bulkcount = 0
                    except IntegrityError as e:
                        lfile.writelines('Integrity error with value: ' + str(val) + ' Error: ' + str(e) + '\n')
                        lfile.writelines(str(row) + '\n')
                        continue

                # Final bulk create for remaining items
                if bulktimeseriesvalues:
                    print(f'Final bulk creating {bulkcount} time series values')
                    Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)
                    bulktimeseriesvalues = []
                    bulkcount = 0
        # End of transaction.atomic


# -----------------------------------------------------------------------------
# Main process: Multi-threaded processing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    directory = r'./2024'
    multithread = True
    processes = []
    for filename in os.listdir(directory):
        print(filename)
        if multithread:
            p = Process(target=loadtimeseries, args=(directory, filename))
            p.start()
            processes.append(p)
        else:
            loadtimeseries(directory, filename)
    if multithread:
        for p in processes:
            p.join()

