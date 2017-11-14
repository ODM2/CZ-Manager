from __future__ import unicode_literals

import argparse
import os
from urlparse import urlparse
# import kronos
import shutil
import urllib2
from contextlib import closing
from django.core.management.base import BaseCommand
from django.core.management import settings

from odm2admin.models import Dataloggerfiles
from odm2admin.models import ProcessDataloggerfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='update datalogger file from ftp - ' +
                                             'ftp file URL should be the file description.')\




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)
        parser.add_argument('ftpfrequencyhours', nargs=1, type=str)
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)
        parser.add_argument('reversed', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        fileid = int(options['dataloggerfileid'][0])
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
        check_dates = bool(options['check_dates'][0])
        ftpfrequencyhours = int(options['ftpfrequencyhours'][0])
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        ftpfile = fileid.dataloggerfiledescription
        ftpparse = urlparse(ftpfile)
        pythonpath = settings.PYTHON_PATH
        apppath = settings.BASE_DIR
        # print(ftpparse.netloc)
        if len(ftpparse.netloc) > 0:
            out_file = str(settings.MEDIA_ROOT)+ filename
            # print(out_file)
            # print(ftpfile)
            # urllib.urlretrieve(ftpfile, out_file)
            with closing(urllib2.urlopen(ftpfile)) as r:
                with open(out_file, 'w') as f:
                    shutil.copyfileobj(r, f)
            # pdlf = ProcessDataloggerfile.objects.filter(dataloggerfileid=fileid).\
            #     filter(processingCode__icontains='hours between download')
            # ftpestablished = len(pdlf)
            # if ftpestablished == 0:
            #     # ProcessDataloggerfile(dataloggerfileid=fileid,
            #     #                      processingCode=str(ftpfrequencyhours)+" hours between download",
            #     #                      databeginson=databeginson,columnheaderson=columnheaderson)
            #     # ProcessDataloggerfile.save()
            #     intftpfrequencyhours = int(ftpfrequencyhours)
            #     kronos.register('0 */'+ str(intftpfrequencyhours) + ' * * * wget -q ' +out_file)
            #     # need a setting
            #     kronos.register('5 */' + str(intftpfrequencyhours) + ' * * *  ' + pythonpath +
            #                     " " +  apppath + "/manage.py updata_preprocess_process_datalogger_file dataloggerfiles/"+
            #                     filename + " " + str(fileid.dataloggerfileid) + " " +
            #                     str(databeginson) + " " + str(columnheaderson) + " True ")
        # file = str(settings.MEDIA_ROOT) + filename  # args[0].name
