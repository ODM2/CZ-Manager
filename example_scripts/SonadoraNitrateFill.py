import os
import csv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.development")
application = get_wsgi_application()
from django.db.models import Q
import re
import datetime as dt
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime as dt
from datetime import timedelta
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max
import time as time

f = open('nitratefillshort.csv','r')

#for a set of time series, fill in missing data from a CSV file.

fa = Featureactions.objects.filter(featureactionid=1699).get()
NO3uMresult = Timeseriesresults.objects.get(resultid=16524)
NO3NO3mgLresult = Timeseriesresults.objects.get(resultid=16525)
Abs254nmresult = Timeseriesresults.objects.get(resultid=16543)
Abs350nmresult = Timeseriesresults.objects.get(resultid=16544)
censorcode = CvCensorcode.objects.filter(name="Not censored").get()
qualitycodegood = CvQualitycode.objects.filter(name="Good").get()
reader = csv.reader(f)
lastrow=None
i=0
insertRecord = False
for row in reader:
    i+=1
    if insertRecord:
        tsrNO3uM = Timeseriesresultvalues(resultid=NO3uMresult,
                                          datavalue=float(row[2]),
                                          valuedatetime=curdt,
                                          valuedatetimeutcoffset=4,
                                          censorcodecv=censorcode,
                                          qualitycodecv=qualitycodegood,
                                          timeaggregationinterval=NO3uMresult.intendedtimespacing,
                                          timeaggregationintervalunitsid=NO3uMresult.intendedtimespacingunitsid
                                          )
        print(tsrNO3uM)
        tsrNO3uM.save()
        tsrNO3mgL = Timeseriesresultvalues(resultid=NO3NO3mgLresult,
                                           datavalue=float(row[3]),
                                           valuedatetime=curdt,
                                           valuedatetimeutcoffset=4,
                                           censorcodecv=censorcode,
                                           qualitycodecv=qualitycodegood,
                                           timeaggregationinterval=NO3NO3mgLresult.intendedtimespacing,
                                           timeaggregationintervalunitsid=NO3NO3mgLresult.intendedtimespacingunitsid
                                           )
        print(tsrNO3mgL)
        tsrNO3mgL.save()
        tsrAbs254nm = Timeseriesresultvalues(resultid=Abs254nmresult,
                                             datavalue=float(row[4]),
                                             valuedatetime=curdt,
                                             valuedatetimeutcoffset=4,
                                             censorcodecv=censorcode,
                                             qualitycodecv=qualitycodegood,
                                             timeaggregationinterval=Abs254nmresult.intendedtimespacing,
                                             timeaggregationintervalunitsid=Abs254nmresult.intendedtimespacingunitsid
                                             )
        print(tsrAbs254nm)
        tsrAbs254nm.save()
        tsrAbs350nm = Timeseriesresultvalues(resultid=Abs350nmresult,
                                             datavalue=float(row[5]),
                                             valuedatetime=curdt,
                                             valuedatetimeutcoffset=4,
                                             censorcodecv=censorcode,
                                             qualitycodecv=qualitycodegood,
                                             timeaggregationinterval=Abs350nmresult.intendedtimespacing,
                                             timeaggregationintervalunitsid=Abs350nmresult.intendedtimespacingunitsid
                                             )
        print(tsrAbs350nm)
        tsrAbs350nm.save()
    if i > 17:
        if lastrow:
            #print(row)
            try:
                # if the difference in time between the current row
                # and the last row are at least 10 minutes insert the
                # next record.
                curdt = dt.strptime(row[1], '%m/%d/%y %H:%M:%S')
                lastdt = dt.strptime(lastrow[1], '%m/%d/%y %H:%M:%S')
                # diff = (curdt - lastdt).days  * 24 * 60
                curdt_ts = time.mktime(curdt.timetuple())
                lastdt_ts = time.mktime(lastdt.timetuple())
                diff = (curdt_ts - lastdt_ts) /60
                if diff >10:
                    insertRecord = True
                else:
                    insertRecord = False
            except ValueError:
                print(row)
        lastrow = row
