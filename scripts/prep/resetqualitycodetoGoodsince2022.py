import os
import re

import pandas as pd

from django.db import IntegrityError

from django.core.exceptions import ObjectDoesNotExist

import datetime

from odm2admin.models import *

import odm2admin.modelHelpers as modelHelpers

from django.db.models import Min, Max, Avg

import time as time

import xlrd

import pickle

from datetime import datetime, timedelta

from django.contrib.auth.models import User

# C:\Users\12672\Box\PREPDataShare\PREP_NHDES\dataFromEMD\FirstReports\Lamprey

from multiprocessing import Process

import multiprocessing as mp





def findCVVar(var):

    varf = var.lower().title()

    cvvars = CvVariablename.objects.filter(name__icontains=varf)

    finalvar = None

    tmpvarfcum = ''

    tmpvarf = ''

    # print(var)

    with open('varmap.csv', 'r') as mapfile:

        reader = csv.reader(mapfile)

        for row in reader:

            # print(row[0])

            # print(var.upper() == row[0])

            if var.upper() == row[0]:

                finalvar = CvVariablename.objects.filter(name=row[2])

                # print('cvtable: ' + row[0] +' from table: ' + var.upper()  +  ' final: ' + str(finalvar))

                if len(finalvar) > 0:

                    return finalvar.first()

                else:

                    print('cvtable: ' + row[0] +' from table: ' + var.upper()  +  ' final: ' + str(finalvar))

    if len(cvvars) == 1:

        finalvar = cvvars.first()

        return finalvar

    else:

        varfsubs = varf.split()



        for tmpvarf in varfsubs:

            cvvars = CvVariablename.objects.filter(name__icontains=tmpvarf)

            if len(cvvars) > 0:

                finalvar = cvvars.first()

                return finalvar

            else:

                tmpvarfcum += ' ' + tmpvarf

                cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)

                if len(cvvars) > 0:

                    finalvar = cvvars.first()

                    return finalvar

        cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)

        if len(cvvars) == 1:

            # print('icontains: ' +tmpvarf)

            finalvar = cvvars.first()

            return finalvar

        varfsubs = varf.split()

        tmpvarfcum = ''

        for tmpvarf in varfsubs:

            cvvars = CvVariablename.objects.filter(name__icontains=tmpvarf)

            if len(cvvars) > 0:

                # print('icontains: ' + tmpvarf)

                finalvar = cvvars.first()

                return finalvar

            else:

                tmpvarfcum += ' ' + tmpvarf

                cvvars = CvVariablename.objects.filter(name__icontains=tmpvarfcum)

                if len(cvvars) > 0:

                    # print('icontains: ' + tmpvarfcum)

                    finalvar = cvvars.first()

                    return finalvar

    return None





def findCVunit(unit):

    unitf = unit.lower()

    cvunits = []

    with open('unitmap.csv', 'r') as mapfile:

        reader = csv.reader(mapfile)

        for row in reader:

            if unit == row[1]:

                cvunits = CvUnitstype.objects.filter(name__icontains=row[2])

                if len(cvunits) > 0:

                    return cvunits.first()

    cvunits = CvUnitstype.objects.filter(name__icontains=unit)

    if len(cvunits) > 0:

        return cvunits.first()

    return None



