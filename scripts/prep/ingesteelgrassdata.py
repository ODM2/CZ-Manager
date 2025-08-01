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
from datetime import datetime, timedelta
from django.contrib.auth.models import User


filepath = r'./eelgrassdataingest.csv'

#variables
# Biomass-Eelgrass=2171
# eelgrass cover=2172
# canopy height = 2173
# shoot density = 2174
# biomass above ground =2175
# biomass below ground =2176

# Method Eelgrass survey Tier 2=76311
# action Eelgrass survey Tier 2== 76328

# method Eelgrass survey Tier 3 Seagrass net=76312
# action Eelgrass survey Tier 3 Seagrass net=76329
censorcode = CvCensorcode.objects.filter(name="Not censored").get()
qualitycode = CvQualitycode.objects.filter(name="Good").get()
newtimeunit = Units.objects.get(unitsname='minute')

biomass = Variables.objects.get(variableid=2171)
coverage = Variables.objects.get(variableid=2172)
canopyheight = Variables.objects.get(variableid=2173)
shootdensity= Variables.objects.get(variableid=2174)
agBiomass= Variables.objects.get(variableid=2175)
bgBiomass= Variables.objects.get(variableid=2176)

with open(filepath, 'r')as tempfile:
    reader = csv.DictReader(tempfile)
    i = 0
    for row in reader:
        i+=1
        print(row)
        sf = Samplingfeatures.objects.filter(samplingfeaturecode=row['sitecode']).get()
        print(sf)
        fa = Featureactions.objects.filter(samplingfeatureid=sf).get()
        rs = Results.objects.filter(featureactionid=fa)
        for r in rs:
            tsr= Timeseriesresults.objects.filter(resultid=r).get()
            datet = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M')
            print(r)
            if r.variableid == biomass:
                print('biomass')
                val = row['Biomass_(g/m2)']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()
            elif r.variableid == coverage:
                print('coverage')
                val = row['Eelgrass_Cover_precent']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()
            elif r.variableid == canopyheight:
                print('Canopy_Height_cm')
                val = row['Canopy_Height_cm']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()
            elif r.variableid == shootdensity:
                print('Shoot_Density_plants/m2')
                val = row['Shoot_Density_plants/m2']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()
            elif r.variableid == agBiomass:
                print('Biomass_AboveGrnd')
                val = row['Biomass_AboveGrnd']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()
            elif r.variableid == bgBiomass:
                print('Biomass_BelowGrnd')
                val = row['Biomass_BelowGrnd']
                if len(val) == 0:
                    continue
                else:
                    val = float(val)
                tsrv = Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                              valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                              qualitycodecv=qualitycode, timeaggregationinterval=1,
                                              timeaggregationintervalunitsid=newtimeunit)
                tsrv.save()