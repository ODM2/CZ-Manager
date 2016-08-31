__author__ = 'leonmi'
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
#from odm2testapp.forms import VariablesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
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
import math
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
from django.db.models import Min, Max
from django.template import loader
from .forms import CitationsAdminForm
from .forms import CitationextensionpropertyvaluesAdminForm
from .forms import AuthorlistsAdminForm
from django.http import StreamingHttpResponse
from django.core import mail
from subprocess import *
import sys as sys
from django.core import management
from django.shortcuts import render_to_response
from django.contrib.gis.geos import GEOSGeometry
from templatesAndSettings.settings import map_config
from templatesAndSettings.base import ADMIN_SHORTCUTS
from django.contrib import admin
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
from django.views.generic.edit import FormView

#class CreatePubView(FormView):
#    template_name = "publications2.html"
#    model = Citations
from django.forms.models import inlineformset_factory
from django.db import IntegrityError
from django.forms import widgets
from django.db import models

def add_pub(request,citationid='NotSet'):
    if request.user.is_authenticated():
        #if 'citationidnew' in request.POST:
            #if not request.POST['citationidnew'] == '':
                #citationid = int(request.POST['citationidnew'])
                #citationidnew = citationid
        AuthorInlineFormSet = inlineformset_factory(Citations,Authorlists,extra=6)

        CitationpropertyInlineFormSet = inlineformset_factory(Citations,Citationextensionpropertyvalues)
        #citation_form=CitationsAdminForm(request.POST,instance=citation)
        if request.method=="POST":
            if 'delete_citation' in request.POST:
                citation= Citations.objects.filter(citationid=citationid).get()
                citation.delete()
                return HttpResponseRedirect('../../publications.html')
            if citationid == 'NotSet':
                citation= Citations(title=request.POST['title'],publisher=request.POST['publisher'],publicationyear=int(request.POST['publicationyear']),citationlink=request.POST['citationlink'])
                #if citation.is_valid():
                citation.save()
                citationid=citation.citationid
                citation_form=CitationsAdminForm(request.POST,instance=citation)
            else:
                citation= Citations.objects.filter(citationid=citationid).get()
                citation_form=CitationsAdminForm(request.POST,instance=citation)
            #citation= Citations.objects.filter(citationid=citationid).get()
            Authorformset=AuthorInlineFormSet(request.POST,instance=citation)

            Citationpropertyformset = CitationpropertyInlineFormSet(request.POST,instance=citation)

            if Authorformset.is_valid():
                try:
                    Authorformset.save()
                except IntegrityError:
                    pass
            if Citationpropertyformset.is_valid():
                Citationpropertyformset.save()
            #for form in CitationPorpertyformset:
                #if form.changed_data.__len__() > 0:
                    #form.save()
            if citation_form.is_valid():
                citation_form.save()
            return HttpResponseRedirect('../../pubview/citationid=' + str(citationid) +'/')
        elif not citationid=='NotSet':
            citation= Citations.objects.filter(citationid=citationid).get()
            Authorformset = AuthorInlineFormSet(instance=citation)

            #Authorformset.empty_permitted=False
            Citationpropertyformset = CitationpropertyInlineFormSet(instance=citation)
            #CitationPorpertyformset.empty_permitted=True
            citation_form=CitationsAdminForm(instance=citation)
        else:
            AuthorInlineFormSet = inlineformset_factory(Citations,Authorlists,extra=6)
            CitationpropertyInlineFormSet = inlineformset_factory(Citations,Citationextensionpropertyvalues,extra=8)
            Authorformset=AuthorInlineFormSet(instance=Authorlists())
            # i=1
            # for form in Authorformset:
            #     form.fields['authororder'].initial = i
            #     i+=1
            Citationpropertyformset = CitationpropertyInlineFormSet(instance=Citationextensionpropertyvalues())
            citation_form=CitationsAdminForm(instance=Citations())
            citationidnew=''
        i=1
        for form in Authorformset:
            if form.fields['authororder'].initial == None:
                form.fields['authororder'].initial = i
            i+=1
        #for form in Citationpropertyformset:

            #if  'propertyid' in form.initial: #not propertyid==None
                #propertyid = form.initial['propertyid'] #.initial #type number
                #extensionprop = Extensionproperties.objects.filter(propertyid=propertyid).get()
                #name = extensionprop.propertydatatypecv
                #typecv = CvPropertydatatype.objects.filter(name=name.name).get()
                #if typecv.name == "Boolean":
                    #form.fields['propertyvalue'].widget = widgets.CheckboxInput
                    #form.fields['propertyvalue']= models.BooleanField()
            #elif citationid=='NotSet':

            #if form.fields['authororder'].initial == None:

        return render(request, 'publications3.html', {'Authorformset':Authorformset, 'Citationpropertyformset':Citationpropertyformset,'citation_form':citation_form,})
    else:
        return HttpResponseRedirect('../../')
