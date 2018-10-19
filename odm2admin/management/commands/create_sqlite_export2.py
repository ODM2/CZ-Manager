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

        parser.add_argument('dbfile', nargs=1, type=str)
        parser.add_argument('jsonfile', nargs='*', type=str)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        try:
            i=0
            jsonfileargs = options['jsonfile']
            jsonfiles = []
            for jsonfile in jsonfileargs:
                jsonfiles.append(str(options['jsonfile'][i]))
                i+=1
            dbfile = str(options['dbfile'][0])
            self.stdout.write('start data load')
            self.stdout.write(dbfile)
            print('start data load')
            print(dbfile)
            #f = open('/home/azureadmin/webapps/logs/logfile.txt', 'rw')
            #f.write('start load data')
            #f.write(jsonfile1,jsonfile2)
            exportdb.DATABASES['default']['NAME'] = dbfile
            # print(connection.settings_dict['NAME'])
            #f.close()
            for jsonfile in jsonfiles:
                print(jsonfile)
                management.call_command('loaddata',jsonfile)  # ,database='export'
            # print('end data load')
        except Exception as e:
            self.stdout.write(e)
            return e
