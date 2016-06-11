__author__ = 'leonmi'

from ODM2CZOData.models import *
import os
import csv
from django.db.models import Avg, Max, Min
from django.db.models import F
from datetime import datetime
import warnings
import time
from django.db import transaction
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")
from django.db.models import Q
from  django.core.exceptions import MultipleObjectsReturned


#searchTextString = some string to search a models charField for
# Model = the model in which to search
# columnName = the name of the charField column to search in
#return = if one model object matches the search string return the object
# if multiple objects are returned print those objects and return None.
# example: searchModelColumnFor(" milligrams per kilogram ",Units,'unitsname')
def searchModelColumnFor(searchTextString,Model,columnName):
    searchText= re.split(',| ',searchTextString)
    searchText = filter(lambda name: name.strip(), searchText)
    modelObjects = Model.objects.all()

    #variable_column = 'variable_name__name'
    search_type = 'icontains'
    filter2 = columnName + '__' + search_type
    for search_string in searchText:
        #namefield = "variable_name__name__icontains"
        modelObjects = modelObjects.filter(**{ filter2: search_string })
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

def newMeasurementResult(Level0values,plevel,printvals,save):
    resulttype = CvResulttype.objects.filter(name='Time series coverage').get()
    sonadoraval = Level0values[:1].get()

    faid=sonadoraval.resultid.resultid.featureactionid
    varid = sonadoraval.resultid.resultid.variableid
    unitid = sonadoraval.resultid.resultid.unitsid
    taxid = sonadoraval.resultid.resultid.taxonomicclassifierid

    datetime = sonadoraval.resultid.resultid.resultdatetime
    datetimeoffset = sonadoraval.resultid.resultid.resultdatetimeutcoffset
    valcount = sonadoraval.resultid.resultid.valuecount
    samplemedium = sonadoraval.resultid.resultid.sampledmediumcv
    newr = Results(featureactionid=faid,result_type=resulttype,variableid=varid,unitsid=unitid,processing_level=plevel,
                taxonomicclassifierid=taxid,resultdatetime=datetime,resultdatetimeutcoffset=datetimeoffset,
                valuecount=valcount,sampledmediumcv=samplemedium)
    if save: newr.save()
    if printvals: print(plevel)
    if printvals: print(newr)

    censorcode = sonadoraval.resultid.censorcodecv
    qualitycode = sonadoraval.resultid.qualitycodecv
    aggregationstatistic = sonadoraval.resultid.aggregationstatisticcv
    timeaggregationinterval = sonadoraval.resultid.timeaggregationinterval
    timeaggregationintervalunitsid = sonadoraval.resultid.timeaggregationintervalunitsid
    newmr= Measurementresults(resultid=newr,censorcodecv=censorcode,qualitycodecv=qualitycode,aggregationstatisticcv=aggregationstatistic,
            timeaggregationinterval=timeaggregationinterval,timeaggregationintervalunitsid=timeaggregationintervalunitsid)
    if save: newmr.save()
    if printvals: print(newmr)
    return newmr
