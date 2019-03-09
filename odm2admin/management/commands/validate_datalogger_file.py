from __future__ import unicode_literals

import argparse
import os
import csv
import io
import itertools
import time
import xlrd
# import numpy as np
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import settings
from django.utils.crypto import get_random_string
import sys
from odm2admin.models import ProcessDataloggerfile
from odm2admin.models import Dataloggerfiles
from odm2admin.models import Featureactions
from odm2admin.models import Samplingfeatures
from odm2admin.models import Methods
from odm2admin.models import Actions
from odm2admin.models import Results
from odm2admin.models import Extensionproperties
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Dataloggerfilecolumns
from odm2admin.models import Timeseriesresultvalues

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

parser = argparse.ArgumentParser(description='validate dates in datalogger file.')



def getStartDateEndDate(results,stdout):
    StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
    EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    # result = results#.objects.get(resultid=results.resultid.resultid)
    repvstart = None
    repvend = None
    try:
        # raise CommandError(" start date "str(startdate)))
        #
        repvstart= Resultextensionpropertyvalues.objects.filter(resultid=results.resultid.resultid).filter(
            propertyid=StartDateProperty).get() #.update(propertyvalue=startdate)
        repvend = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid.resultid).filter(
            propertyid=EndDateProperty).get() #.update(propertyvalue=enddate)
        return repvstart,repvend
    except ObjectDoesNotExist:
        tsrvs = Timeseriesresultvalues.objects.filter(resultid=results.resultid.resultid)
        tsrvscount = len(tsrvs)
        stdout.write('the time series with resultid ' + str(results.resultid.resultid)
                     + ' has no start date or end date the number of time series values in the database is: '
                     + str(tsrvscount))
        return repvstart, repvend

def get_results(fileid):
    dataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
        dataloggerfileid=fileid)
    surface_results_ = Results.objects.filter(resultid__in=dataloggerfilecolumnSet.values('resultid'))
    return surface_results_


# def check for existing data, check greater than start, less than end, and if size equal to all new data
def check_existing_data(sr_, startdate_, enddate_,stdout):
    for surface_result in sr_:
        time_series_values_ = Timeseriesresultvalues.objects.filter(valuedatetime__lte= enddate_).filter(
            valuedatetime__gte= startdate_).filter(resultid=surface_result.resultid.resultid)

        valuecounts_ = time_series_values_.count()
        stdout.write('values already exist in the database for result: ' + str(surface_result))
        stdout.write('The number of existing database values between the file start data and end date is: ' + str(valuecounts_))
    return valuecounts_


def get_start_index(alldate, startdateODMstring_,stdout):
    # Check for Start date
    try:
        s = alldate.index(startdateODMstring_)
    except ValueError:
        searchval = datetime.datetime.strptime(startdateODMstring_, "%Y-%m-%d %H:%M:%S")
        # ii = bisect.bisect_right(values, searchval)
        newstart = (
            min([datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in alldate], key=lambda x: abs(x - searchval))).strftime(
            "%Y-%m-%d %H:%M:%S")
        rs_ = alldate.index(newstart)
        stdout.write("File does not contain the database start date, the nearest date in the file is: " + str(newstart))
        return rs_
    stdout.write("the file contains the database start date %s on row: %d" % (alldate[s], s))
    rs_ = s

    return rs_

def check_duplicate_dates(resultids_, checkdate_,alldata,stdout):
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
                valuedatetime = d).filter(resultid=rid.resultid.resultid)  # Need to get ResultID automatically still
            # ResultID=surface_result.ResultID)
            value_check.append(time_series_values.count())

        # if sum(value_check) == len(resultids_):
        # Newdates_[i] = np.nan
        for resultid, value in alldata.items():
            # print('value!!!')
            # print(value)
            val = value[0]
            newdatetime = val[0]
            newvalue = val[1]
            if rid == resultid and newdatetime == d:
                stdout.write('duplicate data on: ' + str(d) + 'duplicate value:' + str(val[1]) + ' for result: ' +str(rid))
                val[1] = float('NaN')# np.nan

        i += 1
    return Newdates_,alldata

def writefile(alldate,alldata,writer,new_file_name,stdout):
    alldataanddatesbydate = {}
    # w.writeheader()
    for date in alldate:
        if alldataanddatesbydate.get(date) is None:
            alldataanddatesbydate[date] = []
        for key, values in alldata.items():
            popval = None
            for value in values:
                alldataanddatesbydate[date].append(value)
                popval = value
                break
            values.pop(0)
        # for dloggerfileColumn in DataloggerfilecolumnSet:
        #    foundColumn = False
        #    resultid = dloggerfileColumn.resultid
        #    if key == resultid:
    for date, vals in alldataanddatesbydate:
        r = [date]
        for val in vals:
            r.append(val)
        writer.writerow(r)
    stdout.write('<a href=' + settings.MEDIA_URL + new_file_name + '> validated file</a>')

