import csv

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.db.models import Min, Max
import pandas as pd
import numpy
import math
import re
from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction
from django.db.models import Q

from odm2admin.models import Actions
from odm2admin.models import Annotations
from odm2admin.models import CvAggregationstatistic
from odm2admin.models import CvAnnotationtype
from odm2admin.models import CvCensorcode
from odm2admin.models import CvMedium
from odm2admin.models import CvQualitycode
from odm2admin.models import CvRelationshiptype
from odm2admin.models import CvResulttype
from odm2admin.models import CvStatus
from odm2admin.models import CvDataqualitytype
from odm2admin.models import Dataquality
from odm2admin.models import Timeseriesresults
from odm2admin.models import Featureactions
from odm2admin.models import Measurementresults
from odm2admin.models import Measurementresultvalueannotations
from odm2admin.models import Measurementresultvalues
from odm2admin.models import People
from odm2admin.models import Processinglevels
from odm2admin.models import Profileresults
from odm2admin.models import Profileresultvalues
from odm2admin.models import Relatedfeatures
from odm2admin.models import Results
from odm2admin.models import Resultsdataquality
from odm2admin.models import Samplingfeatures
from odm2admin.models import Units
from odm2admin.models import Variables

__author__ = 'leonmi'


def new_results_dataquality_upper_and_lower_bounds(unit, variable, upperbound, lowerbound, save=False):
    upper_bound_quality_type = CvDataqualitytype.objects.get(name = 'Physical limit upper bound')
    lower_bound_quality_type = CvDataqualitytype.objects.get(name = 'Physical limit lower bound')

    lower_bound= Dataquality(dataqualitytypecv=lower_bound_quality_type,
        dataqualitycode=str(variable.variablecode) + ' lower bound',
        dataqualityvalue=lowerbound,dataqualityvalueunitsid=unit,
        dataqualitydescription='lower bound for ' + str(variable.variablecode))
    print(lower_bound)
    if save:
        lower_bound.save()
    upper_bound= Dataquality(dataqualitytypecv=upper_bound_quality_type,
        dataqualitycode=str(variable.variablecode) + ' upper bound',
        dataqualityvalue=upperbound,dataqualityvalueunitsid=unit,
        dataqualitydescription='lower bound for '+ str(variable.variablecode))
    print(upper_bound)
    if save:
        upper_bound.save()

    variables_results = Results.objects.filter(variableid=variable).filter(unitsid=unit).order_by('featureactionid')
    print('number of series to add bounds for ' + str(variables_results.count()))
    for variables_result in variables_results:
        upper_bound_dq = Resultsdataquality(resultid=variables_result,dataqualityid=upper_bound)
        lower_bound_dq = Resultsdataquality(resultid=variables_result,dataqualityid=lower_bound)
        print(upper_bound_dq)
        print(lower_bound_dq)
        if save:
            upper_bound_dq.save()
            lower_bound_dq.save()

    variable_data_quality=Resultsdataquality.objects.filter(resultid__in=variables_results)

    for varq in variable_data_quality:
        print(varq)


# searchTextString = some string to search a models charField for
# Model = the model in which to search
# columnName = the name of the charField column to search in
# return = if one model object matches the search string return the object
# if multiple objects are returned print those objects and return None.
# example: searchModelColumnFor(" milligrams per kilogram ",Units,'unitsname')
def searchModelColumnFor(searchTextString, Model, columnName):
    searchText = re.split(',| ', searchTextString)
    searchText = filter(lambda name: name.strip(), searchText)
    modelObjects = Model.objects.all()

    # variable_column = 'variable_name__name'
    search_type = 'icontains'
    filter2 = columnName + '__' + search_type
    for search_string in searchText:
        # namefield = "variable_name__name__icontains"
        modelObjects = modelObjects.filter(**{filter2: search_string})
    try:
        variable = modelObjects.get()
    except MultipleObjectsReturned:
        print("multiple items match this name, they are: ")
        for var in modelObjects:
            print(var)
        return None
    return variable


def unitIDLookup(unitsname):
    unit = Units.objects.filter(unitsname__name__icontains=unitsname).get()
    return unit.unitsid


def newMeasurementResult(Level0values, plevel, printvals, save):
    resulttype = CvResulttype.objects.filter(name='Time series coverage').get()
    sonadoraval = Level0values[:1].get()

    faid = sonadoraval.resultid.resultid.featureactionid
    varid = sonadoraval.resultid.resultid.variableid
    unitid = sonadoraval.resultid.resultid.unitsid
    taxid = sonadoraval.resultid.resultid.taxonomicclassifierid

    datetime = sonadoraval.resultid.resultid.resultdatetime
    datetimeoffset = sonadoraval.resultid.resultid.resultdatetimeutcoffset
    valcount = sonadoraval.resultid.resultid.valuecount
    samplemedium = sonadoraval.resultid.resultid.sampledmediumcv
    newr = Results(featureactionid=faid, result_type=resulttype, variableid=varid, unitsid=unitid,
                   processing_level=plevel,
                   taxonomicclassifierid=taxid, resultdatetime=datetime,
                   resultdatetimeutcoffset=datetimeoffset,
                   valuecount=valcount, sampledmediumcv=samplemedium)
    if save:
        newr.save()
    if printvals:
        print(plevel)
    if printvals:
        print(newr)

    censorcode = sonadoraval.resultid.censorcodecv
    qualitycode = sonadoraval.resultid.qualitycodecv
    aggregationstatistic = sonadoraval.resultid.aggregationstatisticcv
    timeaggregationinterval = sonadoraval.resultid.timeaggregationinterval
    timeaggregationintervalunitsid = sonadoraval.resultid.timeaggregationintervalunitsid
    newmr = Measurementresults(resultid=newr, censorcodecv=censorcode, qualitycodecv=qualitycode,
                               aggregationstatisticcv=aggregationstatistic,
                               timeaggregationinterval=timeaggregationinterval,
                               timeaggregationintervalunitsid=timeaggregationintervalunitsid)
    if save:
        newmr.save()
    if printvals:
        print(newmr)
    return newmr


