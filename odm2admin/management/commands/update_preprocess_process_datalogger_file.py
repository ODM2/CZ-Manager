from __future__ import unicode_literals

import argparse
import os
#from urlparse import urlparse
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.core.management import settings
from django.core import management
from odm2admin.models import Dataloggerfiles
from odm2admin.models import ProcessDataloggerfile
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

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
        parser.add_argument('ftpfrequencyhours', nargs=1, type=str)
        parser.add_argument('setupcomplete', nargs=1, type=str)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        setupcomplete = str(options['setupcomplete'][0])
        print(setupcomplete)
        filename = str(options['dataloggerfilelink'][0])
        print(filename)
        fileid = int(options['dataloggerfileid'][0])
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        ftpfrequencyhours = int(options['ftpfrequencyhours'][0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
        dlf = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()

        filename = dlf.dataloggerfilelinkname()
        fileid = dlf.dataloggerfileid
        if setupcomplete == 'False':
            try:
                pdlf = ProcessDataloggerfile.objects.filter(dataloggerfileid=dlf.dataloggerfileid
                                                            ).filter(processingCode__icontains='hours between download'
                                                                     ).get()
                raise ValidationError("This data logger file has already been setup for FTP.")
            except ObjectDoesNotExist:
                print('setup cron')
                ftpfile = dlf.dataloggerfiledescription
                management.call_command('update_datalogger_file', filename,str(fileid)
                                        , str(databeginson), str(columnheaderson),str(ftpfrequencyhours),ftpfile,
                                        True, False, True)
        else:
            filenameout = management.call_command('preprocess_datalogger_file', filename, str(fileid)
                                    , str(databeginson), str(columnheaderson),
                                    True)

            management.call_command('ProcessDataLoggerFile', filenameout, str(fileid)
                                    , str(databeginson), str(columnheaderson),
                                    True, False, True)