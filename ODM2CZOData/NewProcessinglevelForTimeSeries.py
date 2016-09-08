__author__ = 'leonmi'


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "templatesAndSettings.settings")

# from django.db.models import Q  # imported but unused
# from ODM2CZOData.models import Samplingfeatures  # imported but unused
# from ODM2CZOData.models import Profileresultvalues  # imported but unused
# from ODM2CZOData.models import Profileresults  # imported but unused
# from ODM2CZOData.models import Results  # imported but unused
# from ODM2CZOData.models import Featureactions  # imported but unused
# from ODM2CZOData.models import Samplingfeatures  # imported but unused
# from ODM2CZOData.models import Variables  # imported but unused
# from ODM2CZOData.models import Units  # imported but unused
# from ODM2CZOData.models import CvResulttype  # imported but unused
from ODM2CZOData.models import Processinglevels
# from ODM2CZOData.models import CvStatus  # imported but unused
# from ODM2CZOData.models import CvMedium  # imported but unused
# from ODM2CZOData.models import CvQualitycode  # imported but unused
# from ODM2CZOData.models import CvCensorcode  # imported but unused
# from ODM2CZOData.models import CvAggregationstatistic  # imported but unused
# from ODM2CZOData.models import Actions  # imported but unused
# from ODM2CZOData.models import Relatedfeatures  # imported but unused
from ODM2CZOData.models import Measurementresults
from ODM2CZOData.models import Measurementresultvalues
# from ODM2CZOData.models import CvAnnotationtype  # imported but unused
# from ODM2CZOData.models import People  # imported but unused
# from django.db.models import Avg, Max, Min  # imported but unused
# from django.db.models import F  # imported but unused
# from ODM2CZOData.models import Measurementresultvalueannotations  # imported# but unused  # noqa
# from ODM2CZOData.models import Annotations  # imported but unused
from datetime.datetime import strptime
import warnings
# import time  # imported but unused
# from django.db import transaction  # imported but unused
from modelHelpers import QAProcessLevelCreation
# range 0 to 26.7
# measurementresutlannotations; annotations

timeRangesToRemove = list()
# timeRangesToRemove.append([strptime('2015-04-24 15:15', '%Y-%m-%d %H:%M'),
#                            strptime('2015-05-18  11:15', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-03-17 12:00', '%Y-%m-%d %H:%M'),
                           strptime('2014-03-28  19:00', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-03-29 21:30', '%Y-%m-%d %H:%M'),
                           strptime('2014-04-03  10:00', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-06-16 20:00', '%Y-%m-%d %H:%M'),
                           strptime('2014-06-19  3:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-06-19 20:45', '%Y-%m-%d %H:%M'),
                           strptime('2014-06-20  11:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-06-21 15:30', '%Y-%m-%d %H:%M'),
                           strptime('2014-06-30  18:30', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-07-01 4:00', '%Y-%m-%d %H:%M'),
                           strptime('2014-07-05  17:45', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2014-07-26 15:00', '%Y-%m-%d %H:%M'),
                           strptime('2014-08-01  1:15', '%Y-%m-%d %H:%M')])
timeRangesToRemove.append([strptime('2015-04-24 15:00', '%Y-%m-%d %H:%M'),
                           strptime('2015-05-08  11:15', '%Y-%m-%d %H:%M')])

warnings.filterwarnings('ignore')
# variableid = 3 water temp
# variableid = 2 conductivity
# unitsid =1 microsimens per centimeter
# unitsid=3 celsius
# Sonadora Conductivity - featureaction 1 = http://lczodata.com/ODM2/ODM2CZOData/ODM2CZOData/featureactions/1/  # noqa
mrvsSonadoraTemp = Measurementresultvalues.objects.filter(
    resultid__resultid__variableid=3) \
    .filter(resultid__resultid__unitsid=3) \
    .filter(resultid__resultid__featureactionid__samplingfeatureid=3) \
    .filter(resultid__resultid__featureactionid=1) \
    .filter(valuedatetime__gte='2014-01-01') \
    .filter(valuedatetime__lte='2015-12-30').order_by('valuedatetime')

# print(newmr)

printvals = True
save = False
annotationtextHigh = ("Value above 43 degrees C, this is considered out of "
                      "range for stream water temperature, Original value was")
annotationtextLow = ("Value below 0 C, this is considered out of range for "
                     "stream water temperature, Original value was")
annotationtextDateRange = ("Values are out of range during this time period "
                           "water level was low and probe was out of the "
                           "water, Original value was ")

plevel = Processinglevels.objects.filter(processinglevelid=2).get()
# result=Measurementresults.objects.filter(resultid=16153).get()
# QAProcessLevelCreation(mrvsSonadoraTemp, result, timeRangesToRemove,
#                        printvals, save, 43, 0, annotationtextHigh,
#                        annotationtextLow, annotationtextDateRange)

mrvsSonadoraCond = Measurementresultvalues.objects.filter(
    resultid__resultid__variableid=2) \
    .filter(resultid__resultid__unitsid=1) \
    .filter(resultid__resultid__featureactionid__samplingfeatureid=3) \
    .filter(resultid__resultid__featureactionid=1) \
    .filter(valuedatetime__gte='2014-01-01') \
    .filter(valuedatetime__lte='2016-03-23').order_by('valuedatetime')
# result=Measurementresults.objects.filter(resultid=16153).get()

annotationtextHigh = ("Value above 1000 uS/cm, this is considered out of "
                      "range for stream conductivity, Original value was ")
annotationtextLow = ("Value below 15 uS/cm, this is considered out of range "
                     "for stream conductivity, Original value was")
annotationtextDateRange = ("Values are out of range during this time period "
                           "water level was low and probe was out of the "
                           "water, Original value was")


# newmr = newMeasurementResult(mrvsSonadoraCond, plevel, printvals, save)  # got  # 16156  # noqa
newmr = Measurementresults.objects.filter(resultid=16156).get()
printvals = False
save = False
QAProcessLevelCreation(mrvsSonadoraCond, newmr, timeRangesToRemove, printvals,
                       save, 1000, 15, annotationtextHigh, annotationtextLow,
                       annotationtextDateRange)
