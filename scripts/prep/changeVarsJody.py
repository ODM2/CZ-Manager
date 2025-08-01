
import os
import csv
import pandas as pd
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
application = get_wsgi_application()
from django.db.models import Q
import re
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max, Avg
import time as time
import xlrd
import pickle
from django.db.utils import IntegrityError
from datetime import datetime, timedelta
from django.contrib.auth.models import User

varstochangeNO3 = [1646, 1683, 1730]
NO3var = 1638
for no3var in varstochangeNO3:
    newvar = Variables.objects.filter(variableid=1638).get()
    results = Results.objects.filter(variableid=no3var)
    for result in results:
        result.variableid = newvar

        result.save()

varstochangeDN = 1636
DNvar = 1641

# newvar = Variables.objects.filter(variableid=1641).get()
# results = Results.objects.filter(variableid=1636)
# for result in results:
#     result.variableid = newvar
#     result.save()