# badperiod = mrvsSonadoraTemp.filter(valuedatetime__gte='2015-04-24 15:15').
# filter(valuedatetime_lte='2015-05-18  11:15:00')
def QAProcessLevelCreation(SeriesToProcess, result, timeRangesToRemove, printvals, save,
                           highThreshold, lowThreshold,
                           annotationtextHigh, annotationtextLow, annotationtextDateRange):
    QAFlagHigh = False
    QAFlagOutofWater = False
    QAFlagLow = False
    annotationtypecv = CvAnnotationtype.objects.filter(
        name="Measurement result value annotation").get()
    annotatorid = People.objects.filter(personid=1).get()
    with transaction.atomic():
        for mrv in SeriesToProcess:
            datavalue = mrv.datavalue
            valuedatetime = mrv.valuedatetime
            if printvals:
                print(valuedatetime)
            # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            flagdatavalue = mrv.datavalue
            for range in timeRangesToRemove:
                # if printvals: print(range[0] + ' to ' + range[1])
                if range[0] < valuedatetime < range[1]:
                    QAFlagOutofWater = True
                    datavalue = -6999
                    if printvals:
                        print("bad " + str(mrv))
            if datavalue > highThreshold:
                QAFlagHigh = True
                datavalue = -6999
                if printvals:
                    print("bad " + str(mrv))
            elif datavalue <= lowThreshold:
                QAFlagLow = True
                datavalue = -6999
                if printvals:
                    print("bad " + str(mrv))
            elif not QAFlagOutofWater:
                if printvals:
                    print("good " + str(mrv))
            valuedatetime = mrv.valuedatetime
            valuedatetimeutcoffset = mrv.valuedatetimeutcoffset
            newmrv = Measurementresultvalues(resultid=result, datavalue=datavalue,
                                             valuedatetime=valuedatetime,
                                             valuedatetimeutcoffset=valuedatetimeutcoffset)
            if save:
                newmrv.save()
            if printvals:
                print(str(newmrv))
            if QAFlagHigh or QAFlagOutofWater:
                if QAFlagHigh:
                    annotationtext = annotationtextHigh + str(flagdatavalue) + " on " + str(
                        valuedatetime)
                    annotationdatetime = datetime.now()
                    newanno = Annotations(annotationtypecv=annotationtypecv,
                                          annotationcode="Value out of Range: High",
                                          annotationtext=annotationtext,
                                          annotationdatetime=annotationdatetime,
                                          annotationutcoffset=5, annotatorid=annotatorid)
                elif QAFlagOutofWater:
                    annotationtext = annotationtextDateRange + str(flagdatavalue) + " on " + str(
                        valuedatetime)
                    annotationdatetime = datetime.now()
                    newanno = Annotations(annotationtypecv=annotationtypecv,
                                          annotationcode="Date range excluded",
                                          annotationtext=annotationtext,
                                          annotationdatetime=annotationdatetime,
                                          annotationutcoffset=5, annotatorid=annotatorid)
                if save:
                    newanno.save()
                newmrvanno = Measurementresultvalueannotations(valueid=newmrv, annotationid=newanno)
                if save:
                    newmrvanno.save()
            if QAFlagLow:
                annotationtext = annotationtextLow + str(flagdatavalue)
                annotationdatetime = datetime.now()
                newanno = Annotations(annotationtypecv=annotationtypecv,
                                      annotationcode="Value out of Range: Low",
                                      annotationtext=annotationtext,
                                      annotationdatetime=annotationdatetime,
                                      annotationutcoffset=5, annotatorid=annotatorid)
                if save:
                    newanno.save()
                newmrvanno = Measurementresultvalueannotations(valueid=newmrv, annotationid=newanno)
                if save:
                    newmrvanno.save()
            QAFlagHigh = False
            QAFlagLow = False
            QAFlagOutofWater = False


def groupSites(featurecode, containerfeaturecode):
    samplingfeatures = Samplingfeatures.objects.filter(
        samplingfeaturecode__icontains=featurecode).filter(
        ~Q(sampling_feature_type="Field area"))
    # relatedfeatures = Samplingfeatures.objects.extra(where=["CHAR_LENGTH(samplingfeaturecode)
    # < 11"])
    # samplingfeaturecode__icontains='PALMDYS-22')
    # relatedfeatures = relatedfeatures.filter(sampling_feature_type="Excavation")
    # #MyModel.objects.extra(where=["CHAR_LENGTH(text) > 300"])
    print(containerfeaturecode)
    # print(containerfeatureCode2)
    groups = Samplingfeatures.objects.filter(samplingfeaturecode=containerfeaturecode)
    # if groups.__len__() >1:
    #    for g in groups:
    #        if str(g.samplingfeaturecode).endswith(containerfeaturecode):
    #            group = g
    # else:
    group = groups.get()
    # print(group)
    relationshiptype = CvRelationshiptype.objects.filter(name='Is part of').get()
    for samplingfeature in samplingfeatures:
        # if relatedfeature.samplingfeaturecode in samplingfeature.samplingfeaturecode:
        # print(str(group) + " contains " + str(samplingfeature))
        if samplingfeature.samplingfeatureid != group.samplingfeatureid:
            rf = Relatedfeatures(samplingfeatureid=samplingfeature, relatedfeatureid=group,
                                 relationshiptypecv=relationshiptype)
            print(rf)
            # rf.save()


