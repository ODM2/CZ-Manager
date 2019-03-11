import argparse
import os
import io
import itertools
import csv
import shutil
from django.db import connection
from django.core.management.base import BaseCommand
# from django.core.management import settings
from django.core import management
from django import db
from odm2admin.models import Dataloggerfiles
from templatesAndSettings.settings import development
from templatesAndSettings.settings import exportdb

from django.conf import settings

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
            exportdb.DATABASES['export']['NAME'] = dbfile
            db.close_old_connections()
            # db.router()
            #settings.EXPORTDB = True
            #settings.configure(EXPORTDB=True)
            db_name = connection.settings_dict['NAME']
            print('current db')
            print(db_name)
            #f.close()
            for jsonfile in jsonfiles:
                print('LOAD FILE')
                print(jsonfile)
                if '.json' in jsonfile:
                    filesize = os.path.getsize(jsonfile)
                    print(filesize)

                    if filesize > 0:
                        load = management.call_command('loaddata',jsonfile,database='export')  #
                        print('load complete')
                        print(load)
            # print('end data load')
        except Exception as e:
            self.stdout.write(e)
            print(e)
            #settings.configure(EXPORTDB=False)
            return e
        #settings.configure(EXPORTDB=False)
