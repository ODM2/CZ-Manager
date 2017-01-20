__author__ = 'leonmi'

import argparse
import csv
import io
import itertools
import os
import time
import StringIO
import re
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.core import mail
from odm2admin.models import Timeseriesresultvaluesext
from odm2admin.models import Results
from odm2admin.models import Timeseriesresultvaluesextwannotations

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

parser = argparse.ArgumentParser(description='export time series result values with annotations, if annotations exist.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('outgoingemail',nargs=1, type=str)
        parser.add_argument('startdate',nargs=1, type=str)
        parser.add_argument('enddate',nargs=1, type=str)
        parser.add_argument('usedates',nargs=1, type=str)
        parser.add_argument('timeseriesresults',nargs='+', type=str)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        timeseriesresults = options['timeseriesresults'][0]
        outgoingemail = options['outgoingemail'][0]
        usedates = bool(options['usedates'][0])
        entered_start_date = options['startdate'][0]
        entered_end_date = options['enddate'][0]
        csvfile = StringIO.StringIO()
        emailtitle = 'your ODM2 Admin data is attached'
        emailtext = 'Attached are results for the following time series: '
        # csvwriter = csv.writer(csvfile)
        # print(timeseriesresults)
        timeseriesresultlist= [item for item in timeseriesresults.split(',') if item.isdigit()]
        # print(timeseriesresultlist)
        timeseriesresultlist2 =[]
        tmpResult = ''
        for resultval in timeseriesresults:
            if not resultval ==',':
                tmpResult += resultval
            else:
                timeseriesresultlist2.append(int(tmpResult))
                tmpResult = ''
        timeseriesresultlist2.append(int(tmpResult))
        print(timeseriesresultlist2)
        if usedates:
            tsrvs = Timeseriesresultvaluesext.objects.filter(resultid__in=timeseriesresultlist2)\
                .filter(valuedatetime__gte=entered_start_date)\
                .filter(valuedatetime__lt=entered_end_date).order_by('valuedatetime')
        else:
            tsrvs = Timeseriesresultvaluesext.objects.filter(resultid__in=timeseriesresultlist2).\
                order_by('valuedatetime')
        i=0
        # print("time series result list2")
        # print(timeseriesresultlist2)
        print(outgoingemail)
        tolist = []
        tolist.append(outgoingemail) #= re.findall('\'([^\']*)\'',outgoingemail)
        resultid = None
        lastResultid = None
        results = Results.objects.filter(resultid__in=timeseriesresultlist2)
        for result in results:
            emailtext = emailtext + ' - ' + result.csvheaderShort()
            csvfile.write(result.csvheader())
            csvfile.write(result.csvheaderShort())
        csvfile.write('\n')
        lasttime = None
        curtime = None
        for tsrv in tsrvs:
            if curtime == None:
                curtime = tsrv.valuedatetime
                lasttime = tsrv.valuedatetime
            else:
                lasttime = curtime
                curtime = tsrv.valuedatetime
            if not curtime == lasttime:
                csvfile.write('\n')
            csvfile.write(tsrv.csvoutput())
            csvfile.write(tsrv.csvoutputShort())

        email = EmailMessage(emailtitle,emailtext,
                             'leonmi@sas.upenn.edu', tolist)
        email.attach('mydata.csv', csvfile.getvalue(),'text/csv')
        email.send()
