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


filepath = r'./eelgrasssitenamest2only.csv'
log = r'./eelgrass.log'
sft = CvSamplingfeaturetype.objects.get(name='Transect')
print(sft)
sfgt = CvSamplingfeaturegeotype.objects.get(name='Point')

sts = CvSitetype.objects.all()
for st in sts:
    print(st)
st = CvSitetype.objects.get(name='Estuary')
stc = CvSitetype.objects.get(name='Coastal')
spatref = Spatialreferences.objects.get(spatialreferenceid=1)
# Time series coverage
rt = CvResulttype.objects.get(name='Time series coverage')
plevel = Processinglevels.objects.get(processinglevelid=1)
aggstat = CvAggregationstatistic.objects.get(name='Continuous')
sm = CvMedium.objects.get(name='Liquid aqueous')
# variables
# Biomass-Eelgrass=2171
# eelgrass cover=2172
# canopy height = 2173
# shoot density = 2174
# biomass above ground =2175
# biomass below ground =2176
biomass = Variables.objects.get(variableid=2171)
coverage = Variables.objects.get(variableid=2172)
canopyheight = Variables.objects.get(variableid=2173)
shootdensity= Variables.objects.get(variableid=2174)
agBiomass= Variables.objects.get(variableid=2175)
bgBiomass= Variables.objects.get(variableid=2176)
t2a = Actions.objects.get(actionid=76328)
t3a = Actions.objects.get(actionid=76329)
# units

