import argparse
import os
import io
import itertools
import csv
import shutil
from django.db import connection
from django.core.management.base import BaseCommand
import datetime as datetime
# from django.core.management import settings
from django.core import management
from django import db
from odm2admin.models import Dataloggerfiles
from templatesAndSettings.settings import development
from django.conf import settings
from hs_restclient import HydroShare, HydroShareAuthOAuth2

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.development")

os.environ['DJANGO_SETTINGS_MODULE'] = "templatesAndSettings.settings.development"
__author__ = 'leonmi'


parser = argparse.ArgumentParser(description='this command will create an sqlite database dump of the provided JSON files.')

# just passing database='export' to loaddata doesn't work because we need to tell models.py to use the correct table names.
class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument('username', nargs=1, type=str)
        parser.add_argument('password', nargs=1, type=str)
        parser.add_argument('django_user_name', nargs=1, type=str)
        parser.add_argument('datasettitle', nargs=1, type=str)

        parser.add_argument('startdate', nargs=1, type=str)
        parser.add_argument('enddate', nargs=1, type=str)
        parser.add_argument('datafile', nargs=1, type=str)
        parser.add_argument('dbfilename', nargs=1, type=str)
    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        # cmdline = bool(options['cmdline'][0])
        username = str(options['username'][0])
        password = str(options['password'][0])
        hs_client_id = settings.SOCIAL_AUTH_HYDROSHARE_UP_KEY
        hs_client_secret = settings.SOCIAL_AUTH_HYDROSHARE_UP_SECRET
        auth = HydroShareAuthOAuth2(hs_client_id, hs_client_secret,
                                    username=username, password=password)
        # print(username)
        # print(password)
        export_complete = True
        resource_link = ''
        user = str(options['django_user_name'][0])
        datasettitle = str(options['datasettitle'][0])
        startdate = str(options['startdate'][0])
        enddate = str(options['enddate'][0])
        datafile = str(options['datafile'][0])
        dbfilename = str(options['dbfilename'][0])
        # print(request.POST['hydroshareusername'])

        # hs = get_oauth_hs(request)
        # userInfo = hs.getUserInfo()
        #
        hs = HydroShare(auth=auth)
        # username = hs.getUserInfo()
        # print(username)
        abstracttext = ''
        title = ''

        abstracttext += 'ODM2 Admin dataset: ' + str(datasettitle)
        title += 'ODM2 Admin dataset ' + str(datasettitle)
        abstract = abstracttext
        keywords = ['ODM2']
        rtype = 'GenericResource'
        fpath = datafile  # str(exportdb.DATABASES['default']['NAME'])

        # # print(fpath)
        # #metadata = '[{"coverage":{"type":"period", "value":{"start":"'+entered_start_date +'", "end":"'+ entered_end_date +'"}}}, {"creator":{"name":"Miguel Leon"}}]'
        metadata = '[{"coverage":{"type":"period", "value":{"start":"' + str(startdate) + '", "end":"' + str(
            enddate) + '"}}}, ' \
                       '{"creator":{"name":"' + user + '"}}]'
        extra_metadata = '{"key-1": "value-1", "key-2": "value-2"}'
        # #abstract = 'My abstract'
        # #title = 'My resource'
        # #keywords = ('my keyword 1', 'my keyword 2')
        # #rtype = 'GenericResource'
        # #fpath = 'C:/Users/leonmi/Google Drive/ODM2AdminLT2/ODM2SQliteBlank.db'
        # #metadata = '[{"coverage":{"type":"period", "value":{"start":"01/01/2000", "end":"12/12/2010"}}}, {"creator":{"name":"John Smith"}}, {"creator":{"name":"Lisa Miller"}}]'
        # #extra_metadata = '{"key-1": "value-1", "key-2": "value-2"}'
        # messages.success(request, 'Profile details updated.')
        resource_id = hs.createResource(rtype, title, resource_file=datafile,
                                        resource_filename=dbfilename, keywords=keywords,
                                        abstract=abstract, metadata=metadata, extra_metadata=extra_metadata)
        print('resource created')
        print(resource_id)