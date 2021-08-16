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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('startdate', nargs=1, type=str)
        parser.add_argument('enddate', nargs=1, type=str)
        parser.add_argument('cmdline', nargs=1, type=str, help='when specifying execution from the' +
                                                               ' file locking does not occur allowing for repeated execution' +
                                                               ' in a cron job or other automation')
        parser.add_argument('reversed', nargs=1, type=str, default=False)
        parser.add_argument('check_dates', nargs=1, type=str)
        parser.add_argument('emailaddress', nargs='?', type=str, default='')

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        file = str(settings.MEDIA_ROOT) + filename  # args[0].name
        fileid = int(options['dataloggerfileid'][0])
        print(str(options['startdate'][0]))
        print(str(options['enddate'][0]))
        nodates = False
        try:
            startdate = datetime.strptime(str(options['startdate'][0]),'%Y-%m-%d %H:%M:%S.%f')
            enddate = datetime.strptime(str(options['enddate'][0]),'%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            print('no dates')
            print(str(options['startdate'][0]))
            print(str(options['enddate'][0]))
            nodates = True
        try:
            print('email address')
            emailaddress = str(options['emailaddress'])
            print(emailaddress)
        except IndexError:
            emailaddress = ''
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        check_dates = False
        reversed = False
        cmdline = False
        if options['check_dates'][0] == 'True':
            check_dates = True
        if options['cmdline'][0] == 'True':
            cmdline = True
        stop_reading_reversed = False
        rowColumnMap = list()
        bulktimeseriesvalues = []
        bulkcount = 0
        valuesadded =0
        upper_bound_quality_type = CvDataqualitytype.objects.get(name='Physical limit upper bound')
        lower_bound_quality_type = CvDataqualitytype.objects.get(name='Physical limit lower bound')
        result_lower_bound = None
        result_upper_bound = None
        emailtitle = "CZ Manager Alarm"
        tolist = []
        sendemail = True
        exceldatetime = False
        emailtext = ""
        dateTimeColNum = 0
        alarmcount = 0
        alarms = ""
        pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=fileid)
        DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
            dataloggerfileid=fileid)
        i = 0
        numCols = 0
        numDLCols = DataloggerfilecolumnSet.count()
        resultsToCheck = []
        dataqualitybool = False
        qualitycodegood = CvQualitycode.objects.filter(name="Good").get()
        qualitycodebad = CvQualitycode.objects.filter(name="Bad").get()
        result_upper_bound = None
        result_lower_bound = None
        for dloggerfileColumns in DataloggerfilecolumnSet:
            result= dloggerfileColumns.resultid
            dataqualitybool = True
            dataqualityUpperAlarm = True
            dataqualityLowerAlarm = True
            # don't do this if this is the datetime column

            Timeseriesresult = Timeseriesresults.objects.filter(
                resultid=result)
            annotationtypecv = CvAnnotationtype.objects.filter(
                name="Time series result value annotation").get()
            annotationdatetime = datetime.now()
            annotatorid = People.objects.filter(personid=1).get()
            # try to get data quality upper and lower bounds if they don't exist
            # proceed without checking.
            dataquality = None
            try:
                resultsdataquality = Resultsdataquality.objects.filter(resultid=result)
                dataquality = Dataquality.objects.filter(
                    dataqualityid__in=resultsdataquality.values('dataqualityid'))
                #assumption only one upper bound and one lower bound per result
                result_upper_bound = dataquality.get(
                    dataqualitytypecv=upper_bound_quality_type, dataqualitycode__icontains='bound')
                result_lower_bound = dataquality.get(
                    dataqualitytypecv=lower_bound_quality_type, dataqualitycode__icontains='bound')
            except ObjectDoesNotExist:
                dataqualitybool = False

            try:
                resultsdataquality = Resultsdataquality.objects.filter(resultid=result)
                dataquality = Dataquality.objects.filter(
                    dataqualityid__in=resultsdataquality.values('dataqualityid'))
                result_upper_bound_alarm = dataquality.get(
                    dataqualitytypecv=upper_bound_quality_type,
                    dataqualitycode__icontains='alarm')
            except ObjectDoesNotExist:
                dataqualityUpperAlarm = False
            try:
                resultsdataquality = Resultsdataquality.objects.filter(resultid=result)
                dataquality = Dataquality.objects.filter(
                    dataqualityid__in=resultsdataquality.values('dataqualityid'))
                result_lower_bound_alarm = dataquality.get(
                    dataqualitytypecv=lower_bound_quality_type,
                    dataqualitycode__icontains='alarm')
            except ObjectDoesNotExist:
                dataqualityLowerAlarm = False
            tsr = Timeseriesresults.objects.get(resultid=result)
            tsrvs = None
            if not nodates:
                tsrvs = Timeseriesresultvalues.objects.filter(resultid=tsr).filter(valuedatetime__gte=startdate).\
                        filter(valuedatetime__lte=enddate)
            else:
                tsrvs = Timeseriesresultvalues.objects.filter(resultid=tsr)
            if dataqualitybool:
                for tsrv in tsrvs:
                    newdatavalue = tsrv.datavalue
                    datestr = str(tsrv.valuedatetime)
                    if newdatavalue > result_upper_bound.dataqualityvalue:
                        alarmcount += 1
                        with transaction.atomic():
                            annotationtext = result_upper_bound.dataqualitycode + \
                                             " of " + str(result_upper_bound.dataqualityvalue) \
                                             + " exceeded, raw value was " + str(newdatavalue)
                            annotation = Annotations(annotationtypecv=annotationtypecv,
                                                     annotationcode="Value out of Range: High",
                                                     annotationtext=annotationtext,
                                                     annotationdatetime=annotationdatetime,
                                                     annotationutcoffset=4,
                                                     annotatorid=annotatorid)
                            alarms += ' ' + annotationtext
                            newdatavalue = float('NaN')
                            qualitycode = qualitycodebad
                            annotation.save()
                            valuesadded +=1
                            tsrv.datavale = newdatavalue
                            tsrv.qualitycodecv=qualitycode
                            tsrv.save()
                            tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                     annotationid=annotation).save()

                    elif newdatavalue < result_lower_bound.dataqualityvalue:
                        alarmcount += 1
                        with transaction.atomic():
                            annotationtext = "value below " + \
                                             result_lower_bound.dataqualitycode + \
                                             " of " + str(result_lower_bound.dataqualityvalue) \
                                             + ", raw value was " + str(newdatavalue)
                            annotation = Annotations(annotationtypecv=annotationtypecv,
                                                     annotationcode="Value out of Range: Low",
                                                     annotationtext=annotationtext,
                                                     annotationdatetime=annotationdatetime,
                                                     annotationutcoffset=4,
                                                     annotatorid=annotatorid)
                            alarms += ' ' + annotationtext
                            newdatavalue = float('NaN')
                            qualitycode = qualitycodebad
                            annotation.save()
                            valuesadded += 1
                            tsrv.datavale = newdatavalue
                            tsrv.qualitycodecv=qualitycode
                            tsrv.save()
                            tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                     annotationid=annotation).save()
                    else:
                        dataqualitybool = False
                    # newdatavalue = float(row[colnum.columnnum])
                    if dataqualityUpperAlarm:
                        if newdatavalue > result_upper_bound_alarm.dataqualityvalue:
                            alarmcount += 1
                            with transaction.atomic():
                                annotationtext = result_upper_bound_alarm.dataqualitycode + \
                                                 " of " + str(
                                    result_upper_bound_alarm.dataqualityvalue) \
                                                 + " exceeded, raw value was " + str(newdatavalue)
                                annotation = Annotations(annotationtypecv=annotationtypecv,
                                                         annotationcode="Alarm level exceeded ",
                                                         annotationtext=annotationtext,
                                                         annotationdatetime=annotationdatetime,
                                                         annotationutcoffset=4,
                                                         annotatorid=annotatorid)
                                alarms += ' ' + annotationtext
                                #qualitycode = qualitycodebad
                                # already created time series result values in
                                # result upper bound check

                                # print(dataqualitybool)
                                boundexceeded = False
                                if result_upper_bound:
                                    if newdatavalue > result_upper_bound.dataqualityvalue:
                                        annotation.save()
                                        boundexceeded = True
                                elif not boundexceeded: # already created time series result values in
                                    # result upper bound check
                                    annotation.save()
                                    valuesadded += 1
                                    tsvrbulk = False
                                tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                         annotationid=annotation).save()
                                emailtext += "Alarm value of " + \
                                             str(result_upper_bound_alarm.dataqualityvalue) \
                                             + "  exceeded for " + str(result
                                                                       ) + "\n " + "data value " + str(newdatavalue) + " on " \
                                             + datestr + "\n "
                        else:
                            dataqualityUpperAlarm = False
                        if dataqualityLowerAlarm:
                            alarmcount += 1
                            if newdatavalue < result_lower_bound_alarm.dataqualityvalue:
                                with transaction.atomic():
                                    sendemail = True
                                    annotationtext = "value below "
                                    annotationtext += str(result_lower_bound_alarm.dataqualitycode) + \
                                                      " of " + str(
                                        result_lower_bound_alarm.dataqualityvalue) \
                                                      + ", raw value was " + str(newdatavalue)
                                    annotation = Annotations(annotationtypecv=annotationtypecv,
                                                             annotationcode="Data value fell below Alarm level",
                                                             annotationtext=annotationtext,
                                                             annotationdatetime=annotationdatetime,
                                                             annotationutcoffset=4,
                                                             annotatorid=annotatorid)
                                    alarms += ' ' + annotationtext
                                    #qualitycode = qualitycodebad
                                    boundexceeded = False
                                    if result_lower_bound:
                                        if newdatavalue < result_lower_bound.dataqualityvalue:
                                            annotation.save()
                                            boundexceeded = True
                                    elif not boundexceeded:
                                        annotation.save()
                                        valuesadded += 1
                                    tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                             annotationid=annotation).save()
                                    emailtext += "Alarm value fell below threshold of " \
                                                 + str(result_lower_bound_alarm.dataqualityvalue) + \
                                                 " for time series " + str(result
                                                                           ) + "\n " + "data value " + str(newdatavalue) + " on " \
                                                 + datestr + "\n "
                            else:
                                dataqualityLowerAlarm = False
        if sendemail:
            email = EmailMessage(emailtitle, emailtext, settings.EMAIL_FROM_ADDRESS, tolist)
            # print('email')
            # print(emailtext)
            email.send()
        emailtitle = 'CZ Manager - file processing complete for: ' + str(pdlf)
        emailtext = 'CZ Manager - file processing complete for: ' + str(pdlf) + ' \n'
        emailtext += 'Alarms: ' + str(alarmcount) + ' \n'
        if alarmcount > 0:
            emailtext += alarms + ' \n'
        emailtext += 'total time series result values add: ' + str(valuesadded) + ' \n'
        emailtext += 'These time series were updated: \n'
        tolist.append(emailaddress)
        for colnum in rowColumnMap:
            results = Timeseriesresults.objects.filter(resultid=colnum.resultid)
            for result in results:
                emailtext += str(result)
        email2 = EmailMessage(emailtitle, emailtext, settings.EMAIL_FROM_ADDRESS, tolist)
        email2.send()
        pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=fileid)
        print(pdlf.processingCode)
        print('unlock')
        pdlf.processingCode = '0'
        pdlf.save()
        print(emailtitle)
        print(emailtext)
