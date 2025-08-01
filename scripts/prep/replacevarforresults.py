
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
deletevars1 = True
goodvar = 1638
results = [110716, 110698, 110741]
goodvar = Variables.objects.filter(variableid=goodvar)[0]
badresults = Results.objects.filter(resultid__in=results)
#if deletevars1:
for result in badresults:
    # lastvar = curvar
    # curvar = var
    print(result)
    # print(var.variable_name.name)
    # print(var.variable_type)
    # results = Results.objects.filter(variableid=var)
    # for result in results:
    # result.variableid = lastvar
    result.variableid=goodvar
    result.save()
    # delvars.append(lastvar)
    varcount +=1
if deletevars1:
    print("NEXT")
    for result in badresults:

        # results = Results.objects.filter(variableid=var)
        print(result)
        # print(len(results))
        # if len(results) == 0:
        #     var.delete()
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