def importValues(file, variableFileIndex, variableDBID, variableUnitID, actionID, save):
    infile = open(file, "rt")  # open('50-80cmHorizon.csv', "rt")
    reader = csv.reader(infile)

    var = list()
    featureCode = list()
    containerfeatureCode = list()
    # containerfeatureCode2 = list()
    zspacinglist = list()
    zintervallist = list()

    xylist = list()
    zlist = list()
    count = 0
    for line in reader:
        count += 1
        if count < 2:
            continue
        var.append(line[variableFileIndex])
        featureCode.append(line[1])
        containerfeatureCode.append(line[2])
        # containerfeatureCode2.append('-'+line[4][:1])
        zspacinglist.append(line[10])
        zintervallist.append(line[11])
        xylist.append("POINT(" + line[4] + " " + line[3] + ")")
        zlist.append(line[5])
    features = Samplingfeatures.objects.filter(samplingfeaturecode__in=featureCode)
    if features.__len__() == 0:  # create features
        # featuretype = CvSamplingfeaturetype.objects.filter(name="Excavation").get()
        # featuregeotype = CvSamplingfeaturegeotype.objects.filter(name="Point").get()
        oldfc = None
        for fc, xy, z in zip(featureCode, xylist, zlist):
            if fc != oldfc:
                pass
                # print(newSF)
            oldfc = fc

            # if save:
            # newSF.save()
        features = Samplingfeatures.objects.filter(samplingfeaturecode__in=featureCode)
    for feature in features:
        print(feature)

        # print(feature.samplingfeatureid)
    variable = Variables.objects.filter(variableid=variableDBID).get()
    unit = Units.objects.filter(unitsid=variableUnitID).get()
    timaggunits = Units.objects.filter(unitsid=23).get()
    resulttype = CvResulttype.objects.filter(name='Measurement').get()
    processinglevel = Processinglevels.objects.filter(processinglevelid=2).get()
    status = CvStatus.objects.filter(name='Complete').get()
    medium = CvMedium.objects.filter(name='Soil').get()
    zspaceunit = Units.objects.filter(unitsid=18).get()
    qualityCode = CvQualitycode.objects.filter(name='Good').get()
    censorCode = CvCensorcode.objects.filter(name='Not censored').get()
    aggStat = CvAggregationstatistic.objects.filter(name='Average').get()
    featureactions = Featureactions.objects.filter(
        samplingfeatureid__in=features.values("samplingfeatureid")).filter(
        action=actionID)
    # print(featureactions)
    act = Actions.objects.filter(actionid=actionID).get()
    # print(type(act))
    if featureactions.__len__() == 0:
        famissing = features.filter(
            ~Q(samplingfeatureid__in=featureactions.values("samplingfeatureid")))
        for feature in famissing:
            newFA = Featureactions(samplingfeatureid=feature, action=act)
            # newFA.save()
            print(newFA)
    for value, fCode, containerFCode, zspacing, zinterval in zip(var, featureCode,
                                                                 containerfeatureCode, zspacinglist,
                                                                 zintervallist):
        # for fCode in featureCode:
        # print(fCode)
        feature = Samplingfeatures.objects.filter(samplingfeaturecode=fCode).get()
        # groupSites(feature.samplingfeaturecode,containerFCode)
        # print(feature)
        featureaction = Featureactions.objects.filter(samplingfeatureid=feature).get()
        if fCode in featureaction.samplingfeatureid.samplingfeaturecode:

            result = Results(featureactionid=featureaction, variableid=variable, unitsid=unit,
                             result_type=resulttype,
                             processing_level=processinglevel, statuscv=status,
                             sampledmediumcv=medium, valuecount=1)

            # print(featureaction)
            if save:
                result.save()
            presult = Profileresults(resultid=result, intendedzspacing=zspacing,
                                     intendedzspacingunitsid=zspaceunit,
                                     aggregationstatisticcv=aggStat)
            print(presult)
            if save:
                presult.save()
            presultvalue = Profileresultvalues(resultid=presult, datavalue=value,
                                               zlocation=zspacing,
                                               zaggregationinterval=zinterval,
                                               zlocationunitsid=zspaceunit,
                                               qualitycodecv=qualityCode,
                                               censorcodecv=censorCode,
                                               valuedatetime='2011-01-01 00:00:00',
                                               valuedatetimeutcoffset=4,
                                               timeaggregationinterval=0,
                                               timeaggregationintervalunitsid=timaggunits)
            print(presultvalue)
            if save:
                presultvalue.save()

