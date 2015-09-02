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
#form .forms import MeasurementresultsForm
from datetime import datetime
import time
from django.db.models import Q

def PeopleAndOrgs(request):
    #return HttpResponse("odm2testsite says hello world!")
    return TemplateResponse(request, 'PeopleAndOrgs.html', {})

def AddSensor(request):
    #return HttpResponse("odm2testsite says hello world!")
    return TemplateResponse(request, 'AddSensor.html', {})

def temp_pivot_chart_view(request):
    #Step 1: Create a PivotDataPool with the data we want to retrieve.
    tempdata = DataPool(
       series=
        [{'options': {
            'source': Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))
                        .filter(resultid=5).order_by('-valuedatetime')[:4000]},
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
               'text': 'Sonadora Water Temperature'},
           'xAxis': {
                'title': {
                   'text': 'Date'}},
            'yAxis': {
                'title': {
                   'text': 'Temperature Degrees F'}}},
            x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%m-%d-%Y-%H:%M"), False))

    return render_to_response('chart.html',{'temppivchart': temppivcht})
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


