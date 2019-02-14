from __future__ import unicode_literals

import argparse
import os
import csv
import io
import itertools
import time
import xlrd
import numpy as np
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.management import settings
from django.utils.crypto import get_random_string

from odm2admin.models import ProcessDataloggerfile
from odm2admin.models import Dataloggerfiles
from odm2admin.models import Featureactions
from odm2admin.models import Samplingfeatures
from odm2admin.models import Methods
from odm2admin.models import Actions
from odm2admin.models import Results
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Dataloggerfilecolumns
from odm2admin.models import Timeseriesresultvalues

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

parser = argparse.ArgumentParser(description='validate dates in datalogger file.')


def get_results(fileid):
    dataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
        dataloggerfileid=fileid)
    surface_results_ = Results.objects.filter(resultid__in=dataloggerfilecolumnSet.values('resultid'))
    return surface_results_


# def check for existing data, check greater than start, less than end, and if size equal to all new data
def check_existing_data(sr_, startdate_, enddate_):
    for surface_result in sr_:
        resultid = surface_result.resultid

        time_series_values_ = Timeseriesresultvalues.objects.filter(valuedatetime__lte= enddate_).filter(
            valuedatetime__gte= startdate_).filter(resultid=surface_result.resultid)

        valuecounts_ = time_series_values_.count()

    return valuecounts_


def get_start_index(alldate, startdateODMstring_):
    # Check for Start date
    try:
        s = alldate.index(startdateODMstring_)
    except ValueError:
        searchval = datetime.strptime(startdateODMstring_, '%m/%d/%Y %H:%M')
        # ii = bisect.bisect_right(values, searchval)
        newstart = (
            min([datetime.strptime(x, '%m/%d/%Y %H:%M') for x in alldate], key=lambda x: abs(x - searchval))).strftime(
            "%-m/%-d/%Y %-H:%M")
        rs_ = alldate.index(newstart)
        print("Value does not exist, Found start closest to")
    else:
        print("Index of start value %s: %d" % (alldate[s], s))
        rs_ = s

    return rs_

def check_duplicate_dates(resultids_, checkdate_,alldata):
    Newdates_ = checkdate_
    # NewTr_ = allTr
    # NewTc_ = allTc
    # NewPr_ = allPr
    # NewPc_ = allPc

    i = 0
    for d in checkdate_:
        value_check = []

        for rid in resultids_:
            time_series_values =Timeseriesresultvalues.objects.filter(
                valuedatetime = d).filter(ResultID=rid)  # Need to get ResultID automatically still
            # ResultID=surface_result.ResultID)
            value_check.append(time_series_values.count())

        # if sum(value_check) == len(resultids_):
        # Newdates_[i] = np.nan
        for resultid, value in alldata.items():
            newdatetime = value[0]
            newvalue = value[1]
            if rid == resultid and newdatetime == d:
                value[1] = np.nan
                print('duplicate data on: ' + str(d) + ' for result: ' +str(rid))
        i += 1
    return Newdates_,alldata


