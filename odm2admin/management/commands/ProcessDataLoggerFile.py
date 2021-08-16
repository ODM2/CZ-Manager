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
# TRY THIS
# http://stefano.dissegna.me/django-pg-bulk-insert.html

__author__ = 'leonmi'
# using atomic transaction should improve the speed of loading the data.


# process_datalogger_file(self.dataloggerfileid.dataloggerfilelink,self.dataloggerfileid,
# self.databeginson,
# self.columnheaderson)


parser = argparse.ArgumentParser(description='process datalogger file.')


# entered_start_date,entered_end_date,emailAddress,profileResult,selectedMResultSeries

# args = parser.parse_args()
# process_datalogger_file(args.dataloggerfilelink,args
# .dataloggerfileid,args.databeginson,args.columnheaderson , True)

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
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)
        parser.add_argument('check_dates', nargs=1, type=str)
        parser.add_argument('cmdline', nargs=1, type=str, help='when specifying execution from the' +
                                               ' file locking does not occur allowing for repeated execution' +
                                                ' in a cron job or other automation')
        parser.add_argument('reversed', nargs=1, type=str, default=False)
        parser.add_argument('emailaddress', nargs='?', type=str, default='')

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        file = str(settings.MEDIA_ROOT) + filename  # args[0].name
        fileid = int(options['dataloggerfileid'][0])
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
        if options['reversed'][0] == 'True':
            reversed = True
        if options['cmdline'][0] == 'True':
            cmdline = True
        stop_reading_reversed = False
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
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
        sendemail = False
        exceldatetime = False
        emailtext = ""
        dateTimeColNum = 0
        alarmcount = 0
        alarms = ""
        pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=fileid)
        if not pdlf.processingCode == 'done' and not pdlf.processingCode=='locked':
            if not cmdline:
                pdlf.processingCode = 'locked'
                pdlf.save()
            print(pdlf)
            print(pdlf.processingCode)
            for admin in settings.ADMINS:
                tolist.append(admin['email'])
            try:
                with io.open(file, 'rt', encoding='ascii') as f:
                    print('begin processing ' + str(pdlf))
                    # reader = csv.reader(f)
                    columnsinCSV = None
                    reader, reader2 = itertools.tee(csv.reader(f))
                    for i in range(0, databeginson):
                        columnsinCSV = len(next(reader2))
                    DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
                        dataloggerfileid=fileid)
                    i = 0
                    numCols = 0
                    numDLCols = DataloggerfilecolumnSet.count()

                    if numDLCols == 0:
                        raise CommandError(
                            'This file has no dataloggerfilecolumns associated with it. ')
                    # if not numDLCols == columnsinCSV:
                    #    raise CommandError(
                    #        'The number of columns in the ' + str(
                    #            columnsinCSV) + ' csv file do not match the number of' +
                    #        ' dataloggerfilecolumns ' + str(
                    #            numDLCols) + ' associated with the dataloggerfile in the database. ')
                    for row in reader:
                        numCols = len(row)
                        # print(row)
                        # map the column objects to the column in the file assumes first row in
                        # file contains columnlabel.
                        if i == columnheaderson:

                            for dloggerfileColumns in DataloggerfilecolumnSet:
                                foundColumn = False
                                for j in range(numCols):
                                    # raise ValidationError(" in file " + row[j] + "
                                    # in obj column label "+dloggerfileColumns.columnlabel)
                                    if row[j].strip() == dloggerfileColumns.columnlabel \
                                            and dloggerfileColumns.columndescription !="skip":
                                        foundColumn = True
                                        dloggerfileColumns.columnnum = j
                                        rowColumnMap += [dloggerfileColumns]
                                    if dloggerfileColumns.columndescription =="skip":
                                        foundColumn = True
                                    if row[j].strip() == dloggerfileColumns.columnlabel \
                                            and dloggerfileColumns.columndescription == "datetime":
                                        dateTimeColNum = j
                                    if row[j].strip() == dloggerfileColumns.columnlabel \
                                            and dloggerfileColumns.columndescription == 'exceldatetime':
                                        dateTimeColNum = j
                                        exceldatetime = True
                                if not foundColumn:
                                    raise CommandError(
                                        u'Cannot find a column in the CSV matching the '
                                        u'dataloggerfilecolumn {0}'.format(
                                            str(dloggerfileColumns.columnlabel)))
                                    # if you didn't find a matching name for this column
                                    # amoung the dloggerfileColumns raise error

                        elif i >= databeginson:
                            rawdt = row[dateTimeColNum].strip()
                            # assume date is first column for the moment
                            dateT = None
                            datestr = ''
                            try:
                                dateT = time.strptime(rawdt, "%m/%d/%Y %H:%M")  # '1/1/2013 0:10
                                datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                            except ValueError:
                                try:
                                    dateT = time.strptime(rawdt, "%m/%d/%Y %H:%M:%S")  # '1/1/2013 0:10
                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                except ValueError:
                                    try:
                                        dateT = time.strptime(rawdt,
                                                              "%Y-%m-%d %H:%M:%S")  # '1/1/2013 0:10
                                        datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                    except ValueError:
                                        try:
                                            dateT = time.strptime(rawdt,
                                                                  "%Y-%m-%d %H:%M:%S.%f")  # '1/1/2013 0:10
                                            datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                        except ValueError:
                                            try:
                                                dateT = time.strptime(rawdt,
                                                                      "%Y/%m/%d %H:%M")  # '1/1/2013 0:10
                                                datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                            except ValueError:
                                                try:
                                                    dateT = time.strptime(rawdt,
                                                                          "Y-%m-%d %H:%M %p")  # '1/1/2013 0:10
                                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                                except ValueError:
                                                    try:
                                                        if exceldatetime:
                                                                # deal with excel formatted datetimes
                                                                tmpdate = float(row[dateTimeColNum])
                                                                dateTuple = xlrd.xldate_as_tuple(tmpdate, 0)
                                                                dt_obj = datetime(*dateTuple[0:6])
                                                                dateT = dt_obj.strptime(row[dateTimeColNum],
                                                                                  "%Y-%m-%d %H:%M:%S.%f")
                                                                datestr= dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                                                    except ValueError:
                                                        continue
                            #if you encounter a blank line continue and try the next one
                            except IndexError:
                                continue
                            # for each column in the data table
                            # raise ValidationError("".join(str(rowColumnMap)))
                            # if check_dates:
                            # mrs = Results.objects.filter(
                            #         resultid__in=DataloggerfilecolumnSet.values("resultid"))
                            #     mrvs = Timeseriesresultvalues.objects.filter(resultid__in=mrs)
                            for dlfc in rowColumnMap:
                                if len(row) < dlfc.columnnum:
                                    print('bad row ' +str(row))
                                    continue

                            for colnum in rowColumnMap:
                                if stop_reading_reversed:
                                    break
                                dataqualitybool = True
                                dataqualityUpperAlarm = True
                                dataqualityLowerAlarm = True
                                # don't do this if this is the datetime column
                                if not colnum.columnnum == dateTimeColNum:
                                    # raise ValidationError("result: " + str(colnum.resultid) +
                                    # " datavalue "+
                                    # str(row[colnum.columnnum])+ " dateTime " + datestr)
                                    # thisresultid = colnum.resultid #result.values('resultid')

                                    Timeseriesresult = Timeseriesresults.objects.filter(
                                        resultid=colnum.resultid)
                                    annotationtypecv = CvAnnotationtype.objects.filter(
                                        name="Time series result value annotation").get()
                                    annotationdatetime = datetime.now()
                                    annotatorid = People.objects.filter(personid=1).get()
                                    # try to get data quality upper and lower bounds if they don't exist
                                    # proceed without checking.
                                    try:
                                        resultsdataquality = Resultsdataquality.objects.filter(resultid=colnum.resultid)
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
                                        result_upper_bound_alarm = dataquality.get(
                                            dataqualitytypecv=upper_bound_quality_type,
                                            dataqualitycode__icontains='alarm')
                                    except ObjectDoesNotExist:
                                        dataqualityUpperAlarm = False
                                    try:
                                        result_lower_bound_alarm = dataquality.get(
                                            dataqualitytypecv=lower_bound_quality_type,
                                            dataqualitycode__icontains='alarm')
                                    except ObjectDoesNotExist:
                                        dataqualityLowerAlarm = False
                                    if Timeseriesresult.count() == 0:
                                        raise CommandError(
                                            'No time series results for column ' + colnum.columnlabel +
                                            ' Add time series results for' +
                                            'each column. Both results and time series ' +
                                            'results are needed.')
                                    # only one measurement result is allowed per result
                                    # print('error')
                                    # print(str(row))
                                    # print(str(colnum.columnlabel))
                                    # print(str(colnum.columnnum))
                                    try:
                                        value = row[colnum.columnnum]
                                    except IndexError:
                                        continue
                                    if value == '':
                                        # print("error")
                                        # skip blank value
                                        continue

                                    # print("value to save")
                                    # print(value)
                                    censorcode = CvCensorcode.objects.filter(name="Not censored").get()
                                    qualitycodegood = CvQualitycode.objects.filter(name="Good").get()
                                    qualitycodebad = CvQualitycode.objects.filter(name='Bad').get()
                                    qualitycode = None



                                    for mresults in Timeseriesresult:
                                        tsvr = None
                                        tsvrbulk = True
                                        # print(mresults)
                                        try:

                                            if check_dates:
                                                try:
                                                    enddatestr = getEndDate(mresults)
                                                    if len(enddatestr) == 16:
                                                        enddate = time.strptime(enddatestr, '%Y-%m-%d %H:%M')
                                                    elif len(enddatestr) == 19:
                                                        enddate = time.strptime(enddatestr, '%Y-%m-%d %H:%M:%S')
                                                    else:
                                                        enddate = time.strptime(enddatestr, '%Y-%m-%d %H:%M:%S.%f')
                                                    if enddate >= dateT:  #.valuedatetime.strftime('%Y-%m-%d %H:%M')
                                                        if reversed:
                                                            stop_reading_reversed = True
                                                        break
                                                except (ObjectDoesNotExist, TypeError) as e:
                                                    pass
                                            try:
                                                newdatavalue = float(row[colnum.columnnum])
                                            except ValueError:
                                                if row[colnum.columnnum].strip() == "":
                                                    newdatavalue = float('NaN')
                                                else:
                                                    continue
                                            if datestr == '':
                                                print('bad date on row: ' +str(row))
                                                raise IntegrityError
                                            qualitycode = qualitycodegood
                                            # print(newdatavalue)
                                            if dataqualitybool:
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
                                                        tsvr = Timeseriesresultvalues(
                                                            resultid=mresults,
                                                            datavalue=newdatavalue,
                                                            valuedatetime=datestr,
                                                            valuedatetimeutcoffset=4,
                                                            censorcodecv=censorcode,
                                                            qualitycodecv=qualitycode,
                                                            timeaggregationinterval=mresults
                                                            .intendedtimespacing,
                                                            timeaggregationintervalunitsid=mresults
                                                            .intendedtimespacingunitsid
                                                        )
                                                        annotation.save()
                                                        tsvr.save()
                                                        valuesadded +=1
                                                        tsvrbulk = False
                                                        tsrva = Timeseriesresultvalueannotations(valueid=tsvr,
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
                                                        tsvr = Timeseriesresultvalues(
                                                            resultid=mresults,
                                                            datavalue=newdatavalue,
                                                            valuedatetime=datestr,
                                                            valuedatetimeutcoffset=4,
                                                            censorcodecv=censorcode,
                                                            qualitycodecv=qualitycode,
                                                            timeaggregationinterval=mresults
                                                            .intendedtimespacing,
                                                            timeaggregationintervalunitsid=mresults
                                                            .intendedtimespacingunitsid
                                                        )
                                                        annotation.save()
                                                        tsvr.save()
                                                        valuesadded += 1
                                                        tsvrbulk = False
                                                        tsrva = Timeseriesresultvalueannotations(valueid=tsvr,
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
                                                            tsvr = Timeseriesresultvalues(
                                                                resultid=mresults,
                                                                datavalue=newdatavalue,
                                                                valuedatetime=datestr,
                                                                valuedatetimeutcoffset=4,
                                                                censorcodecv=censorcode,
                                                                qualitycodecv=qualitycode,
                                                                timeaggregationinterval=mresults
                                                                .intendedtimespacing,
                                                                timeaggregationintervalunitsid=mresults
                                                                .intendedtimespacingunitsid
                                                            )
                                                            annotation.save()
                                                            tsvr.save()
                                                            valuesadded += 1
                                                            tsvrbulk = False
                                                        tsrva = Timeseriesresultvalueannotations(valueid=tsvr,
                                                                                                annotationid=annotation).save()
                                                        emailtext += "Alarm value of " + \
                                                                     str(result_upper_bound_alarm.dataqualityvalue) \
                                                                     + "  exceeded for " + str(mresults
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
                                                            tsvr = Timeseriesresultvalues(
                                                                resultid=mresults,
                                                                datavalue=newdatavalue,
                                                                valuedatetime=datestr,
                                                                valuedatetimeutcoffset=4,
                                                                censorcodecv=censorcode,
                                                                qualitycodecv=qualitycode,
                                                                timeaggregationinterval=mresults
                                                                .intendedtimespacing,
                                                                timeaggregationintervalunitsid=mresults
                                                                .intendedtimespacingunitsid
                                                            )
                                                            annotation.save()
                                                            tsvr.save()
                                                            valuesadded += 1
                                                            tsvrbulk = False
                                                        # print(tsvr)
                                                        tsrva = Timeseriesresultvalueannotations(valueid=tsvr,
                                                                                                 annotationid=annotation).save()
                                                        emailtext += "Alarm value fell below threshold of " \
                                                                     + str(result_lower_bound_alarm.dataqualityvalue) + \
                                                                     " for time series " + str(mresults
                                                        ) + "\n " + "data value " + str(newdatavalue) + " on " \
                                                                     + datestr + "\n "
                                                else:
                                                    dataqualityLowerAlarm = False

                                            # print(row[colnum.columnnum])
                                            # check if values are above or below quality bounds
                                            # create an annotation if they are.
                                            # print(dataqualitybool)
                                            # print(dataqualityUpperAlarm)
                                             #print(dataqualityLowerAlarm)
                                            if not dataqualitybool and not dataqualityUpperAlarm \
                                                    and not dataqualityLowerAlarm:
                                                tsvr = Timeseriesresultvalues(
                                                    resultid=mresults,
                                                    datavalue=newdatavalue,
                                                    valuedatetime=datestr,
                                                    valuedatetimeutcoffset=4,
                                                    censorcodecv=censorcode,
                                                    qualitycodecv=qualitycode,
                                                    timeaggregationinterval=mresults
                                                    .intendedtimespacing,
                                                    timeaggregationintervalunitsid=mresults
                                                    .intendedtimespacingunitsid
                                                )
                                                if tsvrbulk:
                                                    bulktimeseriesvalues.append(tsvr)
                                                    bulkcount +=1
                                                    valuesadded += 1
                                                if bulkcount > 20000:
                                                    Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)
                                                    del bulktimeseriesvalues[:]
                                                    tsvr = None
                                                    bulkcount = 0
                                                    # print("saved value - bulk create")
                                            if tsvr is None and not tsvrbulk:
                                                tsvr = Timeseriesresultvalues(
                                                    resultid=mresults,
                                                    datavalue=newdatavalue,
                                                    valuedatetime=datestr,
                                                    valuedatetimeutcoffset=4,
                                                    censorcodecv=censorcode,
                                                    qualitycodecv=qualitycode,
                                                    timeaggregationinterval=mresults
                                                    .intendedtimespacing,
                                                    timeaggregationintervalunitsid=mresults
                                                    .intendedtimespacingunitsid
                                                )
                                                tsvr.save()
                                                valuesadded += 1
                                        except IntegrityError:
                                            pass
                                            # Timeseriesresultvalues.delete()
                                            # row[0] is this column object

                        i += 1
                        if stop_reading_reversed:
                            break
                        # Timeseriesresults.objects.raw("SELECT odm2.\
                        # "TimeseriesresultValsToResultsCountvalue\"()")
                # print('last bulk create')
                Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)
                del bulktimeseriesvalues[:]

            except Exception as e:
                print('Error')
                print(row)
                print(e)
                pass
            bulkpropertyvals = []
            for colnum in rowColumnMap:
                results = Timeseriesresults.objects.filter(resultid=colnum.resultid)
                for result in results:
                    mrvsexist = Timeseriesresultvalues.objects.filter(resultid=result).exists()
                    if mrvsexist:
                        startdate = Timeseriesresultvalues.objects.filter(resultid=result).annotate(
                            Min('valuedatetime')). \
                            order_by('valuedatetime')[0].valuedatetime.strftime(
                            '%Y-%m-%d %H:%M:%S.%f')  # .annotate(Min('price')).order_by('price')[0]
                        enddate = Timeseriesresultvalues.objects.filter(resultid=result).annotate(
                            Max('valuedatetime')). \
                            order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
                        updateStartDateEndDate(result, startdate, enddate)  # repvstart, repvend =
                        # bulkpropertyvals.append(repvstart)
                        # bulkpropertyvals.append(repvend)
            # will bulk create or update the property values
            # Resultextensionpropertyvalues.objects.bulk_create(bulkpropertyvals)
            # print('email?')
            # pdlf.processingCode = 'done'
            # pdlf.save()
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
            # print('email sent')