def interpolateMissingHI(hystIndex,raisingfalling,responseanddis,interval,lastinterval,i,maxWidth,closestopposite=None):
    # find discharge value closest to interval and last interval
    # if raisingfalling == 'raising':
    closestunderrow = None
    closestoverrow = None
    closestoverfallingrow = None
    closestoverraisingrow = None
    lastclosestoverrow = None
    closestunderfallingrow = None
    closestunderraisingrow = None
    lastclosestunderrow = None
    #rescale interval

    x = 0
    x0 = 0
    xf = 0
    xr = 0
    xf0 = 0
    xr0 = 0
    y = 0
    y0 = 0
    yf = 0
    yr = 0
    yr0 = 0
    yf0 = 0
    for index, row in responseanddis.iterrows():

        if row['datavaluedis'] > 0:
            if closestunderfallingrow is None and raisingfalling == 'raising and falling':
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalue']):
                        closestunderfallingrow = row
            if closestunderraisingrow is None and raisingfalling == 'raising and falling':
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalueraising']):
                            closestunderraisingrow = row
            if closestunderrow is None:
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                        # print(row)
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        # print('HERHEHEHE')
                        closestunderrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestunderrow = row

            else:
                if row['datavaluedis'] < lastinterval and row['datavaluedis'] > closestunderrow['datavaluedis']:
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        closestunderrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestunderrow = row
                    elif raisingfalling =='raising and falling':
                        # print(row)
                        if not math.isnan(row['datavalue']):
                            closestunderfallingrow = row
                        if not math.isnan(row['datavalueraising']):
                            closestunderraisingrow = row

            if closestoverrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        closestoverrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestoverrow = row
            if raisingfalling == 'raising and falling' and closestoverfallingrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalue']):
                        closestoverfallingrow = row
                        # closestoverrow = row
            if raisingfalling == 'raising and falling' and closestoverraisingrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalueraising']):
                        closestoverraisingrow = row
                    # closestoverrow = row
            if closestoverrow is not None:
                if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverrow['datavaluedis']:
                        if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                            closestoverrow = row
                        elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                            closestoverrow = row
            if raisingfalling == 'raising and falling':
                # print('assign closestoverfallingrow and closestoverraisingrow')
                # print(row['datavalue'])
                # print(row['datavalueraising'])
                # print('closest over raising row?')
                # print(row['valuedatetime'])
                if closestoverfallingrow is not None:
                    # print(closestoverfallingrow['datavaluedis'])
                    # print(closestoverfallingrow['datavalue'])
                    if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverfallingrow['datavaluedis']:
                        if not math.isnan(row['datavalue']):
                            closestoverfallingrow = row
                if closestoverraisingrow is not None:
                   #  print(closestoverraisingrow['datavaluedis'])
                    # print(closestoverraisingrow['datavalueraising'])
                    if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverraisingrow['datavaluedis']:
                        if not math.isnan(row['datavalueraising']):
                            # print('HERE@@@@&')
                            closestoverraisingrow = row
                    #print('yf!!!!')
                    #print(closestoverrow['datavalue'])
                    #print(yf)
        if closestunderrow is not None and closestoverrow is not None:
            if raisingfalling == 'raising' :
                if  (math.isnan(row['datavaluedis']) or math.isnan(row['datavalueraising'])):
                    continue
                x0 = closestunderrow['datavaluedis']
                x = closestoverrow['datavaluedis']
                y0 = closestunderrow['datavalueraising']
                y = closestoverrow['datavalueraising']
            elif raisingfalling == 'falling':
                # print(closestunderrow['datavaluedis'])
                # print(closestoverrow['datavaluedis'])
                # print(closestunderrow['datavaluefalling'])
                # print(closestoverrow['datavaluefalling'])
                if (math.isnan(row['datavaluedis']) or math.isnan(row['datavaluefalling'])):
                    continue
                x0 = closestunderrow['datavaluedis']
                x = closestoverrow['datavaluedis']
                y0 = closestunderrow['datavaluefalling']
                y = closestoverrow['datavaluefalling']
        if raisingfalling =='raising and falling':
            #if math.isnan(row['datavaluedis']): # or math.isnan(row['datavalueraising'])or math.isnan(row['datavalue'])
            #    continue
            # x0 = closestunderrow['datavaluedis']
            # print('NAN????')
            if closestunderraisingrow is not None:
                if not math.isnan(closestunderraisingrow['datavaluedis']):
                    xr0 = closestunderraisingrow['datavaluedis']
            if closestunderfallingrow is not None:
                if not math.isnan(closestunderfallingrow['datavaluedis']):
                    xf0 = closestunderfallingrow['datavaluedis']

            if closestoverraisingrow is not None:
                # print(closestoverraisingrow['datavaluedis'])
                if not math.isnan(closestoverraisingrow['datavaluedis']):
                    xr = closestoverraisingrow['datavaluedis']
            if closestoverfallingrow is not None:
                # print(closestoverfallingrow['datavaluedis'])
                if not math.isnan(closestoverfallingrow['datavaluedis']):
                    xf = closestoverfallingrow['datavaluedis']

            if closestunderraisingrow is not None:
                # print(closestunderraisingrow['datavalueraising'])
                if not math.isnan(closestunderraisingrow['datavalueraising']): # or math.isnan(row['datavalueraising'])or math.isnan(row['datavalue'])
                    yr0 = closestunderraisingrow['datavalueraising']

            if not closestunderfallingrow is None:
                # print(closestunderfallingrow['datavalue'])
                if not math.isnan(closestunderfallingrow['datavalue']):
                    yf0 = closestunderfallingrow['datavalue']  # this is falling limb; it didn't receive a suffix in this case
                #if not math.isnan(closestunderrow['datavalue']):
                #    yf = closestunderrow['datavalue']

            # print('over!!!')
            # print(interval)
            if closestoverraisingrow is not None:
                if not math.isnan(closestoverraisingrow['datavalueraising']):
                    yr = closestoverraisingrow['datavalueraising']
            if closestoverfallingrow is not None:
                if not math.isnan(closestoverfallingrow['datavalue']): # falling
                    yf = closestoverfallingrow['datavalue']



    xmidpoint = (lastinterval - interval) / 2

    m = 0
    b = 0

    estimatedresponse = 0
    if not raisingfalling == 'raising and falling' and not x == x0:
        # print('x: '+str(x))
        # print('x0: ' + str(x0))
        m = (y-y0)/(x-x0)
        b = y - m*x
        estimatedresponse = m*xmidpoint +b
    HI = None
    # print('closest rows')
    # print(raisingfalling)


    if raisingfalling == 'raising and falling' and not xf == xf0 and not xr == xr0:
        # print('raising and falling components')
        # print('interval ' + str(interval))
        # print('lastinterval ' + str(lastinterval))
        # print(responseanddis['datavaluedis'].describe())
        #responsenormpdf[(responsenormpdf['valuedatetime'] <= maxnormdischargedate)]
        aboveinterval = responseanddis[responseanddis['datavaluedis'] >= interval]
        raisingaboveinterval = aboveinterval[~aboveinterval['datavalueraising'].isnull()]
        # print("discharge above interval " + str(len(responseanddis[responseanddis['datavaluedis'] >= interval])))
        # print("riasing response above interval " + str(len(aboveinterval)))
        # print("riasing response above interval not na " + str(len(raisingaboveinterval)))
        belowlastinterval = responseanddis[responseanddis['datavaluedis'] < lastinterval]
        # print("riasing response below last interval " + str(len(belowlastinterval)))
        # print(aboveinterval.head())

        fallingaboveinterval = responseanddis[responseanddis['datavaluedis'] > interval]
        fallingaboveintervalnonan = aboveinterval[~aboveinterval['datavalue'].isnull()]


        # print(closestoverrow)
        mr = (yr - yr0) / (xr - xr0)
        yrmidpoint = (yr + yr0) / 2
        xrmidpoint = (xr + xr0) / 2
        br = yrmidpoint - mr * xrmidpoint
        estimatedresponseraising = mr * xrmidpoint + br
        # print('midpoint y: ' + str(yrmidpoint))
        # print('estimatedresponseraising: ' + str(estimatedresponseraising))
        mf = (yf - yf0) / (xf - xf0)
        yfmidpoint = (yf + yf0) / 2
        xfmidpoint = (xf + xf0) / 2
        bf = yfmidpoint - mf * xfmidpoint
        estimatedresponsefalling = mf * xfmidpoint + bf
        HI = estimatedresponseraising - estimatedresponsefalling
        # print('mr: '+ str(mr))
        # print('br: ' + str(br))
    #closestopposite
    if raisingfalling == 'raising':
        HI = estimatedresponse - closestopposite['datavaluefalling']
        # print('HI: ' +  str(tmp))
    elif raisingfalling == 'falling':
        HI = closestopposite['datavalueraising'] - estimatedresponse

    hystIndex['Interpolated HI for ' + str(i * 2) + '% discharge'] = HI
    # else:
    #     hystIndex['Interpolated HI for ' + str(i * 2) + '% discharge'] = 'no values present'
    if maxWidth and HI:
        if abs(HI) > abs(maxWidth):
            maxWidth = HI
    elif HI:
        maxWidth = HI


    return hystIndex,maxWidth