def get_end_index(alldate,enddateODMstring_,):
    # check for end date
    try:
        e = alldate.index(enddateODMstring_)
    except ValueError:
        searchval = datetime.strptime(enddateODMstring_, '%m/%d/%Y %H:%M')
        # ii = bisect.bisect_right(values, searchval)
        newend = (
            min([datetime.strptime(x, '%m/%d/%Y %H:%M') for x in alldate], key=lambda x: abs(x - searchval))).strftime(
            "%-m/%-d/%Y %-H:%M")
        re_ = alldate.index(newend)
        print("Value does not exist, Found end closest to")
    else:
        re_ = e
        print("Index of end value %s: %d" % (alldate[e], e))

    return re_

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)


    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        file = str(settings.MEDIA_ROOT) + filename  # args[0].name
        random_string = get_random_string(length=5)
        new_file = str(settings.MEDIA_ROOT) + 'prerpocessed_' +random_string + '_'+  filename  # args[0].name
        fileid = int(options['dataloggerfileid'][0])
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
        alldate = []
        fields = ['datetime']
        try:
            with io.open(file, 'rt', encoding='ascii') as f:
                with io.open(new_file, 'w', encoding='ascii') as outfile:

                    # reader = csv.reader(f)
                    columnsinCSV = None
                    reader = itertools.tee(csv.reader(f))
                    print('beginning validation')
                    results = get_results(fileid)
                    DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
                        dataloggerfileid=fileid)
                    i = 0
                    numCols = 0
                    numDLCols = DataloggerfilecolumnSet.count()
                    startdateNEW = ''
                    enddateNEW = ''
                    alldata = {}
                    alldataanddates={}
                    results = []
                    for dlfc in DataloggerfilecolumnSet:
                        fields.append(dlfc.resultid)
                    w = csv.DictWriter(outfile, fieldnames=fields)
                    for row in reader:
                        if i == columnheaderson:

                            for dloggerfileColumn in DataloggerfilecolumnSet:
                                foundColumn = False
                                resultid = dloggerfileColumn.resultid
                                results.append(dloggerfileColumn)
                                startdateODM = Resultextensionpropertyvalues.objects.filter(
                                    resultid=resultid).filter(
                                    propertyid=1).get()  # DBSession.query(ResultExtensionPropertyValues).filter(
                                # ResultExtensionPropertyValues.ResultID == resultids[0]).filter(ResultExtensionPropertyValues.PropertyID == 1)
                                enddateODM = Resultextensionpropertyvalues.objects.filter(
                                    resultid=resultid).filter(propertyid=2).get()
                                sdopd = str(startdateODM.PropertyValue)
                                edopd = str(enddateODM.PropertyValue)

                                sdODMF = datetime.strptime(sdopd[:16], "%Y-%m-%d %H:%M")
                                edODMF = datetime.strptime(edopd[:16], "%Y-%m-%d %H:%M")
                                startdateODMstring = sdODMF.strftime("%-m/%-d/%Y %-H:%M")
                                enddateODMstring = edODMF.strftime("%-m/%-d/%Y %-H:%M")


                                for j in range(numCols):
                                    if row[j].strip() == dloggerfileColumn.columnlabel \
                                            and dloggerfileColumn.columndescription !="skip":
                                        foundColumn = True
                                        dloggerfileColumn.columnnum = j
                                        rowColumnMap += [dloggerfileColumn]
                                    if dloggerfileColumn.columndescription =="skip":
                                        foundColumn = True
                                    if row[j].strip() == dloggerfileColumn.columnlabel \
                                            and dloggerfileColumn.columndescription == "datetime":
                                        dateTimeColNum = j
                                    if row[j].strip() == dloggerfileColumn.columnlabel \
                                            and dloggerfileColumn.columndescription == 'exceldatetime':
                                        dateTimeColNum = j
                                        exceldatetime = True
                                if not foundColumn:
                                    raise CommandError(
                                        u'Cannot find a column in the CSV matching the '
                                        u'dataloggerfilecolumn {0}'.format(
                                            str(dloggerfileColumn.columnlabel)))

                        elif i >= databeginson:
                            rawdt = row[dateTimeColNum].strip()
                            # assume date is first column for the moment
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
                                                            datestr = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                                                    except ValueError:
                                                        continue
                            if startdateNEW == '':
                                startdateNEW = datestr
                            alldate.append(datestr)
                            for j in range(numCols):
                                curcol = -1
                                for col in DataloggerfilecolumnSet:
                                    if col.columnnum == j:
                                        curcol = col
                                if col.resultid in alldata:
                                    alldata[col.resultid].append(row[j])
                                    alldataanddates[col.resultid].append([dateT, row[j]])
                                else:
                                    alldata[col.resultid] = []
                                    alldata[col.resultid].append(row[j]) # [dateT, row[j]]
                                    alldataanddates[col.resultid] = []
                                    alldataanddates[col.resultid].append([dateT, row[j]])

                    enddateNEW = datestr
                    startdateNEWDT = datetime.strptime(startdateNEW, "%m/%d/%Y %H:%M")
                    enddateNEWDT = datetime.strptime(enddateNEW, "%m/%d/%Y %H:%M")
                    if edODMF < startdateNEWDT:
                        print("All new data after end date of existing data, proceed to process")
                    elif sdODMF > enddateNEWDT:
                        print("All new data before start date of existing data, proceed to process")
                    elif edODMF < enddateNEWDT and sdODMF < startdateNEWDT:
                        end_index = get_end_index(enddateODMstring)
                        end_index = end_index + 1  # add one since the index at the new start would overlap
                        for resultid, value in alldata.items():
                            value = value[end_index:]
                    elif sdODMF > startdateNEWDT and edODMF < enddateNEWDT:
                        print("Cutting out what is inbetween ODM start and end")
                        # call fctn to get index of start and end
                        start_index = get_start_index(alldate,startdateODMstring)
                        end_index = get_end_index(alldate,enddateODMstring)
                        end_index = end_index + 1  # add one since the index at the new start would overlap
                        for resultid, value in alldata.items():
                            value = value[:start_index] + value[end_index:]
                    elif edODMF >= enddateNEWDT and sdODMF < startdateNEWDT:
                        counts = check_existing_data(results, alldate[0], alldate[-1])
                        if len(alldate) == counts:
                            print("All %d values are redundant" % (counts))
                        elif counts < len(alldate) and counts != 0:
                            print("Number of redundant values to be kicked out: %d " % (counts))
                            print("Proceeding to check each value...")
                            dates, alldata = check_duplicate_dates(results, alldate,alldataanddates)
                    alldata['datetime'] = alldate
                    w.writeheader()
                    w.writerows(alldata)
        except IndexError:
            raise ValidationError('encountered a problem with row ' + str(i) for i in row)