from __future__ import unicode_literals

import argparse
import os
from urlparse import urlparse
import urllib

from django.core.management.base import BaseCommand
from django.core.management import settings

from odm2admin.models import Dataloggerfiles


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
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)
        parser.add_argument('reversed', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        fileid = int(options['dataloggerfileid'][0])
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        ftpfile = fileid.dataloggerfiledescription
        ftpparse = urlparse(ftpfile)
        ftpfile = False
        print(ftpparse.netloc)
        if len(ftpparse.netloc) > 0:
            out_file = str(settings.MEDIA_ROOT) + filename
            print(out_file)
            print(ftpfile)
            urllib.urlretrieve(ftpfile, out_file)
            ftpfile = True
        # file = str(settings.MEDIA_ROOT) + filename  # args[0].name
