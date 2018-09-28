from __future__ import unicode_literals

import argparse
import os
import re
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.core.management import settings
from django.core import management
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from odm2admin.models import Dataloggerfiles
from odm2admin.models import ProcessDataloggerfile
from odm2admin.models import Dataloggerfilecolumns
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='loop through all data logger files and process ftp files.')\




class Command(BaseCommand):

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        dlfs = Dataloggerfiles.objects.all()
        for dlf in dlfs:
            try:
                dlfccount = Dataloggerfilecolumns.objects.filter(dataloggerfileid=dlf.dataloggerfileid).count()
                if dlfccount > 0:
                    pdlf = ProcessDataloggerfile.objects.filter(dataloggerfileid=dlf.dataloggerfileid
                                                                ).filter(processingCode__icontains='hours between download'
                                                                         ).get()
                    linkname = str(pdlf.dataloggerfileid.dataloggerfilelinkname())
                    fileid = pdlf.dataloggerfileid.dataloggerfileid
                    ftpfile = pdlf.dataloggerfileid.dataloggerfiledescription
                    ftpparse = urlparse(ftpfile)
                    if len(ftpparse.netloc) > 0:
                        ftpfrequencyhours = re.findall(r'^\D*(\d+)', pdlf.processingCode)[0]
                        management.call_command('update_datalogger_file', linkname, str(fileid)
                                                , str(pdlf.databeginso), str(pdlf.columnheaderson), str(ftpfrequencyhours),
                                                True, False, True)
                        management.call_command('preprocess_datalogger_file', linkname, str(fileid)
                                                , str(pdlf.databeginso), str(pdlf.columnheaderson),
                                                True)
                        management.call_command('ProcessDataLoggerFile', linkname, str(fileid)
                                                , str(pdlf.databeginson), str(pdlf.columnheaderson),
                                                True, False, True)
            except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
                pass