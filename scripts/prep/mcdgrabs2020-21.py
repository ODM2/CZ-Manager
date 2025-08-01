
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
censorcode = CvCensorcode.objects.filter(name="Not censored").get()
qualitycode = CvQualitycode.objects.filter(name="Good").get()
qualitycodebad = CvQualitycode.objects.filter(name="Bad").get()
newtimeunit = Units.objects.get(unitsname='minute')
annotationtypecv = CvAnnotationtype.objects.filter(
    name="Specimen annotation").get()
annotatorid = People.objects.filter(personid=1).get()
dontrun = True
with open('./to do/newgrabvars.csv') as varfile:
    with open('./to do/newgrabs.csv') as grabfile:
        vars = csv.reader(varfile)
        grabs = csv.reader((grabfile))
        i = 0
        varmap = {}
        unitmap = {}
        sfs = []
        fas = []
        for grab in grabs:
            foundsfss = False
            i += 1
            if i == 1:

                j = 0
                for var in vars:
                    j += 1
                    if j > 1:
                        k = 0
                        for colheader in grab:
                            if var[0] == colheader:
                                print(colheader + ': ' + var[2])
                                varmap[k] = var[2]
                                unitmap[k] = var[3]
                            k +=1
            elif not foundsfss:
                dup = False
                sfcode = grab[1]
                if 'DUP' in sfcode:
                    sfcode = sfcode.split(' ')[0]
                    dup = True
                print(sfcode)
                newsf = Samplingfeatures.objects.filter(samplingfeaturecode=sfcode).get()
                found = False
                for sf in sfs:
                    if sf == newsf.samplingfeatureid:
                        found = True
                if not found:
                    sfs.append(newsf.samplingfeatureid)
                if len(sfs) == 8:
                    foundsfss = True
                    fas = Featureactions.objects.filter(samplingfeatureid__in=sfs)
                    rs = Results.objects.filter(featureactionid__in=fas).filter(variableid__in=varmap.values())
                    rfas = None
                    lastrfas = None
                    newresults = []
                    for sf in sfs:
                        lastrfas = rfas
                        sffas = fas.filter(samplingfeatureid=sf)
                        rfas = rs.filter(featureactionid__in=sffas).order_by('variableid')
                        print(sf)
                        if sf == 99999 and not dontrun:
                            sffa = sffas.first()
                            print(sffa)
                            print(sffa.featureactionid)
                            curvar = None
                            lastvar = None
                            for r in lastrfas:
                                if not r.variableid.variableid ==1645:
                                    lastvar = curvar
                                    curvar = r.variableid.variableid
                                    if lastvar:
                                        if lastvar == curvar:
                                            continue
                                    print('here')
                                    rid = r.resultid
                                    tsr = Timeseriesresults.objects.filter(resultid=r.resultid).get()
                                    r.resultid = None
                                    r.featureactionid = sffa
                                    r.save()
                                    tsr.resultid = None
                                    tsr.resultid = r
                                    tsr.save()
                                    # tsr.save()
                                    print(r)
                                    newresults.append(r.resultid)
                        # for r in rfas:
                        #     print(r)
            if foundsfss:
                print('all sfs found after: ' + str(i))
            if i > 1 and not dontrun:
                dup = False
                sfcode = grab[1]
                if 'DUP' in sfcode:
                    sfcode = sfcode.split(' ')[0]
                    dup = True
                # print(sfcode)
                sf = Samplingfeatures.objects.filter(samplingfeaturecode=sfcode).get()
                k = 0
                for col in grab:
                    if k in varmap.keys():
                        varid = varmap[k]
                        uid = unitmap[k]
                        fas = Featureactions.objects.filter(samplingfeatureid=sf)
                        var = Variables.objects.filter(variableid=varid).get()
                        unit = Units.objects.filter(unitsid=uid).get()
                        print(fas)
                        print(varid)
                        print(uid)
                        # rs = Results.objects.filter(featureactionid__in=fas).filter(variableid=var)
                        # for r in rs:
                        #     print(r)
                        # Max('begindate')
                        r = Results.objects.filter(featureactionid__in=fas).filter(variableid=var).annotate(
                                Max('featureactionid__action__begindatetime')).filter(unitsid=uid
                                ).order_by('-featureactionid__action__begindatetime__max').first()
                        print(r)
                        tsr = Timeseriesresults.objects.get(resultid=r)
                        val = col
                        date = grab[2] + ' ' +  grab[3]
                        datet = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        print(r)
                        print(val)
                        print(datet)
                        if len(val) > 0:
                            tsrv=Timeseriesresultvalues(resultid=tsr, datavalue=val, valuedatetime=datet,
                                                          valuedatetimeutcoffset=-5, censorcodecv=censorcode,
                                                          qualitycodecv=qualitycode, timeaggregationinterval=1,
                                                          timeaggregationintervalunitsid=newtimeunit)
                            tsrv.save()
                            # example TTMP06191302 6/19/2013 10:01
                            # 2019-03-27
                            specimenid = str('TTMP' + grab[2][:4] + grab[2][5:7] + grab[2][8:])
                            print(specimenid)
                            annotationtext = 'sample ID (missing last 2 digits): ' + specimenid + str(grab[22] + ' ' + grab[23])
                            if dup:
                                annotationtext = ' sample marked as DUP - multiple samples taken this day. ' + annotationtext
                            annotation = Annotations(annotationtypecv=annotationtypecv,
                                                     annotationcode=annotationtext[0:50],
                                                     annotationtext=annotationtext,
                                                     annotationdatetime=datet,
                                                     annotationlink=specimenid,
                                                     annotationutcoffset=4,
                                                     annotatorid=annotatorid)
                            annotation.save()
                            tsrva = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                     annotationid=annotation)
                            tsrva.save()
                    k +=1


        # create timeseriesresultvalues and annotations and timeseriesresultvalueannotations
        print('new results')
        print(newresults)
        print(varmap)
        print(sfs)

# I forgot to set the values to pending QA. So I ran this SQL command afterwards:
# update odm2.timeseriesresultvalues
# set qualitycodecv = 'Pending QA'
# where valuedatetime > '2020-01-01' and resultid in(
#     select resultid from odm2.results where featureactionid in (
# select featureactionid from odm2.featureactions where samplingfeatureid in (1466, 1105, 2242, 1361, 2053, 1483, 1510, 1465)))