percent = Units.objects.get(unitsid=5)
cm = Units.objects.get(unitsid=29)
gm2 = Units.objects.get(unitsid=76) # 76
plantsm2 = Units.objects.get(unitsid=77)
newsfids = []
newrids = []
with open(log, "a") as logout:
    with open(filepath, 'r')as tempfile:
        reader = csv.reader(tempfile)
        i = 0
        for row in reader:
            i+=1
            if i >1:
                # print(row)
                desc = row[2] + ' ' + row[3] + ' Transect: ' + row[4]
                if len(row[5]) >0:
                    desc = desc + ' Quadrat: ' + row[5]
                desc = desc + ' site code: ' + row[6] + ' Location: ' + row[1]+' - ' + row[0]
                fg = 'Point(' + row[9] + ' ' + row[8] + ')'
                print(desc)
                print(fg)

                newsf = Samplingfeatures(sampling_feature_type=sft,
                                         samplingfeaturecode=row[6],
                                         samplingfeaturename=row[3] + " - " + row[1],
                                         samplingfeaturedescription=desc,
                                         sampling_feature_geo_type=sfgt,
                                         featuregeometry=fg)
                newsf.save()
                print(newsf)
                logout.writelines('new sampling feature: ' + str(newsf) + ' \r\n')
                logout.writelines('new sampling feature ID: ' + str(newsf.samplingfeatureid) + ' \r\n')
                newsfids.append(newsf.samplingfeatureid)
                if row[1] in ('Fort Foster','Portsmouth Harbor') :
                    newSite = Sites(samplingfeatureid=newsf, sitetypecv=stc, latitude=float(row[8]),
                                    longitude=float(row[9]), spatialreferenceid=spatref)
                else:
                    newSite = Sites(samplingfeatureid=newsf, sitetypecv=st, latitude=float(row[8]),
                                    longitude=float(row[9]), spatialreferenceid=spatref)
                newSite.save()
                print(newSite)
                logout.writelines('new site: ' + str(newSite) + ' \r\n')

                # add feature actions

                # action Eelgrass survey Tier 2== 76328
                # action Eelgrass survey Tier 3 Seagrass net=76329
                if row[0] == 'tier 2':
                    newfa = Featureactions(samplingfeatureid=newsf, action=t2a)
                else:
                    newfa = Featureactions(samplingfeatureid=newsf, action=t3a)
                newfa.save()
                print(newfa)
                logout.writelines('new feature action: ' + str(newfa) + ' \r\n')
                logout.writelines('new feature action ID: ' + str(newfa.featureactionid) + ' \r\n')
                # create result
                # variables

                newrbm = Results(featureactionid=newfa, result_type=rt,
                               variableid=biomass, unitsid=gm2,processing_level=plevel,
                               resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                               sampledmediumcv=sm, valuecount=1)
                newrbm.save()
                logout.writelines('new result: ' + str(newrbm) + ' \r\n')
                logout.writelines('new result ID: ' + str(newrbm.resultid) + ' \r\n')
                newrids.append(newrbm.resultid)
                tsrbm = Timeseriesresults(resultid=newrbm, aggregationstatisticcv=aggstat)
                tsrbm.save()

                if row[0] == 'tier 2':
                    newrcp = Results(featureactionid=newfa, result_type=rt,
                                   variableid=coverage, unitsid=percent, processing_level=plevel,
                                   resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                                   sampledmediumcv=sm, valuecount=1)
                    newrcp.save()
                    logout.writelines('new result: ' + str(newrcp) + ' \r\n')
                    logout.writelines('new result ID: ' + str(newrcp.resultid) + ' \r\n')
                    newrids.append(newrcp.resultid)
                    tsrcp = Timeseriesresults(resultid=newrcp, aggregationstatisticcv=aggstat)
                    tsrcp.save()


                    newrch = Results(featureactionid=newfa, result_type=rt,
                                   variableid=canopyheight, unitsid=cm, processing_level=plevel,
                                   resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                                   sampledmediumcv=sm, valuecount=1)
                    newrch.save()
                    logout.writelines('new result: ' + str(newrch) + ' \r\n')
                    logout.writelines('new result ID: ' + str(newrch.resultid) + ' \r\n')
                    newrids.append(newrch.resultid)
                    tsrch = Timeseriesresults(resultid=newrch, aggregationstatisticcv=aggstat)
                    tsrch.save()



                    newrsd = Results(featureactionid=newfa, result_type=rt,
                                   variableid=shootdensity, unitsid=plantsm2, processing_level=plevel,
                                   resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                                   sampledmediumcv=sm, valuecount=1)
                    newrsd.save()
                    logout.writelines('new result: ' + str(newrsd) + ' \r\n')
                    logout.writelines('new result ID: ' + str(newrsd.resultid) + ' \r\n')
                    newrids.append(newrsd.resultid)
                    tsrsd = Timeseriesresults(resultid=newrsd, aggregationstatisticcv=aggstat)
                    tsrsd.save()



                    newragb = Results(featureactionid=newfa, result_type=rt,
                                   variableid=agBiomass, unitsid=gm2, processing_level=plevel,
                                   resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                                   sampledmediumcv=sm, valuecount=1)
                    newragb.save()
                    newrids.append(newragb.resultid)
                    logout.writelines('new result: ' + str(newragb) + ' \r\n')
                    logout.writelines('new result ID: ' + str(newragb.resultid) + ' \r\n')

                    tsragb = Timeseriesresults(resultid=newragb, aggregationstatisticcv=aggstat)
                    tsragb.save()



                    newrbgb = Results(featureactionid=newfa, result_type=rt,
                                   variableid=bgBiomass, unitsid=gm2, processing_level=plevel,
                                   resultdatetimeutcoffset=-5, validdatetimeutcoffset=-5,
                                   sampledmediumcv=sm, valuecount=1)
                    newrbgb.save()
                    newrids.append(newrbgb.resultid)
                    logout.writelines('new result: ' + str(newrbgb) + ' \r\n')
                    logout.writelines('new result ID: ' + str(newrbgb.resultid) + ' \r\n')

                    tsrbgb = Timeseriesresults(resultid=newrbgb, aggregationstatisticcv=aggstat)
                    tsrbgb.save()



print("new sfids:")
print(newsfids)
print("new rids:")
print(newrids)