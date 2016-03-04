from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
#from odm2testapp.forms import VariablesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Measurementresultvalues
from .models import Profileresultvalues
from .models import Dataloggerfiles
from .models import Dataloggerfilecolumns
from .models import Featureactions
from .models import Samplingfeatures
from .models import Variables
from .models import Units
from .models import Results
from .models import Actions
from .models import Relatedfeatures
from .models import Profileresults
from .models import Citationextensionpropertyvalues
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
from templatesAndSettings.settings import MEDIA_ROOT
import itertools
from django.core.exceptions import ValidationError
from daterange_filter.filter import DateRangeFilter
from django import template
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic import View
from django.template import RequestContext
from .forms import DataloggerfilesAdmin
from .forms import DataloggerfilesAdminForm
import json
from templatesAndSettings.settings import CUSTOM_TEMPLATE_PATH
import re
register = template.Library()
from .models import Citations
from .models import Authorlists
from .models import Extensionproperties
from .forms import CitationsAdminForm
#
# class FeatureactionsAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         if not self.request.is_authenticated():
#             return Featureactions.objects.none()
#
#         qs = Featureactions.objects.all()
#
#         if self.q:
#             names = FeatureactionsNames.objects.filter(name__icontains=self.q)
#             qs = Featureactions.objects.filter(featureactionid=names.values("featureactionid"))
#             #qs = qs.filter(__istartswith=self.q)
#
#         return self.q
from django.views.generic.edit import CreateView

#class CreatePubView(CreateView):
    #template_name = "publications2.html"
    #model = Citations


def publications(request):
    if request.user.is_authenticated():
        citationList = Citations.objects.all()
        authList = Authorlists.objects.all()
        selectedTag = 'CZO Authors'
        if 'filterTags' in request.POST:
            if not request.POST['filterTags'] == 'All':
                selectedTag = request.POST['filterTags']
                if request.POST['filterTags'] == 'CZO Authors':
                    citationList =Citations.objects.filter(citationid__in=authList.values("citationid"))
                else:
                    citationList =Citations.objects.filter(publisher__icontains=selectedTag)
            else:
                selectedTag = 'All'
        else:
            citationList =Citations.objects.filter(citationid__in=authList.values("citationid"))
        filterTags=['CZO Authors','All','AGU', 'LCZO Meeting']

        citationCategories = Citationextensionpropertyvalues.objects.filter(propertyid=5).distinct("propertyvalue") #citation category Extensionproperties
        selectedCategory = None
        if 'citationCategories' in request.POST:
            if not request.POST['citationCategories'] == 'All':
                selectedCategory = request.POST['citationCategories']
                citationPropValueFilter = Citationextensionpropertyvalues.objects.filter(propertyvalue__icontains=selectedCategory)
                citationList = citationList.filter(citationid__in=citationPropValueFilter.values("citationid"))
            else:
                selectedCategory = 'All'
        #context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        if request.REQUEST.get('export_data'):
            response=exportcitations(request,citationList, True)
            return response
        if request.REQUEST.get('export_endnote'):
            response=exportcitations(request,citationList, False)
            return response
        return TemplateResponse(request,'publications.html',{'citationList': citationList,'authList':authList,
                'filterTags':filterTags,'citationCategories':citationCategories,'selectedCategory':selectedCategory,
                'selectedTag':selectedTag,'prefixpath': CUSTOM_TEMPLATE_PATH,})
    else:
        return HttpResponseRedirect('../')

def AddSensor(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'AddSensor.html', context)
    else:
        return HttpResponseRedirect('../')