#badperiod = mrvsSonadoraTemp.filter(valuedatetime__gte='2015-04-24 15:15').filter(valuedatetime_lte='2015-05-18  11:15:00')
def QAProcessLevelCreation(SeriesToProcess,result,timeRangesToRemove,printvals,save,highThreshold,lowThreshold,annotationtextHigh,annotationtextLow,annotationtextDateRange):
    QAFlagHigh = False
    QAFlagOutofWater = False
    QAFlagLow = False
    annotationtypecv = CvAnnotationtype.objects.filter(name="Measurement result value annotation").get()
    annotatorid = People.objects.filter(personid=1).get()
    with transaction.atomic():
        for mrv in SeriesToProcess:
            datavalue= mrv.datavalue
            valuedatetime= mrv.valuedatetime
            if printvals: print(valuedatetime)
            flagdatavalue= mrv.datavalue #datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            for range in timeRangesToRemove:
                #if printvals: print(range[0] + ' to ' + range[1])
                if valuedatetime >range[0] and valuedatetime < range[1]:
                    QAFlagOutofWater=True
                    datavalue = -6999
                    if printvals: print("bad " + str(mrv))
            if datavalue >highThreshold:
                QAFlagHigh=True
                datavalue = -6999
                if printvals: print("bad " + str(mrv))
            elif datavalue <=lowThreshold:
                QAFlagLow=True
                datavalue = -6999
                if printvals: print("bad " + str(mrv))
            elif not QAFlagOutofWater:
                if printvals: print("good " + str(mrv))
            valuedatetime=mrv.valuedatetime
            valuedatetimeutcoffset=mrv.valuedatetimeutcoffset
            newmrv = Measurementresultvalues(resultid=result,datavalue=datavalue,valuedatetime=valuedatetime,
                                             valuedatetimeutcoffset=valuedatetimeutcoffset)
            if save: newmrv.save()
            if printvals: print(str(newmrv))
            if QAFlagHigh or QAFlagOutofWater:
                if QAFlagHigh:
                    annotationtext = annotationtextHigh+ str(flagdatavalue) + " on " + str(valuedatetime)
                    annotationdatetime = datetime.now()
                    newanno = Annotations(annotationtypecv=annotationtypecv,annotationcode="Value out of Range: High",
                                          annotationtext=annotationtext,annotationdatetime=annotationdatetime,annotationutcoffset=5,annotatorid=annotatorid)
                elif QAFlagOutofWater:
                    annotationtext = annotationtextDateRange+ str(flagdatavalue) + " on " + str(valuedatetime)
                    annotationdatetime = datetime.now()
                    newanno = Annotations(annotationtypecv=annotationtypecv,annotationcode="Date range excluded",
                                          annotationtext=annotationtext,annotationdatetime=annotationdatetime,annotationutcoffset=5,annotatorid=annotatorid)
                if save: newanno.save()
                newmrvanno= Measurementresultvalueannotations(valueid=newmrv,annotationid=newanno)
                if save: newmrvanno.save()
            if QAFlagLow:
                annotationtext = annotationtextLow + str(flagdatavalue)
                annotationdatetime = datetime.now()
                newanno = Annotations(annotationtypecv=annotationtypecv,annotationcode="Value out of Range: Low",
                                      annotationtext=annotationtext,annotationdatetime=annotationdatetime,annotationutcoffset=5,annotatorid=annotatorid)
                if save: newanno.save()
                newmrvanno= Measurementresultvalueannotations(valueid=newmrv,annotationid=newanno)
                if save: newmrvanno.save()
            QAFlagHigh=False
            QAFlagLow=False
            QAFlagOutofWater=False



def groupSites(featurecode,containerfeaturecode):
    samplingfeatures = Samplingfeatures.objects.filter(samplingfeaturecode__icontains=featurecode).filter(~Q(sampling_feature_type = "Field area"))
    #relatedfeatures = Samplingfeatures.objects.extra(where=["CHAR_LENGTH(samplingfeaturecode) < 11"])#samplingfeaturecode__icontains='PALMDYS-22')
    #relatedfeatures = relatedfeatures.filter(sampling_feature_type="Excavation")
    # #MyModel.objects.extra(where=["CHAR_LENGTH(text) > 300"])
    print(containerfeaturecode)
    #print(containerfeatureCode2)
    groups = Samplingfeatures.objects.filter(samplingfeaturecode=containerfeaturecode)
    #if groups.__len__() >1:
    #    for g in groups:
    #        if str(g.samplingfeaturecode).endswith(containerfeaturecode):
    #            group = g
    #else:
    group = groups.get()
    #print(group)
    relationshiptype = CvRelationshiptype.objects.filter(name='Is part of').get()
    for samplingfeature in samplingfeatures:
        #if relatedfeature.samplingfeaturecode in samplingfeature.samplingfeaturecode:
        #print(str(group) + " contains " + str(samplingfeature))
        if samplingfeature.samplingfeatureid != group.samplingfeatureid:
            rf = Relatedfeatures(samplingfeatureid=samplingfeature,relatedfeatureid=group,relationshiptypecv=relationshiptype)
            print(rf)
            #rf.save()

