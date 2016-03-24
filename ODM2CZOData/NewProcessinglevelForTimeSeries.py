__author__ = 'leonmi'


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")
from django.db.models import Q
from ODM2CZOData.models import Samplingfeatures
from ODM2CZOData.models import Profileresultvalues
from ODM2CZOData.models import Profileresults
from ODM2CZOData.models import Results
from ODM2CZOData.models import Featureactions
from ODM2CZOData.models import Samplingfeatures
from ODM2CZOData.models import Variables
from ODM2CZOData.models import Units
from ODM2CZOData.models import CvResulttype
from ODM2CZOData.models import Processinglevels
from ODM2CZOData.models import CvStatus
from ODM2CZOData.models import CvMedium
from ODM2CZOData.models import CvQualitycode
from ODM2CZOData.models import CvCensorcode
from ODM2CZOData.models import CvAggregationstatistic
from ODM2CZOData.models import Actions
from ODM2CZOData.models import Relatedfeatures
from ODM2CZOData.models import Measurementresults
from ODM2CZOData.models import Measurementresultvalues
from ODM2CZOData.models import Processinglevels
from ODM2CZOData.models import CvAnnotationtype
from ODM2CZOData.models import People
from django.db.models import Avg, Max, Min
from django.db.models import F
from ODM2CZOData.models import Measurementresultvalueannotations
from ODM2CZOData.models import Annotations
from datetime import datetime
import warnings
import time
from django.db import transaction

warnings.filterwarnings('ignore')
#variableid = 3 water temp
#variableid = 2 conductivity
#unitsid =1 microsimens per centimeter
#unitsid=3 celsius
#Sonadora Conductivity - featureaction 1 = http://lczodata.com/ODM2/ODM2CZOData/ODM2CZOData/featureactions/1/
mrvsSonadoraTemp = Measurementresultvalues.objects.filter(resultid__resultid__variableid=3)\
    .filter(resultid__resultid__unitsid=3).filter(resultid__resultid__featureactionid__samplingfeatureid=3).filter(resultid__resultid__featureactionid=1)\
    .filter(valuedatetime__gte='2014-01-01').filter(valuedatetime__lte='2015-12-30').order_by('valuedatetime')

#print(newmr)

#range 0 to 26.7
#measurementresutlannotations; annotations

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
            elif not QAFlagOutofWater:
                if printvals: print("good " + str(mrv))
            if datavalue <=lowThreshold:
                QAFlagLow=True
                datavalue = -6999
            valuedatetime=mrv.valuedatetime
            valuedatetimeutcoffset=mrv.valuedatetimeutcoffset
            newmrv = Measurementresultvalues(resultid=result,datavalue=datavalue,valuedatetime=valuedatetime,
                                             valuedatetimeutcoffset=valuedatetimeutcoffset)
            if save: newmrv.save()
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

timeRangesToRemove =list()
#timeRangesToRemove.append([datetime.strptime('2015-04-24 15:15', '%Y-%m-%d %H:%M'),datetime.strptime('2015-05-18  11:15', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-03-17 12:00', '%Y-%m-%d %H:%M'),datetime.strptime('2014-03-28  19:00', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-03-29 21:30', '%Y-%m-%d %H:%M'),datetime.strptime('2014-04-03  10:00', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-06-16 20:00', '%Y-%m-%d %H:%M'),datetime.strptime('2014-06-19  3:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-06-19 20:45', '%Y-%m-%d %H:%M'),datetime.strptime('2014-06-20  11:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-06-21 15:30', '%Y-%m-%d %H:%M'),datetime.strptime('2014-06-30  18:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-07-01 4:00', '%Y-%m-%d %H:%M'),datetime.strptime('2014-07-05  17:45', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2014-07-26 15:00', '%Y-%m-%d %H:%M'),datetime.strptime('2014-08-01  1:15', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([datetime.strptime('2015-04-24 15:00', '%Y-%m-%d %H:%M'),datetime.strptime('2015-05-08  11:15', '%Y-%m-%d %H:%M')])

printvals = True
save = False
annotationtextHigh = "Value above 43 degrees C, this is considered out of range for stream water temperature, Original value was "
annotationtextLow = "Values are out of range during this time period water level was low and probe was out of the water, Original value was "
annotationtextDateRange = "Value below 0 C, this is considered out of range for stream water temperature, Original value was"
#result to add the values too

plevel = Processinglevels.objects.filter(processinglevelid=2).get()
#result=Measurementresults.objects.filter(resultid=16153).get()
#QAProcessLevelCreation(mrvsSonadoraTemp,result,timeRangesToRemove,printvals,save,43,0,annotationtextHigh,annotationtextLow,annotationtextDateRange)

mrvsSonadoraCond = Measurementresultvalues.objects.filter(resultid__resultid__variableid=2)\
    .filter(resultid__resultid__unitsid=1).filter(resultid__resultid__featureactionid__samplingfeatureid=3).filter(resultid__resultid__featureactionid=1)\
    .filter(valuedatetime__gte='2014-01-01').filter(valuedatetime__lte='2016-03-23').order_by('valuedatetime')
#result=Measurementresults.objects.filter(resultid=16153).get()

annotationtextHigh = "Value above 1000 uS/cm, this is considered out of range for stream conductivity, Original value was "
annotationtextLow = "Values are out of range during this time period water level was low and probe was out of the water, Original value was "
annotationtextDateRange = "Value below 15 uS/cm, this is considered out of range for stream conductivity, Original value was"


#newmr=newMeasurementResult(mrvsSonadoraCond,plevel,printvals,save) #got 16156
newmr=Measurementresults.objects.filter(resultid=16156).get()
printvals = False
save = False
QAProcessLevelCreation(mrvsSonadoraCond,newmr,timeRangesToRemove,printvals,save,1000,15,annotationtextHigh,annotationtextLow,annotationtextDateRange)
