from __future__ import unicode_literals

import argparse
import csv
import io
import itertools
import os
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
import datetime

from odm2admin.models import CvCensorcode
from odm2admin.models import CvQualitycode
from odm2admin.models import Dataloggerfilecolumns
from odm2admin.models import Dataloggerfiles
from odm2admin.models import Extensionproperties
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Timeseriesresults
from odm2admin.models import Timeseriesresultvalues
from odm2admin.models import Dataquality
from odm2admin.models import Results
from odm2admin.models import Resultsdataquality
from odm2admin.models import People
from odm2admin.models import CvDataqualitytype
from odm2admin.models import Processinglevels
from odm2admin.models import CvAnnotationtype
from odm2admin.models import Annotations
from odm2admin.models import Timeseriesresultvalueannotations
from odm2admin.models import ProcessDataloggerfile
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")
from django.core.mail import EmailMessage

parser = argparse.ArgumentParser(description='create L1 time series from L0 and copy over raw values.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('createorupdateL1', nargs=1, type=str)
        parser.add_argument('resultid', nargs=1, type=str)
        parser.add_argument('startdate', nargs=1, type=str)
        parser.add_argument('enddate', nargs=1, type=str)
        parser.add_argument('email', nargs=1, type=str)
    def handle(self, *args, **options):
        resultid = int(options['resultid'][0])
        email = str(options['email'][0])
        # response_data = {}
        createorupdateL1 = str(options['createorupdateL1'][0])
        startdate = str(options['startdate'][0])
        enddate = str(options['enddate'][0])
        startdate = datetime.datetime.strptime(str(startdate), '%Y-%m-%d %H:%M:%S')
        enddate = datetime.datetime.strptime(str(enddate), '%Y-%m-%d %H:%M:%S')
        pl1 = Processinglevels.objects.get(processinglevelid=2)
        pl0 = Processinglevels.objects.get(processinglevelid=1)
        valuesadded = 0
        tsresultTocopyBulk = []
        tsresultL1 =None
        # print('starting L1 create or update')
        # print(createorupdateL1)
        # print('result')
        # print(resultid)
        # print('email')
        # print(email)
        if createorupdateL1 == "create":
            #print('create')
            resultTocopy = Results.objects.get(resultid=resultid)
            tsresultTocopy = Timeseriesresults.objects.get(resultid=resultid)
            resultTocopy.resultid = None
            resultTocopy.processing_level = pl1
            resultTocopy.save()
            tsrvToCopy = Timeseriesresultvalues.objects.filter(resultid=tsresultTocopy)
            tsresultTocopy.resultid = resultTocopy
            tsresultTocopy.save()
            tsresultL1 = tsresultTocopy.resultid
            # tsrvToCopy.update(resultid=tsresultTocopy)
            for tsrv in tsrvToCopy:
                tsrv.resultid = tsresultTocopy
                try:
                    tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                    tsrv.valueid = None
                    tsrv.save()
                    tsrva.valueid = tsrv
                    # print(tsrv.valueid)
                    tsrva.save()
                except ObjectDoesNotExist:
                    tsrv.valueid = None
                    tsresultTocopyBulk.append(tsrv)
            newtsrv = Timeseriesresultvalues.objects.bulk_create(tsresultTocopyBulk)

        elif createorupdateL1 == "update":
            # print('update')
            tsresultL1 = Timeseriesresults.objects.get(resultid=resultid)
            resultL1 = Results.objects.get(resultid=resultid)
            # tsrvL1 = Timeseriesresultvalues.objects.filter(resultid=tsresultL1)
            tsrvAddToL1Bulk = []
            relatedL0result = Results.objects.filter(
                featureactionid = resultL1.featureactionid).filter(
                variableid = resultL1.variableid
            ).filter(unitsid = resultL1.unitsid).filter(
                processing_level=pl0)

            # newresult = relatedL0result.resultid
            relateL0tsresults = Timeseriesresults.objects.filter(resultid__in= relatedL0result)
            relateL0tsresult = None
            for L0result in relateL0tsresults:
                if L0result.intendedtimespacing == tsresultL1.intendedtimespacing and L0result.intendedtimespacingunitsid == tsresultL1.intendedtimespacingunitsid:
                    relateL0tsresult =L0result
            tsrvAddToL1 = None
            tsrvAddToL1 = Timeseriesresultvalues.objects.filter(resultid=relateL0tsresult
                                                           ).filter(valuedatetime__gt=startdate
                                                                    ).filter(valuedatetime__lt=enddate)
            # print(relateL0tsresult)
            # maxtsrvL1=Timeseriesresultvalues.objects.filter(resultid=relateL1tsresult).annotate(
            #        Max('valuedatetime')). \
            #        order_by('-valuedatetime')
            # print(relateL1tsresult)
            # for r in maxtsrvL1:
            #     print(r)
            # print('L1 result')
            # print(tsresultL1)
            # print(relateL0tsresult)
            novals = False
            print(relateL0tsresult)
            print(relateL0tsresult.resultid)
            print('vals to add')
            print(len(tsrvAddToL1))

            # print('max L0')
            # print(maxtsrvL0)
            # print('max L1')
            # print(maxtsrvL1)
            for tsrv in tsrvAddToL1:
                tsrv.resultid = tsresultL1
                try:
                    tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                    tsrv.valueid = None
                    tsrv.save()
                    tsrva.valueid = tsrv
                    # print(tsrv.valueid)
                    tsrva.save()
                except ObjectDoesNotExist:
                    # print('doesnt exist')
                    tsrv.valueid = None
                    tsresultTocopyBulk.append(tsrv)
            newtsrv = Timeseriesresultvalues.objects.bulk_create(tsresultTocopyBulk)
        valuesadded = newtsrv.__len__()
        # print('values added')
        # print(valuesadded)
        # for tsrv in newtsrv:
        #     print(tsrv.resultid.resultid)
        #     print(tsrv)
        emailtitle = "L1 complete"
        tolist = []
        emailtext = ' L1 result complete for new or updated result: ' + str(tsresultL1) + '\n' + ' values added to time series: ' + str(valuesadded)
        for admin in settings.ADMINS:
            tolist.append(admin['email'])
        tolist.append(email)
        # print(tolist)
        if len(email) > 0:
            email = EmailMessage(emailtitle, emailtext, settings.EMAIL_FROM_ADDRESS, tolist)
            # print('email')
            # print(emailtext)
            emailout = email.send()
        # print(str(emailout))
        # print('emailed?')
        # response_data['newresultid'] = newresult
        # print(result)
    # return HttpResponse(json.dumps(response_data),content_type='application/json')
