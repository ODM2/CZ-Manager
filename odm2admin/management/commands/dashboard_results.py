import argparse
import os
import time
__author__ = 'leonmi'

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import settings
from django.core.management.base import BaseCommand, CommandError
from odm2admin.models import Extensionproperties
from odm2admin.models import Featureactions
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Results
from odm2admin.models import Timeseriesresults
from odm2admin.models import Timeseriesresultvalues
from odm2admin.models import Resultsdataquality
from odm2admin.models import Dataquality
from datetime import datetime
from datetime import timedelta
from time import mktime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

parser = argparse.ArgumentParser(description='update dashboard result extension properties.')


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('dataloggerfilelink', nargs=1, type=str)
    #     parser.add_argument('dataloggerfileid', nargs=1, type=str)
    #     parser.add_argument('databeginson', nargs=1, type=str)
    #     parser.add_argument('columnheaderson', nargs=1, type=str)
    #     parser.add_argument('check_dates', nargs=1, type=bool)
    #     parser.add_argument('cmdline', nargs=1, type=bool)
    #     parser.add_argument('reversed', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):  # (f,fileid, databeginson,columnheaderson, cmd):
        ids = settings.SENSOR_DASHBOARD['featureactionids']
        timeseriesdays = settings.SENSOR_DASHBOARD['time_series_days']
        fas = Featureactions.objects.filter(featureactionid__in=ids).order_by('samplingfeatureid')
        # samplingfeatures = Samplingfeatures.filter(samplingfeatureid__in=fas)
        results = Results.objects.filter(featureactionid__in=fas)
        tsrs = Timeseriesresults.objects.filter(resultid__in=results)
        rexpvs = Resultextensionpropertyvalues.objects.filter()
        endDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date") #
        dashboardStartDateProperty = Extensionproperties.objects.get(propertyname__icontains="dashboard begin date")
        dashboardcountep = Extensionproperties.objects.get(propertyname__icontains="dashboard count")
        dashboardmaxcountep = Extensionproperties.objects.get(propertyname__icontains="dashboard maximum count")
        #dashboard sensor active
        dashboardsensoractivepid = Extensionproperties.objects.get(propertyname__icontains="dashboard sensor active")
        dashboardlastrecordedvaluepid = Extensionproperties.objects.get(propertyname__icontains="dashboard last recorded value")
        dashboardlowerboundcountep = Extensionproperties.objects.get(
            propertyname__icontains="dashboard below lower bound count")
        dashboardupperboundcountep = Extensionproperties.objects.get(
            propertyname__icontains="dashboard above upper bound count")
        for tsr in tsrs:
            # print(tsr)
            recordedenddate = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                propertyid=endDateProperty)
            end_date = recordedenddate.propertyvalue
            if len(end_date) == 16:
                enddt = time.strptime(end_date, "%Y-%m-%d %H:%M")
            elif len(end_date) == 19:
                enddt = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            else:
                enddt = time.strptime(end_date, "%Y-%m-%d %H:%M:%S.%f")
            dt = datetime.fromtimestamp(mktime(enddt))
            dashboard_start_date = dt - timedelta(days=timeseriesdays)
            tmp_start_date = dashboard_start_date.strftime('%Y-%m-%d %H:%M')
            try:
                dashboardstartproperty=Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                    propertyid=dashboardStartDateProperty)
                dashboardstartproperty.propertyvalue = tmp_start_date
                dashboardstartproperty.save()
                # print(dashboardstartproperty)
            except ObjectDoesNotExist:
                dashboardstartproperty = Resultextensionpropertyvalues(resultid=tsr.resultid, propertyid=dashboardStartDateProperty,
                                                          propertyvalue=tmp_start_date)
                dashboardstartproperty.save()
                # print('new dashboard begin date')
                # print(dashboardstartproperty)
            timeseriesresultvalues = Timeseriesresultvalues.objects.filter(
                resultid=tsr.resultid.resultid).exclude(datavalue=float('NaN')).filter(valuedatetime__gt=dashboard_start_date).order_by(
                'valuedatetime')
            lastvalue = Timeseriesresultvalues.objects.filter(
                resultid=tsr.resultid.resultid).filter(valuedatetime__gt=dashboard_start_date).order_by(
                'valuedatetime').reverse()[0]
            try:
                dashboardlastrecordedvalue = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                    propertyid=dashboardlastrecordedvaluepid)
                dashboardlastrecordedvalue.propertyvalue = str(lastvalue.datavalue) + " " \
                                                           + str(lastvalue.resultid.resultid.unitsid.unitsname)
                dashboardlastrecordedvalue.save()
            except ObjectDoesNotExist:
                dashboardlastrecordedvalue = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                      propertyid=dashboardlastrecordedvaluepid,
                                                                      propertyvalue=str(lastvalue.datavalue) + " "
                                                                        + str(lastvalue.resultid.resultid.unitsid))
                dashboardlastrecordedvalue.save()
            if lastvalue.datavalue == float('NaN'):
                try:
                    dashboardsensoractive = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                        propertyid=dashboardsensoractivepid)
                    dashboardsensoractive.propertyvalue = 0
                    dashboardsensoractive.save()
                except ObjectDoesNotExist:
                    dashboardsensoractive = Resultextensionpropertyvalues(resultid=tsr.resultid, propertyid=dashboardsensoractivepid,
                                                              propertyvalue=0)
                    dashboardsensoractive.save()
            else:
                try:
                    dashboardsensoractive = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                        propertyid=dashboardsensoractivepid)
                    dashboardsensoractive.propertyvalue = 1
                    dashboardsensoractive.save()
                except ObjectDoesNotExist:
                    dashboardsensoractive = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                          propertyid=dashboardsensoractivepid,
                                                                          propertyvalue=1)
                    dashboardsensoractive.save()
            rdqs = Resultsdataquality.objects.filter(resultid=tsr.resultid)
            rdqcount = rdqs.count()
            upperbound = None
            lowerbound = None
            if rdqcount>0:
                for rdq in rdqs:
                    if rdq.dataqualityid.dataqualitytypecv == 'Physical limit upper bound':
                        upperbound = rdq
                        # print(upperbound)
                    if rdq.dataqualityid.dataqualitytypecv == 'Physical limit lower bound':
                        lowerbound = rdq
                        # print(lowerbound)
            # print(tsr.intendedtimespacing)
            # print(tsr.intendedtimespacingunitsid)
            tsrvcount = timeseriesresultvalues.count()
            maxcount = 0
            if "Minute" in str(tsr.intendedtimespacingunitsid) or "minute" in str(tsr.intendedtimespacingunitsid):
                #1440
                spacesperday = 1440.0/tsr.intendedtimespacing
                maxcount = spacesperday *timeseriesdays
            elif "Hour" in str(tsr.intendedtimespacingunitsid) or "hour" in str(tsr.intendedtimespacingunitsid):
                spacesperday = 24.0/tsr.intendedtimespacing
                maxcount = spacesperday *timeseriesdays

            elif "Day" in str(tsr.intendedtimespacingunitsid) or "day" in str(tsr.intendedtimespacingunitsid) \
                    or "Days" in str(tsr.intendedtimespacingunitsid) or "days" in str(tsr.intendedtimespacingunitsid):
                spacesperday = tsr.intendedtimespacing
                maxcount = spacesperday * timeseriesdays
            try:
                dashboardcountrepv = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                    propertyid=dashboardcountep)
                dashboardcountrepv.propertyvalue = tsrvcount
                dashboardcountrepv.save()
                #print(dashboardcountrepv)
            except ObjectDoesNotExist:
                dashboardcountrepv = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                       propertyid=dashboardcountep,
                                                                       propertyvalue=tsrvcount)
                dashboardcountrepv.save()
                # print('new dashboard count')
                # print(dashboardcountrepv)


            try:
                dashboardmaxcountrepv = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                    propertyid=dashboardmaxcountep)
                # print(maxcount)
                dashboardmaxcountrepv.propertyvalue = maxcount
                dashboardmaxcountrepv.save()
                # print(dashboardmaxcountrepv)
            except ObjectDoesNotExist:
                dashboardmaxcountrepv = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                       propertyid=dashboardmaxcountep,
                                                                       propertyvalue=maxcount)
                dashboardmaxcountrepv.save()
                # print('new max dashboard count')
                # print(dashboardmaxcountrepv)
            lowcount = 0
            highcount = 0
            for tsrv in timeseriesresultvalues:
                if lowerbound and upperbound:
                    if tsrv.datavalue < float(lowerbound.dataqualityid.dataqualityvalue):
                        lowcount +=1
                    if tsrv.datavalue > float(upperbound.dataqualityid.dataqualityvalue):
                        highcount +=1
            # print(lowcount)
            # print(highcount)

            if lowerbound:
                try:
                    dashboardlowerboundcountrepv = Resultextensionpropertyvalues.objects.filter(resultid=tsr.resultid).get(
                        propertyid=dashboardlowerboundcountep)
                    dashboardlowerboundcountrepv.propertyvalue = lowcount
                    dashboardlowerboundcountrepv.save()
                    # print(dashboardlowerboundcountrepv)
                except ObjectDoesNotExist:
                    dashboardlowerboundcountrepv = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                           propertyid=dashboardlowerboundcountep,
                                                                           propertyvalue=lowcount)
                    dashboardlowerboundcountrepv.save()
                    # print('new low bound dashboard count')
                    # print(dashboardlowerboundcountrepv)

            if upperbound:
                try:
                    dashboardupperboundcountrepv = Resultextensionpropertyvalues.objects.filter(
                        resultid=tsr.resultid).get(
                        propertyid=dashboardupperboundcountep)
                    dashboardupperboundcountrepv.propertyvalue = highcount
                    dashboardupperboundcountrepv.save()
                    # print(dashboardupperboundcountrepv)
                except ObjectDoesNotExist:
                    dashboardupperboundcountrepv = Resultextensionpropertyvalues(resultid=tsr.resultid,
                                                                                 propertyid=dashboardupperboundcountep,
                                                                                 propertyvalue=highcount)
                    dashboardupperboundcountrepv.save()
                    # print('new upper bound dashboard count')
                    # print(dashboardupperboundcountrepv)
            # calculated_result_properties[tsr.resultid.resultid] = [end_date, tmp_start_date]
