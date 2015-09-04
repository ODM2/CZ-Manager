from django.http import HttpResponse
from django.template.response import TemplateResponse
from chartit import DataPool, Chart
from .models import Measurementresultvalues
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
from datetime import datetime
import time
from django.db.models import Q
from django.views.generic import ListView
import csv
import io
import binascii
import unicodedata
from io import TextIOWrapper
from odm2testsite.settings import MEDIA_ROOT
from django.core.exceptions import ValidationError
from daterange_filter.filter import DateRangeFilter
from django import template

register = template.Library()

def PeopleAndOrgs(request):
    #return HttpResponse("odm2testsite says hello world!")
    return TemplateResponse(request, 'PeopleAndOrgs.html', {})

def AddSensor(request):
    #return HttpResponse("odm2testsite says hello world!")

    return TemplateResponse(request, 'AddSensor.html', {})
#
# def ImportData(request, pk):
#     #YOUR_OBJECT.objects.filter(pk=pk).update(views=F('views')+1)
#     raise ValidationError('encountered a problem  ')
#     return HttpResponseRedirect(request.META["HTTP_REFERER"])
#
# def request_page(request):
#     if(request.GET.get('mybtn')):
#         print("something")
#     #mypythoncode.mypythonfunction( int(request.GET.get('mytextbox')) )
#         #raise ValidationError('encountered a problem  ')
#     return render_to_response('/admin/odm2testapp/dataloggerfiles/change_list.html')

# def ImportData(self,request):
#     #request.GET.get('q', '')
#     f = self.Dataloggerfiles
#     #raise ValidationError('encountered a problem  ')
#     try:
#         with io.open(MEDIA_ROOT + '/dataloggerfiles/' + f.dataloggerfilename +'.csv', 'rt', encoding='ascii') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 #raise ValidationError(row) #print the current row
#                 print("hi")
#                 #dateT = time.strptime(row[0],"%m/%d/%Y %H:%M")#'1/1/2013 0:10
#                 #datestr = time.strftime("%Y-%m-%d %H:%M",dateT)
#                 #Measurementresultvalues(resultid=id,datavalue=row[1],valuedatetime=datestr,valuedatetimeutcoffset=4).save()
#     except IndexError:
#         raise ValidationError('encountered a problem with row '+row)
#
#     return HttpResponseRedirect(request.META["HTTP_REFERER"])
#     #return HttpResponse('<h1>'+ f.dataloggerfilename +' was found</h1>')

def resultDDList(request):
    #resultList = Results.objects.all()
    if request.method == "POST":
        resultList = Results.objects.all(request.POST)

        if resultList.is_valid():
            selection = resultList.cleaned_data['selection']
            request.session["selection"] = request.POST['selection']
            request.session["startDate"] = request.POST['startDate']
            request.session["endDate"] = request.POST['endDate']
            return HttpResponseRedirect('chart.html','selection', 'startDate','endDate',)
    else:
        ResultsForm = Results.objects.all()

    return render(request, 'resultList.html', {'resultList': resultList,}) # 'ResultsForm':ResultsForm
     #return TemplateResponse(request,'resultList.html',{ 'resultList': resultList,},)



def Measurementresultvalues_for_Results(Results):
    resultValues = Measurementresultvalues.objects.filter(Measurementresultvalues__resultid=Results.resultid)
    return {'resultValues': resultValues}

register.inclusion_tag('resultList.html')(Measurementresultvalues_for_Results)
register.inclusion_tag('chart.html')(Measurementresultvalues_for_Results)

def temp_pivot_chart_view(request):

    if 'selection' in request.POST:
        selected_resultid = request.POST['selection']
    else:
        selected_resultid = 5
    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
    else:
        entered_start_date = "2015-06-21"
    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        entered_end_date = "2015-08-21"

    if entered_end_date =='':
        entered_end_date = "2015-08-21"
    if entered_start_date=='':
        entered_start_date = "2015-06-21"
    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    # host_data = HostData.objects.filter( managers__in=managers )
    #get the name of the sampling feature for the graph title
    selected_result = Results.objects.filter(resultid=selected_resultid)
    title_feature_action = Featureactions.objects.filter(featureactionid=selected_result.values('feature_action'))
    title_sampling_feature = Samplingfeatures.objects.filter(samplingfeatureid=title_feature_action.values('sampling_feature'))
    s = str(title_sampling_feature.values_list('samplingfeaturename',flat=True))
    name_of_sampling_feature= s.split('\'')[1]

    title_variables = Variables.objects.filter(variableid=selected_result.values('variable'))
    s = str(title_variables.values_list('variable_name',flat=True))
    name_of_variable= s.split('\'')[1]

    #unitsid
    title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
    s = str(title_units.values_list('unitsname',flat=True))
    name_of_units= s.split('\'')[1]

    resultList = Results.objects.all()
    tempdata = DataPool(
       series=
        [{'options': {
            'source': Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))
                        .filter(valuedatetime__gt= entered_start_date)
                        .filter(valuedatetime__lt = entered_end_date)
                        .filter(resultid=selected_resultid).order_by('-valuedatetime')[:8000]},
          'terms': [
              ('valuedatetime',  lambda d: time.mktime(d.timetuple())),
            'datavalue']}
         ])

    temppivcht = Chart(
        datasource = tempdata,
        series_options =
          [{'options':{
              'type': 'line',
              'stacking': False},
            'terms':{
              'valuedatetime': [
                'datavalue']
              }}],
        chart_options =
          {'title': {
               'text': ''+name_of_sampling_feature  + ', ' +name_of_variable+''},
           'xAxis': {
                'title': {
                   'text': 'Date'}},
            'yAxis': {
                'title': {
                   'text': '' + name_of_units}}},
            x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%m-%d-%Y-%H:%M"), False))

    return TemplateResponse(request,'chart.html',{'temppivchart': temppivcht, 'resultList': resultList,},)
    #
    # temppivotdata = \
    #     PivotDataPool(
    #        series =
    #         [{'options': {
    #            'source': Measurementresultvalues.objects.all(),
    #            'categories': ['resultid']},
    #           'terms': [
    #             'valuedatetime',
    #             'datavalue'
    #
    #             ]}
    #          ])
    #
    # #Step 2: Create the PivotChart object
    # temppivcht = \
    #     PivotChart(
    #         datasource = temppivotdata,
    #         series_options =
    #           [{'options':{
    #               'type': 'line',
    #               'stacking': False},
    #             'terms':{
    #           'valuedatetime': [
    #             'datavalue']
    #           }}],
    #         chart_options =
    #           {'title': {
    #                'text': 'Temperature'},
    #            'xAxis': {
    #                 'title': {
    #                    'text': 'date time'}}})


