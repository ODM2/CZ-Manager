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
import csv
import time
from django.db.models import Q
from django.views.generic import ListView
import csv
import io
import binascii
import unicodedata
from io import TextIOWrapper
import cStringIO as StringIO
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

def dataloggercolumnView(request):
    DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.all()
#DataloggerfilecolumnsDisplay.html
    return render(request, '.', {'DataloggerfilecolumnsList':DataloggerfilecolumnsList,}) #DataloggerfilecolumnsDisplay.html

#register.inclusion_tag('DataloggerfilecolumnsDisplay.html')(dataloggercolumnView)

def resultDDList(request):
    #resultList = Results.objects.all()
    startDate = ''
    endDate = ''
    selected_resultid=5
    if request.method == "POST":
        resultList = Results.objects.all(request.POST)

        if resultList.is_valid():
            selection = resultList.cleaned_data['selection']
            request.session["selection"] = request.POST['selection']
            request.session["startDate"] = request.POST['startDate']
            request.session["endDate"] = request.POST['endDate']
            startDate = request.POST['startDate']
            endDate = request.POST['endDate']
            selected_resultid= int(request.POST['SelectedResult'])

            return HttpResponseRedirect('chart.html','selection', 'startDate','endDate',)
    else:
        resultList = Results.objects.all()

    return render(request, 'resultList.html', {'resultList': resultList,'startDate':startDate,
                                               'endDate':endDate, 'SelectedResult':selected_resultid}) # 'ResultsForm':ResultsForm
     #return TemplateResponse(request,'resultList.html',{ 'resultList': resultList,},)


#
# def Measurementresultvalues_for_Results(Results):
#     resultValues = Measurementresultvalues.objects.filter(Measurementresultvalues__resultid=Results.resultid)
#     return {'resultValues': resultValues}
#
# register.inclusion_tag('resultList.html')(Measurementresultvalues_for_Results)
# register.inclusion_tag('chart.html')(Measurementresultvalues_for_Results)

def temp_pivot_chart_view(request):
    entered_start_date = ''
    entered_end_date = ''
    selected_resultid = 5
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
    #


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
    myresults = Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
        .filter(valuedatetime__gt= entered_start_date)\
        .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid=selected_resultid).order_by('-valuedatetime')[:8000]
    resultList = Results.objects.all()
    tempdata = DataPool(
       series=
        [{'options': {
            'source':myresults },
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

    int_selectedresultid = int(selected_resultid)
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if request.REQUEST.get('export_data'):
        csvexport=True

        myfile = StringIO.StringIO()
        for mresults in myresults:
            myfile.write(mresults.csvoutput())
        response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+'-'+ name_of_variable +'.csv"'
    if csvexport:
        return response
    else:
        return TemplateResponse(request,'chart.html',{'temppivchart': temppivcht, 'resultList': resultList,
            'startDate':entered_start_date,'endDate':entered_end_date, 'SelectedResult':int_selectedresultid,},)