def check_start_end_dates_equal(ODM2startdates,ODM2enddates,stdout):
    teststartd = None
    oldteststartd = None
    testendd = None
    oldtestendd = None
    dates_all_equal = True
    for odm2start, odm2end in zip(ODM2startdates, ODM2enddates):
        oldteststartd = teststartd
        teststartd = odm2start
        if not oldteststartd is None:
            if oldteststartd.propertyvalue == teststartd.propertyvalue:
                continue
            else:
                stdout.write('Time series related to this file do not have the same start date.')
                stdout.write('If your loading new data this may not be a problem, maybe you added an instrument,' +
                                  ' or time series after you began data collection.')
                stdout.write('Time series with result: ' + str(
                    oldteststartd.resultid) + ' has a start date of ' + str(oldteststartd.propertyvalue))
                stdout.write('Time series with result: ' + str(
                    teststartd.resultid) + ' has a start date of ' + str(teststartd.propertyvalue))
                dates_all_equal = False
        oldtestendd = testendd
        testendd = odm2end
        if not oldtestendd is None:
            if oldtestendd.propertyvalue == testendd.propertyvalue:
                continue
            else:
                stdout.write('Time series related to this file do not have the same end date.')
                stdout.write('Time series with result: ' + str(
                    oldtestendd.resultid) + ' has a end date of ' + str(oldtestendd.propertyvalue))
                stdout.write('Time series with result: ' + str(
                    testendd.resultid) + ' has a end date of ' + str(testendd.propertyvalue))
                dates_all_equal = False
        if not dates_all_equal:
            stdout.write("not all time series related to this file begin and end on the same datetimes.")
        return dates_all_equal