def chartIndex(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
        return TemplateResponse(request, 'chartIndex.html', context)
    else:
        return HttpResponseRedirect('../')

#chartIndex
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

def get_name_of_sampling_feature(selected_result):

     title_feature_action = Featureactions.objects.filter(featureactionid=selected_result.values('featureactionid'))
     title_sampling_feature = Samplingfeatures.objects.filter(samplingfeatureid=title_feature_action.values('samplingfeatureid'))
     s = str(title_sampling_feature.values_list('samplingfeaturename',flat=True))
     name_of_sampling_feature= s.split('\'')[1]
     return name_of_sampling_feature

def get_name_of_variable(selected_result):
     title_variables = Variables.objects.filter(variableid=selected_result.values('variableid'))
     s = str(title_variables.values_list('variablecode',flat=True))
     name_of_variable= s.split('\'')[1]
     return name_of_variable

def get_name_of_units(selected_result):
     title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
     s = str(title_units.values_list('unitsname',flat=True))
     name_of_units= s.split('\'')[1]
     return name_of_units


def relatedFeaturesFilter(request,done,selected_relatedfeatid,selected_resultid,resultType='Temporal observation'):
    #selected_relatedfeatid = 18
    if 'SelectedRelatedFeature' in request.POST and not 'update_result_list' in request.POST:
        if not request.POST['SelectedRelatedFeature'] == 'All':
            done=True
            selected_relatedfeatid= int(request.POST['SelectedRelatedFeature'])
            relatedFeatureList = Relatedfeatures.objects.filter(relatedfeatureid=int(selected_relatedfeatid)).distinct('relatedfeatureid')
            relatedFeatureListLong = Relatedfeatures.objects.filter(relatedfeatureid=int(selected_relatedfeatid))#.select_related('samplingfeatureid','relationshiptypecv','relatedfeatureid')
            samplingfeatids= relatedFeatureListLong.values_list('samplingfeatureid', flat=True)
            resultList = Results.objects.filter(featureactionid__in=Featureactions.objects.filter(samplingfeatureid__in=samplingfeatids))#.select_related('variable','feature_action')
            if 'update_result_on_related_feature' in request.POST:
                #raise ValidationError(relatedFeatureList)
                selected_relatedfeatid= relatedFeatureList[0].relatedfeatureid.samplingfeatureid
                selected_resultid= resultList[0].resultid
        else:
            selected_relatedfeatid= request.POST['SelectedRelatedFeature']
            resultList = Results.objects.filter(result_type=resultType) # remove slice just for testing [:25]
    else:
        selected_relatedfeatid='All'
        resultList = Results.objects.filter(result_type=resultType)# remove slice just for testing
    return selected_relatedfeatid, done, resultList,selected_resultid




def temp_pivot_chart_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('../')

    selected_resultid = 15
    selected_featureactionid = 5
    selected_relatedfeatid = 18

    #relatedfeatureList
    #update_result_on_related_feature
    done=False
    selected_relatedfeatid, done, resultList,selected_resultid = relatedFeaturesFilter(request, done,selected_relatedfeatid,selected_resultid)

    if 'SelectedFeatureAction' in request.POST and not done:
        #raise ValidationError(done)
        if not request.POST['SelectedFeatureAction'] == 'All':
            selected_featureactionid= int(request.POST['SelectedFeatureAction'])
            resultList = Results.objects.filter(featureactionid=selected_featureactionid)
            if 'update_result_list' in request.POST:
                selected_resultid= resultList[0].resultid
        else:
            selected_featureactionid= request.POST['SelectedFeatureAction']
            resultList = Results.objects.filter(result_type="Temporal observation")
    elif not done:
        resultList = Results.objects.filter(featureactionid=selected_featureactionid)



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
        #name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        # if name_of_sampling_features.__len__() >0:
        #     namefound=False
        #     for name in name_of_sampling_features:
        #         if name == tmpname:
        #             namefound=True
        #     if not namefound:
        #         name_of_sampling_features.append(tmpname)
        #     else:
        #         name_of_sampling_features.append('')
        # else:
        name_of_sampling_features.append(tmpname)


        tmpname = get_name_of_variable(selected_result)
        if name_of_variables.__len__() >0:
            namefound=False
            for name in name_of_variables:
                if name == tmpname:
                    namefound=True
            if not namefound:
                 name_of_variables.append(tmpname)
            else:
                 name_of_variables.append('')
        else:
              name_of_variables.append(tmpname)

        tmpname = get_name_of_units(selected_result)
        if name_of_units.__len__() >0:
            namefound=False
            for name in name_of_units:
                if name == tmpname:
                    namefound=True
            if not namefound:
                name_of_units.append(tmpname)
            else:
                name_of_units.append('')
        else:
             name_of_units.append(tmpname)

        myresultSeries.append(Measurementresultvalues.objects.all().filter(~Q(datavalue=-6999))\
        .filter(~Q(datavalue=-888.88)).filter(valuedatetime__gt= entered_start_date)\
        .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid=selectedMResult).order_by('-valuedatetime'))
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


    #build strings for graph labels
    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    tmpUnit = ''
    tmpVariableName = ''
    tmpLocName= ''
    for name_of_unit,name_of_sampling_feature,name_of_variable in zip(name_of_units,name_of_sampling_features,name_of_variables) :
        i+=1
        if i==1 and not name_of_unit == '':
            seriesStr +=name_of_unit
        elif not name_of_unit == '':
                tmpUnit = name_of_unit
                seriesStr+=' - '+name_of_unit
        if not name_of_variable=='':
            tmpVariableName = name_of_variable
        if not name_of_unit == '':
            tmpUnit = name_of_unit
        if not name_of_sampling_feature =='':
            tmpLocName = name_of_sampling_feature
        series.append({"name": tmpUnit +' - '+ tmpVariableName +' - '+ tmpLocName,"yAxis": tmpUnit, "data": data['datavalue'+str(i)]})
    i=0
    for name_of_sampling_feature,name_of_variable in zip(name_of_sampling_features,name_of_variables) :
        i+=1
        if i ==1:
            titleStr += name_of_sampling_feature  #+ ', ' +name_of_variable
        else:
            titleStr += ' - '  +name_of_sampling_feature #+name_of_variable+ ', '

    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter',  "zoomType": 'xy',}
    title2 = {"text": titleStr}
    xAxis = {"type": 'datetime', "title": {"text": 'Date'},}
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'line'
    opposite = False


    actionList = Actions.objects.filter(action_type="Observation") #where the action is not of type estimation
    #assuming an estimate is a single value.
    featureactionList = Featureactions.objects.filter(action__in=actionList)
    relatedFeatureList = Relatedfeatures.objects.order_by('relatedfeatureid').distinct('relatedfeatureid')
    int_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if request.REQUEST.get('export_data'):
        csvexport=True
        k=0
        myfile = StringIO.StringIO()
        for myresults in myresultSeries:
            for result in myresults:
                if k==0:
                    myfile.write(result.csvheader())
                    myfile.write('\n')
                myfile.write(result.csvoutput())
                myfile.write('\n')
                k+=1
        response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        #raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,'chart.html',{ 'featureactionList': featureactionList,'prefixpath': CUSTOM_TEMPLATE_PATH, 'resultList': resultList,
            'startDate':entered_start_date,'endDate':entered_end_date, 'SelectedResults':int_selectedresultid_ids,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2, 'graphType':graphType, 'xAxis': xAxis, 'yAxis': yAxis,'name_of_units':name_of_units,
            'relatedFeatureList': relatedFeatureList,'SelectedRelatedFeature':selected_relatedfeatid, 'SelectedFeatureAction':selected_featureactionid,},)