# def add_pub(request,citation='NotSet'):
#     #citation_form
#     #author_form
#     #citation_property_form
#     author_forms= []
#     citation_property_forms=[]
#     if request.method=="POST":
#         citation_form=CitationsAdminForm(request.POST,instance=Citations())
#         author_forms=[AuthorlistsAdminForm(request.POST,prefix=str(x),instance=Authorlists()) for x in range(0,3)]
#         citation_property_forms=[CitationextensionpropertyvaluesAdminForm(request.POST,prefix=str(x),instance=Citationextensionpropertyvalues())for x in range(0,3)]
#         if citation_form.is_valid():
#             new_citation= citation_form.save()
#             citationid= new_citation.citationid
#             for af in author_forms:
#                 if af.is_valid():
#                     new_author = af.save(commit=False)
#                     new_author.citationid = new_citation
#                     new_author.save()
#             for cpf in citation_property_forms:
#                 if cpf.is_valid():
#                     new_cepv = cpf.save(commit=False)
#                     new_cepv.citationid = new_citation
#                     new_cepv.save()
#             return HttpResponseRedirect('/pubview/citationid=' + str(citationid))
#     elif not citation=='NotSet':
#         citation_form=CitationsAdminForm(instance=Citations.objects.filter(citationid=citation).get())
#         authors = Authorlists.objects.filter(citationid=citation)
#         for auth in authors:
#             author_forms.append(AuthorlistsAdminForm(instance=auth))
#         cepvs= Citationextensionpropertyvalues.objects.filter(citationid=citation)
#         for cepv in cepvs:
#             citation_property_forms.append(CitationextensionpropertyvaluesAdminForm(instance=cepv))
#     else:
#         citation_form=CitationsAdminForm(instance=Citations())
#         author_forms=[AuthorlistsAdminForm(prefix=str(x), instance=Authorlists()) for x in range(0,3)]
#         citation_property_forms=[CitationextensionpropertyvaluesAdminForm(prefix=str(x), instance=Citationextensionpropertyvalues()) for x in range(0,3)]
#     return TemplateResponse(request, 'publications2.html',{'citation_form':citation_form,'author_forms':author_forms,'citation_property_forms':citation_property_forms,})

def publications(request):
    #if request.user.is_authenticated():
    citationList = Citations.objects.all()
    authList = Authorlists.objects.all()
    peopleList = People.objects.filter(personid__in=authList.values("personid"))
    selectedTag = 'CZO Authors'
    selectedAuthor= 'All'

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

    if 'selectedAuthor' in request.POST:
        if not request.POST['selectedAuthor'] == 'All':
            selectedAuthor= int(request.POST['selectedAuthor'])
            authored = Authorlists.objects.filter(personid=selectedAuthor)
            citationList = citationList.filter(citationid__in=authored.values("citationid"))


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
    if 'export_data' in request.POST:
        response=exportcitations(request,citationList, True)
        return response
    if 'export_endnote' in request.POST:
        response=exportcitations(request,citationList, False)
        return response
    return TemplateResponse(request,'publications.html',{'citationList': citationList,'authList':authList,
            'filterTags':filterTags,'citationCategories':citationCategories,'selectedCategory':selectedCategory,
            'selectedTag':selectedTag,'peopleList':peopleList,'selectedAuthor':selectedAuthor,'prefixpath': CUSTOM_TEMPLATE_PATH,})

################# SHORTCUTS ##################################################
def AddSensor(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH, 'name':request.user,
                   'authenticated':True, 'site_title': admin.site.site_title,
                   'site_header':admin.site.site_header,'short_title':ADMIN_SHORTCUTS[0]['shortcuts'][1]['title']}
        return TemplateResponse(request, 'AddSensor.html', context)
    else:
        return HttpResponseRedirect('../')

