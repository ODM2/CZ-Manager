from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
#from odm2testapp.forms import VariablesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Measurementresultvalues
from .models import Dataloggerfiles
from .models import Dataloggerfilecolumns
from .models import Featureactions
from .models import Samplingfeatures
from .models import Variables
from .models import Units
from .models import Results
from .models import Actions
from datetime import datetime
import csv
import time
import datetime
from datetime import timedelta
from django.db.models import Q
from django.views.generic import ListView
import csv
import io
import binascii
import unicodedata
from io import TextIOWrapper
import cStringIO as StringIO
from odm2testsite.settings import MEDIA_ROOT
import itertools
from django.core.exceptions import ValidationError
from daterange_filter.filter import DateRangeFilter
from django import template
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic import View
from django.template import RequestContext
from forms import DataloggerfilesAdmin
from forms import DataloggerfilesAdminForm
from odm2testsite.settings import CUSTOM_TEMPLATE_PATH
register = template.Library()
import admin


def AddSensor(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'AddSensor.html', context)
    else:
        return HttpResponseRedirect('../')


def AddProfile(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'AddProfile.html', context)
    else:
        return HttpResponseRedirect('../')

def RecordAction(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'RecordAction.html', context)
    else:
        return HttpResponseRedirect('../')


def ManageCitations(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'ManageCitations.html', context)
    else:
        return HttpResponseRedirect('../')
# #
# def dataloggerfilesView(request, id):
#      #model = Dataloggerfiles
#      #template_name = 'admin/odm2testapp/dataloggerfiles/change_form.html'#'DataloggerfilecolumnsDisplay.html'
#      DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.filter(dataloggerfileid=id)
#      DataloggerfilecolumnsListvalues =  str(DataloggerfilecolumnsList.values())
#      #raise ValidationError(DataloggerfilecolumnsListvalues)
#      DataloggerfilecolumnsListvalues= DataloggerfilecolumnsList#DataloggerfilecolumnsListvalues.split('\'')
#      #request.session["DataloggerfilecolumnsList"] =DataloggerfilecolumnsListvalues
#      #fieldsets = Dataloggerfiles.objects.filter(dataloggerfileid=id)
#      adm = DataloggerfilesAdmin(Dataloggerfiles,admin) #.change_form_template
#      admform = DataloggerfilesAdminForm(request.POST)
#      #data =request.POST
#      data = {
#           'opts': Dataloggerfiles._meta,
#           'adminform': admform.formset,
#           'change': True,
#           'is_popup': False,
#           'to_field' : True,
#           'save_as': False,
#           #'prepopulated_fields' : adm.get_prepopulated_fields(request),
#           'has_delete_permission': True,
#           'has_add_permission': True,
#           'has_change_permission': True,
#           'DataloggerfilecolumnsList' : DataloggerfilecolumnsListvalues,}
# #
# # #DataloggerfilecolumnsDisplay.html
#      return render_to_response('admin/odm2testapp/dataloggerfiles/change_form.html', data, context_instance=RequestContext(request)) # DataloggerfilecolumnsDisplay.html

    # def get_context_data(self, **kwargs):
    #     context = super(dataloggercolumnView, self).get_context_data(**kwargs)
    #
    #     data = {'test': 'test',
    #     'opts': Dataloggerfiles._meta,
    #     'change': True,
    #     'is_popup': False,
    #     'save_as': False,
    #     'has_delete_permission': False,
    #     'has_add_permission': False,
    #     'has_change_permission': False}
    #     context['data'] = data
    #     context['DataloggerfilecolumnsList'] = Dataloggerfilecolumns.objects.all()
    #     return context
#register.inclusion_tag('DataloggerfilecolumnsDisplay.html')(dataloggercolumnView)

