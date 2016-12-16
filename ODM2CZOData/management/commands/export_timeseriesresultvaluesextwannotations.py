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
from ODM2CZOData.models import Timeseriesresultvaluesext
from ODM2CZOData.models import Results
from ODM2CZOData.models import Timeseriesresultvaluesextwannotations

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

parser = argparse.ArgumentParser(description='export time series result values with annotations, if annotations exist.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('outgoingemail',nargs=1, type=str)
        parser.add_argument('timeseriesresults',nargs='+', type=str)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        timeseriesresults = options['timeseriesresults'][0]
        outgoingemail = options['outgoingemail'][0]
        # csvfile = StringIO.StringIO()
        # csvwriter = csv.writer(csvfile)
        # for leads in assigned_leads:
        #     csvwriter.writerow([leads.business_name, leads.first_name, leads.last_name, leads.email, leads.phone_number,leads.address, leads.city, leads.state, leads.zipcode, leads.submission_date, leads.time_frame, leads.comments])
        # message = EmailMessage("Hello","Your Leads","myemail@gmail.com",["myemail@gmail.com"])
        # message.attach('invoice.csv', csvfile.getvalue(), 'text/csv')
        csvfile = StringIO.StringIO()
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
        tsrvs = Timeseriesresultvaluesext.objects.filter(resultid__in=timeseriesresultlist2).order_by('valuedatetime')
        i=0
        # print("time series result list2")
        # print(timeseriesresultlist2)
        print(outgoingemail)
        tolist = []
        tolist.append('leonmi@sas.upenn.edu') #= re.findall('\'([^\']*)\'',outgoingemail)
        resultid = None
        lastResultid = None
        results = Results.objects.filter(resultid__in=timeseriesresultlist2)
        for result in results:
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

        email = EmailMessage('data email subject', 'your data is attached body.',
                             'leonmi@sas.upenn.edu', tolist)
        email.attach('mydata.csv', csvfile.getvalue(),'text/csv')
        email.send()
