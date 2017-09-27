from __future__ import unicode_literals

import argparse
import os
from urlparse import urlparse
import urllib

from django.core.management.base import BaseCommand
from django.core.management import settings
from django.core import management
from odm2admin.models import Dataloggerfiles


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='complete three step datalogger file processing - ' +
                                             'download file from ftp, preprocess the file, and ' +
                                             'load the data into the database.')\




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)
        parser.add_argument('reversed', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        fileid = int(options['dataloggerfileid'][0])
        check_dates = bool(options['check_dates'][0])
        reversed = bool(options['reversed'][0])
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
        management.call_command('update_datalogger_file', filename,str(fileid)
                                , str(databeginson), str(columnheaderson),
                                True, False, True)
        management.call_command('preprocess_datalogger_file', filename,str(fileid)
                                , str(databeginson), str(columnheaderson),
                                 True)

        management.call_command('ProcessDataLoggerFile', filename,str(fileid)
                                , str(databeginson), str(columnheaderson),
                                True, False, True)