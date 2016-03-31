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
import modelHelpers
#range 0 to 26.7
#measurementresutlannotations; annotations

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
