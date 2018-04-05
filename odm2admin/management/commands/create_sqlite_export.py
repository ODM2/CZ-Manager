from __future__ import unicode_literals

import argparse
import os
import io
import itertools
import csv
import shutil
from django.db import connection
from django.core.management.base import BaseCommand
from django.core.management import settings
from django.core import management
from odm2admin.models import Dataloggerfiles
from templatesAndSettings.settings import exportdb

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.exportdb")
os.environ['DJANGO_SETTINGS_MODULE'] = "templatesAndSettings.settings.exportdb"
__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='this command will create an sqlite database dump of the provided JSON files.')



# just passing database='export' to loaddata doesn't work because we need to tell models.py to use the correct table names.
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('jsonfile1', nargs=1, type=str)
        parser.add_argument('jsonfile2', nargs=1, type=str)
        parser.add_argument('dbfile', nargs=1, type=str)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        try:
            jsonfile1 = str(options['jsonfile1'][0])
            jsonfile2 = str(options['jsonfile2'][0])
            dbfile = str(options['dbfile'][0])
            self.stdout.write('start data load')
            # print('start data load')
            #f = open('/home/azureadmin/webapps/logs/logfile.txt', 'rw')
            #f.write('start load data')
            #f.write(jsonfile1,jsonfile2)
            exportdb.DATABASES['default']['NAME'] = dbfile
            # print(connection.settings_dict['NAME'])
            #f.close()
            management.call_command('loaddata',jsonfile1)  # ,database='export'
            management.call_command('loaddata',jsonfile2)
            # print('end data load')
        except Exception as e:
            return e
