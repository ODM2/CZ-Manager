from __future__ import unicode_literals

import argparse
import csv
import io
import itertools
import os
import re
import time
import xlrd
#import utils

#from contextlib import closing
#import csv
#from cStringIO import StringIO

from django.db import connection

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.management import settings
from django.core.mail import EmailMessage

from django.db import IntegrityError
from django.db import transaction
from django.db.models import Min, Max
from datetime import datetime

from odm2admin.models import CvCensorcode
from odm2admin.models import CvQualitycode
from odm2admin.models import Dataloggerfilecolumns
from odm2admin.models import Dataloggerfiles
from odm2admin.models import Extensionproperties
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Timeseriesresults
from odm2admin.models import Timeseriesresultvalues
from odm2admin.models import Dataquality
from odm2admin.models import Resultsdataquality
from odm2admin.models import People
from odm2admin.models import CvDataqualitytype
from odm2admin.models import CvAnnotationtype
from odm2admin.models import Annotations
from odm2admin.models import Timeseriesresultvalueannotations
from odm2admin.models import ProcessDataloggerfile
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

# 18699

def getEndDate(results):
    #EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    #enddate = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
    #    propertyid=EndDateProperty).get()
    enddate = None
    try:
        enddate = Timeseriesresultvalues.objects.filter(resultid=results.resultid.resultid).annotate(
            Max('valuedatetime')). \
            order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    except IndexError:
        return None
    return enddate


def updateStartDateEndDate(results, startdate, enddate):
    StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
    EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    # result = results#.objects.get(resultid=results.resultid.resultid)
    try:
        # raise CommandError(" start date "str(startdate)))
        #
        repvstart= Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=StartDateProperty).get() #.update(propertyvalue=startdate)
        repvstart.propertyvalue=startdate
        repvstart.save()
        repvend = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=EndDateProperty).get() #.update(propertyvalue=enddate)
        repvend.propertyvalue = enddate
        repvend.save()

    except ObjectDoesNotExist:
        # raise CommandError("couldn't find extension property values " +str(repvstart) + "for " +
        # str(StartDateProperty + "for" + str(results))
        repvstart = Resultextensionpropertyvalues(resultid=results.resultid, propertyid=StartDateProperty,
                                                  propertyvalue=startdate)
        # print(repvstart.propertyvalue)
        repvstart.save()
        repvend = Resultextensionpropertyvalues(resultid=results.resultid, propertyid=EndDateProperty,
                                                propertyvalue=enddate)
        # print(repvend.propertyvalue)
        repvend.save()
        # return repvstart, repvend

class Command(BaseCommand):
    def handle(self, *args, **options):

        cs451depthfttsr = Timeseriesresults.objects.filter(resultid=18699).get()

        cs451derivedftlastdate = Timeseriesresultvalues.objects.filter(resultid=18699).aggregate(Max('valuedatetime'))

        print(cs451derivedftlastdate)
        if not cs451derivedftlastdate['valuedatetime__max'] == None:
            cs451depth = Timeseriesresultvalues.objects.filter(resultid=17278).filter(
                valuedatetime__gt=cs451derivedftlastdate['valuedatetime__max'])
        else:
            cs451depth = Timeseriesresultvalues.objects.filter(resultid=17278)
        for cmdepth in cs451depth:
            # delete adj stage height feet from after 5-26-2020 - 9:45
            #  rerun this code -
            # 1.238588 to 20.29754
            # from C:\Users\12672\Box\SonadoraDischarge
            # cmdepth = cmdepth - (19.058952)
            # old values sensor moved 5-26-2020
            # a = 2.51
            # b = 0.125
            # a = 1.2148
            # b = 0.290636
            # adjH =  a*(cmdepth.datavalue**b)
            H = cmdepth.datavalue
            # adjH = ((H / 30.48) +2.93011)/1.00858
            adjH = ((H / 30.48) +2.163838)/1.026083
            if isinstance(adjH, complex):
                adjH = float('nan')
            tsrv = Timeseriesresultvalues(resultid=cs451depthfttsr, datavalue=adjH,
                                          valuedatetime=cmdepth.valuedatetime,
                                          valuedatetimeutcoffset=cmdepth.valuedatetimeutcoffset,
                                          censorcodecv=cmdepth.censorcodecv,
                                          qualitycodecv=cmdepth.qualitycodecv,
                                          timeaggregationinterval=cmdepth.timeaggregationinterval,
                                          timeaggregationintervalunitsid=cmdepth.timeaggregationintervalunitsid)
            tsrv.save()

        startdate = Timeseriesresultvalues.objects.filter(resultid=cs451depthfttsr).annotate(
            Min('valuedatetime')). \
            order_by('valuedatetime')[0].valuedatetime.strftime(
            '%Y-%m-%d %H:%M:%S.%f')  # .annotate(Min('price')).order_by('price')[0]
        enddate = Timeseriesresultvalues.objects.filter(resultid=cs451depthfttsr).annotate(
            Max('valuedatetime')). \
            order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        updateStartDateEndDate(cs451depthfttsr, startdate, enddate)