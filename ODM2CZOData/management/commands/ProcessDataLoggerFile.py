from __future__ import unicode_literals
__author__ = 'leonmi'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "templatesAndSettings.settings")
# from django.db.models import Q  # imported but unused
from ODM2CZOData.models import (Dataloggerfiles, Dataloggerfilecolumns,
                                Results, Measurementresultvalues,
                                Measurementresults)

import argparse
from django.core.exceptions import ObjectDoesNotExist


from templatesAndSettings.settings import MEDIA_ROOT
from django.db import transaction
from django.db import IntegrityError
# from django.contrib.gis.db import models
import time

import csv
import io

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
import itertools
# from django.utils.translation import ugettext as _    # imported but unused
# Using atomic transaction should improve the speed of loading the data.


# process_datalogger_file(self.dataloggerfileid.dataloggerfilelink,self.dataloggerfileid, self.databeginson, self.columnheaderson)  # noqa


parser = argparse.ArgumentParser(description='process datalogger file.')
# entered_start_date,entered_end_date,emailAddress,profileResult,selectedMResultSeries

# args = parser.parse_args()
# process_datalogger_file(args.dataloggerfilelink,args.dataloggerfileid,args.databeginson,args.columnheaderson , True)  # noqa


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1)
        parser.add_argument('dataloggerfileid', nargs=1)
        parser.add_argument('databeginson', nargs=1, type=int)
        parser.add_argument('columnheaderson', nargs=1, type=int)
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)

    @transaction.atomic
    def handle(self, *args, **options):
        # (f, fileid, databeginson,columnheaderson, cmd):
        cmdline = bool(args[4])
        if cmdline:
            file = MEDIA_ROOT + args[0]  # f[0]
            fileid = args[1]  # fileid[0]
            fileid = Dataloggerfiles.objects.filter(dataloggerfilename=fileid).get()  # noqa
        else:
            file = MEDIA_ROOT + args[0].name
            fileid = args[1]
        check_dates = bool(args[5])
        databeginson = int(args[2])  # int(databeginson[0])
        print(databeginson)
        columnheaderson = int(args[3])  # int(columnheaderson[0])
        try:
            with io.open(file, 'rt', encoding='ascii') as f:
                # reader = csv.reader(f)
                columnsinCSV = None
                reader, reader2 = itertools.tee(csv.reader(f))
                for i in range(0, databeginson):
                    columnsinCSV = len(next(reader2))
                rowColumnMap = list()
                # FIXME: 'dateTimeColumnNum' is assigned to but never used.
                # dateTimeColumnNum = -1
                DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
                    dataloggerfileid=fileid.dataloggerfileid
                )
                i = 0
                numCols = DataloggerfilecolumnSet.count()
                if numCols == 0:
                    raise CommandError('This file has no dataloggerfilecolumns associated with it.')  # noqa
                if not numCols == columnsinCSV:
                    raise CommandError('The number of columns in the {} csv '
                                       'file do not match the number of '
                                       'dataloggerfilecolumns {} associated '
                                       'with the dataloggerfile in the database.'.format(columnsinCSV, numCols))  # noqa
                for row in reader:
                    # Map the column objects to the column in the file assumes
                    # first row in file contains columnlabel.
                    if i == columnheaderson:
                        for dloggerfileColumns in DataloggerfilecolumnSet:
                            foundColumn = False
                            for j in range(numCols):
                                # raise ValidationError(" in file " + row[j] + " in obj column label "+dloggerfileColumns.columnlabel)  # noqa
                                if row[j] == dloggerfileColumns.columnlabel:
                                    foundColumn = True
                                    dloggerfileColumns.columnnum = j
                                    rowColumnMap += [dloggerfileColumns]
                            if not foundColumn:
                                raise CommandError(
                                    'Cannot find a column in the CSV matching the dataloggerfilecolumn {}'.format(dloggerfileColumns.columnlabel)  # noqa
                                )
                            # If you didn't find a matching name for this
                            # column amoung the dloggerfileColumns raise error.

                    elif i >= databeginson:
                        # Assume date is first column for the moment.
                        # (1/1/2013 0:10)
                        try:
                            dateT = time.strptime(row[0], "%m/%d/%Y %H:%M")
                            datestr = time.strftime("%Y-%m-%d %H:%M", dateT)
                        except ValueError:
                            try:
                                dateT = time.strptime(row[0], "%m/%d/%Y %H:%M:%S")  # noqa
                                datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)  # noqa
                            except ValueError:
                                try:
                                    dateT = time.strptime(row[0], "%Y-%m-%d %H:%M:%S")  # noqa
                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)  # noqa
                                except ValueError:
                                    dateT = time.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")  # noqa
                                    datestr = time.strftime("%Y-%m-%d %H:%M:%S", dateT)  # noqa
                        # For each column in the data table.
                        # raise ValidationError("".join(str(rowColumnMap)))
                        if check_dates:
                            mrs = Results.objects.filter(resultid__in=DataloggerfilecolumnSet.values("resultid"))  # noqa
                            mrvs = Measurementresultvalues.objects.filter(resultid__in=mrs)  # noqa
                        for colnum in rowColumnMap:
                            # x[0] for x in my_tuples
                            # column[0] = column number, colnum[1] = dataloggerfilecolumn object  # noqa
                            if not colnum.columnnum == 0:
                                # raise ValidationError("result: " + str(colnum.resultid) + " datavalue "+  # noqa
                                #                       str(row[colnum.columnnum])+ " dateTime " + datestr)  # noqa
                                # thisresultid = colnum.resultid #result.values('resultid')  # noqa

                                measurementresult = Measurementresults.objects.filter(resultid=colnum.resultid)  # noqa
                                if measurementresult.count() == 0:
                                    raise CommandError(
                                        'No Measurement results for column {} '
                                        'Add measurement results for each column. '  # noqa
                                        'Both results and measurement results are needed.'.format(colnum.columnlabel)  # noqa
                                    )
                                # Only one measurement result
                                # is allowed per result.
                                value = row[colnum.columnnum]
                                for mresults in measurementresult:
                                    try:
                                        if(value == ''):
                                            raise IntegrityError
                                        # This check is really slowing down
                                        # ingestion this flag to turns it off.
                                        if check_dates:
                                            try:
                                                # FIXME: 'mrv' is assigned to but never used  # noqa
                                                mrv = mrvs.filter(valuedatetime=datestr).filter(resultid=mresults.resultid).get()  # noqa
                                            except ObjectDoesNotExist:
                                                Measurementresultvalues(resultid=mresults, datavalue=row[colnum.columnnum], valuedatetime=datestr, valuedatetimeutcoffset=4).save()  # noqa
                                        else:
                                            Measurementresultvalues(resultid=mresults, datavalue=row[colnum.columnnum], valuedatetime=datestr, valuedatetimeutcoffset=4).save()  # noqa
                                    except IntegrityError:
                                        pass
                                        # Measurementresultvalues.delete()
                                    # row[0] is this column object
                    i += 1
            Measurementresults.objects.raw("SELECT odm2.\"MeasurementResultValsToResultsCountvalue\"()")  # noqa

        except IndexError:
            raise ValidationError('encountered a problem with row '+row)