def importValues(file,variableFileIndex,variableDBID,variableUnitID,actionID,save):
    infile = open(file, "rt")#open('50-80cmHorizon.csv', "rt")
    reader = csv.reader(infile)

    var = list()
    featureCode = list()
    containerfeatureCode = list()
    #containerfeatureCode2 = list()
    zspacinglist = list()
    zintervallist=list()

    xylist = list()
    zlist = list()
    count = 0
    for line in reader:
        count +=1
        if count <2:
            continue
        var.append(line[variableFileIndex])
        featureCode.append(line[1])
        containerfeatureCode.append(line[2])
        #containerfeatureCode2.append('-'+line[4][:1])
        zspacinglist.append(line[10])
        zintervallist.append(line[11])
        xylist.append("POINT("+line[4] + " " + line[3]+")")
        zlist.append(line[5])
    features = Samplingfeatures.objects.filter(samplingfeaturecode__in=featureCode)
    if features.__len__()==0: #create features
        featuretype= CvSamplingfeaturetype.objects.filter(name="Excavation").get()
        featuregeotype= CvSamplingfeaturegeotype.objects.filter(name="Point").get()
        oldfc = None
        for fc,xy,z in zip(featureCode, xylist, zlist):
            if fc !=oldfc:
                newSF = Samplingfeatures(sampling_feature_type=featuretype,samplingfeaturecode=fc,samplingfeaturename=fc,
                            samplingfeaturedescription="Stone M.M. et al. site, see http://dx.doi.org/10.1016/j.soilbio.2014.10.019",
                            sampling_feature_geo_type=featuregeotype,featuregeometry=xy,elevation_m=z)
                #print(newSF)
            oldfc= fc

            #if save:
            #newSF.save()
        features = Samplingfeatures.objects.filter(samplingfeaturecode__in=featureCode)
    for feature in features:
        print(feature)

        #print(feature.samplingfeatureid)
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
    featureactions = Featureactions.objects.filter(samplingfeatureid__in=features.values("samplingfeatureid")).filter(action=actionID)
    #print(featureactions)
    act = Actions.objects.filter(actionid=actionID).get()
    #print(type(act))
    if featureactions.__len__()==0:
        famissing=features.filter(~Q(samplingfeatureid__in=featureactions.values("samplingfeatureid")))
        for feature in famissing:
                newFA=Featureactions(samplingfeatureid=feature,action=act)
                #newFA.save()
                print(newFA)
    for value,fCode,containerFCode,zspacing,zinterval in zip(var,featureCode,containerfeatureCode,zspacinglist,zintervallist):
        #for fCode in featureCode:
        #print(fCode)
        feature = Samplingfeatures.objects.filter(samplingfeaturecode=fCode).get()
        #groupSites(feature.samplingfeaturecode,containerFCode)
        #print(feature)
        featureaction = Featureactions.objects.filter(samplingfeatureid=feature).get()
        if fCode in featureaction.samplingfeatureid.samplingfeaturecode:

            result = Results(featureactionid=featureaction, variableid=variable, unitsid=unit, result_type=resulttype,
                              processing_level=processinglevel, statuscv=status, sampledmediumcv= medium,valuecount=1)

            print(featureaction)
            if save:
                result.save()
            presult = Profileresults(resultid=result, intendedzspacing=zspacing, intendedzspacingunitsid=zspaceunit,aggregationstatisticcv=aggStat)
            print(presult)
            if save:
                presult.save()
            presultvalue = Profileresultvalues(resultid=presult,datavalue=value,zlocation=zspacing,zaggregationinterval=zinterval,
                                                 zlocationunitsid=zspaceunit,qualitycodecv=qualityCode,censorcodecv=censorCode,
                                                  valuedatetime='2011-01-01 00:00:00',valuedatetimeutcoffset=4,
                                                 timeaggregationinterval=0,timeaggregationintervalunitsid=timaggunits)
            print(presultvalue)
            if save:
                presultvalue.save()