def hysteresisMetrics(discharge,response, debug=False, interpall=True):
    hystdict = {}
    HIsandInterp = []
    #normalize times for discharge
    discharge = discharge.order_by('valuedatetime')
    response = response.order_by('valuedatetime')
    dischargetsr = Timeseriesresults.objects.filter(resultid=discharge[0].resultid.resultid).get()
    dtimeagg = dischargetsr.intendedtimespacing
    dtimeaggunit = dischargetsr.intendedtimespacingunitsid.unitsname
    dischargepdf = pd.DataFrame(list(discharge.values()))
    if 'minute' in dtimeaggunit or 'Minutes' in dtimeaggunit:
        # print(responsenormpdf['valuedatetime'])
        # print(str(dtimeaggunit))
        # print(str(dischargetsr.resultid))
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60)) / dtimeagg))))
    if 'hour' in dtimeaggunit:
        dtimeagg = dtimeagg * 60
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60) / dtimeagg)))))

    maxdischarge = discharge.aggregate(Max('datavalue'))
    mindischarge = discharge.aggregate(Min('datavalue'))
    hystdict['Peak Q'] = maxdischarge['datavalue__max']
    hystdict['Min Q'] = mindischarge['datavalue__min']
    hystdict['discharge_units'] = str(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    # print('units!!')
    # print(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    hystdict['Normalized slope of response'] = None
    hystdict['Max width of response'] = None
    hystdict['Hysteresis_Index'] = {}
    hystdict["HI_mean"] = None
    hystdict["HI_standard_deviation"] = None
    hystdict["HI_count"] = 0
    hystdict["HI values missing due to no raising limb measurement"] = 0
    hystdict["HI values missing due to no falling limb measurement"] = 0
    hystdict["HI values missing due to no raising and no falling limb measurement"] = 0
    hystdict['interpolated Max width of response'] = float('nan')
    hystdict["HI_mean_with_Interp"] = None
    hystdict["HI_standard_deviation_with_Interp"] = None
    hystdict['HI_count_and_interp'] = None
    if maxdischarge:
        # print(maxdischarge['datavalue__max'])
        # normalize discharge
        maxdischargerecord = discharge.order_by('-datavalue')[0]# .get(datavalue=float(maxdischarge['datavalue__max']))
        mindischargerecord = discharge.order_by('datavalue')[0]
        # dischargenorm = []
       #  dischargepdf = pd.DataFrame(list(discharge.values()))
        dischargepdf['datavalue'] = (dischargepdf['datavalue']- mindischargerecord.datavalue)/(maxdischargerecord.datavalue - mindischargerecord.datavalue)
        # print(dischargepdf['datavalue'])
        maxdisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmax()]
        mindisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmin()]
        maxnormdischargerecord = maxdisrow['datavalue']
        maxnormdischargedate = maxdisrow['valuedatetime']
        minnormdischargerecord = mindisrow['datavalue']
        minnormdischargedate = mindisrow['valuedatetime']

        # print('discharge norm max: ' + str(maxnormdischargerecord))
        # print('discharge norm min: ' + str(minnormdischargerecord))
        # normalize response
        maxresponse = response.order_by('-datavalue')[0]# .get(datavalue=float(maxdischarge['datavalue__max']))
        minresponse = response.order_by('datavalue')[0]
        hystdict["Max response"] = maxresponse.datavalue
        hystdict["Min response"] = minresponse.datavalue
        # responsenorm = []
        responsenormpdf = pd.DataFrame(list(response.values()))
        responsenormpdf['datavalue'] = (responsenormpdf['datavalue']- minresponse.datavalue)/(maxresponse.datavalue - minresponse.datavalue)

        responsetsr = Timeseriesresults.objects.filter(resultid=response[0].resultid.resultid).get()
        timeagg =responsetsr.intendedtimespacing
        timeaggunit = responsetsr.intendedtimespacingunitsid.unitsname
        # print('timeaggunit')
        # print(timeaggunit)
        if 'minute' in timeaggunit or 'Minutes' in timeaggunit:
            # print(responsenormpdf['valuedatetime'])

            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))
        if 'hour' in timeaggunit:
            timeagg = timeagg * 60
            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))
        # print(maxdischargerecord)
        # print(maxdischargerecord.valuedatetime)
        # print('maxnormdischargedate ' + str(maxnormdischargedate))
        # print(responsenormpdf[responsenormpdf['valuedatetime'] == maxnormdischargedate]['valuedatetime'])
        raisinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] <= maxnormdischargedate)] # response.filter(valuedatetime__lte=maxdischargerecord.valuedatetime)
        fallinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] > maxnormdischargedate)]  # response.filter(valuedatetime__gt=maxdischargerecord.valuedatetime)
        # pd.DataFrame(list(raisinglimbresponse.values()))
        # print('response units ' +str(response[0].resultid.resultid.unitsid.unitsabbreviation))
        # print('falling limb val count: ' + str(len(fallinglimbresponse.index)))
        # print('raising limb val count: ' + str(len(raisinglimbresponse.index)))
        hystIndex = []
        # 5% intervals of discharge for hysteresis index 20 bucket
        if not len(raisinglimbresponse.index) == 0 and not len(fallinglimbresponse.index) == 0:

            dischargerange = maxnormdischargerecord- minnormdischargerecord
            dischargeinterval = dischargerange / 50
            hystIndex = {}
            maxWidth = None
            premaxWidth = None
            countMissingRaising = 0
            countMissingFalling = 0
            countHIs = 0
            countHIsandInterp = 0
            countMissingBoth = 0
            firstRaisingResponse = None
            firstRaisingDis = None
            lastRaisingResponse = None
            lastRaisingDis = None
            for i in range(1,51):
                if i == 1:
                    lastinterval = 0
                else:
                    lastinterval = interval
                interval = dischargeinterval*i
                #  print(' here interval: ' + str(interval))
                #dischargeintervalvals = discharge.filter(datavalue__lte=interval).filter(datavalue__gte=lastinterval)
                dischargeintervalvals = dischargepdf[(dischargepdf['datavalue'] <= interval) & (dischargepdf['datavalue'] > lastinterval)]
                # find matching response records
                # keys = list(dischargeintervalvals['valuedatetime'])
                dischargeandraisingresponse = pd.merge(dischargeintervalvals, raisinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','raising'))
                dischargeandfallingresponse = pd.merge(dischargeintervalvals, fallinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','falling'))

                if debug:
                    print('for interval: ' + str(interval))
                    # print(dischargeintervalvals.head())
                    # print(raisinglimbresponse.head())
                    # print('falling limb')
                    # print(fallinglimbresponse.head())
                    # print('raising response ' + str(len(dischargeandraisingresponse.index)))
                    # print(dischargeandraisingresponse['datavalueraising'])
                    #print(dischargeandraisingresponse.head())
                    # print('falling response ' + str(len(dischargeandfallingresponse.index)))
                    # print(dischargeandfallingresponse['datavaluefalling'])
                closestraisingrow = None
                closestfallingrow = None
                closestraisingdistance = None
                closestfallingdistance = None


                for index, raisingrow in dischargeandraisingresponse.iterrows():
                    # for slope calculation
                    if not firstRaisingDis:
                        if raisingrow['datavaluedis'] > 0:
                            firstRaisingDis = raisingrow['datavaluedis']
                    if not firstRaisingResponse:
                        if  raisingrow['datavalueraising'] > 0:
                            firstRaisingResponse = raisingrow['datavalueraising']
                    else:
                        if raisingrow['datavaluedis'] > 0:
                            lastRaisingDis = raisingrow['datavaluedis']
                        if raisingrow['datavalueraising'] > 0:
                            lastRaisingResponse = raisingrow['datavalueraising']

                    # for HI caclulation
                    if raisingrow['datavalueraising'] > 0:
                        if closestraisingdistance:
                            if abs(interval - raisingrow['datavaluedis']) < closestraisingdistance:
                                closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                                closestraisingrow = raisingrow
                        else:
                            closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                            closestraisingrow = raisingrow


                for index2, fallingrow in dischargeandfallingresponse.iterrows():
                    if fallingrow['datavaluefalling'] > 0: #and raisingrow['datavalueraising'] == fallingrow['datavaluefalling'] :
                        if closestfallingdistance:
                            if abs(interval - fallingrow['datavaluedis']) < closestfallingdistance:
                                closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                                closestfallingrow = fallingrow
                        else:
                            closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                            closestfallingrow = fallingrow
                       # print(raisingrow)
                       # print(fallingrow)

                dischargeandraisingresponseall = pd.merge(dischargepdf, raisinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'raising'))
                dischargeandfallingresponseall = pd.merge(dischargepdf, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'falling'))
                dischargeriaisingandfallingresponseall = pd.merge(dischargeandraisingresponseall, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('', 'raising'))
                if interpall:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                elif not closestraisingrow is None and not closestfallingrow is None:
                    # print('HERE HERE HERE')

                    tmp = closestraisingrow['datavalueraising'] - closestfallingrow['datavaluefalling']
                    # print('HI: ' +  str(tmp))
                    countHIs += 1
                    hystIndex['HI for ' + str(i*2) + '% discharge'] = tmp
                    if maxWidth:
                        if abs(tmp) > abs(maxWidth):
                            maxWidth = tmp
                    elif tmp:
                        maxWidth = tmp
                elif closestfallingrow is None and not closestraisingrow is None:
                    countMissingFalling += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'falling',dischargeandfallingresponseall,interval,lastinterval,i,maxWidth,closestraisingrow)
                elif closestraisingrow is None and not closestfallingrow is None:
                    countMissingRaising += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising',dischargeandraisingresponseall,interval,lastinterval,i,maxWidth,closestfallingrow)
                else:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                    # hystdict = interpolateMissingHI(hystdict,'raising', dischargeandraisingresponseall)
                if premaxWidth != maxWidth:
                    hystdict['interpolated Max width of response'] = maxWidth
                else:
                    hystdict['Max width of response'] = maxWidth
                # print('Max width ' + str(maxWidth))
                # print(hystIndex)
            raisingdf = raisinglimbresponse.sort_values(by='valuedatetime')
            firstraisingresponse = raisingdf.head(1).iloc[0]['datavalue']
            lastraisingresponse = raisingdf.tail(1).iloc[0]['datavalue']

            hystdict['Normalized slope of response'] = lastraisingresponse - firstraisingresponse  # / (lastRaisingDis - firstRaisingDis)
            if hystdict['Normalized slope of response'] == 0:
                print('what???')
                # print('raising response ' + str(len(raisinglimbresponse.index)))
                # print(firstraisingresponse)
                # print(lastraisingresponse)
            # else:
            #     print('No slope!')
            hystdict["HI_count"] = countHIs
            hystdict["HI values missing due to no raising limb measurement"] = countMissingRaising
            hystdict["HI values missing due to no falling limb measurement"] = countMissingFalling
            hystdict["HI values missing due to no raising and no falling limb measurement"] = countMissingBoth
            HIs = []
            HIsandInterp = []
            for key, values in hystIndex.items():
                if not 'Interpolated' in key:
                    if values:
                        HIs.append(values)
                    # print('here here')
                    # print(values)
                #else:
                # print(values)
                if values:
                    HIsandInterp.append(values)
                # print('interper val')
                # print(values)
                if 'Hysteresis_Index' in hystdict:
                    if values:
                        hystdict['Hysteresis_Index'][key] = values
                        # print('HYST Index:' + key + ' val: ' + str(values))
                elif values:
                    tmpdict = {}

                    tmpdict[key ] = values
                    hystdict['Hysteresis_Index'] = tmpdict
                    # 3print('tmpdict: ' + key + 'val: ' +str(values))
            hystAvg = numpy.mean(HIs) #sum(values) / float(len(values))
            hystStd = numpy.std(HIs)
            hystAvgInterp = float('NaN')
            hystStdInterp = float('NaN')
            hystAvgInterp = numpy.mean(HIsandInterp) #sum(values) / float(len(values))
            hystStdInterp = numpy.std(HIsandInterp)
            # print(hystIndex)
            # print("HI mean: " + str(hystAvg))
            # print("HI standard deviation: " + str(hystStd))
            # print(HIsandInterp)
            hystdict["HI_count_and_interp"] = str(len(HIsandInterp))
            hystdict["HI_mean"] = str(hystAvg)
            hystdict["HI_standard_deviation"] = str(hystStd)

            hystdict["HI_mean_with_Interp"] = str(hystAvgInterp)
            hystdict["HI_standard_deviation_with_Interp"] = str(hystStdInterp)
            # hystdict['Hysteresis_Index'].append([key + " values: ", values])
            # print(hystdict)

            # print('hystdict!!')
            # print(hystdict)
            # print(hystdict["HI_mean_with_Interp"])
        # if HIsandInterp:
        #     if len(HIsandInterp) < 50:
        #         print('hystdict asdf')
        #         print('HIs and Interp count: ' + str(len(HIsandInterp)))
        #         print('max date discharge: ' + str(maxnormdischargedate))
        #         print('max response date: ' +str(maxresponse.valuedatetime))
        #         print('max response id: ' + str(maxresponse.resultid.resultid.resultid))
        #         for key, value in hystdict.items():
        #             print(str(key) + ': ' + str(value))
    return hystdict

