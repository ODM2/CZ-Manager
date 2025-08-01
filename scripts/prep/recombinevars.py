
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

vars = Variables.objects.all().order_by('variable_name','variable_type', 'variableid')
lastvar = None
curvar = None
delvars = []
varcount = 0
deletevars1 = False
#if deletevars1:
for var in vars:
    lastvar = curvar
    curvar = var
    if lastvar and curvar:
        if lastvar.variable_type == curvar.variable_type  and  \
                lastvar.variable_name.name == curvar.variable_name.name and lastvar.variablecode==curvar.variablecode:
            print(var.variablecode)
            print(var.variable_name.name)
            print(var.variable_type)
            results = Results.objects.filter(variableid=lastvar)
            # for result in results:
            # result.variableid = lastvar
            results.update(variableid=var.variableid)
            delvars.append(lastvar)
            varcount +=1
if deletevars1:
    print("NEXT")
    for i in range(0,varcount):
        var = delvars[i]
        results = Results.objects.filter(variableid=var)
        print(var)
        print(len(results))
        if len(results) == 0:
            var.delete()
#
# delvars = []
# varcount = 0
# for var in vars:
#     results = Results.objects.filter(variableid=lastvar)
#     if len(results) == 0:
#         delvars.append(var)
#         varcount +=1
#
# print("NEXT")
# for i in range(0,varcount):
#     var = delvars[i]
#     results = Results.objects.filter(variableid=var)
#     print(var)
#     print(len(results))
#     if len(results) == 0:
#         var.delete()