#
#From http://stackoverflow.com/questions/8200342/removing-duplicate-strings-from-a-list-in-python
def removeDupsFromListOfStrings(listOfStrings):
    seen = set()
    result = []
    for item in listOfStrings:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def scatter_plot(request):
    xVariableSelection=yVariableSelection=fieldarea1=fieldarea2=filteredFeatures=fieldareaRF=None
    xVar=None
    yVar=None
    title = None
    if 'fieldarea1' in request.POST and not 'fieldarea2' in request.POST:
        if not request.POST['fieldarea1'] == 'All':
            fieldarea1 = request.POST['fieldarea1']
            fieldarea1RF=Relatedfeatures.objects.filter(relatedfeatureid=fieldarea1)
            filteredFeatures = Samplingfeatures.objects.filter(samplingfeatureid__in=fieldarea1RF.values("samplingfeatureid"))
            fieldarea1= Samplingfeatures.objects.filter(samplingfeatureid=fieldarea1).get()
    if 'fieldarea1' in request.POST and 'fieldarea2' in request.POST:
        if not request.POST['fieldarea1'] == 'All' and not request.POST['fieldarea2'] == 'All':
            fieldarea1 = request.POST['fieldarea1']
            fieldarea2 = request.POST['fieldarea2']
            fieldareaRF1=Relatedfeatures.objects.filter(relatedfeatureid=fieldarea1)
            fieldareaRF2=Relatedfeatures.objects.filter(relatedfeatureid=fieldarea2)
            #fieldareaRF = fieldarea1RF & fieldarea2RF #only sampling features in 1 and 2

            filteredFeatures = Samplingfeatures.objects.filter(samplingfeatureid__in=fieldareaRF1.values("samplingfeatureid"))\
                .filter(samplingfeatureid__in=fieldareaRF2.values("samplingfeatureid"))
            fieldarea1= Samplingfeatures.objects.filter(samplingfeatureid=fieldarea1).get()
            fieldarea2= Samplingfeatures.objects.filter(samplingfeatureid=fieldarea2).get()
            title =str(fieldarea1.samplingfeaturecode) + " - " +str(fieldarea2.samplingfeaturecode) + " : "
    if 'xVariableSelection' and 'yVariableSelection' in request.POST:
        xVariableSelection= request.POST['xVariableSelection']
        yVariableSelection = request.POST['yVariableSelection']
        xVar = Variables.objects.filter(variableid=xVariableSelection).get()
        yVar = Variables.objects.filter(variableid=yVariableSelection).get()
        xVariableSelection= Variables.objects.filter(variableid=xVariableSelection).get()
        yVariableSelection = Variables.objects.filter(variableid=yVariableSelection).get()
        if title:
            title =title+ str(xVar.variablecode) + " - " +str(yVar.variablecode)
        else:
            title =str(xVar.variablecode) + " - " +str(yVar.variablecode)
    prv = Profileresults.objects.all()
    #second filter = exclude summary results attached to field areas
    pr = Results.objects.filter(resultid__in=prv).filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Landscape classification"))\
        .filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
    #variables is the list to pass to the html template
    variables = Variables.objects.filter(variableid__in=pr.values("variableid"))
    fieldareas = Samplingfeatures.objects.filter(sampling_feature_type="Landscape classification") #Field area
    data = {}
    xlocation=[]
    ylocation=[]
    xdata=[]
    ydata=[]
    rvx=rvy=prvx=prvy=xlocs=ylocs=None
    if xVar and yVar:
        rvx=pr.filter(variableid=xVar)
        prvx=Profileresultvalues.objects.filter(~Q(datavalue=-6999))\
        .filter(~Q(datavalue=-888.88)).filter(resultid__in=rvx).order_by("resultid__resultid__unitsid","resultid__resultid__featureactionid__samplingfeatureid","zlocation")
        rvy=pr.filter(variableid=yVar)
        prvy=Profileresultvalues.objects.filter(~Q(datavalue=-6999))\
        .filter(~Q(datavalue=-888.88)).filter(resultid__in=rvy).order_by("resultid__resultid__unitsid","resultid__resultid__featureactionid__samplingfeatureid","zlocation")

        xr =  Results.objects.filter(resultid__in=prvx.values("resultid"))
        xfa = Featureactions.objects.filter(featureactionid__in=xr.values("featureactionid"))
        if filteredFeatures:
            xlocs=Samplingfeatures.objects.filter(samplingfeatureid__in=xfa.values("samplingfeatureid")).filter(samplingfeatureid__in=filteredFeatures)
        else:
            xlocs=Samplingfeatures.objects.filter(samplingfeatureid__in=xfa.values("samplingfeatureid"))
        xloc = xlocs.values_list("samplingfeaturename",flat=True)
        #xlocation = re.sub('[^A-Za-z0-9]+', '', xlocation)
        yr =  Results.objects.filter(resultid__in=prvy.values("resultid"))
        yfa = Featureactions.objects.filter(featureactionid__in=yr.values("featureactionid"))
        if filteredFeatures:
            ylocs=Samplingfeatures.objects.filter(samplingfeatureid__in=yfa.values("samplingfeatureid")).filter(samplingfeatureid__in=filteredFeatures)
        else:
            ylocs=Samplingfeatures.objects.filter(samplingfeatureid__in=yfa.values("samplingfeatureid"))
        yloc = ylocs.values_list("samplingfeaturename",flat=True)
    if prvx and prvx:
        prvx = prvx.filter(resultid__resultid__featureactionid__samplingfeatureid__in=xlocs)
        prvy = prvy.filter(resultid__resultid__featureactionid__samplingfeatureid__in=ylocs)
        for x in prvx:
            xdata.append(str(x.datavalue) + ";"+str(x.resultid.resultid.unitsid.unitsabbreviation)+
                         ";"+str(x.zlocation)+";"+str(x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename))

            tmpLoc = str(x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)  + " " + str(x.zlocation -x.zaggregationinterval) + \
                     "-" + str(x.zlocation) + " " + str(x.zlocationunitsid.unitsabbreviation) +\
                     ";" +str(x.resultid.resultid.unitsid.unitsabbreviation) + ";"+str(x.zlocation) \
                     + ";" + str(x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)+";" +str(x.resultid.resultid.unitsid.unitsabbreviation)
            xlocation.append(tmpLoc)

        for y in prvy:
            ydata.append(str(y.datavalue)+";"+str(y.resultid.resultid.unitsid.unitsabbreviation)+";"+str(y.zlocation)+
                         ";"+str(y.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename))
            foundloc=False
            for x in prvx:
                if x.zlocation == y.zlocation or x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename==y.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename:
                    foundloc=True
                    tmpLoc = str(y.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)  + " " + str(y.zlocation -y.zaggregationinterval) + \
                         "-" + str(y.zlocation) + " " + str(y.zlocationunitsid.unitsabbreviation) +\
                         ";" +str(y.resultid.resultid.unitsid.unitsabbreviation) + ";"+str(y.zlocation) \
                         + ";" + str(y.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)+";" +str(y.resultid.resultid.unitsid.unitsabbreviation)
            if not foundloc:
                xlocation.append(tmpLoc)
            #xlocation.append(tmpLoc)
    data =json.dumps(data)
    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter',  "zoomType": 'xy',}
    title2 = {"text": title }
    #xAxis = {"categories":xAxisCategories,} #"type": 'category',"title": {"text": xAxisCategories},
    yAxis = {"title": {"text": str(yVar)}}
    xAxis = {"title": {"text": str(xVar)}}
    graphType = 'scatter'
    if request.REQUEST.get('export_data'):
        resultValuesSeries=prvx |prvy
        response=exportspreadsheet(request,resultValuesSeries)
        return response
    return TemplateResponse(request,'soilsscatterplot.html',{'prefixpath': CUSTOM_TEMPLATE_PATH,
        'xVariables':variables, 'yVariables':variables,
        'xVariableSelection':xVariableSelection,'yVariableSelection':yVariableSelection,
        'fieldarea1':fieldarea1, 'fieldarea2':fieldarea2, 'fieldareas':fieldareas,
        'chartID': chartID, 'chart': chart,'title2': title2, 'graphType':graphType,
        'yAxis': yAxis, 'xAxis': xAxis,'xdata':xdata,'ydata':ydata,'data':data,'ylocation':ylocation,'xlocation':xlocation,},)