def chartIndex(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': ADMIN_SHORTCUTS[0]['shortcuts'][5]['title']}
        return TemplateResponse(request, 'chartIndex.html', context)
    else:
        return HttpResponseRedirect('../')

#chartIndex
def AddProfile(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': ADMIN_SHORTCUTS[0]['shortcuts'][2]['title']}
        return TemplateResponse(request, 'AddProfile.html', context)
    else:
        return HttpResponseRedirect('../')

def RecordAction(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': ADMIN_SHORTCUTS[0]['shortcuts'][3]['title']}
        return TemplateResponse(request, 'RecordAction.html', context)
    else:
        return HttpResponseRedirect('../')


def ManageCitations(request):
    if request.user.is_authenticated():
        context = {'prefixpath': CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': ADMIN_SHORTCUTS[0]['shortcuts'][4]['title']}
        return TemplateResponse(request, 'ManageCitations.html', context)
    else:
        return HttpResponseRedirect('../')

###################################################################
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


def relatedFeaturesFilter(request,done,selected_relatedfeatid,selected_resultid,featureaction,resultType='Time series coverage',):
    #selected_relatedfeatid = 18
    if 'SelectedRelatedFeature' in request.POST and not 'update_result_list' in request.POST:
        if not request.POST['SelectedRelatedFeature'] == 'All':
            done=True
            selected_relatedfeatid= int(request.POST['SelectedRelatedFeature'])
            relatedFeatureList = Relatedfeatures.objects.filter(relatedfeatureid=int(selected_relatedfeatid)).distinct('relatedfeatureid')
            relatedFeatureListLong = Relatedfeatures.objects.filter(relatedfeatureid=int(selected_relatedfeatid))#.select_related('samplingfeatureid','relationshiptypecv','relatedfeatureid')
            samplingfeatids= relatedFeatureListLong.values_list('samplingfeatureid', flat=True)
            if featureaction=='All':
                resultList = Results.objects.filter(featureactionid__in=Featureactions.objects.filter(samplingfeatureid__in=samplingfeatids))#.select_related('variable','feature_action')
            else:
                resultList = Results.objects.filter(featureactionid__in=Featureactions.
                                                    objects.filter(samplingfeatureid__in=samplingfeatids)).filter(featureactionid=featureaction)
            if 'update_result_on_related_feature' in request.POST:
                #raise ValidationError(relatedFeatureList)
                selected_relatedfeatid= relatedFeatureList[0].relatedfeatureid.samplingfeatureid
                selected_resultid= resultList[0].resultid
        else:
            selected_relatedfeatid= request.POST['SelectedRelatedFeature']
            if featureaction=='All':
                resultList = Results.objects.filter(result_type=resultType) # remove slice just for testing [:25]
            else:
                resultList = Results.objects.filter(result_type=resultType).filter(featureactionid=featureaction)
    else:
        selected_relatedfeatid='All'
        if featureaction=='All':
            resultList = Results.objects.filter(result_type=resultType)# remove slice just for testing [:25]
        else:
            resultList = Results.objects.filter(result_type=resultType).filter(featureactionid=featureaction)
    return selected_relatedfeatid, done, resultList,selected_resultid


def web_map(request,dataset='NotSet'):
    if request.user.is_authenticated():
        authenticated=True
    else:
        authenticated=False
    map_config = map_config
    datasets = Datasets.objects.all()

    ids = [ds.datasetid for ds in datasets]

    selections = request.POST.getlist('datasetselection')
    if dataset!='NotSet':
        selections = list()
        selections.append(int(dataset))
    if selections:
        dataset_ids = []

        selected = []
        for selection in selections:
            dataset_ids.append(int(selection))
            selected.append(int(selection))
        datasetresults = Datasetsresults.objects.filter(datasetid__in=dataset_ids)
        results = Results.objects.filter(resultid__in=datasetresults.values("resultid"))

        fa = Featureactions.objects.filter(featureactionid__in=results.values("featureactionid"))
        features1 = Samplingfeatures.objects.filter(samplingfeatureid__in=fa.values("samplingfeatureid"))
        relatedfeatures = Relatedfeatures.objects.filter(samplingfeatureid__in=features1.values("samplingfeatureid"))
        features2 = Samplingfeatures.objects.filter(samplingfeatureid__in=relatedfeatures.values("relatedfeatureid"))
        features = features1 | features2
    else:
        selected = ids

        features = Samplingfeatures.objects.all()
        results = Results.objects.filter(featureactionid__in=features.values("featureactions"))

    # start_date= Measurementresultvalues.objects.filter(resultid__in=results.values("resultid")).annotate(Min('valuedatetime'))\
    #             .order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
    # end_date= Measurementresultvalues.objects.filter(resultid__in=results.values("resultid")).annotate(Max('valuedatetime'))\
    #             .order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')

    legend_ref = [
        dict(feature_type="Excavation", icon="fa-spoon", color="darkred",
             style_class="awesome-marker-icon-darkred"),
        dict(feature_type="Field area", icon="fa-map-o", color="darkblue",
             style_class="awesome-marker-icon-darkblue"),
        dict(feature_type="Ecological land classification", icon="fa-bar-chart", color="darkpurple",
             style_class="awesome-marker-icon-darkpurple"),
        dict(feature_type="Observation well", icon="fa-eye", color="orange",
             style_class="awesome-marker-icon-orange"),
        dict(feature_type="Site", icon="fa-dot-circle-o", color="green", style_class="awesome-marker-icon-green"),
        dict(feature_type="Stream gage", icon="fa-tint", color="blue", style_class="awesome-marker-icon-blue"),
        dict(feature_type="Transect", icon="fa-area-chart", color="cadetblue",
             style_class="awesome-marker-icon-cadetblue")
    ]


    context = {
        'prefixpath': CUSTOM_TEMPLATE_PATH,'legends':legend_ref, 'features':features,'results':results,
        'datasets':datasets,'selecteddatasets':selected,'authenticated':authenticated, 'map_config':map_config, 'name':request.user,'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': 'Map Sample Locations'}
    return render(request, 'mapdata.html', context)





#
# def web_map(request,dataset='NotSet'):
#     if request.user.is_authenticated():
#         authenticated=True
#     else:
#         authenticated=False
#     if dataset=='NotSet':
#         features = Samplingfeatures.objects.all()
#         results = Results.objects.filter(featureactionid__in=features.values("featureactions"))
#     else:
#         dataset = int(dataset)
#         datasetresults = Datasetsresults.objects.filter(datasetid=dataset)
#         results = Results.objects.filter(resultid__in=datasetresults.values("resultid"))
#         fa = Featureactions.objects.filter(featureactionid__in=results.values("featureactionid"))
#         features = Samplingfeatures.objects.filter(samplingfeatureid__in=fa.values("samplingfeatureid"))
#
#     legend_ref = [
#         dict(feature_type="Excavation", icon="fa-spoon", color="darkred", html="duck",
#              style_class="awesome-marker-icon-darkred"),
#         dict(feature_type="Field area", icon="fa-map-o", color="darkblue",
#              style_class="awesome-marker-icon-darkblue"),
#         dict(feature_type="Ecological land classification", icon="fa-bar-chart", color="darkpurple",
#              style_class="awesome-marker-icon-darkpurple"),
#         dict(feature_type="Observation well", icon="fa-eye", color="orange",
#              style_class="awesome-marker-icon-orange"),
#         dict(feature_type="Site", icon="fa-dot-circle-o", color="green", style_class="awesome-marker-icon-green"),
#         dict(feature_type="Stream gage", icon="fa-tint", color="blue", style_class="awesome-marker-icon-blue"),
#         dict(feature_type="Transect", icon="fa-area-chart", color="cadetblue",
#              style_class="awesome-marker-icon-cadetblue")
#     ]
#
#
#
#     context = {
#         'prefixpath': CUSTOM_TEMPLATE_PATH,'legends':legend_ref, 'features':features,'results':results,'authenticated':authenticated}
#     return render(request, 'mapdata.html', context)


def TimeSeriesGraphing(request,feature_action='All'):
    authenticated=True
    if not request.user.is_authenticated():
        return HttpResponseRedirect('../')
        authenticated=False

    template = loader.get_template('chart.html')
    selected_relatedfeatid=None
    selected_resultid=None
    if feature_action=='All':
        selected_resultid = 15
        selected_featureactionid = 5
        selected_relatedfeatid = 18
    else:
        selected_featureactionid=int(feature_action)

    #relatedfeatureList
    #update_result_on_related_feature
    done=False
    selected_relatedfeatid, done, resultList,selected_resultid = relatedFeaturesFilter(request, done,selected_relatedfeatid,selected_resultid,feature_action)

    if 'SelectedFeatureAction' in request.POST and not done:
        #raise ValidationError(done)
        if not request.POST['SelectedFeatureAction'] == 'All':
            selected_featureactionid= int(request.POST['SelectedFeatureAction'])
            resultList = Results.objects.filter(featureactionid=selected_featureactionid)
            if 'update_result_list' in request.POST:
                selected_resultid= resultList[0].resultid
        else:
            selected_featureactionid= request.POST['SelectedFeatureAction']
            resultList = Results.objects.filter(result_type="Time series coverage")
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
        entered_start_date = "2016-01-01"
    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        entered_end_date = "2016-01-05"
    if entered_end_date =='':
        entered_end_date = "2016-01-05"
    if entered_start_date=='':
        entered_start_date = "2016-01-01"

    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []
    ProcessingLevel = []

    myresultSeries = []
    myresultSeriesExport = None
    i = 0
    data = {}


    for selectedMResult in selectedMResultSeries:
        i +=1
        selected_result = Results.objects.filter(resultid=selectedMResult)
        selected_results.append(selected_result)
        #name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
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


        myresultSeries.append(Measurementresultvalues.objects.all().filter(~Q(datavalue__lte=-6999))\
        .filter(valuedatetime__gt= entered_start_date)\
        .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid=selectedMResult).order_by('-valuedatetime'))

        data.update({'datavalue' + str(i): []})


    myresultSeriesExport = Measurementresultvalues.objects.all()\
                .filter(valuedatetime__gt= entered_start_date)\
                .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
    i = 0

    for myresults in myresultSeries:
        i+=1
        for result in myresults:
            start = datetime.datetime(1970,1,1)
            delta = result.valuedatetime-start
            mills = delta.total_seconds()*1000
            if math.isnan(result.datavalue):
                dataval='null'
            else:
                dataval = result.datavalue
            data['datavalue' + str(i)].append([mills, dataval])
            #data['datavalue' + str(i)].append([mills, result.datavalue]) #dumptoMillis(result.valuedatetime)
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
    name_of_sampling_features = set(name_of_sampling_features)
    sfname = None
    oldsfname = None

    for name_of_sampling_feature in name_of_sampling_features:
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

    if 'export_data' in request.POST:
    #if request.get('export_data'):
        response = exportspreadsheet(request,myresultSeriesExport,False)
        csvexport=True
        # k=0
        # myfile = StringIO.StringIO()
        # for myresults in myresultSeriesExport:
        #     for result in myresults:
        #         if k==0:
        #             myfile.write(result.csvheader())
        #             myfile.write('\n')
        #         myfile.write(result.csvoutput())
        #         myfile.write('\n')
        #         k+=1
        #response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        #response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        #raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,template,{ 'featureactionList': featureactionList,'prefixpath': CUSTOM_TEMPLATE_PATH, 'resultList': resultList,
            'startDate':entered_start_date,'endDate':entered_end_date, 'SelectedResults':int_selectedresultid_ids,'authenticated':authenticated,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2, 'graphType':graphType, 'xAxis': xAxis, 'yAxis': yAxis,'name_of_units':name_of_units,
            'relatedFeatureList': relatedFeatureList,'SelectedRelatedFeature':selected_relatedfeatid, 'SelectedFeatureAction':selected_featureactionid,'name':request.user,'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': 'Time Series'},)


def mappopuploader(request,feature_action='NotSet',samplingfeature='NotSet',dataset='NotSet',resultidu='NotSet',startdate='NotSet',enddate='NotSet',popup='NotSet'):
    authenticated=True
    if not request.user.is_authenticated():
        #return HttpResponseRedirect('../')
        authenticated=False
    if popup=='NotSet':
        template = loader.get_template('chart2.html')
    else:
        template = loader.get_template('chartpopup.html')
    useDataset = False
    useSamplingFeature=False
    if dataset=='NotSet':
        if samplingfeature=='NotSet':
            feature_action=int(feature_action)
        else:
            samplingfeature=int(samplingfeature)
            useSamplingFeature=True
    else:
        useDataset=True
        dataset=int(dataset)
    useResultid = False
    if resultidu!='NotSet':
        useResultid=True
        resultidu=int(resultidu)

    i = 0
    featureActionLocation=None
    featureActionMethod=None
    datasetTitle=None
    datasetAbstract=None
    methods=None
    samplefeature=None
    if not useDataset:
        if useSamplingFeature:
            samplefeature = Samplingfeatures.objects.filter(samplingfeatureid=samplingfeature).get()
            feature_actions = Featureactions.objects.filter(samplingfeatureid=samplefeature)
            resultList = Results.objects.filter(featureactionid__in=feature_actions).filter(~Q(processing_level=4)).order_by("featureactionid__action__method")
            actions = Actions.objects.filter(actionid__in=feature_actions.values("action"))
            methods = Methods.objects.filter(methodid__in=actions.values("method"))
            featureActionLocation= samplefeature.samplingfeaturename
        else:
            resultList = Results.objects.filter(featureactionid=feature_action).filter(~Q(processing_level=4)).order_by("featureactionid__action__method")
            featureAction = Featureactions.objects.filter(featureactionid=feature_action).get()
            featureActionLocation= featureAction.samplingfeatureid.samplingfeaturename
            featureActionMethod= featureAction.action.method.methodname
            action = Actions.objects.filter(actionid=featureAction.action.actionid).get()
            methods = Methods.objects.filter(methodid=action.method.methodid)

    else:
        datasetResults = Datasetsresults.objects.filter(datasetid=dataset)
        resultList = Results.objects.filter(resultid__in=datasetResults.values("resultid")).filter(~Q(processing_level=4)).order_by("featureactionid__action__method")
        datasetTitle = Datasets.objects.filter(datasetid=dataset).get().datasettitle
        datasetAbstract = Datasets.objects.filter(datasetid=dataset).get().datasetabstract

    try:
        startdate= Measurementresultvalues.objects.filter(resultid__in=resultList.values("resultid")).annotate(Min('valuedatetime')).\
        order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M') #.annotate(Min('price')).order_by('price')[0]

        enddate= Measurementresultvalues.objects.filter(resultid__in=resultList.values("resultid")).annotate(Max('valuedatetime')).\
        order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
    except IndexError:
            html = "<html><body>No Data Available Yet.</body></html>"
            return HttpResponse(html)



    return TemplateResponse(request,template,{ 'prefixpath': CUSTOM_TEMPLATE_PATH,
            'useSamplingFeature':useSamplingFeature,
            'featureActionMethod':featureActionMethod,'featureActionLocation':featureActionLocation,
            'datasetTitle':datasetTitle,'datasetAbstract':datasetAbstract,'useDataset':useDataset,'startDate':startdate,'endDate':enddate,
             'authenticated':authenticated,'methods':methods,'resultList':resultList,},)

def TimeSeriesGraphingShort(request,feature_action='NotSet',samplingfeature='NotSet',dataset='NotSet',resultidu='NotSet',startdate='NotSet',enddate='NotSet',popup='NotSet'): #,startdate='',enddate=''
    authenticated=True
    if not request.user.is_authenticated():
        #return HttpResponseRedirect('../')
        authenticated=False
    if popup=='NotSet':
        template = loader.get_template('chart2.html')
    else:
        template = loader.get_template('chartpopup.html')
    useDataset = False
    useSamplingFeature=False
    if dataset=='NotSet':
        if samplingfeature=='NotSet':
            feature_action=int(feature_action)
        else:
            samplingfeature=int(samplingfeature)
            useSamplingFeature=True
    else:
        useDataset=True
        dataset=int(dataset)
    useResultid = False
    if resultidu!='NotSet':
        useResultid=True
        resultidu=int(resultidu)



    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []
    ProcessingLevel = []

    myresultSeries = []
    myresultSeriesExport = None
    i = 0
    data = {}
    featureActionLocation=None
    featureActionMethod=None
    datasetTitle=None
    datasetAbstract=None
    methods=None
    samplefeature=None
    if not useDataset:
        if useSamplingFeature:
            samplefeature = Samplingfeatures.objects.filter(samplingfeatureid=samplingfeature).get()
            feature_actions = Featureactions.objects.filter(samplingfeatureid=samplefeature)
            resultList = Results.objects.filter(featureactionid__in=feature_actions).filter(~Q(processing_level=4))
            actions = Actions.objects.filter(actionid__in=feature_actions.values("action"))
            methods = Methods.objects.filter(methodid__in=actions.values("method"))
            featureActionLocation= samplefeature.samplingfeaturename
        else:
            resultList = Results.objects.filter(featureactionid=feature_action).filter(~Q(processing_level=4))
            featureAction = Featureactions.objects.filter(featureactionid=feature_action).get()
            featureActionLocation= featureAction.samplingfeatureid.samplingfeaturename
            featureActionMethod= featureAction.action.method.methodname
            action = Actions.objects.filter(actionid=featureAction.action.actionid).get()
            methods = Methods.objects.filter(methodid=action.method.methodid)

    else:
        datasetResults = Datasetsresults.objects.filter(datasetid=dataset)
        resultList = Results.objects.filter(resultid__in=datasetResults.values("resultid")).filter(~Q(processing_level=4))
        datasetTitle = Datasets.objects.filter(datasetid=dataset).get().datasettitle
        datasetAbstract = Datasets.objects.filter(datasetid=dataset).get().datasetabstract
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


    #selectedMResultSeries = Results.objects.filter(featureactionid=feature_action)
    i=0
    if selectedMResultSeries.__len__()==0:
        if resultidu == 'NotSet':
            try:
                selectedMResultSeries.append(resultList[0].resultid)
            except IndexError:
                html = "<html><body>No Data Available Yet.</body></html>"
                return HttpResponse(html)
        else:
            selectedMResultSeries.append(int(resultidu))


    if 'startDate' in request.POST:
            entered_start_date = request.POST['startDate']
    else:
        entered_start_date= Measurementresultvalues.objects.filter(resultid__in=selectedMResultSeries).annotate(Min('valuedatetime')).\
        order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M') #.annotate(Min('price')).order_by('price')[0]

    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        entered_end_date= Measurementresultvalues.objects.filter(resultid__in=selectedMResultSeries).annotate(Max('valuedatetime')).\
        order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')


    for selectedMResult in selectedMResultSeries:
        i +=1
        selected_result = Results.objects.filter(resultid=selectedMResult)
        selected_results.append(selected_result)
        #name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
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

        myresultSeries.append(Measurementresultvalues.objects.all().filter(~Q(datavalue__lte=-6999))\
        .filter(valuedatetime__gt= entered_start_date)\
        .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid=selectedMResult).order_by('-valuedatetime'))

        data.update({'datavalue' + str(i): []})


    myresultSeriesExport = Measurementresultvalues.objects.all()\
                .filter(valuedatetime__gt= entered_start_date)\
                .filter(valuedatetime__lt = entered_end_date)\
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')

    i = 0

    for myresults in myresultSeries:
        i+=1
        for result in myresults:
            start = datetime.datetime(1970,1,1)
            delta = result.valuedatetime-start
            mills = delta.total_seconds()*1000
            dataval = None
            if math.isnan(result.datavalue):
                dataval='null'
            else:
                dataval = result.datavalue
            data['datavalue' + str(i)].append([mills, dataval]) #dumptoMillis(result.valuedatetime)
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
    name_of_sampling_features = set(name_of_sampling_features)
    sfname = None
    oldsfname = None

    for name_of_sampling_feature in name_of_sampling_features:
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


    int_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if 'export_data' in request.POST:
        response = exportspreadsheet(request,myresultSeriesExport,False)
        csvexport=True
        # k=0
        # myfile = StringIO.StringIO()
        # for myresults in myresultSeriesExport:
        #     for result in myresults:
        #         if k==0:
        #             myfile.write(result.csvheader())
        #             myfile.write('\n')
        #         myfile.write(result.csvoutput())
        #         myfile.write('\n')
        #         k+=1
        #response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        #response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        #raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,template,{ 'prefixpath': CUSTOM_TEMPLATE_PATH,
            'startDate':entered_start_date,'endDate':entered_end_date,'useSamplingFeature':useSamplingFeature,
            'featureActionMethod':featureActionMethod,'featureActionLocation':featureActionLocation,
            'datasetTitle':datasetTitle,'datasetAbstract':datasetAbstract,'useDataset':useDataset,'startdate':startdate,'enddate':enddate,
             'SelectedResults':int_selectedresultid_ids,'authenticated':authenticated,'methods':methods,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2,'resultList': resultList,
            'graphType':graphType, 'xAxis': xAxis, 'yAxis': yAxis,'name_of_units':name_of_units,},)
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
    authenticated=True
    if not request.user.is_authenticated():
        authenticated=False
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
    pr = Results.objects.filter(resultid__in=prv).filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification"))\
        .filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
    #variables is the list to pass to the html template
    variables = Variables.objects.filter(variableid__in=pr.values("variableid"))
    fieldareas = Samplingfeatures.objects.filter(sampling_feature_type="Ecological land classification") #Field area
    xlocation=[]
    ylocation=[]
    xdata=[]
    ydata=[]
    rvx=rvy=prvx=prvy=xlocs=ylocs=None
    if xVar and yVar:
        rvx=pr.filter(variableid=xVar).values('resultid')
        prvx=Profileresultvalues.objects.filter(~Q(datavalue=-6999))\
        .filter(~Q(datavalue=-888.88)).filter(resultid__in=rvx).order_by("resultid__resultid__unitsid","resultid__resultid__featureactionid__samplingfeatureid","zlocation")
        rvy=pr.filter(variableid=yVar).values('resultid')
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
    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter',  "zoomType": 'xy',}
    title2 = {"text": title }
    #xAxis = {"categories":xAxisCategories,} #"type": 'category',"title": {"text": xAxisCategories},
    yAxis = {"title": {"text": str(yVar)}}
    xAxis = {"title": {"text": str(xVar)}}
    graphType = 'scatter'
    if 'export_data' in request.POST:
        resultValuesSeries=prvx |prvy
        response=exportspreadsheet(request,resultValuesSeries)
        return response
    return TemplateResponse(request,'soilsscatterplot.html',{'prefixpath': CUSTOM_TEMPLATE_PATH,
        'xVariables':variables, 'yVariables':variables,'authenticated':authenticated,
        'xVariableSelection':xVariableSelection,'yVariableSelection':yVariableSelection,
        'fieldarea1':fieldarea1, 'fieldarea2':fieldarea2, 'fieldareas':fieldareas,
        'chartID': chartID, 'chart': chart,'title2': title2, 'graphType':graphType,
        'yAxis': yAxis, 'xAxis': xAxis,'xdata':xdata,'ydata':ydata,'ylocation':ylocation,
        'xlocation':xlocation,'name':request.user, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': 'Soils Scatter Plot'},)

def exportcitations(request,citations,csv):
    myfile = StringIO.StringIO()
    first= True
    citationpropvalues = Citationextensionpropertyvalues.objects.filter(citationid__in=citations).order_by("propertyid")
    authorheader = Authorlists.objects.filter(citationid__in=citations).order_by("authororder").distinct("authororder")
    #MyTable.objects.extra(select={'int_name': 'CAST(t.name AS INTEGER)'},
    #                  order_by=['int_name'])
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
        if csv:
            myfile.write('\n')
        else:
            myfile.write('ER  - \r\n\r\n')
        first=False

    if csv:
        response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mycitations.csv"'
    else:
        response = HttpResponse(myfile.getvalue(),content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename="myCitationsEndNoteImport.txt"'

    return response


def exportspreadsheet(request,resultValuesSeries,profileResult=True):
    #if the user hit the export csv button export the measurement results to csv
    csvexport=True

    myfile = StringIO.StringIO()
    #raise ValidationError(resultValues)
    k=0
    variablesAndUnits=[]
    variable = ''
    unit = ''
    firstheader = True
    processingCode = None
    lastProcessingCode = None
    resultValuesHeaders = resultValuesSeries.filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification")).\
        filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area")).\
        order_by("resultid__resultid__variableid","resultid__resultid__unitsid","resultid__resultid__processing_level")#.distinct("resultid__resultid__variableid","resultid__resultid__unitsid")
    for myresults in resultValuesHeaders:
        lastVariable = variable
        variable=myresults.resultid.resultid.variableid.variablecode
        lastUnit = unit
        unit = myresults.resultid.resultid.unitsid
        lastProcessingCode = processingCode
        processingCode = myresults.resultid.resultid.processing_level
        #if not firstheader and firstVar==variable and firstUnit==unit:
            #only add the first instance of each variable, once one repeats your done.
            #break
        if not lastVariable == variable or not lastUnit==unit or not lastProcessingCode==processingCode:
            variablesAndUnits.append(unicode(variable) + unicode(unit)+unicode(processingCode))
            if firstheader:
                myfile.write(myresults.csvheader())
                firstheader = False
            myfile.write(myresults.csvheaderShort())
        #elif not lastUnit==unit:
             #myfile.write(myresults.csvheaderShortUnitOnly())
    if profileResult:
        resultValuesSeries = resultValuesSeries.filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Landscape classification")).\
            filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area")).\
            order_by("resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
                "resultid__intendedzspacing","resultid__resultid__variableid","resultid__resultid__unitsid")
    else:
         resultValuesSeries = resultValuesSeries.filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Landscape classification")).\
            filter(~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area")).\
            order_by("valuedatetime","resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
                "resultid__resultid__variableid","resultid__resultid__unitsid","resultid__resultid__processing_level")
    #myfile.write(lastResult.csvheaderShort())
    myfile.write('\n')
    lastSamplingFeatureCode=''
    samplingFeatureCode = ''
    lastDepth=0
    depth = 0
    position=0
    time = None
    lastTime = None
    nextRow = False
    #resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode
    for myresults in resultValuesSeries:
        lastVariable = variable
        variable=myresults.resultid.resultid.variableid.variablecode
        lastUnit = unit
        unit = myresults.resultid.resultid.unitsid
        lastSamplingFeatureCode = samplingFeatureCode
        samplingFeatureCode=myresults.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturecode
        lastDepth = depth
        lastProcessingCode = processingCode
        processingCode = myresults.resultid.resultid.processing_level
        if profileResult:
            depth = myresults.resultid.intendedzspacing

            if not k==0 and (not lastSamplingFeatureCode == samplingFeatureCode or not depth==lastDepth):
                myfile.write('\n')
                temp = myresults.csvoutput()
                myfile.write(temp)
                position=0
            elif k==0:
                temp = myresults.csvoutput()
                myfile.write(temp)
        else:
            lastTime = time
            time = myresults.valuedatetime
            if not k==0 and (not lastSamplingFeatureCode == samplingFeatureCode or not time==lastTime):
                myfile.write('\n')
                temp = myresults.csvoutput()
                myfile.write(temp)
                position=0
            elif k==0:
                temp = myresults.csvoutput()
                myfile.write(temp)
        #else:
        #if variablesAndUnits.index(unicode(variable)+unicode(unit)) ==position:
        for i in range(position,variablesAndUnits.index(unicode(variable)+unicode(unit)+unicode(processingCode))):
            myfile.write(",")
            position+=1
        temp=myresults.csvoutputShort()
        myfile.write(myresults.csvoutputShort())
        position+=1
        k+=1
    response = StreamingHttpResponse(myfile.getvalue(),content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    return response

def graph_data(request, selectedrelatedfeature='NotSet', samplingfeature='NotSet', popup='NotSet'):
    authenticated=True
    if not request.user.is_authenticated():
        authenticated=False
    if popup=='NotSet':
        template = loader.get_template('chartVariableAndFeature.html')
    else:
        template = loader.get_template('profileresultgraphpopup.html')
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
            #relatedFeature = Samplingfeatures.objects.filter(samplingfeatureid=selected_relatedfeatid)

    if selectedrelatedfeature != 'NotSet':
        selected_relatedfeatid = int(selectedrelatedfeature)
    else:
        selected_relatedfeatid = 15

    useSamplingFeature=False
    if samplingfeature !='NotSet':
        samplingfeature = int(samplingfeature)
        useSamplingFeature=True
    #find variables found at the sampling feature
    #need to go through featureaction to get to results
    variableList = None
    #need the feature actions for all of the sampling features related to this sampling feature
    if not useSamplingFeature:
        sampling_features = Relatedfeatures.objects.filter(relatedfeatureid__exact=selected_relatedfeatid).values('samplingfeatureid')
        #select the feature actions for all of the related features.
        feature_actions = Featureactions.objects.filter(samplingfeatureid__in = sampling_features)
    else:
        feature_actions = Featureactions.objects.filter(samplingfeatureid= samplingfeature)


    featureresults = Results.objects.filter(featureactionid__in=feature_actions).order_by("variableid","unitsid")\
        .filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification")).\
        filter(~Q(featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
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
        resultValues= Profileresultvalues.objects.all().filter(resultid__exact=selectedMResult.resultid)#.order_by("-zlocation")

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
        key = 'datavalue'+unitAndVariable
        if lastUnitAndVariable != unitAndVariable and update and key in data:
            series.append({"name":tmpUnit +' - '+tmpVariableName,"yAxis": tmpUnit, "data": data['datavalue'+unitAndVariable]}) #removewd from name +' - '+ tmpLocName
            if titleStr =='':
                titleStr = tmpVariableName
            else:
                titleStr += ' - '+ tmpVariableName
        elif i==numberofLocations and len(series)==0 and key in data:
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
    samplefeatid = Featureactions.objects.filter(featureactionid__in=results).values('samplingfeatureid')
    relatedFeatureList = Relatedfeatures.objects.filter(samplingfeatureid__in=samplefeatid).order_by('relatedfeatureid').distinct('relatedfeatureid') #
    #relatedFeatureList = sorted(relatedFeatureList, key=operator.attrgetter('relatedfeatureid__samplingfeaturecode')) #relatedFeatureList.order_by('relatedfeatureid__samplingfeaturecode')
    int_selectedvariable_ids = []
    for int_selectedvariableid in selectedMVariableSeries:
        int_selectedvariable_ids.append(int(int_selectedvariableid))
    csvexport = False
    #if the user hit the export csv button export the measurement results to csv
    if 'export_data' in request.POST:
        resultValuesSeries = resultValuesSeries.order_by("resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
                "resultid__intendedzspacing","resultid__resultid__variableid","resultid__resultid__unitsid")
        response=exportspreadsheet(request,resultValuesSeries)
        return response
    else:
        #this removes duplicates from a list of strings
        name_of_units = removeDupsFromListOfStrings(name_of_units)
        #raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,template,{'prefixpath': CUSTOM_TEMPLATE_PATH,  'variableList': variableList,
             'SelectedVariables':int_selectedvariable_ids,'authenticated':authenticated,
             'chartID': chartID, 'chart': chart,'series': series, 'title2': title2, 'graphType':graphType, 'yAxis': yAxis,'name_of_units':name_of_units,
            'relatedFeatureList': relatedFeatureList,'SelectedRelatedFeature':selected_relatedfeatid,'name':request.user,'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header, 'short_title': 'Soils Data'},)