def loadtimeseries(directory, filename):

    vars = []

    units = []

    varunits = []

    curvar = ''

    curunit = ''

    curvarunit = ''

    # print(varunits)

    # pickle.dump(varunits, 'lampreyvarunits.pickle')

    methtype = CvMethodtype.objects.get(name='Equipment deployment')

    save2 = False

    meth = Methods.objects.get(methodid =4)

    resulttype = CvResulttype.objects.get(name='Time series coverage')

    plevel = Processinglevels.objects.get(processinglevelid=1)

    aggstat = CvAggregationstatistic.objects.get(name='Average')

    sm = CvMedium.objects.get(name='Liquid aqueous')

    # DEPTH	M

    # DISSOLVED OXYGEN	MG/L

    # DISSOLVED OXYGEN SATURATION	%

    # PH	NONE

    # SALINITY	PSS

    # SPECIFIC CONDUCTANCE	MS/CM

    # TEMPERATURE WATER	DEG C

    # TURBIDITY	NTU

    # SALINITY	PPT





    newtimeunit = Units.objects.get(unitsname='minute')

    bulkcount = 0

    bulktimeseriesvalues = []

    bulkannotationvalues = []

    vt = CvVariabletype.objects.get(name='Water quality')



    sft = CvSamplingfeaturetype.objects.get(name='Stream gage')

    # sampling_feature_geo_type

    sfgt = CvSamplingfeaturegeotype.objects.get(name='Point')

    # sitetypecv

    st = CvSitetype.objects.get(name='Stream')



    #not river

    sftEst = CvSamplingfeaturetype.objects.get(name='Stream gage')

    stEst = CvSitetype.objects.get(name='Estuary')

    # pond

    sftPond = CvSamplingfeaturetype.objects.get(name='Stream gage')

    stPond = CvSitetype.objects.get(name='Lake, Reservoir, Impoundment')

    spatref = Spatialreferences.objects.get(spatialreferenceid=1)

    annotationtypecv = CvAnnotationtype.objects.filter(

        name="Time series result value annotation").get()

    bulk = True

    actiontype = CvActiontype.objects.get(name='Equipment deployment')

    # createcsv = False

    with open('logtimeseriessampleNewPREP2025b.log', 'a') as lfile:

        # log = csv.writer(lfile)

        # if createcsv:

       # for filename in os.listdir(directory):

        foundrs = []

        convertfiles = False

        if filename.endswith(".xlsx") and convertfiles:

            filepath = os.path.join(directory, filename)

            try:

                data_xls = pd.read_excel(filepath, 'TimeSeries-Datalogger-Waterbody', index_col=None,header=3)

            except ValueError as e:

                data_xls = pd.read_excel(filepath, 'TimeSeries-Datalogger-StationID', index_col=None,header=3)



                    # TimeSeries-Datalogger-StationID

            # data_xls['Time'] = pd.to_datetime(data_xls['Time']).apply(lambda x: x.strftime(r'%H:%M:%S'), )

            data_xls['Date'] = pd.to_datetime(data_xls['Date'], format='%m/%d/%Y', errors='ignore')

            data_xls['Time'] =  pd.to_datetime(data_xls['Time'], format='%H:%M:%S', errors='ignore')

            newfilepath = os.path.splitext(filepath)[0] + '.csv'

            data_xls.to_csv(newfilepath, encoding='utf-8')

        # for filename in os.listdir(directory):

        if filename.endswith(".csv") : # and not filename == nofile

            filepath = os.path.join(directory, filename)

            print(filepath)

            with open(filepath, 'r')as tempfile:

                reader = csv.reader(tempfile)

                lfile.writelines(filepath)

                i = 0

                for row in reader:

                    # print(row)

                    i+=1

                    if i > 1:

                        # break

                        # print(row)

                        if len(row) <3:

                            continue

                        if len(row[3]) > 0:



                            var = row[5] # .lower().title()

                            stdvar = findCVVar(var)

                            if not stdvar:

                                stdvar = CvVariablename(term=var, name=var,

                                                        definition=' new cv variable for NH DES')

                                stdvar.save()

                                lfile.writelines('new var\n')

                                lfile.writelines(str(stdvar) + '\n')



                            newvar = None

                            # variabledefinition=var.lower().title() + ' from NHDES Grab samples',

                            newvars = Variables.objects.filter(variable_name=stdvar)# \

                                # .filter()

                            if len(newvars) > 0:

                                newvar = newvars.first()

                            if not newvar:

                                newvar = Variables(variable_type=vt,

                                                   variablecode=var.lower().title(),

                                                   variable_name=stdvar,

                                                   variabledefinition=var.lower().title() + ' from NHDES timeseries',

                                                   nodatavalue=-9999)

                                newvar.save()

                                lfile.writelines('new var: ' + str(newvar) + '\n')

                                lfile.writelines(str(row) + '\n')

                                print('new var!!! -' + newvar.variablecode + '- in file: ' + var)

                                print(newvar)

                                print(newvar.variablecode)



                            sfs = Samplingfeatures.objects.filter(samplingfeaturecode__iexact=row[2])

                            if len(sfs) > 0:

                                newsf = sfs.first()

                            else:

                                lfile.writelines('no site match for: ' + row[2].lower())

                                continue



                                # log.writerow('no match for: ' + row[1].lower())

                                # log.writerow(row)

                                # break

                            # print(sf)



                            fas = Featureactions.objects.filter(samplingfeatureid=newsf).filter(action__action_type=actiontype)

                            datet= None

                            try:

                                # 2018-05-02 00:00:00,2019-11-01 19:45:00,

                                datet = datetime.strptime(row[3][:10] + ' ' + row[4][11:], '%Y-%m-%d %H:%M:%S')

                            except ValueError as e:

                                try:

                                    datet = datetime.strptime(row[3] + ' ' + row[4], '%Y-%m-%d %H:%M:%S')

                                except ValueError as e:

                                    try:

                                        datet = datetime.strptime(row[3] + ' ' + row[4], '%Y-%m-%d %H:%M')

                                    except Exception as e:

                                        lfile.writelines('bad date: ' + row[3] + ' ' + row[4] + '\n')

                                        lfile.writelines(str(row) + '\n')

                                        continue

                            #DATE CHECK

                            # Check if date is greater than 2022-12-31

                            # cutoff_date = datetime(2022, 12, 31, 23, 59, 59)

                            # if datet and datet <= cutoff_date:

                                # Date is not greater than 2022-12-31, so continue with the processing

                            #     continue

                            if len(fas) >0:

                                newfa = fas.first()

                            if len(fas) ==0:

                                # datet = datetime.strptime(row[3][:10] + ' ' + row[4][11:], '%Y-%m-%d %H:%M:%S')



                                valid = False



                                meth = Methods.objects.get(methodid =4)

                                actiondescription = row[5].lower().title() + ' imported from NHDES'

                                newaction = Actions(action_type=actiontype, method=meth,

                                                    begindatetime=datet,

                                                    actiondescription=actiondescription)

                                # if save3:

                                newaction.save()

                                lfile.writelines('new action' + '\n')

                                lfile.writelines(str(newaction) + '\n')

                                newfa = Featureactions(samplingfeatureid=newsf, action=newaction)

                                # if save3:

                                newfa.save()

                                lfile.writelines('new fa' + '\n')

                                lfile.writelines(str(newfa) + '\n')



                            # print(fa.featureactionid)





                            newunit = None

                            unit = row[7]

                            # print('raw unit')

                            # print(unit)

                            newunits = Units.objects.filter(unitsabbreviation=unit.lower())

                            if len(newunits) ==1:

                                newunit = newunits.first()

                            if not newunit:

                                ut = findCVunit(unit)

                                if not ut:

                                    ut = CvUnitstype(name=unit,term=unit,definition=' new cv unit type for NH DES')

                                    ut.save()

                                newunit = Units(unit_type=ut, unitsabbreviation=unit.lower(),

                                                unitsname=unit.lower())

                                newunit.save()

                                lfile.writelines('new unit: ' + str(newunit) + '\n')

                                lfile.writelines(str(row) + '\n')

                            rs = Results.objects.filter(featureactionid__in=fas).filter(variableid=newvar).filter(unitsid=newunit)



                            # print('RS var and units')

                            # print(newunit)

                            # print(newvar)

                            # print(rs.first())

                            if len(rs) > 0:

                                r = rs.first()

                                found = False

                                for foundr in foundrs:

                                    if r == foundr:

                                        found = True

                                if not found:

                                    foundrs.append(r)

                                    lfile.writelines('result used: ' + str(r)+ ' resultid: ' + str(r.resultid)+  '\n')

                                try:

                                    tsr = Timeseriesresults.objects.get(resultid=r)

                                except ObjectDoesNotExist:

                                    lfile.writelines('no time series result: ' + str(r) + '\n')

                                    lfile.writelines(str(row) + '\n')

                            elif len(rs) == 0:



                                newresult = Results(featureactionid=newfa, result_type=resulttype,

                                                    variableid=newvar, unitsid=newunit, processing_level=plevel,

                                                    sampledmediumcv=sm, valuecount=1)

                                newresult.save()

                                nozloc = False



                                newtsr = Timeseriesresults(resultid=newresult, aggregationstatisticcv=aggstat)

                                newtsr.save()

                                r = newresult

                                tsr = newtsr

                                lfile.writelines('new result: ' + str(newresult) + '\n')

                                lfile.writelines(str(row) + '\n')



                            # print(datet)

                            censorcode = CvCensorcode.objects.filter(name="Not censored").get()

                            qualitycode = CvQualitycode.objects.filter(name="Good").get()

                            qualitycodebad = CvQualitycode.objects.filter(name="Bad").get()

                            qualitycodeunkown = CvQualitycode.objects.filter(name="Unknown").get()

                            val = None

                            annotate = False

                            unknown = False

                            annotatorid = None

                            annotationtext = ''

                            annocode = ''

                            annotationdatetime = None

                            detect = False

                            if row[6].strip() == '':

                                val = float('nan')

                            else:

                                if "<" in row[6]:

                                    annotate = True

                                    detect = True

                                    annotationdatetime = datetime.now()

                                    annotatorid = People.objects.filter(personid=1).get()

                                    annotationtext = "below detection limit of " + row[6]

                                    annocode = "Below detection limit"





                                if ">" in row[6]:

                                    annotate = True

                                    detect = True

                                    annotationdatetime = datetime.now()



                                    annotationtext = "Above method detection maximum of " + row[6]

                                    annocode = "Above method detection maximum"

                                if len(row[9]) > 0:

                                    annotate = True

                                    annotationdatetime = datetime.now()

                                    annotatorid = People.objects.filter(personid=1).get()

                                    if len(annotationtext) == 0:

                                        annotationtext = "result comment: " + row[9]

                                        annocode = "result comment"

                                    else:

                                        annotationtext += " -- result comment: " + row[9]

                                        annocode += " -- result comment"

                                if len(row[8]) > 0 and not (row[8] == 'Y' or row[8] =='Yes' or row[8] =='YES'): #

                                    annotate = True

                                    annotationdatetime = datetime.now()

                                    annotatorid = People.objects.filter(personid=1).get()

                                    if row[8].lower() == 'unknown':

                                        unknown = True

                                    if len(annotationtext) == 0:

                                        annotationtext = "valid : " + row[8]

                                        annocode = "valid: " + row[8]

                                    else:

                                        annotationtext += " -- valid : " + row[8]

                                        annocode += " -- valid: " + row[8]

                                if annotate:

                                    annotation = Annotations(annotationtypecv=annotationtypecv,

                                                             annotationcode=annocode[0:50],

                                                             annotationtext=annotationtext,

                                                             annotationdatetime=annotationdatetime,

                                                             annotationutcoffset=4,

                                                             annotatorid=annotatorid)

                                    annotation.save()



                                # < DEAL WITH DETECTION LIMIT

                                catagoricalval = False

                                if annotate:

                                    for s in re.findall(r'^[-]?[0-9]*\.?[0-9]+$', row[6]):

                                        if not detect:

                                            val = float(s)

                                        else:

                                            val = float('nan')

                                else:

                                    try:

                                        val = float(row[6])

                                    except ValueError as e:

                                        catagoricalval = True

                                        lfile.writelines('none numeric value: ' + row[6]+ '\n' )

                                        lfile.writelines(str(row) + '\n')

                                        continue

                            if len(str(val)) == 0 or str(val) =='null' or not val:

                                val = float('nan')

                            # print(val)

                            try:

                                if annotate and unknown:

                                    tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,

                                                                  valuedatetimeutcoffset=-5,

                                                                  censorcodecv=censorcode,

                                                                  qualitycodecv=qualitycodeunkown,

                                                                  timeaggregationinterval=1,

                                                                  timeaggregationintervalunitsid=newtimeunit)

                                elif annotate:

                                    tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,

                                                                  valuedatetimeutcoffset=-5,

                                                                  censorcodecv=censorcode,

                                                                  qualitycodecv=qualitycodebad,

                                                                  timeaggregationinterval=1,

                                                                  timeaggregationintervalunitsid=newtimeunit)

                                else:

                                    tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,

                                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,

                                                              qualitycodecv=qualitycode, timeaggregationinterval=1,

                                                              timeaggregationintervalunitsid=newtimeunit)



                                tsrv.save()

                                # print(bulkcount)

                                # print(row)

                                # print(r.variableid)

                                # print(r.resultid)

                                # print(r.unitsid)

                                # print(str(tsrv.valuedatetime) + ' ' + str(tsrv.datavalue))

                                # print(tsrv)

                                bulk=False

                                bulkcount+=1

                                if annotate:

                                    bulk = False

                                    # tsrv.save()

                                    # print(annotation)

                                    # print(tsrv)

                                    # print(tsrv.valueid)

                                    tsrva = Timeseriesresultvalueannotations(valueid=tsrv,

                                                                            annotationid=annotation).save()

                                    # bulkannotationvalues.append(tsrva)

                                # else:

                                #     bulktimeseriesvalues.append(tsrv)

                                #     bulkcount += 1

                                # if bulkcount > 20000 and bulk:

                                #     print('bulkcreate')

                                #     print(len(bulktimeseriesvalues))

                                #     Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)

                                #     del bulktimeseriesvalues[:]

                                #     tsvr = None

                                #     bulkcount = 0





                            except IntegrityError:

                                # bulktimeseriesvalues.pop(tsrv)

                                lfile.writelines('Integrity error none numeric value: ' + str(val) + '\n')

                                # lfile.writelines(tsrv)

                                lfile.writelines(str(row) + '\n')

                                continue

                            # if bulkcount >200:

                            #     break

                # Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)

                # del bulktimeseriesvalues[:]

                tsvr = None

                bulkcount = 0



# nofile = 'C:/Users/12672\Box/ODM2-Admin/omit/PREP/L/021120-TimeSeries-Datalogger-WaterbodyID-NHEST600030709-01-01 (3)'

# directory = 'C:/Users/12672\Box/ODM2-Admin/omit/PREP/to do/'

directory = r'./2024'

multithread = True

if __name__ == '__main__':

    processes = []

    p = None

    for filename in os.listdir(directory):

        print(filename)

        if multithread:

            p = Process(target=loadtimeseries, args=(directory,filename))

            p.start()

            # p.join()

        else:

            loadtimeseries(directory,filename)