def exportcitations(request,citations,csv):
    myfile = StringIO.StringIO()
    first= True
    citationpropvalues = Citationextensionpropertyvalues.objects.filter(citationid__in=citations).order_by("propertyid")
    authorheader = Authorlists.objects.filter(citationid__in=citations).order_by("authororder").distinct("authororder")
    authheadercount=authorheader.__len__()
    citationpropheaders = citationpropvalues.distinct("propertyid").order_by("propertyid")
    for citation in citations:

        if first and csv:
            myfile.write(citation.csvheader())
            for auth in authorheader:
                 myfile.write(auth.csvheader())

            for citationprop in citationpropheaders:
                 myfile.write(citationprop.csvheader())

            myfile.write('\n')
        if csv:
            myfile.write(citation.csvoutput())
        else: #endnote instead
            myfile.write(citation.endnoteexport())
        #export authors
        authors = Authorlists.objects.filter(citationid=citation).order_by("authororder")
        authcount=authors.__len__()
        for auth in authors:
            if csv:
                myfile.write(auth.csvoutput())
            else:
                myfile.write(auth.endnoteexport())
        if csv:
            for i in range(0, authheadercount-authcount, 1):
                 myfile.write('"",')
        thiscitationpropvalues = citationpropvalues.filter(citationid=citation).order_by("propertyid")
        for matchheader in citationpropheaders:
            headermatched = False
            for citationprop in thiscitationpropvalues:
                headermatched=False
                if matchheader.propertyid == citationprop.propertyid:
                    headermatched = True
                if csv and headermatched:
                    myfile.write(citationprop.csvoutput())
                elif headermatched:
                    myfile.write(citationprop.endnoteexport())
                if headermatched:
                    break
            if not headermatched and csv:
                myfile.write('"",')
        myfile.write('ER \n')
        myfile.write('\n')
        first=False

    if csv:
        response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mycitations.csv"'
    else:
        response = HttpResponse(myfile.getvalue(),content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename="myCitationsEndNoteImport.txt"'

    return response


def exportspreadsheet(request,resultValuesSeries):
    #if the user hit the export csv button export the measurement results to csv
    csvexport=True

    myfile = StringIO.StringIO()
    #raise ValidationError(resultValues)
    k=0
    lastVariable=''
    variable = ''
    lastUnit = ''
    unit = ''
    firstheader = True
    firstVar = None
    firstUnit = None
    resultValuesSeries = resultValuesSeries.filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Landscape classification")).\
        filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area")).\
        order_by("resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
            "resultid__intendedzspacing","resultid__resultid__variableid","resultid__resultid__unitsid")
    for myresults in resultValuesSeries:
        lastVariable = variable
        variable=myresults.resultid.resultid.variableid.variable_name
        lastUnit = unit
        unit = myresults.resultid.resultid.unitsid
        if not firstheader and firstVar==variable and firstUnit==unit:
            #only add the first instance of each variable once one repeats your done.
            break
        if not lastVariable == variable or not lastUnit==unit:
            if firstheader:
                myfile.write(myresults.csvheader())
                firstVar=variable
                firstUnit=unit
                firstheader = False
            myfile.write(myresults.csvheaderShort())

    #myfile.write(lastResult.csvheaderShort())
    myfile.write('\n')
    lastSamplingFeatureCode=''
    samplingFeatureCode = ''
    lastDepth=0
    depth = 0
    nextRow = False
    #resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode
    for myresults in resultValuesSeries:
        lastSamplingFeatureCode = samplingFeatureCode
        samplingFeatureCode=myresults.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturecode
        lastDepth = depth
        depth = myresults.resultid.intendedzspacing

        if not k==0 and (not lastSamplingFeatureCode == samplingFeatureCode or not depth==lastDepth):
            myfile.write('\n')
            myfile.write(myresults.csvoutput())
        elif k==0:
            myfile.write(myresults.csvoutput())
        #else:
        myfile.write(myresults.csvoutputShort())

        k+=1
    response = HttpResponse(myfile.getvalue(),content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    return response

def graph_data(request):
    #if not request.user.is_authenticated():
        #return HttpResponseRedirect('../')

    selected_resultid = 9365
    selected_relatedfeatid = 15

    #relatedfeatureList
    #update_result_on_related_feature
    done=False

    #need a variables list instead of a results list
    # find the variables for the selected related feature

    if 'SelectedRelatedFeature' in request.POST:
        if not request.POST['SelectedRelatedFeature'] == 'All':
            #relatedFeature = Samplingfeatures.objects.filter(samplingfeatureid=selected_relatedfeatid) #Relatedfeatures.objects.filter(relatedfeatureid=int(selected_relatedfeatid)).distinct('relatedfeatureid')
            selected_relatedfeatid = int(request.POST['SelectedRelatedFeature'])
        else:
            selected_relatedfeatid = 15
            #relatedFeature = Samplingfeatures.objects.filter(samplingfeatureid=selected_relatedfeatid)

    else:
        selected_relatedfeatid = 15
    #find variables found at the sampling feature
    #need to go through featureaction to get to results
    variableList = None
    #need the feature actions for all of the sampling features related to this sampling feature
    sampling_features = Relatedfeatures.objects.filter(relatedfeatureid=selected_relatedfeatid)
    #select the feature actions for all of the related features.
    feature_actions = Featureactions.objects.filter(samplingfeatureid__in = sampling_features)
    featureresults = Results.objects.filter(featureactionid__in=feature_actions).order_by("variableid","unitsid")\
        .filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Landscape classification")).\
        filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
    variableList = Variables.objects.filter(variableid__in =featureresults.values("variableid"))

    #find the profile results series for the selected variable
    numvariables = variableList.__len__()
    #raise ValidationError(numvariables)
    selectedMVariableSeries = []
    selectionStr = ''
    for i in range(0,numvariables):
        selectionStr = str('selection' + str(i))
        if selectionStr in request.POST:
            #raise ValidationError(request.POST[selectionStr])
            for variable in variableList:
                if int(request.POST[selectionStr]) == variable.variableid:
                    selectedMVariableSeries.append(int(request.POST[selectionStr]))

    #if no series were selected (like on first load) set the series to some value.
    if len(variableList) > 0 and len(selectedMVariableSeries)==0:
        selectedMVariableSeries.append(int(variableList[0].variableid))
    elif len(variableList) == 0 and len(selectedMVariableSeries)==0:
        selectedMVariableSeries.append(15)

    selectedMResultsSeries = None
    for variable in selectedMVariableSeries:
        if not selectedMResultsSeries:
            selectedMResultsSeries = featureresults.filter(variableid=variable)
        else: #concatenante the sets of results for each variable
            selectedMResultsSeries = selectedMResultsSeries | featureresults.filter(variableid=variable)
    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []
    unitAndVariable = ''
    i = 0
    data = {}
    data2= []
    resultValuesSeries = None
    #if 'update_result_on_related_feature' in request.POST:
            #raise ValidationError(selectedMResultsSeries)
    #selectedMResultsSeries.order_by("resultid__")

    #these 5 lines sort the results by there z-spacing low to high, then by alphabelitcally by there sampling
    #feature code, luckily Ridge, Slope, Valley are in alphabetical order.
    profileresults = Profileresults.objects.filter(resultid__in=selectedMResultsSeries).order_by("resultid__variableid",
            "resultid__unitsid","intendedzspacing","resultid__featureactionid__samplingfeatureid__samplingfeaturecode")
    sortedResults = list()
    for result in profileresults:
        sortedResults.append(selectedMResultsSeries.get(resultid=result.resultid.resultid))
    selectedMResultsSeries = sortedResults
    for selectedMResult in selectedMResultsSeries:
        i +=1
        selected_result = Results.objects.filter(resultid=selectedMResult.resultid)
        #if 'update_result_on_related_feature' in request.POST:
            #raise ValidationError(selected_result)
        selected_results.append(selected_result)
        #name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        tmpLocName = tmpname

        tmpname = get_name_of_variable(selected_result)
        unitAndVariable = tmpname
        if name_of_variables.__len__() >0:
            name_of_variables.append(tmpname)
        else:
              name_of_variables.append(tmpname)
        tmpname = get_name_of_units(selected_result)
        #if(selectedMResult.resultid==2072):
            #raise ValidationError(tmpname)
        unitAndVariable = unitAndVariable + " " + tmpname
        if name_of_units.__len__() >0:
            name_of_units.append(tmpname)
        else:
             name_of_units.append(tmpname)

        resultValues= Profileresultvalues.objects.all().filter(resultid=selectedMResult)#.order_by("-zlocation")

        if not resultValuesSeries:
            resultValuesSeries = resultValues
        else:
            resultValuesSeries = resultValuesSeries | resultValues
        #if 'update_result_on_related_feature' in request.POST:
            #raise ValidationError(resultValues)
        for resultValue in resultValues:
            #raise ValidationError(resultValues)
            seriesName = 'datavalue' + unitAndVariable
            tmpLocName = tmpLocName + " Depth " + str(resultValue.zlocation -resultValue.zaggregationinterval) +"-" + str(resultValue.zlocation) + " " + str(resultValue.zlocationunitsid.unitsabbreviation)
            name_of_sampling_features.append(tmpLocName)
            if seriesName in data:
                if resultValue.datavalue!=-6999 and resultValue.datavalue!=-888.88:
                    data['datavalue' + unitAndVariable].append([ tmpLocName,resultValue.datavalue]) #tmpUnit +' - '+tmpVariableName +' - '+
                else:
                    data['datavalue' + unitAndVariable].append([ tmpLocName,None])
            else:
                data.update({'datavalue' + unitAndVariable: []})
                if resultValue.datavalue!=-6999 and resultValue.datavalue!=-888.88:
                    data['datavalue' + unitAndVariable].append([ tmpLocName,resultValue.datavalue]) #tmpUnit +' - '+tmpVariableName +' - '+
                else:
                    data['datavalue' + unitAndVariable].append([ tmpLocName,None])
            #data['datavalue' + unitAndVariable].append( resultValue.datavalue) #get_name_of_variable(selected_result) + " " + get_name_of_sampling_feature(selected_result) ,
            #data2.append(resultValue.datavalue)
    #raise ValidationError(data)
    #build strings for graph labels
    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    tmpUnit = ''
    tmpVariableName = ''
    update = False
    numberofLocations =len(name_of_sampling_features)

    for name_of_unit,name_of_variable in zip(name_of_units,name_of_variables) :
        #raise ValidationError("length of unit names"+ str(len(name_of_units)) +
        #"length of name of variables"+ str(len(name_of_variables))) #get fewer sampling feature names
        i+=1
        lastUnit = tmpUnit
        lastVariableName = tmpVariableName
        tmpVariableName = name_of_variable
        tmpUnit = name_of_unit

        if not name_of_variable ==lastVariableName or not name_of_unit==lastUnit:
            update = True
        else:
            update = False

        if i==1 and not name_of_unit == '':
            seriesStr +=name_of_unit
        elif name_of_unit !=lastUnit and update:
                #tmpUnit = name_of_unit
            seriesStr+=' - '+name_of_unit
        lastUnitAndVariable = unitAndVariable
        unitAndVariable = tmpVariableName + " " + tmpUnit
        #raise ValidationError(data['datavalue'+unitAndVariable])
        #raise ValidationError(name_of_unit)
        if lastUnitAndVariable != unitAndVariable and update:
            series.append({"name":tmpUnit +' - '+tmpVariableName,"yAxis": tmpUnit, "data": data['datavalue'+unitAndVariable]}) #removewd from name +' - '+ tmpLocName
            if titleStr =='':
                titleStr = tmpVariableName
            else:
                titleStr += ' - '+ tmpVariableName
        elif i==numberofLocations and len(series)==0:
             #raise ValidationError(name_of_unit)
             series.append({"name":tmpUnit +' - '+tmpVariableName,"yAxis": tmpUnit, "data": data['datavalue'+unitAndVariable]})
             if titleStr =='':
                titleStr = tmpVariableName
             #titleStr += tmpVariableName
        #series.append(data['datavalue'+str(i)])

    i=0
    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'column',  "zoomType": 'xy',}
    title2 = {"text": titleStr}
    #xAxis = {"categories":xAxisCategories,} #"type": 'category',"title": {"text": xAxisCategories},
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'column'
    opposite = False

    withProfileResults = Profileresults.objects.all()
    results = Results.objects.filter(resultid__in=withProfileResults)
    featureAction = Featureactions.objects.filter(featureactionid__in=results.values("featureactionid"))
    relatedFeatureList = Relatedfeatures.objects.filter(samplingfeatureid__in=featureAction).order_by('relatedfeatureid').distinct('relatedfeatureid') #
    #relatedFeatureList = sorted(relatedFeatureList, key=operator.attrgetter('relatedfeatureid__samplingfeaturecode')) #relatedFeatureList.order_by('relatedfeatureid__samplingfeaturecode')
    int_selectedvariable_ids = []
    for int_selectedvariableid in selectedMVariableSeries:
        int_selectedvariable_ids.append(int(int_selectedvariableid))
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if request.REQUEST.get('export_data'):
        resultValuesSeries = resultValuesSeries.order_by("resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
                "resultid__intendedzspacing","resultid__resultid__variableid","resultid__resultid__unitsid")
        response=exportspreadsheet(request,resultValuesSeries)
        return response
    else:
        #this removes duplicates from a list of strings
        name_of_units = removeDupsFromListOfStrings(name_of_units)
        #raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,'chartVariableAndFeature.html',{'prefixpath': CUSTOM_TEMPLATE_PATH,  'variableList': variableList,
             'SelectedVariables':int_selectedvariable_ids,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2, 'graphType':graphType, 'yAxis': yAxis,'name_of_units':name_of_units,
            'relatedFeatureList': relatedFeatureList,'SelectedRelatedFeature':selected_relatedfeatid,},)