def get_name_of_sampling_feature(selected_result):

     title_feature_action = Featureactions.objects.filter(featureactionid=selected_result.values('feature_action'))
     title_sampling_feature = Samplingfeatures.objects.filter(samplingfeatureid=title_feature_action.values('sampling_feature'))
     s = str(title_sampling_feature.values_list('samplingfeaturename',flat=True))
     name_of_sampling_feature= s.split('\'')[1]
     return name_of_sampling_feature

def get_name_of_variable(selected_result):
     title_variables = Variables.objects.filter(variableid=selected_result.values('variable'))
     s = str(title_variables.values_list('variable_name',flat=True))
     name_of_variable= s.split('\'')[1]
     return name_of_variable

def get_name_of_units(selected_result):
     title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
     s = str(title_units.values_list('unitsname',flat=True))
     name_of_units= s.split('\'')[1]
     return name_of_units

def dumptoMillis(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple())*1000
    )
    return millis

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]


def temp_pivot_chart_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('../')
    entered_start_date = ''
    entered_end_date = ''
    selected_resultid = 15
    selected_featureactionid = 5



    if 'SelectedFeatureAction' in request.POST:
        if not request.POST['SelectedFeatureAction'] == 'All':
            selected_featureactionid= int(request.POST['SelectedFeatureAction'])
            resultList = Results.objects.filter(feature_action=selected_featureactionid)
            if 'update_result_list' in request.POST:
                selected_resultid= resultList[0].resultid
        else:
            selected_featureactionid= request.POST['SelectedFeatureAction']
            resultList = Results.objects.filter(result_type="Temporal observation")
    else:
        resultList = Results.objects.filter(feature_action=selected_featureactionid)

    #find the measurement results series that where selected.
    numresults = resultList.count()
    selectedMResultSeries = []
    selectionStr = ''
    for i in range(0,numresults):
        selectionStr = str('selection' + str(i))
        if selectionStr in request.POST:
            #raise ValidationError(request.POST[selectionStr])
            for result in resultList:
                if int(request.POST[selectionStr]) == result.resultid:
                    selectedMResultSeries.append(int(request.POST[selectionStr]))
    #if 'selection0' in request.POST:
        #raise ValidationError(request.POST['selection0'] + ' '+ request.POST['selection1'])
        #selected_resultid = request.POST['selection0']
    #else:
        #selected_resultid = 15
    #if no series were selected (like on first load) set the series to some value.
    if len(resultList) > 0 and len(selectedMResultSeries)==0:
        selectedMResultSeries.append(int(resultList[0].resultid))
    elif len(resultList) == 0 and len(selectedMResultSeries)==0:
        selectedMResultSeries.append(15)


    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
    else:
        entered_start_date = "2015-07-20"
    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        entered_end_date = "2015-07-21"
    if entered_end_date =='':
        entered_end_date = "2015-07-21"
    if entered_start_date=='':
        entered_start_date = "2015-07-20"

    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []
    myresultSeries = []
    i = 0
    data = {}
    for selectedMResult in selectedMResultSeries:
        i +=1
        selected_result = Results.objects.filter(resultid=selectedMResult)
        selected_results.append(selected_result)
        name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))
        name_of_variables.append(get_name_of_variable(selected_result))
        name_of_units.append(get_name_of_units(selected_result))
        myresultSeries.append(Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
        .filter(valuedatetime__gt= entered_start_date)\
        .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid=selectedMResult).order_by('-valuedatetime')[:8000])
        data.update({'datavalue' + str(i): []})

    # [Date.UTC(1971, 5, 10), 0]
    #{'data': [[1437435900, 71.47], [1437435000, 71.47],
     # [{
     #        data: [
     #            [Date.UTC(1970, 9, 21), 0],
     #            [Date.UTC(1970, 10, 4), 0.28],
    i = 0

    for myresults in myresultSeries:
        i+=1
        for result in myresults:
            start = datetime.datetime(1970,1,1)
            delta = result.valuedatetime-start
            mills = delta.total_seconds()*1000
            data['datavalue' + str(i)].append([mills, result.datavalue]) #dumptoMillis(result.valuedatetime)
            #data['datavalue'].extend(tmplist )
            #data['valuedatetime'].append(dumptoMillis(result.valuedatetime))



    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    for name_of_unit,name_of_sampling_feature in zip(name_of_units,name_of_sampling_features) :
        i+=1
        if i==1:
            seriesStr +=name_of_unit
        else:
            seriesStr+=' - '+name_of_unit
        series.append({"name": name_of_unit+' - '+ name_of_sampling_feature, "data": data['datavalue'+str(i)]})
    i=0
    for name_of_sampling_feature,name_of_variable in zip(name_of_sampling_features,name_of_variables) :
        i+=1
        if i ==1:
            titleStr += name_of_sampling_feature  + ', ' +name_of_variable
        else:
            titleStr += ' -- '+name_of_sampling_feature  + ', ' +name_of_variable

    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'line', "height": 500,}
    title2 = {"text": titleStr}
    xAxis = {"type": 'datetime', "title": {"text": 'Date'},}
    yAxis = {"title": {"text": seriesStr}}
    # series = [
    #     {"name": seriesStr, "data": data['datavalue']},
    #     {"name": name_of_units2, "data": data['datavalue2']},
    #     ]

    actionList = Actions.objects.filter(action_type="Observation") #where the action is not of type estimation
    #assuming an estimate is a single value.
    featureactionList = Featureactions.objects.filter(action__in=actionList)

    int_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if request.REQUEST.get('export_data'):
        csvexport=True

        myfile = StringIO.StringIO()
        for myresults in myresultSeries:
            for result in myresults:
                myfile.write(result.csvoutput())
            myfile.write('\n')
        response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        return TemplateResponse(request,'chart.html',{ 'featureactionList': featureactionList, 'resultList': resultList,
            'startDate':entered_start_date,'endDate':entered_end_date, 'SelectedResults':int_selectedresultid_ids,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2, 'xAxis': xAxis, 'yAxis': yAxis,
            'SelectedFeatureAction':selected_featureactionid,},)