def get_end_index(alldate,enddateODMstring_,stdout):
    # check for end date
    try:
        e = alldate.index(enddateODMstring_)
    except ValueError:
        searchval = datetime.datetime.strptime(enddateODMstring_, "%Y-%m-%d %H:%M:%S")
        # ii = bisect.bisect_right(values, searchval)
        newend = (
            min([datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in alldate], key=lambda x: abs(x - searchval))).strftime(
            "%Y-%m-%d %H:%M:%S")
        re_ = alldate.index(newend)
        stdout.write("File does not contain the database end date, the nearest date in the file is: " +str(re_))
        return re_
    re_ = e
    stdout.write("the file contains the database end date %s on row: %d" % (alldate[e], e))

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
        new_file_name = filename + 'prerpocessed' +random_string + '_'
        new_file = str(settings.MEDIA_ROOT) +  filename + 'prerpocessed' +random_string + '_'  # args[0].name
        fileid = int(options['dataloggerfileid'][0])
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        stop_reading_reversed = False
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
        exceldatetime = False
        rowColumnMap = list()
        bulktimeseriesvalues = []
        bulkcount = 0
        alldate = []
        fields = ['datetime']
        dateTimeColNum = 0
        try:
            with io.open(file, 'rt', encoding='ascii') as f:
                with io.open(new_file, 'w', encoding='ascii') as outfile:

                    # reader = csv.reader(f)
                    columnsinCSV = None
                    reader = csv.reader(f) # itertools.tee(
                    self.stdout.write('beginning validation')
                    # self.stdout.write('test')
                    results = get_results(fileid)
                    DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(
                        dataloggerfileid=fileid)
                    i = 0
                    numCols = 0
                    numDLCols = DataloggerfilecolumnSet.count()
                    startdateNEW = ''
                    enddateNEW = ''
                    ODM2startdates =[]
                    ODM2enddates = []
                    alldata = {}
                    alldataanddates={}
                    results = []
                    for dlfc in DataloggerfilecolumnSet:
                        fields.append(dlfc.resultid)
                    w = csv.writer(outfile)
                    for row in reader:
                        numCols = len(row)
                        # print('reading file')
                        # print(i)
                        # print(columnheaderson)
                        if i == columnheaderson:
                            for dloggerfileColumn in DataloggerfilecolumnSet:
                                foundColumn = False
                                resultid = dloggerfileColumn.resultid
                                results.append(dloggerfileColumn)

                                startdateODM,enddateODM= getStartDateEndDate(dloggerfileColumn, self.stdout)
                                if startdateODM and enddateODM:
                                    sdopd = str(startdateODM.propertyvalue)
                                    edopd = str(enddateODM.propertyvalue)
                                    # print(dloggerfileColumn)
                                    # print(sdODMF)
                                    # print()
                                    sdODMF = datetime.datetime.strptime(sdopd[:16], "%Y-%m-%d %H:%M")
                                    edODMF = datetime.datetime.strptime(edopd[:16], "%Y-%m-%d %H:%M")
                                    startdateODMstring = sdODMF.strftime("%Y-%m-%d %H:%M:%S")
                                    enddateODMstring = edODMF.strftime("%Y-%m-%d %H:%M:%S")
                                    ODM2startdates.append(startdateODMstring)
                                    ODM2enddates.append(enddateODMstring)
                                lastResult = resultid
                                for j in range(numCols):
                                    # print('match Columns')
                                    # print(row[j])
                                    # print(dloggerfileColumn.columnlabel)
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
                            # print('print validation row')
                            # print(row)
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
                            # print('date to append')
                            # print(datestr)
                            enddateNEW = datestr
                            for j in range(numCols):
                                curcol = -1
                                for col in DataloggerfilecolumnSet:
                                    if col.columnnum == j:
                                        curcol = col
                                if col.resultid in alldata:
                                    alldata[col.resultid.resultid].append(row[j])
                                    alldataanddates[col.resultid.resultid].append([dateT, row[j]])
                                else:
                                    alldata[col.resultid.resultid] = []
                                    alldata[col.resultid.resultid].append(row[j]) # [dateT, row[j]]
                                    alldataanddates[col.resultid.resultid] = []
                                    alldataanddates[col.resultid.resultid].append([dateT, row[j]])
                        i+=1
                    # enddateNEW = datestr
                    date_match = check_start_end_dates_equal(ODM2startdates,ODM2enddates, self.stdout)
                    self.stdout.write("Using the last time series for start and end dates: " + str(lastResult))
                    self.stdout.write("Database values begin on: " + str(ODM2startdates))
                    self.stdout.write("Database values end on: " + str(ODM2enddates))
                    self.stdout.write("This dataloggerfile has values that begin on: " + str(startdateNEW))
                    self.stdout.write("This dataloggerfile has values that end on: " + str(enddateNEW))

                    startdateNEWDT = datetime.datetime.strptime(startdateNEW, "%Y-%m-%d %H:%M:%S")
                    enddateNEWDT = datetime.datetime.strptime(enddateNEW, "%Y-%m-%d %H:%M:%S")
                    if sdODMF and edODMF:
                        if sdODMF > startdateNEWDT and edODMF < enddateNEWDT:
                            self.stdout.write("ODM2 start date in database " + str(sdODMF) +
                                              " is greater then the start date in the new file: " + str(startdateNEWDT))
                            self.stdout.write("ODM2 end date in database " + str(edODMF) +
                                              " is less then the end date in the new file: " + str(enddateNEWDT))
                            self.stdout.write("The file contains data both before the time series in the database begin and" +
                                " after data in the database end. Consider uploading two seperate files, one for older " +
                                              " data you are back filling and one for new data.")
                            # call fctn to get index of start and end
                            start_index = get_start_index(alldate,startdateODMstring,self.stdout)
                            end_index = get_end_index(alldate,enddateODMstring,self.stdout)
                            end_index = end_index + 1  # add one since the index at the new start would overlap
                            for resultid, value in alldata.items():
                                value = value[:start_index] + value[end_index:]
                        elif edODMF >= enddateNEWDT and sdODMF < startdateNEWDT:
                            counts = check_existing_data(results, alldate[0], alldate[-1],self.stdout)
                            self.stdout.write('The number of rows in the file you are checking is: ' + str(len(alldate)))
                            if len(alldate) == counts:
                                self.stdout.write("All %d values are redundant" % (counts))
                                self.stdout.write("All data are already in the database, no need to ingest the data again.")
                            elif counts < len(alldate) and counts != 0:
                                self.stdout.write("All data overlap with the existing time series. But there are more time series values in the file" +
                                                  " then in the database, perhaps you are trying to gap fill some time series?")
                                self.stdout.write("The Number of datetimes already in the database is: %d " % (counts))
                                self.stdout.write("The Number of datetimes in the file is: %d " % len(alldate))
                                self.stdout.write("Proceeding to check each value...")
                                dates, alldata2 = check_duplicate_dates(results, alldate,alldataanddates,self.stdout)
                        elif edODMF < enddateNEWDT and sdODMF < startdateNEWDT:
                            end_index = get_end_index(alldate,enddateODMstring,self.stdout)
                            end_index = end_index + 1  # add one since the index at the new start would overlap
                            for resultid, value in alldata.items():
                                value = value[end_index:]
                        elif edODMF < startdateNEWDT:
                            self.stdout.write("All new data are after end date of data in the database, proceed to process")
                        elif sdODMF > enddateNEWDT:
                            self.stdout.write("All new data are before start date of data in the database, proceed to process")
                        elif edODMF >= enddateNEWDT:
                            self.stdout.write("data base end date: " + str(edODMF) +
                                              " is greater then or equal to file end date "+
                                              str(enddateNEWDT) + ", some values overlap")
                        # This condition is always ok actually.
                        # elif sdODMF <= startdateNEWDT:
                        #     self.stdout.write("data base start date: " + str(sdODMF) +
                        #                       " is less then or equal to the file end date "+
                        #                       str(startdateNEWDT) + ", some values overlap")
                        # alldata['datetime'] = alldate
                        # writefile not working yet.
                        # writefile(alldata,alldate,w,new_file_name,self.stdout)
        except IndexError:
            raise ValidationError('encountered a problem with row ' + str(i) for i in row)