def hysteresisMetricsPandasDF(discharge,response, discharge_time_spacing, response_time_spacing, debug=False, interpall=True,
                      discharge_time_spacing_units='minutes', response_time_spacing_units='minutes', discharge_units='CFS'):
    # River discharge response hysteresis loop statistics and hysteresis indices (HI) are calculated for
    # normalized discharge and response. With interpall=True (which is the default)HI values are calculated for 2%
    # intervals of discharge similar to what is described in Vaughan et al., 2017
    # (https://www.doi.org/10.1002/2017WR020491)
    # Args:
    #     discharge (pandas dataframe): a dataframe containing a datetime column named 'valuedatetime',  and discharge
    #                                   values in a column 'datavalue'
    #     response (pandas dataframe): a dataframe containing a datetime column named 'valuedatetime',  and a response
    #                                  variable with values in a column 'datavalue'
    #     discharge_time_spacing (int): amount of time between discharge measurements
    #     response_time_spacing (int): amount of time between response measurements
    #     debug (boolean): indicate if you want debugging print statements
    #     interpall (boolean): indicate if you would like all HI values to be interpolated to 2% intervals of discharge.
    #                          otherwise 2% intervals will pick the closest raising and falling limb response values to
    #                          each 2% interval (but will still interpolate the values if a response value does not
    #                          exist values will be interpolated.
    #      discharge_time_spacing_units (string): this should be 'minutes' or 'hours' and indicates the units for
    #                                             discharge_time_spacing
    #      response_time_spacing_units (string): this should be 'minutes' or 'hours' and indicates the units for
    #                                             response_time_spacing_units
    #      discharge_units (string): this is just included in the returned dictionary.
    #      Returns:
    #             hystdict (dictionary): A python dictionary containing the calculated statistics and indices.
    hystdict = {}
    HIsandInterp = []
    #sort values by date
    discharge = discharge.sort_values(by=['valuedatetime'])
    response = response.sort_values(by=['valuedatetime'])
    #normalize times for discharge
    dtimeagg = discharge_time_spacing # dischargetsr.intendedtimespacing
    dtimeaggunit = discharge_time_spacing_units # dischargetsr.intendedtimespacingunitsid.unitsname
    dischargepdf = discharge # pd.DataFrame(list(discharge.values()))
    if 'minute' in dtimeaggunit or 'Minutes' in dtimeaggunit:
        # print(responsenormpdf['valuedatetime'])
        #print(str(dtimeaggunit))
        #print(str(dischargetsr.resultid))
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60)) / dtimeagg))))
    if 'hour' in dtimeaggunit:
        dtimeagg = dtimeagg * 60
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60) / dtimeagg)))))

    maxdischargerow = dischargepdf.loc[dischargepdf['datavalue'].idxmax()] # discharge.aggregate(Max('datavalue'))
    maxdischarge = maxdischargerow['datavalue']
    hystdict['Peak Q'] = maxdischarge
    hystdict['discharge_units'] = discharge_units # str(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    # print('units!!')
    # print(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    hystdict['Normalized slope of response'] = None
    hystdict['Max width of response'] = None
    hystdict['Hysteresis_Index'] = {}
    hystdict["HI_mean"] = None
    hystdict["HI_standard_deviation"] = None
    hystdict["HI_count"] = 0
    hystdict["HI values missing due to no raising limb measurement"] = 0
    hystdict["HI values missing due to no falling limb measurement"] = 0
    hystdict["HI values missing due to no raising and no falling limb measurement"] = 0
    hystdict['interpolated Max width of response'] = float('nan')
    hystdict["HI_mean_with_Interp"] = None
    hystdict["HI_standard_deviation_with_Interp"] = None
    hystdict['HI_count_and_interp'] = None
    if maxdischarge:
        maxdischargerecord = dischargepdf.loc[dischargepdf['datavalue'].idxmax()]
        mindischargerecord = dischargepdf.loc[dischargepdf['datavalue'].idxmin()]
        #maxdischargerecord = discharge.order_by('-datavalue')[
        #    0]  # .get(datavalue=float(maxdischarge['datavalue__max']))
        #mindischargerecord = discharge.order_by('datavalue')[0]
        # dischargepdf = dischargepdf.sort_values(by=['valuedatetime'])
        dischargepdf['datavalue'] = (dischargepdf['datavalue'] - mindischargerecord['datavalue']) / (
                maxdischargerecord['datavalue'] - mindischargerecord['datavalue'])
        if debug:
            print('normalized discharge head')
            print(dischargepdf.head())
        maxdisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmax()]
        mindisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmin()]

        maxnormdischargerecord = maxdisrow['datavalue']
        maxnormdischargedate = maxdisrow['valuedatetime']
        minnormdischargerecord = mindisrow['datavalue']
        minnormdischargedate = mindisrow['valuedatetime']

        maxresponse = response.loc[response['datavalue'].idxmax()]
        minresponse = response.loc[response['datavalue'].idxmin()]
        hystdict["Max response"] = maxresponse['datavalue']
        hystdict["Min response"] = minresponse['datavalue']
        # responsenorm = []
        responsenormpdf = response
        responsenormpdf['datavalue'] = (responsenormpdf['datavalue']- minresponse.datavalue)/(maxresponse.datavalue - minresponse.datavalue)

        # responsetsr = Timeseriesresults.objects.filter(resultid=response[0].resultid.resultid).get()
        timeagg =response_time_spacing # responsetsr.intendedtimespacing
        timeaggunit = response_time_spacing_units # responsetsr.intendedtimespacingunitsid.unitsname
        if 'minute' in timeaggunit or 'Minutes' in timeaggunit:
            # print(responsenormpdf['valuedatetime'])

            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))
        if 'hour' in timeaggunit:
            timeagg = timeagg * 60
            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))

        raisinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] <= maxnormdischargedate)] # response.filter(valuedatetime__lte=maxdischargerecord.valuedatetime)
        fallinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] > maxnormdischargedate)]  # response.filter(valuedatetime__gt=maxdischargerecord.valuedatetime)

        hystIndex = []
        # 5% intervals of discharge for hysteresis index 20 bucket
        if not len(raisinglimbresponse.index) == 0 and not len(fallinglimbresponse.index) == 0:

            dischargerange = maxnormdischargerecord- minnormdischargerecord
            dischargeinterval = dischargerange / 50
            hystIndex = {}
            maxWidth = None
            premaxWidth = None
            countMissingRaising = 0
            countMissingFalling = 0
            countHIs = 0
            countHIsandInterp = 0
            countMissingBoth = 0
            firstRaisingResponse = None
            firstRaisingDis = None
            lastRaisingResponse = None
            lastRaisingDis = None
            for i in range(1,51):
                if i == 1:
                    lastinterval = 0
                else:
                    lastinterval = interval
                interval = dischargeinterval*i

                dischargeintervalvals = dischargepdf[(dischargepdf['datavalue'] <= interval) & (dischargepdf['datavalue'] > lastinterval)]
                # find matching response records
                # keys = list(dischargeintervalvals['valuedatetime'])
                dischargeandraisingresponse = pd.merge(dischargeintervalvals, raisinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','raising'))
                dischargeandfallingresponse = pd.merge(dischargeintervalvals, fallinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','falling'))

                if debug:
                    print('for interval: ' + str(interval))
                    print(dischargeintervalvals.head())
                    print(raisinglimbresponse.head())
                    print('falling limb')
                    print(fallinglimbresponse.head())
                    print('raising response ' + str(len(dischargeandraisingresponse.index)))
                    # print(dischargeandraisingresponse['datavalueraising'])
                    #print(dischargeandraisingresponse.head())
                    print('falling response ' + str(len(dischargeandfallingresponse.index)))
                    # print(dischargeandfallingresponse['datavaluefalling'])
                closestraisingrow = None
                closestfallingrow = None
                closestraisingdistance = None
                closestfallingdistance = None


                for index, raisingrow in dischargeandraisingresponse.iterrows():
                    # for slope calculation
                    if not firstRaisingDis:
                        if raisingrow['datavaluedis'] > 0:
                            firstRaisingDis = raisingrow['datavaluedis']
                    if not firstRaisingResponse:
                        if  raisingrow['datavalueraising'] > 0:
                            firstRaisingResponse = raisingrow['datavalueraising']
                    else:
                        if raisingrow['datavaluedis'] > 0:
                            lastRaisingDis = raisingrow['datavaluedis']
                        if raisingrow['datavalueraising'] > 0:
                            lastRaisingResponse = raisingrow['datavalueraising']

                    # for HI caclulation
                    if raisingrow['datavalueraising'] > 0:
                        if closestraisingdistance:
                            if abs(interval - raisingrow['datavaluedis']) < closestraisingdistance:
                                closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                                closestraisingrow = raisingrow
                        else:
                            closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                            closestraisingrow = raisingrow


                for index2, fallingrow in dischargeandfallingresponse.iterrows():
                    if fallingrow['datavaluefalling'] > 0: #and raisingrow['datavalueraising'] == fallingrow['datavaluefalling'] :
                        if closestfallingdistance:
                            if abs(interval - fallingrow['datavaluedis']) < closestfallingdistance:
                                closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                                closestfallingrow = fallingrow
                        else:
                            closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                            closestfallingrow = fallingrow

                dischargeandraisingresponseall = pd.merge(dischargepdf, raisinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'raising'))
                dischargeandfallingresponseall = pd.merge(dischargepdf, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'falling'))
                dischargeriaisingandfallingresponseall = pd.merge(dischargeandraisingresponseall, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('', 'raising'))
                if interpall:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                elif not closestraisingrow is None and not closestfallingrow is None:

                    tmp = closestraisingrow['datavalueraising'] - closestfallingrow['datavaluefalling']
                    # print('HI: ' +  str(tmp))
                    countHIs += 1
                    hystIndex['HI for ' + str(i*2) + '% discharge'] = tmp
                    if maxWidth:
                        if abs(tmp) > abs(maxWidth):
                            maxWidth = tmp
                    elif tmp:
                        maxWidth = tmp
                elif closestfallingrow is None and not closestraisingrow is None:
                    countMissingFalling += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'falling',dischargeandfallingresponseall,interval,lastinterval,i,maxWidth,closestraisingrow)
                elif closestraisingrow is None and not closestfallingrow is None:
                    countMissingRaising += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising',dischargeandraisingresponseall,interval,lastinterval,i,maxWidth,closestfallingrow)
                else:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                    # hystdict = interpolateMissingHI(hystdict,'raising', dischargeandraisingresponseall)
                if premaxWidth != maxWidth:
                    hystdict['interpolated Max width of response'] = maxWidth
                else:
                    hystdict['Max width of response'] = maxWidth
                # print('Max width ' + str(maxWidth))
                # print(hystIndex)
            raisingdf = raisinglimbresponse.sort_values(by='valuedatetime')
            firstraisingresponse = raisingdf.head(1).iloc[0]['datavalue']
            lastraisingresponse = raisingdf.tail(1).iloc[0]['datavalue']

            hystdict['Normalized slope of response'] = lastraisingresponse - firstraisingresponse  # / (lastRaisingDis - firstRaisingDis)

            hystdict["HI_count"] = countHIs
            hystdict["HI values missing due to no raising limb measurement"] = countMissingRaising
            hystdict["HI values missing due to no falling limb measurement"] = countMissingFalling
            hystdict["HI values missing due to no raising and no falling limb measurement"] = countMissingBoth
            HIs = []
            HIsandInterp = []
            for key, values in hystIndex.items():
                if not 'Interpolated' in key:
                    if values:
                        HIs.append(values)
                if values:
                    HIsandInterp.append(values)
                if 'Hysteresis_Index' in hystdict:
                    if values:
                        hystdict['Hysteresis_Index'][key] = values
                        # print('HYST Index:' + key + ' val: ' + str(values))
                elif values:
                    tmpdict = {}

                    tmpdict[key ] = values
                    hystdict['Hysteresis_Index'] = tmpdict
                    # 3print('tmpdict: ' + key + 'val: ' +str(values))
            hystAvg = numpy.mean(HIs) #sum(values) / float(len(values))
            hystStd = numpy.std(HIs)
            hystAvgInterp = float('NaN')
            hystStdInterp = float('NaN')
            hystAvgInterp = numpy.mean(HIsandInterp) #sum(values) / float(len(values))
            hystStdInterp = numpy.std(HIsandInterp)
            hystdict["HI_count_and_interp"] = str(len(HIsandInterp))
            hystdict["HI_mean"] = str(hystAvg)
            hystdict["HI_standard_deviation"] = str(hystStd)

            hystdict["HI_mean_with_Interp"] = str(hystAvgInterp)
            hystdict["HI_standard_deviation_with_Interp"] = str(hystStdInterp)
    return hystdict