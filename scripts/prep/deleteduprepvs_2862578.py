
import os
import csv
import pandas as pd
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
application = get_wsgi_application()
from django.db.models import Q
import re

from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max, Avg
import time as time
import xlrd
import pickle
from datetime import datetime, timedelta
from django.contrib.auth.models import User
resultids = [28222,44601,15331]
repvs = Resultextensionpropertyvalues.objects.filter(propertyid=16).order_by('resultid')
lastrepv = None
dels = []
for repv in repvs:
    print(repv)
    if lastrepv:
        if repv.resultid == lastrepv.resultid:
           #  print(repv)
            dels.append(repv)
    lastrepv = repv

if repv in dels:
    print(repv)
    repv.delete()

dels = []
repvs = Resultextensionpropertyvalues.objects.filter(propertyid=17).order_by('resultid')
lastrepv = None
for repv in repvs:
    print(repv)
    if lastrepv:
        if repv.resultid == lastrepv.resultid:
            # print(repv)
            repv.delete()
    lastrepv = repv

if repv in dels:
    print(repv)
    repv.delete()