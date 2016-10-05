from __future__ import unicode_literals

import argparse
import csv
import io
import itertools
import os
import time

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Min, Max

from ODM2CZOData.models import CvCensorcode
from ODM2CZOData.models import CvQualitycode
from ODM2CZOData.models import Dataloggerfilecolumns
from ODM2CZOData.models import Dataloggerfiles
from ODM2CZOData.models import Extensionproperties
from ODM2CZOData.models import Resultextensionpropertyvalues
from ODM2CZOData.models import Results
from ODM2CZOData.models import Timeseriesresults
from ODM2CZOData.models import Timeseriesresultvalues
from templatesAndSettings.settings import MEDIA_ROOT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

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


def updateStartDateEndDate(results, startdate, enddate):
    StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
    EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    # result = results#.objects.get(resultid=results.resultid.resultid)
    try:
        # raise CommandError(" start date "str(startdate)))
        #
        Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=StartDateProperty).update(propertyvalue=startdate)
        # repvstart = Resultextensionpropertyvalues.objects.filter(resultid=results.
        # resultid).filter(propertyid=StartDateProperty).get()
        # print(repvstart.propertyvalue)
        Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=EndDateProperty).update(propertyvalue=enddate)
        # repvend = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).
        # filter(propertyid=EndDateProperty).get()
        # repvend, new = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).
        # filter(propertyid=EndDateProperty).get()
        # print(repvend.propertyvalue)
    except ObjectDoesNotExist:
        # raise CommandError("couldn't find extension property values " +str(repvstart) + "for " +
        # str(StartDateProperty + "for" + str(results))
        repvstart = Resultextensionpropertyvalues(resultid=results, propertyid=StartDateProperty,
                                                  propertyvalue=startdate)
        # print(repvstart.propertyvalue)
        repvstart.save()
        repvend = Resultextensionpropertyvalues(resultid=results, propertyid=EndDateProperty,
                                                propertyvalue=enddate)
        # print(repvend.propertyvalue)
        repvend.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1)
        parser.add_argument('dataloggerfileid', nargs=1)
        parser.add_argument('databeginson', nargs=1, type=int)
        parser.add_argument('columnheaderson', nargs=1, type=int)
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)

    @transaction.atomic
    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        cmdline = bool(args[4])
        if cmdline:
            file = MEDIA_ROOT + args[0]  # f[0]
            fileid = args[1]  # fileid[0]
            fileid = Dataloggerfiles.objects.filter(dataloggerfilename=fileid).get()

        else:
            file = MEDIA_ROOT + args[0].name
            fileid = args[1]
        check_dates = bool(args[5])
        databeginson = int(args[2])  # int(databeginson[0])
        print(databeginson)
        columnheaderson = int(args[3])  # int(columnheaderson[0])
        rowColumnMap = list()
        try:
            with io.open(file, 'rt', encoding='ascii') as f:
                # reader = csv.reader(f)
                columnsinCSV = None
                reader, reader2 = itertools.tee(csv.reader(f))
                for i in range(0, databeginson):
                    columnsinCSV = len(next(reader2))
                dateTimeColumnNum = -1
                DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
                    dataloggerfileid=fileid.dataloggerfileid)
                i = 0
                numCols = DataloggerfilecolumnSet.count()
                if numCols == 0:
                    raise CommandError(
                        'This file has no dataloggerfilecolumns associated with it. ')
                if not numCols == columnsinCSV:
                    raise CommandError(
                        'The number of columns in the ' + str(
                            columnsinCSV) + ' csv file do not match the number of' +
                        ' dataloggerfilecolumns ' + str(
                            numCols) + ' associated with the dataloggerfile in the database. ')
                for row in reader:
                    # map the column objects to the column in the file assumes first row in
                    # file contains columnlabel.
                    if i == columnheaderson:

                        for dloggerfileColumns in DataloggerfilecolumnSet:
                            foundColumn = False
                            for j in range(numCols):
                                # raise ValidationError(" in file " + row[j] + "
                                # in obj column label "+dloggerfileColumns.columnlabel)
                                if row[j] == dloggerfileColumns.columnlabel:
                                    foundColumn = True
                                    dloggerfileColumns.columnnum = j
                                    rowColumnMap += [dloggerfileColumns]
                            if not foundColumn:
                                raise CommandError(
                                    u'Cannot find a column in the CSV matching the '
                                    u'dataloggerfilecolumn {0}'.format(
                                        str(dloggerfileColumns.columnlabel)))
                                # if you didn't find a matching name for this column
                                # amoung the dloggerfileColumns raise error

                    elif i >= databeginson:

                        # assume date is first column for the moment
                        try:
                            dateT = time.strptime(row[0], "%m/%d/%Y %H:%M")  # '1/1/2013 0:10
                            datestr = time.strftime("%Y-%m-%d %H:%M", dateT)
                        except ValueError:
                            try:
                                dateT = time.strptime(row[0], "%m/%d/%Y %H:%M:%S")  # '1/1/2013 0:10
                                datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                            except ValueError:
                                try:
                                    dateT = time.strptime(row[0],
                                                          "%Y-%m-%d %H:%M:%S")  # '1/1/2013 0:10
                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                                except ValueError:
                                    dateT = time.strptime(row[0],
                                                          "%Y-%m-%d %H:%M:%S.%f")  # '1/1/2013 0:10
                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)
                        # for each column in the data table
                        # raise ValidationError("".join(str(rowColumnMap)))
                        if check_dates:
                            mrs = Results.objects.filter(
                                resultid__in=DataloggerfilecolumnSet.values("resultid"))
                            mrvs = Timeseriesresultvalues.objects.filter(resultid__in=mrs)
                        for colnum in rowColumnMap:
                            # x[0] for x in my_tuples
                            # colnum[0] = column number, colnum[1] = dataloggerfilecolumn object
                            if not colnum.columnnum == 0:
                                # raise ValidationError("result: " + str(colnum.resultid) +
                                # " datavalue "+
                                # str(row[colnum.columnnum])+ " dateTime " + datestr)
                                # thisresultid = colnum.resultid #result.values('resultid')

                                Timeseriesresult = Timeseriesresults.objects.filter(
                                    resultid=colnum.resultid)
                                if Timeseriesresult.count() == 0:
                                    raise CommandError(
                                        'No Measurement results for column ' + colnum.columnlabel +
                                        ' Add measurement results for' +
                                        'each column. Both results and measurement ' +
                                        'results are needed.')
                                # only one measurement result is allowed per result
                                value = row[colnum.columnnum]
                                censorcode = CvCensorcode.objects.filter(name="Not censored").get()
                                qualitycode = CvQualitycode.objects.filter(name="Good").get()
                                for mresults in Timeseriesresult:
                                    try:
                                        if (value == ''):
                                            raise IntegrityError
                                        if check_dates:
                                            # this check is really slowing down
                                            # ingestion so I added a flag to turn it off
                                            try:
                                                mrv = mrvs.filter(valuedatetime=datestr).filter(
                                                    resultid=mresults.resultid).get()
                                            except ObjectDoesNotExist:
                                                Timeseriesresultvalues(
                                                    resultid=mresults,
                                                    datavalue=row[colnum.columnnum],
                                                    valuedatetime=datestr,
                                                    valuedatetimeutcoffset=4,
                                                    censorcodecv=censorcode,
                                                    qualitycodecv=qualitycode,
                                                    timeaggregationinterval=
                                                    mresults.intendedtimespacing,
                                                    timeaggregationintervalunitsid=
                                                    mresults.intendedtimespacingunitsid).save()
                                        else:
                                            Timeseriesresultvalues(
                                                resultid=mresults,
                                                datavalue=row[colnum.columnnum],
                                                valuedatetime=datestr,
                                                valuedatetimeutcoffset=4,
                                                censorcodecv=censorcode,
                                                qualitycodecv=qualitycode,
                                                timeaggregationinterval=
                                                mresults.intendedtimespacing,
                                                timeaggregationintervalunitsid=
                                                mresults.intendedtimespacingunitsid).save()
                                    except IntegrityError:
                                        pass
                                        # Timeseriesresultvalues.delete()
                                        # row[0] is this column object
                    i += 1
                    # Timeseriesresults.objects.raw("SELECT odm2.\
                    # "TimeseriesresultValsToResultsCountvalue\"()")

        except IndexError:
            raise ValidationError('encountered a problem with row ' + str(i) for i in row)

        for colnum in rowColumnMap:
            results = Timeseriesresults.objects.filter(resultid=colnum.resultid)
            for result in results:
                mrvs_count = len(Timeseriesresultvalues.objects.filter(resultid=result))
                if mrvs_count > 0:
                    startdate = Timeseriesresultvalues.objects.filter(resultid=result).annotate(
                        Min('valuedatetime')). \
                        order_by('valuedatetime')[0].valuedatetime.strftime(
                        '%Y-%m-%d %H:%M')  # .annotate(Min('price')).order_by('price')[0]
                    enddate = Timeseriesresultvalues.objects.filter(resultid=result).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
                    updateStartDateEndDate(result, startdate, enddate)
