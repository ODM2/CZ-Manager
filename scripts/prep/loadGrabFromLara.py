
import os
import csv
import pandas as pd
import traceback
import importlib
# import sys
from django.core.wsgi import get_wsgi_application
# sys.path.append(r"C:\Users\ml1451\OneDrive - USNH\CZ-Manager")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'templatesAndSettings.settings.developmentPREP10'
# module_name = './templatesAndSettings.settings.developmentPREP10'
# special_module = importlib.import_module(module_name)

application = get_wsgi_application()
from django.db.models import Q
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
# from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from django.contrib.auth.models import User
# C:\Users\12672\Box\PREPDataShare\PREP_NHDES\dataFromEMD\FirstReports\Lamprey
from multiprocessing import Process

def findVar(varname):
    with open('./omit/PREP/varmap.csv', 'r') as mapfile:
        reader = csv.reader(mapfile)
        varfound = None
        for row in reader:
            if varname.lower() == row[0].lower():
                varcode = row[3]
                varfound = Variables.objects.filter(variablecode=varcode)
        if varfound:
            return varfound.first()
def findCVVar(var):
    varf = var.lower().title()
    cvvars = CvVariablename.objects.filter(name__icontains=varf)
    finalvar = None
    tmpvarfcum = ''
    tmpvarf = ''
    # print(var)
    with open('./omit/PREP/varmap.csv', 'r') as mapfile:
        reader = csv.reader(mapfile)
        for row in reader:
            # print(row[0])
            # print(var.upper() == row[0])
            if var.lower() == row[0].lower():
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
    with open('./omit/PREP/unitmap.csv', 'r') as mapfile:
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

