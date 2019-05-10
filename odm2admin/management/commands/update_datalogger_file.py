from __future__ import unicode_literals

import argparse
import os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
# import kronos
import urllib
import subprocess
import sys
import shutil
import stat
from contextlib import closing
from django.core.management.base import BaseCommand
from django.core.management import settings
from django.db.models import Q
from odm2admin.models import Dataloggerfiles
from odm2admin.models import ProcessDataloggerfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='update datalogger file from ftp - ' +
                                             'ftp file URL should be the file description.')\



# @kronos.register('55 14 * * *', args={'-dataloggerfilelink': [],
#                                       '-dataloggerfileid': [],
#                                       '-databeginson': [],
#                                       '-columnheaderson': [],
#                                       '-ftpfrequencyhours': [],
#                                       '-ftpfile': [],
#                                       '-check_dates': [],
#                                       '-cmdline': [],
#                                       '-reversed': []})
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('dataloggerfilelink', nargs=1, type=str)
        parser.add_argument('dataloggerfileid', nargs=1, type=str)
        parser.add_argument('databeginson', nargs=1, type=str)
        parser.add_argument('columnheaderson', nargs=1, type=str)
        parser.add_argument('ftpfrequencyhours', nargs=1, type=str)
        # parser.add_argument('ftpfile', nargs=1, type=bool)
        parser.add_argument('check_dates', nargs=1, type=bool)
        parser.add_argument('cmdline', nargs=1, type=bool)
        # parser.add_argument('reversed', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        cmdline = bool(options['cmdline'][0])
        filename = str(options['dataloggerfilelink'][0])
        fileid = int(options['dataloggerfileid'][0])
        databeginson = int(options['databeginson'][0])  # int(databeginson[0])
        columnheaderson = int(options['columnheaderson'][0])  # int(columnheaderson[0])
        check_dates = bool(options['check_dates'][0])
        ftpfrequencyhours = int(options['ftpfrequencyhours'][0])
        # reversed = bool(options['reversed'][0])
        print(ftpfrequencyhours)
        intfileid = fileid
        fileid = Dataloggerfiles.objects.filter(dataloggerfileid=fileid).get()
        ftpfile = fileid.dataloggerfiledescription
        ftpparse = urlparse(ftpfile)
        pythonpath = settings.PYTHON_EXEC
        apppath = settings.BASE_DIR
        # print(ftpparse.netloc)
        if len(ftpparse.netloc) > 0:
            out_file = str(settings.MEDIA_ROOT)+ filename
            # print(settings.MEDIA_ROOT)
            # print(out_file)
            # print(ftpfile)
            # urllib.urlretrieve(ftpfile, out_file)
            # with closing(urllib.request.urlopen(ftpfile)) as r:
            #     with open(out_file, 'wb+') as f:
            #        shutil.copyfileobj(r, f)
            # write script file
            pdlf = ProcessDataloggerfile.objects.filter(dataloggerfileid=fileid). \
                filter(Q(processingCode__icontains='ftp setup complete') | Q(processingCode__icontains='done'))
            # filter(processingCode__icontains='done')
            ftpestablished = pdlf.count()
            localbasedir = settings.TEMPLATE_DIR
            if ftpestablished == 0:
                pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=fileid)
                pdlf.processingCode = 'ftp setup complete'
                pdlf.save()
                print('create ftp file')
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
                sysout = sys.stdout

                sys.stdout = open(localbasedir + '/templatesAndSettings/scripts/ftp_file_download.sh', 'w')
                # / home / miguelcleon / webapps / odm2admin2 / manageexport.py
                # create_sqlite_export
                # sys.stdout = sysout
                commandstring = '#!/usr/bin/env bash \n '
                # print(commandstring)
                commandstring += 'sudo crontab -l >'+ localbasedir + '/templatesAndSettings/scripts/mycron \n '
                # print(commandstring)
                commandstring += 'echo "49 */' + str(ftpfrequencyhours) + ' * * * wget -q ' +ftpfile + ' -O ' + \
                                out_file + '" >> '+ localbasedir + '/templatesAndSettings/scripts/mycron \n'
                # commandstring += ' %>> ' + settings.BASE_DIR + '/logging/ftp_download.log'
                # print(commandstring)

                commandstring += 'echo "50 */' + str(ftpfrequencyhours) + ' * * * '
                commandstring += pythonpath + ' '
                commandstring += settings.TEMPLATE_DIR  + '/managecli.py'
                commandstring += ' update_preprocess_process_datalogger_file ' + filename + ' ' \
                            +  str(intfileid) + ' ' + str(databeginson)+ ' ' + str(columnheaderson) + ' ' + str(ftpfrequencyhours) + ' ' \
                            + ' True'
                commandstring += " &>> " + localbasedir + '/templatesAndSettings/logging/downloadftp.log " >> ' +\
                                 localbasedir + '/templatesAndSettings/scripts/mycron \n'
                # print(commandstring)
                commandstring += 'sudo crontab '+ localbasedir + '/templatesAndSettings/scripts/mycron \n '
                print(commandstring)
                # command = settings.BASE_DIR + '/scripts/ftp_file_download.sh'  # + dbfile2 + ' %>> ' + settings.BASE_DIR +'/logging/sqlite_export.log'
                # st = os.stat(command)
                # try:
                #     os.chmod(command, st.st_mode | stat.S_IEXEC)
                # except OSError as e:
                #     pass
                # # print(command)
                sys.stdout = sysout
                # print(commandstring)
                # response = subprocess.check_call(command, shell=True)  #