from __future__ import unicode_literals

import argparse
import os
import io
import itertools
import csv
import shutil

from django.core.management.base import BaseCommand
from django.core.management import settings

from odm2admin.models import Dataloggerfiles


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='this command will reverse a file while first preappending the header.')




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)
        parser.add_argument('cmdline', nargs=1, type=bool)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        print('preprocess')
        filenameparts = filename.split('/')
        filenameout = ''
        i = 0
        lastpart = len(filenameparts)
        for part in filenameparts:
            i+=1
            if i ==lastpart:
                filenameout += '/reversed_' + part
            else:
                filenameout += part
        fileid = int(options['dataloggerfileid'][0])
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])
        file_in = str(settings.MEDIA_ROOT) + filename  # args[0].name
        file_out = str(settings.MEDIA_ROOT) + filenameout
        i=0
        # write the header to the new file
        with io.open(file_in, 'rt', encoding='ascii') as f_in:
            with io.open(file_out, 'w', encoding='ascii') as f_out:
                reader =csv.reader(f_in)
                writer = csv.writer(f_out)
                for row in reader:
                    # print(row)
                    # map the column objects to the column in the file assumes first row in
                    # file contains columnlabel.
                    i+=1
                    if i <= databeginson:
                        writer.writerow(row)
                    else:
                        break
        # write the reversed data
        with io.open(file_in, 'rt', encoding='ascii') as f_in:
            with io.open(file_out, 'a', encoding='ascii') as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)
                row2 = []
                for row in reversed(list(reader)):
                    #for cell in row:
                    #    row2.append(unicode(cell))
                    writer.writerow(row)

        #shutil.copy(src, dst
        #Replace original file with reversed
        shutil.copy(file_out,file_in)
        return filenameout