def loadgrabdata(directory, filename, baddateonly=False, stopatdupvalue=False):

    # nofile = '' #  'C:/Users/12672\Box/ODM2-Admin/omit/PREP/L/021120-TimeSeries-Datalogger-WaterbodyID-NHEST600030709-01-01 (3)'

    vars = []
    units = []
    varunits = []
    curvar = ''
    curunit = ''
    curvarunit = ''

    # print(varunits)
    # pickle.dump(varunits, 'lampreyvarunits.pickle')
    for meth in CvMethodtype.objects.all():
        print(meth)
    methtype = CvMethodtype.objects.get(name='Equipment deployment')
    save2 = False
    meth = Methods.objects.get(methodid =1)
    resulttype = CvResulttype.objects.get(name='Time series coverage')
    plevel = Processinglevels.objects.get(processinglevelid=1)
    aggstat = CvAggregationstatistic.objects.get(name='Continuous')
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
    # vt = CvVariabletype.objects.get(name='Water quality')
    # vts = CvVariabletype.objects.get(name='Sediment')
    # convertfiles = True
    sft = CvSamplingfeaturetype.objects.get(name='Specimen')
    sftsed = CvSamplingfeaturetype.objects.get(name='Sediment sample')
    # sampling_feature_geo_type
    sfgt = CvSamplingfeaturegeotype.objects.get(name='Point')
    # sitetypecv
    st = CvSitetype.objects.get(name='Stream')

    #not river
    sftEst = CvSamplingfeaturetype.objects.get(name='Specimen')
    stEst = CvSitetype.objects.get(name='Estuary')
    # pond
    sftPond = CvSamplingfeaturetype.objects.get(name='Specimen')
    stPond = CvSitetype.objects.get(name='Lake, Reservoir, Impoundment')
    spatref = Spatialreferences.objects.get(spatialreferenceid=1)
    annotationtypecv = CvAnnotationtype.objects.filter(
        name="Time series result value annotation").get()
    annotationtypeCatcv = CvAnnotationtype.objects.filter(
        name="Categorical result value annotation").get()


    writecsv = False
    samedays = []
    samevars = []
    sameloc = []


    # annotatecatONLY = False
    with open('./omit/PREP/loggrabsamples'+ filename + '.log', 'a') as lfile:
        # log = csv.writer(lfile)
        if writecsv:
            # for filename in os.listdir(directory):
            if filename.endswith(".xlsx"):
                filepath = os.path.join(directory, filename)
                # GrabSample_Bio_WaterbodyID
                #GrabSample_PhysChem_Project, GrabSample_PhysChem_Parameter
                try:
                    data_xls = pd.read_excel(filepath, 'GrabSample_PhysChem_StationID', index_col=None,header=4)

                except Exception as e:
                    try:
                        data_xls = pd.read_excel(filepath, 'GrabSample_Bio_WaterbodyID', index_col=None,header=4)
                    except Exception as e:
                        try:
                            data_xls = pd.read_excel(filepath, 'GrabSample_PhysChem_RiverName', index_col=None,
                                                     header=4)
                        except Exception as e:
                            #GrabSample_PhysChem_WaterbodyID
                            try:
                                data_xls = pd.read_excel(filepath, 'GrabSample_PhysChem_WaterbodyID', index_col=None,header=4)
                            except Exception as e:
                                try:
                                    data_xls = pd.read_excel(filepath, 'GrabSample_PhysChem_Project', index_col=None,header=4)
                                except Exception as e:
                                    data_xls = pd.read_excel(filepath, 'GrabSample_PhysChem_Parameter', index_col=None,header=4)

                data_xls['START DATE'] = pd.to_datetime(data_xls['START DATE'], format='%m/%d/%Y', errors='ignore')
                data_xls['START TIME'] = pd.to_datetime(data_xls['START TIME'], format='%H:%M:%S', errors='ignore')
                newfilepath = os.path.splitext(filepath)[0] + '.csv'
                data_xls.to_csv(newfilepath, encoding='utf-8')

        # for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            print(filepath)
            with open(filepath, 'r')as tempfile:
                reader = csv.reader(tempfile)
                i = 0
                j = 0
                try:
                    for row in reader:
                        # print(row)
                        i+=1
                        if i >= 1 and j==0 and len(row) >35:
                            print('Substance?')
                            print(row[26])
                            print(j)
                            if not (row[26] == 'Substance Name' or row[26] == 'SubstanceName'):

                                print('BAD LINE')
                                #print(filename)
                                # print('ERROR ERROR')
                                if i<10:
                                    print('header: ' + row[26])
                                    print(row)
                                # print(str(e))
                                #  lfile.writelines('ERROR ERROR')
                                lfile.writelines(filename)
                                # lfile.writelines(row)
                                # lfile.writelines(str(e))
                            elif j ==0:
                                j=i
                                print('header line found')
                                print(j)
                                continue
                                # break
                        if j >= 1:
                            # print(row)
                            valuevalid = False
                            baddata= False
                            unknown = False
                            if len(row[38]) == 0 or row[38] == 'Y' or row[38] == 'YES':
                                valuevalid = True
                            if row[38] == 'N' or row[38].lower() == 'no':
                                baddata = True
                                valuevalid = True
                            if row[38].lower() == 'unknown':
                                unknown = True
                                valuevalid = True
                            # if 'DUPLICATE' in row[21] or 'REPLICATE' in row[21]:
                            #     print('DUPLICATE')
                            #     print(row)
                            #     valuevalid = False
                            # if row[36] == 'NITROGEN, AMMONIA AS N':
                            #     print('Ammonia')
                            #    print(row)
                            # QUALIFIER AND RESULTS = RDLMeasureValue
                            if row[28].strip() == '':
                                valuevalid = False
                            if len(row[26]) > 0 and valuevalid:
                                # FRACTION_TYPE = ResultBasisName
                                if len(row[31]) > 0:
                                    var = row[26].lower().title() + ' ' + row[31].lower().title()
                                else:
                                    var = row[26].lower().title()
                                stdvar = findCVVar(var)
                                if not stdvar:
                                    stdvar = CvVariablename(term=var, name=var,
                                                            definition=' new cv variable for NH DES')
                                    stdvar.save()
                                    lfile.writelines('new var'+ '\r\n')
                                    lfile.writelines(str(stdvar)+ '\r\n')

                                newvar = None
                                vartype = row[23]
                                cvvartype = CvVariabletype.objects.get(name='Water quality')
                                if vartype == 'SEDIMENT':
                                    cvvartype = CvVariabletype.objects.get(name='Sediment')
                                elif vartype =='SOIL':
                                    cvvartype = CvVariabletype.objects.get(name='Soil')
                                elif vartype == 'TISSUE':
                                    cvvartype = CvVariabletype.objects.get(name='Tissue')
                                elif vartype == 'AIR':
                                    cvvartype = CvVariabletype.objects.get(name='Air')
                                elif vartype == 'SOLID':
                                    cvvartype = CvVariabletype.objects.get(name='Tissue')
                                elif vartype == 'HABITAT':
                                    cvvartype = CvVariabletype.objects.get(name='Habitat')

                                # if row[36] == 'TIDE STAGE':
                                #     tidestage = row[37]
                                newvars = Variables.objects.filter(variable_name=stdvar).filter(variablecode__icontains=var[:49]).filter(variable_type=cvvartype)
                                if len(newvars) > 0:
                                    newvar = newvars.first()
                                    # if not newvar:
                                    #     newvar = findVar(var[:49])
                                    #     if not newvar:
                                    #         newvar = findVar(var)
                                if not newvar:
                                    newvar = Variables(variable_type=cvvartype,
                                                       variablecode=var.lower().title()[:49],
                                                       variable_name=stdvar,
                                                       variabledefinition=var.lower().title() + ' from NHDES Grab samples',
                                                       nodatavalue=-9999)
                                    newvar.save()
                                    lfile.writelines('new var: ' + str(newvar)+ '\r\n')
                                    # lfile.writelines(str(row) + '\r\n')
                                    print('new var!!!')
                                    print(newvar)
                                    print(newvar.variablecode)

                                sfs = Samplingfeatures.objects.filter(samplingfeaturecode__iexact=row[0].lower().title())
                                if len(sfs) > 0:
                                    newsf = sfs.first()
                                else:
                                    print('CANT FIND SITE')
                                    print(row)
                                    # HERE
                                    lfile.writelines('new site for: ' + row[0].lower()+ '\r\n')
                                    lfile.writelines(str(newsf)+ '\r\n')
                                    # lfile.writelines(str(row) + '\r\n')

                                # print(sf)
                                actiontype = CvActiontype.objects.get(name='Specimen analysis')
                                methtype = CvMethodtype.objects.get(name='Specimen analysis')
                                detectionlimit = ''
                                if len(row[32]) > 0:
                                    detectionlimit = ' Reporting Limit (RDL): ' + row[32] + ' ' + row[33]  + ' ' + row[34]
                                methdesc = 'NHDES grab- sample method: ' + row[
                                    21].lower().title() + ' - lab: ' + row[20] + ' - analytical method: ' \
                                           + row[21].lower().title() + '-  analytical method source: ' + row[
                                               22] + detectionlimit
                                fas = Featureactions.objects. \
                                    filter(samplingfeatureid=newsf). \
                                    filter(action__action_type=actiontype) \
                                    .filter(action__method__methoddescription=methdesc)
                                if len(fas) > 0:
                                    newfa = fas.first()
                                if len(fas) ==0:
                                    print('FA doesnt exist!!!')
                                    print(newsf.samplingfeaturecode)
                                    print(methdesc)
                                    rowtime = row[7]
                                    if rowtime == '0:00' or rowtime == '00:00' or rowtime == '00:00:00':
                                        rowtime = '12:00'
                                    rowdate = row[6]
                                    baddate = False
                                    try:
                                        # '2001-03-23', '12:00','2001-03-20', '15:00', 2001-03-20 15:00
                                        datet = datetime.strptime(rowdate[:10] + ' ' + rowtime[11:], '%Y-%m-%d %H:%M:%S')
                                    except ValueError as e:
                                        try:
                                            datet = datetime.strptime(rowdate + ' ' + rowtime, '%Y-%m-%d %H:%M:%S')
                                        except ValueError as e:
                                            try:
                                                datet = datetime.strptime(rowdate + ' ' + rowtime,
                                                                          '%Y-%m-%d %H:%M')
                                            except ValueError as e:
                                                try:
                                                    datet = datetime.strptime(rowdate[:10] + ' ' + rowtime,
                                                                              '%Y-%m-%d %H:%M')

                                                except ValueError as e:
                                                    try:
                                                        datet = datetime.strptime(rowdate[:10] + ' ' + rowtime,
                                                                                  '%m/%d/%Y %H:%M')
                                                    except ValueError as e:
                                                        baddate= True
                                                        try:
                                                            datet = datetime.strptime(rowdate[:10].split(' ', 1)[0] + ' ' + rowtime,
                                                                                      '%m/%d/%Y %H:%M')
                                                        except Exception as e:
                                                            try:
                                                                datet = datetime.strptime(rowdate[:10] + ' ' + rowtime,
                                                                                          '%m/%d/%Y %H:%M:%S')
                                                            except Exception as e:
                                                                lfile.writelines('bad date: ' + row[6][:10] + ' ' + rowtime + '\n')
                                                                lfile.writelines('bad date: ' + rowdate + ' ' + rowtime + '\n')
                                                                lfile.writelines(str(row) + '\n')
                                                                continue
                                    if row[7] == '0:00' or row[7] == '00:00' or row[7] == '00:00:00':
                                        # print('zero hour')
                                        datet = datet + timedelta(hours=12)
                                        #   editedt = True
                                    methcode = 'NHDES grab: ' + row[21].lower().title() #  row[41] + ' ' +row[42]

                                    methname = 'NHDES grab ' + row[21].lower().title()
                                    # methdesc = 'NHDES grab- sample method: ' + row[34].lower().title() + '- analytical method: ' \
                                    #          + row[42].lower().title() + '-  analytical method source: ' + row[43].lower().title()
                                    meth = Methods(methodtypecv=methtype, methodcode=methcode,
                                                   methodname=methname,
                                                   methoddescription=methdesc)
                                    meth.save()
                                    lfile.writelines('new method '+ '\r\n')
                                    lfile.writelines(str(meth)+ '\r\n')

                                    actiondescription = row[5].lower().title() + ' ' \
                                                        + row[3].lower().title() + '  ' +row[23].lower().title() # \
                                                        # + ' ' +row[1].lower().title()

                                    newaction = Actions(action_type=actiontype, method=meth,
                                                        begindatetime=datet,
                                                        actiondescription=actiondescription)
                                    # if save3:
                                    newaction.save()
                                    lfile.writelines('new action'+ '\r\n')
                                    lfile.writelines(str(newaction)+ '\r\n')
                                    # print('HERE')
                                    # print(newaction)

                                    # print(newsf)
                                    newfa = Featureactions(samplingfeatureid=newsf, action=newaction)
                                    # if save3:
                                    newfa.save()
                                    # print(newfa)
                                    lfile.writelines('new fa'+ '\r\n')
                                    lfile.writelines(str(newfa)+ '\r\n')

                                # print(fa.featureactionid)


                                newunit = None
                                unit = row[29]
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
                                    lfile.writelines('new unit: ' + str(newunit)+ '\r\n')
                                    # lfile.writelines(str(row) + '\r\n')
                                # lfile.writelines('new var: ' + str(newvar) + '\r\n')
                                # lfile.writelines('new fas: ' + str(fas) + '\r\n')
                                # lfile.writelines(str(row) + '\r\n')
                                rs = Results.objects.filter(featureactionid__in=fas).filter(variableid=newvar).filter(unitsid=newunit)

                                if len(rs) ==1:
                                    r = rs.first()
                                    try:
                                        tsr = Timeseriesresults.objects.get(resultid=r)
                                    except ObjectDoesNotExist:
                                        lfile.writelines('no time series result: ' + str(r)+ '\r\n')
                                        # lfile.writelines(str(row) + '\r\n')
                                elif len(rs) == 0:
                                    newresult = Results(featureactionid=newfa, result_type=resulttype,
                                                        variableid=newvar, unitsid=newunit, processing_level=plevel,
                                                        sampledmediumcv=sm, valuecount=1)
                                    newresult.save()
                                    zlocationunittype = findCVunit(row[10])
                                    nozloc = False
                                    newtsr = None
                                    if len(row[10]) == 0:
                                        nozloc = True
                                    if zlocationunittype:
                                        zlocationunits = Units.objects.get(unitsabbreviation=row[10].lower())
                                        try:
                                            zval =float(row[9])
                                        except ValueError as e:
                                            nozloc = True
                                        if not nozloc:
                                            newtsr = Timeseriesresults(resultid=newresult, aggregationstatisticcv=aggstat,
                                                                       zlocationunitsid=zlocationunits,
                                                                       zlocation=zval)
                                    if not newtsr:
                                        newtsr = Timeseriesresults(resultid=newresult, aggregationstatisticcv=aggstat)
                                    # print(nozloc)
                                    # print(zlocationunittype)
                                    # print(zlocationunits)
                                    # print(zval)
                                    # print(newresult)
                                    # print(row)
                                    newtsr.save()


                                    r = newresult
                                    tsr = newtsr
                                    lfile.writelines('new result: ' + str(newresult)+ '\r\n')
                                    # lfile.writelines(str(row) + '\r\n')
                                # print(tsr)
                                # "%Y-%m-%d %H:%M:%S"
                                rowtime = row[7]
                                if rowtime == '0:00' or rowtime == '00:00' or rowtime == '00:00:00':
                                    rowtime = '12:00'
                                rowdate = row[6]
                                baddate = False
                                try:
                                    # '2001-03-23', '12:00','2001-03-20', '15:00', 2001-03-20 15:00
                                    datet = datetime.strptime(rowdate[:10] + ' ' + rowtime[11:], '%Y-%m-%d %H:%M:%S')
                                except ValueError as e:
                                    try:
                                        datet = datetime.strptime(rowdate + ' ' + rowtime, '%Y-%m-%d %H:%M:%S')
                                    except ValueError as e:
                                        try:
                                            datet = datetime.strptime(rowdate + ' ' + rowtime,
                                                                      '%Y-%m-%d %H:%M')
                                        except ValueError as e:
                                            try:
                                                datet = datetime.strptime(rowdate[:10] + ' ' + rowtime,
                                                                          '%Y-%m-%d %H:%M')

                                            except ValueError as e:
                                                baddate= True
                                                try:
                                                    datet = datetime.strptime(rowdate[:10].split(' ', 1)[0] + ' ' + rowtime,
                                                                              '%m/%d/%Y %H:%M')
                                                except Exception as e:
                                                    lfile.writelines('bad date: ' + row[6][:10] + ' ' + rowtime + '\n')
                                                    lfile.writelines('bad date: ' + rowdate + ' ' + rowtime + '\n')
                                                    lfile.writelines(str(row) + '\n')
                                                    continue
                                # print(datet)
                                # editedt = False
                                if row[7] == '0:00' or row[7] == '00:00' or row[7] == '00:00:00':
                                    # print('zero hour')
                                    datet = datet + timedelta(hours=9)
                                    # editedt = True
                                newloc = row[0]
                                k = 0
                                edittime = False
                                for day, v, loc in zip(samedays, samevars, sameloc):
                                    if day == datet and v == var and newloc == loc:
                                        datet = datet + timedelta(minutes=1)
                                        edittime = True
                                        # print('HERE HERE ')

                                samedays.append(datet)
                                samevars.append(var)
                                sameloc.append(row[0])
                                # print(datet)
                                # print(datet)
                                censorcode = CvCensorcode.objects.filter(name="Not censored").get()
                                qualitycode = CvQualitycode.objects.filter(name="Good").get()
                                qualitycodebad = CvQualitycode.objects.filter(name="Bad").get()
                                qualitycodeunkown = CvQualitycode.objects.filter(name="Unknown").get()
                                timeUnit = Units.objects.filter()
                                val = None
                                annotate = False
                                annotatorid = None
                                annotationtext = ''
                                annocode = "sample ID-" + row[1] + '- '
                                annotationdatetime = None
                                # if row[37].strip() == '':
                                # val = float('nan')
                                detect = False
                                if not row[28].strip() == '':
                                    # print('valid row')
                                    if "<" in row[28]:
                                        annotate = True
                                        detect = True
                                        annotationdatetime = datetime.now()
                                        annotatorid = People.objects.filter(personid=1).get()
                                        annotationtext = "below detection limit of " + row[32] + ' ' + row[33]
                                        annocode += "Below detection limit"


                                    if ">" in row[28]:
                                        annotate = True
                                        detect = True
                                        annotationdatetime = datetime.now()
                                        annotatorid = People.objects.filter(personid=1).get()
                                        annotationtext = "Above method detection maximum of " + row[32] + ' ' + row[33]
                                        annocode += "Above method detection maximum"
                                    if len(row[34]) > 0 or len(row[17]):
                                        annotate = True
                                        annotationdatetime = datetime.now()
                                        annotatorid = People.objects.filter(personid=1).get()
                                        if len(annotationtext) == 0:
                                            annotationtext = "result comment: " + row[34]
                                            annotationtext = "-- sample comment: " + row[17]
                                            annocode += " comment"
                                        else:
                                            annotationtext += " -- result comment: " + row[34]
                                            annotationtext += " -- sample comment: " + row[17]
                                            annocode += " -- comment"
                                    if len(row[9]) > 0 or len(row[10]) > 0:
                                        depth = ''
                                        annotate = True
                                        try:
                                            if float(row[9]) > 0:
                                                depth = row[9]
                                            if len(annotationtext) == 0:
                                                annotationtext = "depth of sample: " + depth + ' ' + row[10].lower()
                                            else:
                                                annotationtext += " -- depth of sample: " + depth + ' ' + row[10].lower()
                                                annocode += " -- depth of sample "  + depth # + ' ' + row[27].lower()
                                        except ValueError as e:
                                            depth = 'no depth recorded'
                                        # annotate = True
                                    if len(row[1]) > 0:
                                        annotate=True
                                        if len(annotationtext) == 0:
                                            annotationtext = " sample ID: " + row[1] + ' '

                                        else:
                                            annotationtext += " sample ID: " + row[1] + ' '

                                    if annotate and valuevalid:
                                        # annotationtypeCatcv
                                        #annotationlink is set to the sample ID
                                        annotation = Annotations(annotationtypecv=annotationtypecv,
                                                                 annotationcode=annocode[0:50],
                                                                 annotationtext=annotationtext,
                                                                 annotationdatetime=annotationdatetime,
                                                                 annotationlink=str(row[1]),
                                                                 annotationutcoffset=4,
                                                                 annotatorid=annotatorid)

                                        # annotation.save()

                                    # < DEAL WITH DETECTION LIMIT
                                    catagoricalval = False
                                    # print(row)
                                    if annotate:
                                        # print(row[37])
                                        nonnum = True
                                        for s in re.findall(r'^[-]?[0-9]*\.?[0-9]+$', row[28]):
                                            nonnum = False
                                            try:
                                                if not detect:
                                                    # print(detect)
                                                    val = float(row[28])
                                                    # print(val)
                                                else:
                                                    val = float(row[28])
                                                    # print(val)
                                            except ValueError as e:
                                                # print('asdfasdf')
                                                print(row[28])
                                                print('none num')
                                                lfile.writelines('none numeric value: ' + row[28] + '\r\n')
                                                # lfile.writelines(str(row) + '\r\n')
                                                catagoricalval = True
                                                # print('here 1')
                                                pass
                                        if nonnum:
                                            catagoricalval = True
                                            # print(val)
                                    else:
                                        try:
                                            # print('ahd')
                                            # print(row[37])
                                            val = float(row[28])

                                        except ValueError as e:
                                            lfile.writelines('none numeric value: ' + row[28] + '\r\n')
                                            catagoricalval = True
                                            # print('here 2')
                                            # lfile.writelines(str(row) + '\r\n')
                                            pass
                                if len(str(val)) == 0 or str(val) =='null' or not val:
                                    val = float('nan')
                                # print(val)
                                # print(catagoricalval)
                                if (baddate and baddateonly) or not baddateonly:
                                    try:
                                        # if not annotatecatONLY:
                                        if valuevalid and not catagoricalval:
                                            if baddata:
                                                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                                                              qualitycodecv=qualitycodebad, timeaggregationinterval=1,
                                                                              timeaggregationintervalunitsid=newtimeunit)
                                            elif unknown:
                                                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                                                              qualitycodecv=qualitycodeunkown, timeaggregationinterval=1,
                                                                              timeaggregationintervalunitsid=newtimeunit)
                                            else:
                                                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                                                              timeaggregationintervalunitsid=newtimeunit)
                                            tsrv.save()
                                            #  if i <500:
                                            #      print('SAVE')
                                            #      print(tsrv)
                                            # if edittime:

                                            # print('TIME EDITED')
                                            # print(tsrv)
                                            # print(tsrv.valueid)
                                            # print(r.resultid)
                                            if annotate:
                                                annotation.save()
                                                tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                                         annotationid=annotation).save()
                                    except Exception as e:
                                        # print('INTEGRITY ERROR')
                                        # lfile.writelines(e.message)
                                        # print(val)
                                        lfile.writelines(
                                            'Integrity error 1: ' + str(val) + ', ' + str(datet) + '\r\n')
                                        # lfile.writelines(str(row) + '\r\n')
                                        if not stopatdupvalue:
                                            pass
                                        else:
                                            lfile.writelines(
                                                'Integrity error 1: ' + str(val) + ', ' + str(datet) + '\r\n')
                                            lfile.writelines(str(row) + '\r\n')
                                            print('dup value found in: ' + filename + ' for row: ' + str(row))
                                            break

                                    if catagoricalval: # and annotatecatONLY
                                        cr = None
                                        # print(row)
                                        try:
                                            cr = Categoricalresults.objects.get(resultid=r)
                                        except ObjectDoesNotExist:
                                            cr = Categoricalresults(resultid=r, qualitycodecv=qualitycode).save()
                                            # print(cr)
                                            # zlocationunitsid=zlocationunits,
                                            # zlocation=zval
                                        cr = Categoricalresults.objects.get(resultid=r)
                                        # print(cr)
                                        val = row[28]
                                        try:
                                            # print(val)
                                            # print(datet)
                                            crv = Categoricalresultvalues(resultid=cr, datavalue=val, valuedatetime=datet,
                                                                          valuedatetimeutcoffset=-5)
                                            crv.save()
                                            # print('CAT VAL')
                                            # print(crv)
                                            if annotate:
                                                annotation = Annotations(annotationtypecv=annotationtypeCatcv,
                                                                         annotationcode=annocode[0:50],
                                                                         annotationtext=annotationtext,
                                                                         annotationdatetime=annotationdatetime,
                                                                         annotationutcoffset=4,
                                                                         annotatorid=annotatorid)
                                                annotation.save()
                                                crva = Categoricalresultvalueannotations(valueid=crv,
                                                                                         annotationid=annotation).save()
                                        except Exception as e:
                                            # print('INTEGRITY ERROR')
                                            # lfile.writelines(e.message)
                                            # print(val)
                                            # print(crv)
                                            # if annotate:
                                            # print(annotation)
                                            lfile.writelines(
                                                'Integrity error 2: ' + str(val) + ', ' + str(datet) + '\r\n')
                                # except UniqueViolation:
                except Exception as e:
                    print('ERROR ERROR')
                    print(filename)
                    print(row)
                    print(str(e))
                    traceback.print_exc()
                    lfile.writelines('ERROR ERROR')
                    lfile.writelines(filename)
                    lfile.writelines(row)
                    lfile.writelines(str(e))


directory = './omit/PREP/2022/todo/'
multithread = True
if __name__ == '__main__':
    processes = []
    p = None
    baddateonly=False
    stopatdupvalue = False
    # last new timeseriesresultvalues.valueid = 72223559
    for filename in os.listdir(directory):
        print(filename)
        if multithread:
            p = Process(target=loadgrabdata, args=(directory,filename, baddateonly,stopatdupvalue))
            p.start()
            # p.join()
        else:
            loadgrabdata(directory,filename, baddateonly,stopatdupvalue)