#
# def Measurementresultvalues_for_Results(Results):
#     resultValues = Measurementresultvalues.objects.filter(Measurementresultvalues__resultid=Results.resultid)
#     return {'resultValues': resultValues}
#
# register.inclusion_tag('resultList.html')(Measurementresultvalues_for_Results)
# register.inclusion_tag('chart.html')(Measurementresultvalues_for_Results)
#
# def createChart(tempdata,name_of_sampling_feature,name_of_variable,name_of_units
#     ,name_of_sampling_feature2=None,name_of_variable2=None,name_of_units2=None):
#
#      if name_of_sampling_feature2 is None:
#          titletext = ''+name_of_sampling_feature  + ', ' +name_of_variable
#      else:
#         titletext = ''+name_of_sampling_feature  + ', ' +name_of_variable+\
#                      ' -- '+name_of_sampling_feature2  + ', ' +name_of_variable2+''
#      if name_of_units2 is None:
#          yLabel = '' + name_of_units
#      else:
#          yLabel = '' + name_of_units + ' and ' + name_of_units2
#      if name_of_sampling_feature2 is None:
#           myChart = Chart(
#             datasource = tempdata,
#             series_options =
#               [{'options':{
#                   'type': 'line',
#                   'stacking': False},
#                 'terms':{
#                   'valuedatetime': [
#                     'datavalue'],
#
#                   }}],
#             chart_options =
#               {'title': {
#                    'text': titletext},
#                'xAxis': {
#                     'title': {
#                        'text': 'Date'}},
#                 'yAxis': {
#                     'title': {
#                        'text': yLabel}}},
#                 x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%m-%d-%Y-%H:%M"), False))
#      else:
#          myChart = Chart(
#             datasource = tempdata,
#             series_options =
#               [{'options':{
#                   'type': 'line',
#                   'stacking': False},
#                 'terms':{
#                   'valuedatetime': [
#                     'datavalue'],
#                 'valuedatetime': [
#                     'datavalue2'],
#                   }}],
#             chart_options =
#               {'title': {
#                    'text': titletext},
#                'xAxis': {
#                     'title': {
#                        'text': 'Date'}},
#                 'yAxis': {
#                     'title': {
#                        'text': yLabel}}},
#                 x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%m-%d-%Y-%H:%M"), False))
#      return myChart
#
# def createDataPool(myresults, myresults2=None):
#     if myresults2 is None:
#         tempdata = DataPool(
#            series=
#             [{'options': {
#                 'source':myresults},
#               'terms': [
#                   ('valuedatetime',  lambda d: time.mktime(d.timetuple())),
#                 'datavalue']}
#              ])
#
#     else:
#         tempdata = DataPool(
#            series=
#             [{'options': {
#                 'source':myresults},
#               'terms': [
#                   ('valuedatetime',  lambda d: time.mktime(d.timetuple())),
#                 'datavalue']},
#              {'options': {
#                 'source':myresults2},
#               'terms': [
#                   ('valuedatetime',  lambda d: time.mktime(d.timetuple())),
#                   {'datavalue2': 'datavalue'}]},
#              ])
#     return tempdata
# #{'valuedatetime' : ('valuedatetime',  lambda d: time.mktime(d.timetuple()))},
#                  # {'datavalue':'datavalue'}
# def get_name_of_sampling_feature(selected_result):
#
#     title_feature_action = Featureactions.objects.filter(featureactionid=selected_result.values('feature_action'))
#     title_sampling_feature = Samplingfeatures.objects.filter(samplingfeatureid=title_feature_action.values('sampling_feature'))
#     s = str(title_sampling_feature.values_list('samplingfeaturename',flat=True))
#     name_of_sampling_feature= s.split('\'')[1]
#     return name_of_sampling_feature
#
# def get_name_of_variable(selected_result):
#     title_variables = Variables.objects.filter(variableid=selected_result.values('variable'))
#     s = str(title_variables.values_list('variable_name',flat=True))
#     name_of_variable= s.split('\'')[1]
#     return name_of_variable
#
# def get_name_of_units(selected_result):
#     title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
#     s = str(title_units.values_list('unitsname',flat=True))
#     name_of_units= s.split('\'')[1]
#     return name_of_units
#
# def temp_pivot_chart_view(request):
#     entered_start_date = ''
#     entered_end_date = ''
#     selected_resultid = '5'
#     selected_resultid2 = '0'
#     selected_resultid3 = '0'
#     selected_resultid4 = '0'
#     if 'selection' in request.POST:
#         selected_resultid = request.POST['selection']
#     else:
#         selected_resultid = '5'
#     if 'selection2' in request.POST:
#         selected_resultid2 = request.POST['selection2']
#     else:
#         selected_resultid2 = '0'
#     if 'selection3' in request.POST:
#         selected_resultid3 = request.POST['selection3']
#     else:
#         selected_resultid3 = '0'
#     if 'selection4' in request.POST:
#         selected_resultid4 = request.POST['selection4']
#     else:
#         selected_resultid4 = '0'
#     if 'startDate' in request.POST:
#         entered_start_date = request.POST['startDate']
#     else:
#         entered_start_date = "2015-06-21"
#     if 'endDate' in request.POST:
#         entered_end_date = request.POST['endDate']
#     else:
#         entered_end_date = "2015-08-21"
#     if entered_end_date =='':
#         entered_end_date = "2015-08-21"
#     if entered_start_date=='':
#         entered_start_date = "2015-06-21"
#     resultList = Results.objects.all()
#
#
#     selected_result = Results.objects.filter(resultid=selected_resultid)
#
#     name_of_sampling_feature = get_name_of_sampling_feature(selected_result)
#     name_of_variable = get_name_of_variable(selected_result)
#     name_of_units = get_name_of_units(selected_result)
#     plt2 = False
#     plt3 = False
#     plt4= False
#     myMeasurementResults2= None
#     myMeasurementResults3=None
#     myMeasurementResults4=None
#     if not selected_resultid2 =='0':
#         plt2 = True
#         selected_result2 = Results.objects.filter(resultid=selected_resultid2)
#
#         name_of_sampling_feature2 = get_name_of_sampling_feature(selected_result2)
#         name_of_variable2 = get_name_of_variable(selected_result2)
#         name_of_units2 = get_name_of_units(selected_result2)
#
#         myMeasurementResults2 = Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
#         .filter(valuedatetime__gt= entered_start_date)\
#         .filter(valuedatetime__lt = entered_end_date)\
#                     .filter(resultid=selected_resultid2).order_by('-valuedatetime')[:8000]
#     if not selected_resultid3 =='0':
#         plt3 = True
#         selected_result3 = Results.objects.filter(resultid=selected_resultid3)
#
#         name_of_sampling_feature3 = get_name_of_sampling_feature(selected_result3)
#         name_of_variable3 = get_name_of_variable(selected_result3)
#         name_of_units3 = get_name_of_units(selected_result3)
#
#         myMeasurementResults3 = Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
#         .filter(valuedatetime__gt= entered_start_date)\
#         .filter(valuedatetime__lt = entered_end_date)\
#                     .filter(resultid=selected_resultid3).order_by('-valuedatetime')[:8000]
#     if not selected_resultid4 =='0':
#         plt4=True
#         selected_result4 = Results.objects.filter(resultid=selected_resultid4)
#
#         name_of_sampling_feature4 = get_name_of_sampling_feature(selected_result4)
#         name_of_variable4 = get_name_of_variable(selected_result4)
#         name_of_units4 = get_name_of_units(selected_result4)
#
#
#         myMeasurementResults4 = Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
#         .filter(valuedatetime__gt= entered_start_date)\
#         .filter(valuedatetime__lt = entered_end_date)\
#                     .filter(resultid=selected_resultid4).order_by('-valuedatetime')[:8000]
#     #unitsid
#
#     myMeasurementResults = Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
#         .filter(valuedatetime__gt= entered_start_date)\
#         .filter(valuedatetime__lt = entered_end_date)\
#                     .filter(resultid=selected_resultid).order_by('-valuedatetime')[:8000]
#
#     if not plt2 and not plt3 and not plt4:
#         tempdata = createDataPool(myMeasurementResults)
#         temppivcht = createChart(tempdata,name_of_sampling_feature,name_of_variable,name_of_units)
#     if plt2 and not plt3 and not plt4:
#         tempdata = createDataPool(myMeasurementResults,myMeasurementResults2)
#         temppivcht = createChart(tempdata,name_of_sampling_feature,name_of_variable,name_of_units,
#                                  name_of_sampling_feature2,name_of_variable2,name_of_units2)
#
#     csvexport = False
#     #if the user hit the export csv button export the measurement results to csv
#     if request.REQUEST.get('export_data'):
#         csvexport=True
#
#         myfile = StringIO.StringIO()
#         for mresults in myMeasurementResults:
#             myfile.write(mresults.csvoutput())
#         response = HttpResponse(myfile.getvalue(),content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+'-'+ name_of_variable +'.csv"'
#
#     #need to make sure selected result id is an int so it can be handled correctly in the template.
#     int_selectedresultid = int(selected_resultid)
#     int_selectedresultid2 = int(selected_resultid2)
#     int_selectedresultid3 = int(selected_resultid3)
#     int_selectedresultid4 = int(selected_resultid4)
#     if csvexport:
#         return response
#     else:
#         return TemplateResponse(request,'chart.html',{'temppivchart': temppivcht, 'resultList': resultList,
#             'startDate':entered_start_date,'endDate':entered_end_date, 'SelectedResult':int_selectedresultid,
#             'SelectedResult2':int_selectedresultid2,'SelectedResult3':int_selectedresultid3,
#             'SelectedResult4':int_selectedresultid4},)


