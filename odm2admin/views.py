import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from io import StringIO
from decimal import *
import math
import json
import time
import sys
import os
import subprocess
import re
# import pandas as pd
# import numpy
# from colour import Color
# from celery import shared_task
# import odm2admin.tasks as tasks
from urllib.parse import urlparse
from datetime import datetime
from datetime import timedelta
from time import mktime
from django import template
from django.contrib import admin
from django.db import connection
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.template import loader

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# from django.core import mail
from django.core.management.base import CommandError
from django.core import serializers
from django.core.management import settings
from templatesAndSettings.settings import exportdb
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
# from hs_restclient_helper import get_oauth_hs
from django.core import management
# from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils.crypto import get_random_string
# from django.contrib.gis.geos import GEOSGeometry
# import hs_restclient as hs_r
from hs_restclient import HydroShare, HydroShareAuthOAuth2
# from oauthlib.oauth2 import TokenExpiredError
# from oauthlib.oauth2 import InvalidGrantError, InvalidClientError

import requests
# from templatesAndSettings.settings import CUSTOM_TEMPLATE_PATH
# from templatesAndSettings.settings import DATA_DISCLAIMER as DATA_DISCLAIMER
# from templatesAndSettings.settings import MAP_CONFIG as MAP_CONFIG
# from templatesAndSettings.settings import RECAPTCHA_PRIVATE_KEY
from .models import Actions
from .models import Annotations
from .models import Authorlists
from .models import Citationextensionpropertyvalues
from .models import Citations
from .models import CvQualitycode
from .models import CvAnnotationtype
from .models import Dataloggerfiles
from .models import Datasetcitations
from .models import Datasets
from .models import Datasetsresults
from .models import Featureactions
from .models import Methods
from .models import People
from .models import Processinglevels
from .models import Profileresults
from .models import Profileresultvalues
from .models import ProcessDataloggerfile
from .models import Relatedfeatures
from .models import Results
from .models import Samplingfeatureextensionpropertyvalues
from .models import Samplingfeatureexternalidentifiers
from .models import Samplingfeatures
from .models import Sites
from .models import Specimens
from .models import Timeseriesresultvalues
from .models import Timeseriesresultvaluesext
from .models import Timeseriesresultvaluesextwannotations
from .models import Timeseriesresultvalueannotations
from .models import Units
from .models import Variables
from .models import Timeseriesresults
from .models import Resultextensionpropertyvalues
from .models import Extensionproperties
# from .forms import LoginForm
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login


register = template.Library()

__author__ = 'leonmi'


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

# class CreatePubView(FormView):
#    template_name = "publications2.html"
#    model = Citations
#
#
# def add_pub(request,citationid='NotSet'):
#     if request.user.is_authenticated():
#         #if 'citationidnew' in request.POST:
#             #if not request.POST['citationidnew'] == '':
#                 #citationid = int(request.POST['citationidnew'])
#                 #citationidnew = citationid
#         AuthorInlineFormSet = inlineformset_factory(Citations,Authorlists,extra=6)
#
#         CitationpropertyInlineFormSet = inlineformset_factory(Citations,
# Citationextensionpropertyvalues)
#         #citation_form=CitationsAdminForm(request.POST,instance=citation)
#         if request.method=="POST":
#             if 'delete_citation' in request.POST:
#                 citation= Citations.objects.filter(citationid=citationid).get()
#                 citation.delete()
#                 return HttpResponseRedirect('../../publications.html')
#             if citationid == 'NotSet':
#                 citation= Citations(title=request.POST['title'],
# publisher=request.POST['publisher'],
# publicationyear=int(request.POST['publicationyear']),citationlink=request.POST['citationlink'])
#                 #if citation.is_valid():
#                 citation.save()
#                 citationid=citation.citationid
#                 citation_form=CitationsAdminForm(request.POST,instance=citation)
#             else:
#                 citation= Citations.objects.filter(citationid=citationid).get()
#                 citation_form=CitationsAdminForm(request.POST,instance=citation)
#             #citation= Citations.objects.filter(citationid=citationid).get()
#             Authorformset=AuthorInlineFormSet(request.POST,instance=citation)
#
#             Citationpropertyformset = CitationpropertyInlineFormSet
# (request.POST,instance=citation)
#
#             if Authorformset.is_valid():
#                 try:
#                     Authorformset.save()
#                 except IntegrityError:
#                     pass
#             if Citationpropertyformset.is_valid():
#                 Citationpropertyformset.save()
#             #for form in CitationPorpertyformset:
#                 #if form.changed_data.__len__() > 0:
#                     #form.save()
#             if citation_form.is_valid():
#                 citation_form.save()
#             return HttpResponseRedirect('../../pubview/citationid=' + str(citationid) +'/')
#         elif not citationid=='NotSet':
#             citation= Citations.objects.filter(citationid=citationid).get()
#             Authorformset = AuthorInlineFormSet(instance=citation)
#
#             #Authorformset.empty_permitted=False
#             Citationpropertyformset = CitationpropertyInlineFormSet(instance=citation)
#             #CitationPorpertyformset.empty_permitted=True
#             citation_form=CitationsAdminForm(instance=citation)
#         else:
#             AuthorInlineFormSet = inlineformset_factory(Citations,Authorlists,extra=6)
#             CitationpropertyInlineFormSet = inlineformset_factory(Citations,
# Citationextensionpropertyvalues,extra=8)
#             Authorformset=AuthorInlineFormSet(instance=Authorlists())
#             # i=1
#             # for form in Authorformset:
#             #     form.fields['authororder'].initial = i
#             #     i+=1
#             Citationpropertyformset = CitationpropertyInlineFormSet
# (instance=Citationextensionpropertyvalues())
#             citation_form=CitationsAdminForm(instance=Citations())
#             citationidnew=''
#         i=1
#         for form in Authorformset:
#             if form.fields['authororder'].initial == None:
#                 form.fields['authororder'].initial = i
#             i+=1
#         #for form in Citationpropertyformset:
#
#             #if  'propertyid' in form.initial: #not propertyid==None
#                 #propertyid = form.initial['propertyid'] #.initial #type number
#                 #extensionprop = Extensionproperties.objects.filter(propertyid=propertyid).get()
#                 #name = extensionprop.propertydatatypecv
#                 #typecv = CvPropertydatatype.objects.filter(name=name.name).get()
#                 #if typecv.name == "Boolean":
#                     #form.fields['propertyvalue'].widget = widgets.CheckboxInput
#                     #form.fields['propertyvalue']= models.BooleanField()
#             #elif citationid=='NotSet':
#
#             #if form.fields['authororder'].initial == None:
#
#         return render(request, 'publications3.html', {'Authorformset':Authorformset,
# 'Citationpropertyformset':Citationpropertyformset,'citation_form':citation_form,})
#     else:
#         return HttpResponseRedirect('../../')
# def add_pub(request,citation='NotSet'):
#     #citation_form
#     #author_form
#     #citation_property_form
#     author_forms= []
#     citation_property_forms=[]
#     if request.method=="POST":
#         citation_form=CitationsAdminForm(request.POST,instance=Citations())
#         author_forms=[AuthorlistsAdminForm(request.POST,prefix=str(x),
# instance=Authorlists()) for x in range(0,3)]
#         citation_property_forms=[CitationextensionpropertyvaluesAdminForm(request.POST,
# prefix=str(x),instance=Citationextensionpropertyvalues())for x in range(0,3)]
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
#         citation_form=CitationsAdminForm(instance=Citations.objects.filter(citationid=citation)
# .get())
#         authors = Authorlists.objects.filter(citationid=citation)
#         for auth in authors:
#             author_forms.append(AuthorlistsAdminForm(instance=auth))
#         cepvs= Citationextensionpropertyvalues.objects.filter(citationid=citation)
#         for cepv in cepvs:
#             citation_property_forms.append(CitationextensionpropertyvaluesAdminForm(instance=cepv))
#     else:
#         citation_form=CitationsAdminForm(instance=Citations())
#         author_forms=[AuthorlistsAdminForm(prefix=str(x),
# instance=Authorlists()) for x in range(0,3)]
#         citation_property_forms=[CitationextensionpropertyvaluesAdminForm(prefix=str(x),
# instance=Citationextensionpropertyvalues()) for x in range(0,3)]
#     return TemplateResponse(request, 'publications2.html',{'citation_form':citation_form,
# 'author_forms':author_forms,'citation_property_forms':citation_property_forms,})

@login_required()
def oauth_view(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

def publications(request):
    # if request.user.is_authenticated():
    citationList = Citations.objects.all()
    authList = Authorlists.objects.all()
    peopleList = People.objects.filter(personid__in=authList.values("personid"))
    selectedTag = 'CZO Authors'
    selectedAuthor = 'All'

    if 'filterTags' in request.POST:
        if not request.POST['filterTags'] == 'All':
            selectedTag = request.POST['filterTags']
            if request.POST['filterTags'] == 'CZO Authors':
                citationList = Citations.objects.filter(
                    citationid__in=authList.values("citationid"))
            else:
                citationList = Citations.objects.filter(publisher__icontains=selectedTag)
        else:
            selectedTag = 'All'
    else:
        citationList = Citations.objects.filter(citationid__in=authList.values("citationid"))

    if 'selectedAuthor' in request.POST:
        if not request.POST['selectedAuthor'] == 'All':
            selectedAuthor = int(request.POST['selectedAuthor'])
            authored = Authorlists.objects.filter(personid=selectedAuthor)
            citationList = citationList.filter(citationid__in=authored.values("citationid"))

    filterTags = ['CZO Authors', 'All', 'AGU', 'LCZO Meeting']

    citationCategories = Citationextensionpropertyvalues.objects.filter(propertyid=5).distinct(
        "propertyvalue")  # citation category Extensionproperties
    selectedCategory = None
    if 'citationCategories' in request.POST:
        if not request.POST['citationCategories'] == 'All':
            selectedCategory = request.POST['citationCategories']
            citationPropValueFilter = Citationextensionpropertyvalues.objects.filter(
                propertyvalue__icontains=selectedCategory)
            citationList = citationList.filter(
                citationid__in=citationPropValueFilter.values("citationid"))
        else:
            selectedCategory = 'All'
    # context = {'prefixpath': CUSTOM_TEMPLATE_PATH}
    if 'export_data' in request.POST:
        response = exportcitations(request, citationList, True)
        return response
    if 'export_endnote' in request.POST:
        response = exportcitations(request, citationList, False)
        return response
    return TemplateResponse(request, 'publications.html',
                            {'citationList': citationList, 'authList': authList,
                             'filterTags': filterTags,
                             'citationCategories': citationCategories,
                             'selectedCategory': selectedCategory,
                             'selectedTag': selectedTag, 'peopleList': peopleList,
                             'selectedAuthor': selectedAuthor,
                             'prefixpath': settings.CUSTOM_TEMPLATE_PATH})


# ======================= SHORTCUTS =========================================
def AddSensor(request):
    if request.user.is_authenticated:
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][1]['title']}
        return TemplateResponse(request, 'AddSensor.html', context)
    else:
        return HttpResponseRedirect('../')

@login_required()
def chartIndex(request):
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'featureaction': settings.SENSOR_DASHBOARD['featureactionids'][0],
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][5]['title']}
        return TemplateResponse(request, 'chartIndex.html', context)



# chartIndex
def AddProfile(request):
    if request.user.is_authenticated:
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][2]['title']}
        return TemplateResponse(request, 'AddProfile.html', context)
    else:
        return HttpResponseRedirect('../')



def RecordAction(request):
    if request.user.is_authenticated:
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][3]['title']}
        return TemplateResponse(request, 'RecordAction.html', context)
    else:
        return HttpResponseRedirect('../')


def ManageCitations(request):
    if request.user.is_authenticated:
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][4]['title']}
        return TemplateResponse(request, 'ManageCitations.html', context)
    else:
        return HttpResponseRedirect('../')


###################################################################
# #
# def dataloggerfilesView(request, id):
#      #model = Dataloggerfiles
#      #template_name = 'admin/odm2testapp/dataloggerfiles/change_form.html'
# #'DataloggerfilecolumnsDisplay.html'
#      DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.filter(dataloggerfileid=id)
#      DataloggerfilecolumnsListvalues =  str(DataloggerfilecolumnsList.values())
#      #raise ValidationError(DataloggerfilecolumnsListvalues)
#      DataloggerfilecolumnsListvalues= DataloggerfilecolumnsList
# #DataloggerfilecolumnsListvalues.split('\'')
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
    title_feature_action = Featureactions.objects.filter(
        featureactionid=selected_result.featureactionid.featureactionid).get()
    title_sampling_feature = Samplingfeatures.objects.filter(
        samplingfeatureid=title_feature_action.samplingfeatureid.samplingfeatureid).get()
    s = str(title_sampling_feature.samplingfeaturename)
    return s


def get_name_of_variable(selected_result):
    title_variables = Variables.objects.filter(variableid=selected_result.variableid)
    # s = str(title_variables.values_list('variablecode', flat=True))
    name_of_variable = title_variables.variablecode # s.split('\'')[1]
    return name_of_variable


def get_name_of_units(selected_result):
    title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
    # s = str(title_units.values_list('unitsname', flat=True))
    name_of_units = title_units.unitsname # s.split('\'')[1]
    return name_of_units


def relatedFeaturesFilter(request, done, selected_resultid, featureaction,
                          resultType='Time series coverage', ):
    # selected_relatedfeatid = 18
    if 'SelectedRelatedFeature' in request.POST and 'update_result_list' not in request.POST:
        if not request.POST['SelectedRelatedFeature'] == 'All':
            done = True
            selected_relatedfeatid = int(request.POST['SelectedRelatedFeature'])
            relatedFeatureList = Relatedfeatures.objects.filter(
                relatedfeatureid=int(selected_relatedfeatid)).distinct(
                'relatedfeatureid')
            relatedFeatureListLong = Relatedfeatures.objects.filter(relatedfeatureid=int(
                selected_relatedfeatid))
            # .select_related('samplingfeatureid','relationshiptypecv','relatedfeatureid')
            samplingfeatids = relatedFeatureListLong.values_list('samplingfeatureid', flat=True)
            if featureaction == 'All':
                resultList = Results.objects.filter(
                    featureactionid__in=Featureactions.objects.filter(
                        samplingfeatureid__in=samplingfeatids))
                # .select_related('variable','feature_action')
            else:
                resultList = Results.objects.filter(
                    featureactionid__in=Featureactions.objects.filter(
                        samplingfeatureid__in=samplingfeatids)).filter(
                    featureactionid=featureaction)
            if 'update_result_on_related_feature' in request.POST:
                # raise ValidationError(relatedFeatureList)
                selected_relatedfeatid = relatedFeatureList[0].relatedfeatureid.samplingfeatureid
                selected_resultid = resultList[0].resultid
        else:
            selected_relatedfeatid = request.POST['SelectedRelatedFeature']
            if featureaction == 'All':
                resultList = Results.objects.filter(
                    result_type=resultType)  # remove slice just for testing [:25]
            else:
                resultList = Results.objects.filter(result_type=resultType).filter(
                    featureactionid=featureaction)
    else:
        selected_relatedfeatid = 'All'
        if featureaction == 'All':
            resultList = Results.objects.filter(
                result_type=resultType)  # remove slice just for testing [:25]
        else:
            resultList = Results.objects.filter(result_type=resultType).filter(
                featureactionid=featureaction)
    return selected_relatedfeatid, done, resultList, selected_resultid


def web_map(request):
    if request.user.is_authenticated:
        authenticated = True
    else:
        authenticated = False
    map_config = settings.MAP_CONFIG
    data_disclaimer = settings.DATA_DISCLAIMER

    features = Samplingfeatures.objects.all()

    datasets = Datasets.objects.all()
    externalidentifiers = None
    ids = [ds.datasetid for ds in datasets]

    sf_type_list = [sf.sampling_feature_type for sf in features]
    sf_types = set(sf_type_list)
    terms = [sf_type.name for sf_type in sf_types]

    ds_selections = request.POST.getlist('datasetselection')

    if ds_selections != []:
        selected_ds = []
        for ds in ds_selections:
            selected_ds.append(int(ds))
    else:
        selected_ds = ids

    sftype_selections = request.POST.getlist('sftypeselection')
    if sftype_selections != []:
        selected_type = []
        for sf in sftype_selections:
            selected_type.append(sf)
    else:
        selected_type = terms

    legend_ref = [ settings.LEGEND_MAP[sftype] for sftype in map_config['feature_types']]

    base_maps = [
        {
            'name': 'Esri_NatGeoWorldMap',
            'url': 'http://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/'
                   'MapServer/tile/{z}/{y}/{x}',
            'options': {
                'attribution': 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, '
                               'NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, '
                               'iPC',
                'maxZoom': 16
            },
            'group': 'ESRI Basemaps'
        },
        {
            'name': 'Esri_WorldImagery',
            'url': 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/'
                   'MapServer/tile/{z}/{y}/{x}',
            'options': {
                'attribution': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, '
                               'AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the '
                               'GIS User Community'
            },
            'group': 'ESRI Basemaps'
        },
        {
            'name': 'Esri_WorldTopoMap',
            'url': 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/'
                   'MapServer/tile/{z}/{y}/{x}',
            'options': {
                'attribution': 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, '
                               'Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, '
                               'Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and '
                               'the GIS User Community'
            },
            'group': 'ESRI Basemaps'
        },
        {
            'name': 'MapBox_RunBikeHike',
            'url': 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?'
                   'access_token={accessToken}',
            'options': {
                'maxZoom': 20,
                'attribution': 'Map data &copy; '
                               '<a href="http://openstreetmap.org">OpenStreetMap</a> '
                               'contributors, <a href="http://creativecommons.org/licenses/'
                               'by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; '
                               '<a href="http://mapbox.com">Mapbox</a>',
                'id': 'mapbox.run-bike-hike',
                'accessToken': map_config['MapBox']['access_token']
            },
            'group': 'OpenStreetMap Basemaps'
        }
    ]

    context = {
        'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'legends': json.dumps(legend_ref),
        'features': features,
        'externalidentifiers': externalidentifiers,
        'datasets': datasets, 'selecteddatasets': selected_ds, 'authenticated': authenticated,
        'map_config': map_config,
        'data_disclaimer': data_disclaimer, 'name': request.user,
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header, 'short_title': 'Map Locations',
        'basemaps': base_maps, 'sf_types': sf_types, 'selectedterms': selected_type,
        'selectedds': json.dumps(ds_selections), 'selectedtype': json.dumps(sftype_selections),
        'urlpath': settings.BASE_URL
    }
    return render(request, 'mapdata.html', context)


def get_features(request, sf_type="all", ds_ids="all"):
    if ds_ids == "all" or sf_type == "all":
        features = Samplingfeatures.objects.exclude(featuregeometry__isnull=True)
    elif sf_type == 'filtered':
        dataset_ids = list(ds_ids.split(','))
        datasetresults = Datasetsresults.objects.filter(datasetid__in=dataset_ids)
        results = Results.objects.filter(resultid__in=datasetresults.values("resultid"))

        fa = Featureactions.objects.filter(featureactionid__in=results.values("featureactionid"))
        features1 = Samplingfeatures.objects.filter(
            samplingfeatureid__in=fa.values("samplingfeatureid"))
        relatedfeatures = Relatedfeatures.objects.filter(
            samplingfeatureid__in=features1.values("samplingfeatureid"))
        features2 = Samplingfeatures.objects.filter(
            samplingfeatureid__in=relatedfeatures.values("relatedfeatureid"))
        features = features1 | features2
    elif ds_ids == 'filtered':
        samplingfeature_types = list(sf_type.split(','))
        if 'Site' in samplingfeature_types:
            pass
        features = Samplingfeatures.objects.filter(sampling_feature_type__in=samplingfeature_types)
    else:
        features = []

    feats = [model_to_dict(f) for f in features]
    feats_filtered = list()
    for feat in feats:
        sf = Samplingfeatures.objects.get(samplingfeatureid=feat['samplingfeatureid'])

        # Get url to sf
        feat.update({
            'samplingfeatureurl': 'odm2admin/samplingfeatures/{}/change/'.format(sf.samplingfeatureid),
            'samplingfeaturetypeurl': sf.sampling_feature_type.sourcevocabularyuri
        })

        # Get Site Attr
        if sf.sampling_feature_type.name == 'Site':
            try:
                site = Sites.objects.get(samplingfeatureid=sf.samplingfeatureid)
                feat.update({
                    'sitetype': site.sitetypecv.name,
                    'sitetypeurl': site.sitetypecv.sourcevocabularyuri
                })
            except Sites.DoesNotExist:
                site = None

        # Get Specimen Attr
        if sf.sampling_feature_type.name == 'Specimen':
            try:
                specimen = Specimens.objects.get(samplingfeatureid=sf.samplingfeatureid)
                feat.update({
                    'specimentype': specimen.specimentypecv.name,
                    'specimentypeurl': specimen.specimentypecv.sourcevocabularyuri,
                    'specimenmedium': specimen.specimenmediumcv.name,
                    'specimenmediumurl': specimen.specimenmediumcv.sourcevocabularyuri,
                })
            except Specimens.DoesNotExist:
                specimen = None
        # Get Relations
        relationship = get_relations(sf)
        if all(value == [] for value in relationship.values()):
            feat.update({
                'relationships': None
            })
        else:
            feat.update({
                'relationships': relationship
            })

        # Get IGSN's
        if Samplingfeatureexternalidentifiers.objects.filter(
                samplingfeatureid=sf.samplingfeatureid).first() is not None:
            igsn = sf.samplingfeatureexternalidentifiers_set.get()
            feat.update({
                'igsn': igsn.samplingfeatureexternalidentifier,
                'igsnurl': igsn.samplingfeatureexternalidentifieruri
            })


        # Get Soil top and bottom depth
        if Samplingfeatureextensionpropertyvalues.objects.filter(
                samplingfeatureid=sf.samplingfeatureid).first() is not None:
            sfep = sf.samplingfeatureextensionpropertyvalues_set.get_queryset()
            if len(sfep) != 0:
                for ep in sfep:
                    feat.update({
                        '{}'.format(ep.propertyid.propertyname): ep.propertyvalue,
                        '{}_units'.format(ep.propertyid.propertyname): ep.propertyid.propertyunitsid.unitsabbreviation,
                    })
        # Get lat, lon
        lat = sf.featuregeometrywkt().coords[1]
        lon = sf.featuregeometrywkt().coords[0]
        epsg = None
        if sf.featuregeometrywkt().crs is not None:
            epsg = sf.featuregeometrywkt().crs.srid
        if lat != 0 and lon != 0:
            feat['featuregeometry'] = {
                'lat': lat,
                'lng': lon,
                'crs': epsg
            }
            feats_filtered.append(feat)

    return HttpResponse(json.dumps(feats_filtered))

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def sensor_dashboard(request, feature_action='NotSet', sampling_feature='NotSet'):
    authenticated = True
    if not request.user.is_authenticated:
        # return HttpResponseRedirect('../')
        authenticated = False
    ids = settings.SENSOR_DASHBOARD['featureactionids']
    timeseriesdays = settings.SENSOR_DASHBOARD['time_series_days']
    fas = None
    allfas = None
    if not feature_action == 'NotSet':
        selected_featureactionid = int(feature_action)
        # print(selected_featureactionid)
        fas = Featureactions.objects.filter(featureactionid=selected_featureactionid
                                        ).order_by('-samplingfeatureid')
        allfas = Featureactions.objects.filter(featureactionid__in=ids).order_by('-samplingfeatureid')
    elif not sampling_feature == 'NotSet':
        selected_featureactionid = 'NotSet'
        samplingfeatureid = int(sampling_feature)
        fas = Featureactions.objects.filter(samplingfeatureid=samplingfeatureid
                                        ).order_by('-samplingfeatureid')
        allfas = Featureactions.objects.filter(featureactionid__in=ids).order_by('-samplingfeatureid')
    else:
        selected_featureactionid = 'NotSet'
        # print(selected_featureactionid)
        fas = Featureactions.objects.filter(featureactionid__in=ids).order_by('-samplingfeatureid')
        allfas = fas
    #samplingfeatures = Samplingfeatures.filter(samplingfeatureid__in=fas)
    results = Results.objects.filter(featureactionid__in=fas)
    tsrs = Timeseriesresults.objects.filter(resultid__in=results)
    endDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    #calculated_result_properties={}
    #for tsr in tsrs:
        #print(tsr)
    repvs = Resultextensionpropertyvalues.objects.filter(resultid__in=results).order_by("resultid","propertyid")
    dcount = 0
    dmaxcount = 0
    lastResult = None
    for repv in repvs:
        # print(repv.resultid)
        if "start date" in str(repv.propertyid.propertyname):
            startdate = repv.propertyvalue
            repv.propertyname = "Time series began on: "
        elif "end date" in str(repv.propertyid.propertyname):
            enddate = repv.propertyvalue
            # (enddate)
            repv.propertyname = "most recent value on: "
        elif "dashboard count" in str(repv.propertyid.propertyname):
            dcount = repv.propertyvalue
            repv.propertyname = "number of values recorded over last " + str(timeseriesdays) + " days"
        elif "dashboard maximum count" in str(repv.propertyid.propertyname):
            dmaxcount = repv.propertyvalue
            # print(dcount)
            # print(dmaxcount)
            # repv.propertyname = str(dcount) + " of " + str(dmaxcount)
            repv.propertyname = "up time"
            if float(dmaxcount) > 0:
                repv.propertyvalue = str(dcount) + " of " + str(dmaxcount) + \
                                     " or " + str(truncate((float(dcount)/float(dmaxcount))*100, 2)) + "%"
            # else:
                # print("dmaxcount less then 0")
                # print(repv)
                # print(repv.resultid)
        elif "dashboard below lower bound count" in  str(repv.propertyid.propertyname):
            repv.propertyname = "values below lower bound "
        elif "dashboard above upper bound count" in  str(repv.propertyid.propertyname):
            repv.propertyname = "values above upper bound "
        #dashboard last recorded value
        elif "dashboard sensor active" in str(repv.propertyid.propertyname):
            repv.propertyname = "sensor active "
        elif "dashboard last recorded value" in str(repv.propertyid.propertyname):
            repv.propertyname = "last recorded value "
        elif "dashboard begin date" in  str(repv.propertyid.propertyname):
            repv.propertyname = "values above upper bound "
            repv.propertyvalue = None
        else:
            repv.propertyname = repv.propertyid.propertyname

        lastResult = repv.resultid
    return TemplateResponse(request,
        'sensordashboard.html',
        {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
         'featureactions':fas,
         'allfeatureactions':allfas,
         'results': results,
         'feature_action': selected_featureactionid,
         'authenticated': authenticated,
         'resultextionproperties':repvs,
         'short_title': 'Time Series'}, )

def get_relations(s):
    pf = Relatedfeatures.objects.filter(samplingfeatureid_id=s.samplingfeatureid)
    cf = Relatedfeatures.objects.filter(relatedfeatureid_id=s.samplingfeatureid)
    sibsf = []
    parents = []
    children = []
    if pf.first() is not None:
        sib = Relatedfeatures.objects.filter(relationshiptypecv_id='Is child of',
                                             relatedfeatureid_id=pf.first().relatedfeatureid_id). \
            exclude(samplingfeatureid_id=s.samplingfeatureid)
        if sib.first() is not None:
            sibsf = list(Samplingfeatureexternalidentifiers.objects.\
                         filter(samplingfeatureid__in=sib.\
                                values_list('samplingfeatureid_id', flat=True)). \
                         values('samplingfeatureexternalidentifieruri',
                                'samplingfeatureid__samplingfeaturecode',
                                'samplingfeatureid__samplingfeatureid',
                                'samplingfeatureexternalidentifier'
                                ))
        parents = list(Samplingfeatureexternalidentifiers.objects.\
                       filter(samplingfeatureid__in=pf.\
                              values_list('relatedfeatureid_id',
                                          flat=True)).\
                       values('samplingfeatureexternalidentifieruri',
                              'samplingfeatureid__samplingfeaturecode',
                              'samplingfeatureid__samplingfeatureid',
                              'samplingfeatureexternalidentifier'
                              ))

    if cf.first() is not None:
        children = list(Samplingfeatureexternalidentifiers.objects.\
                        filter(samplingfeatureid__in=cf.\
                               values_list('samplingfeatureid_id', flat=True)). \
                        values('samplingfeatureexternalidentifieruri',
                               'samplingfeatureid__samplingfeaturecode',
                               'samplingfeatureid__samplingfeatureid',
                               'samplingfeatureexternalidentifier'
                               ))


    return {
        'parents': parents,
        'siblings': sibsf,
        'children': children
    }


def TimeSeriesGraphing(request, feature_action='All'):
    authenticated = True
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../')

    template = loader.get_template('chart.html')
    selected_relatedfeatid = None
    selected_resultid = None
    if feature_action == 'All':
        selected_featureactionid = 1
        result = Results.objects.filter(featureactionid=selected_featureactionid).first()
        selected_resultid = result.resultid

        selected_relatedfeatid = selected_resultid
    else:
        selected_featureactionid = int(feature_action)

    # relatedfeatureList
    # update_result_on_related_feature
    done = False
    selected_relatedfeatid, done, \
        resultList, selected_resultid = relatedFeaturesFilter(request,
                                                              done,
                                                              selected_relatedfeatid,
                                                              selected_resultid,
                                                              feature_action)

    if 'SelectedFeatureAction' in request.POST and not done:
        # raise ValidationError(done)
        if not request.POST['SelectedFeatureAction'] == 'All':
            selected_featureactionid = int(request.POST['SelectedFeatureAction'])
            resultList = Results.objects.filter(featureactionid=selected_featureactionid)
            if 'update_result_list' in request.POST:
                pass
        else:
            selected_featureactionid = request.POST['SelectedFeatureAction']
            resultList = Results.objects.filter(result_type="Time series coverage")
    elif not done:
        resultList = Results.objects.filter(featureactionid=selected_featureactionid)

    # find the measurement results series that where selected.
    numresults = resultList.count()
    selectedMResultSeries = []
    for i in range(0, numresults):
        selectionStr = str('selection' + str(i))
        if selectionStr in request.POST:
            # raise ValidationError(request.POST[selectionStr])
            for result in resultList:
                if int(request.POST[selectionStr]) == result.resultid:
                    selectedMResultSeries.append(int(request.POST[selectionStr]))
                    # if 'selection0' in request.POST:
                    # raise ValidationError(request.POST['selection0'] + ' '+
                    # request.POST['selection1'])
                    # selected_resultid = request.POST['selection0']
                    # else:
                    # selected_resultid = 15
    # if no series were selected (like on first load) set the series to some value.
    if len(resultList) > 0 and len(selectedMResultSeries) == 0:
        selectedMResultSeries.append(int(resultList[0].resultid))
    elif len(resultList) == 0 and len(selectedMResultSeries) == 0:
        selectedMResultSeries.append(15)
    EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
    else:
        # entered_start_date = "2016-01-01"
        recordedenddate = Resultextensionpropertyvalues.objects.\
            filter(resultid=selected_resultid).filter(propertyid=EndDateProperty.propertyid).get()
        end_date = recordedenddate.propertyvalue
        enddt = time.strptime(end_date, "%Y-%m-%d %H:%M:%S.%f")
        dt = datetime.fromtimestamp(mktime(enddt))
        last_day_previous_month = dt - timedelta(days=30)
        entered_start_date = last_day_previous_month.strftime('%Y-%m-%d %H:%M')
        print(entered_start_date)
    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        recordedenddate = Resultextensionpropertyvalues.objects.\
            filter(resultid=selected_resultid).filter(propertyid=EndDateProperty.propertyid).get()
        entered_end_date = recordedenddate.propertyvalue
    if entered_end_date == '':
        recordedenddate = Resultextensionpropertyvalues.objects.\
            filter(resultid=selected_resultid).filter(propertyid=EndDateProperty.propertyid).get()
        entered_end_date = recordedenddate.propertyvalue
    if entered_start_date == '':
        recordedenddate = Resultextensionpropertyvalues.objects.\
            filter(resultid=selected_resultid).filter(propertyid=EndDateProperty.propertyid).get()
        end_date = recordedenddate.propertyvalue
        enddt = time.strptime(end_date, "%Y-%m-%d %H:%M:%S.%f")
        dt = datetime.fromtimestamp(mktime(enddt))
        last_day_previous_month = dt - timedelta(days=30)
        entered_start_date = last_day_previous_month.strftime('%Y-%m-%d %H:%M')
        # entered_start_date = "2016-01-01"

    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []

    myresultSeries = []
    i = 0
    data = {}

    for selectedMResult in selectedMResultSeries:
        i += 1
        selected_result = Results.objects.filter(resultid=selectedMResult).get()
        selected_results.append(selected_result)
        # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        name_of_sampling_features.append(tmpname)

        tmpname = get_name_of_variable(selected_result)
        if name_of_variables.__len__() > 0:
            namefound = False
            for name in name_of_variables:
                if name == tmpname:
                    namefound = True
            if not namefound:
                name_of_variables.append(tmpname)
            else:
                name_of_variables.append('')
        else:
            name_of_variables.append(tmpname)

        tmpname = get_name_of_units(selected_result)
        if name_of_units.__len__() > 0:
            namefound = False
            for name in name_of_units:
                if name == tmpname:
                    namefound = True
            if not namefound:
                name_of_units.append(tmpname)
            else:
                name_of_units.append('')
        else:
            name_of_units.append(tmpname)

        myresultSeries.append(Timeseriesresultvalues.objects.all().filter(
            ~Q(datavalue__lte=-6999)).filter(
            valuedatetime__gt=entered_start_date).filter(
            valuedatetime__lt=entered_end_date).filter(
            resultid=selectedMResult).order_by('-valuedatetime'))

        data.update({'datavalue' + str(i): []})

    myresultSeriesExport = Timeseriesresultvalues.objects.all() \
        .filter(valuedatetime__gt=entered_start_date) \
        .filter(valuedatetime__lt=entered_end_date) \
        .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
    i = 0

    for myresults in myresultSeries:
        i += 1
        for result in myresults:
            start = datetime(1970, 1, 1)
            delta = result.valuedatetime - start
            mills = delta.total_seconds() * 1000
            if math.isnan(result.datavalue):
                dataval = 'null'
            else:
                dataval = result.datavalue
            data['datavalue' + str(i)].append(
                [mills, dataval])
            # data['datavalue' + str(i)].append([mills, result.datavalue])
            # #dumptoMillis(result.valuedatetime)
            # data['datavalue'].extend(tmplist )
            # data['valuedatetime'].append(dumptoMillis(result.valuedatetime))

    # build strings for graph labels
    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    tmpUnit = ''
    tmpVariableName = ''
    tmpLocName = ''
    for name_of_unit, name_of_sampling_feature, name_of_variable in zip(name_of_units,
                                                                        name_of_sampling_features,
                                                                        name_of_variables):
        i += 1
        if i == 1 and not name_of_unit == '':
            seriesStr += name_of_unit
        elif not name_of_unit == '':
            tmpUnit = name_of_unit
            seriesStr += ' - ' + name_of_unit
        if not name_of_variable == '':
            tmpVariableName = name_of_variable
        if not name_of_unit == '':
            tmpUnit = name_of_unit
        if not name_of_sampling_feature == '':
            tmpLocName = name_of_sampling_feature
        series.append(
            {"name": tmpUnit + ' - ' + tmpVariableName + ' - ' + tmpLocName, "yAxis": tmpUnit,
             "data": data['datavalue' + str(i)]})
    i = 0
    name_of_sampling_features = set(name_of_sampling_features)

    for name_of_sampling_feature in name_of_sampling_features:
        i += 1
        if i == 1:
            titleStr += name_of_sampling_feature  # + ', ' +name_of_variable
        else:
            titleStr += ' - ' + name_of_sampling_feature  # +name_of_variable+ ', '

    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter', "zoomType": 'xy'}
    title2 = {"text": titleStr}
    xAxis = {"type": 'datetime', "title": {"text": 'Date'}}
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'scatter'

    actionList = Actions.objects.filter(
        action_type="Observation")  # where the action is not of type estimation
    # assuming an estimate is a single value.
    featureactionList = Featureactions.objects.filter(action__in=actionList)
    relatedFeatureList = Relatedfeatures.objects.distinct(
        'relatedfeatureid')  # .order_by('relatedfeatureid')
    int_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
    csvexport = False
    # if the user hit the export csv button export the measurement results to csv

    if 'export_data' in request.POST:
        # if request.get('export_data'):
        response = exportspreadsheet(request, myresultSeriesExport, False)
        csvexport = True
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
    # response = HttpResponse(myfile.getvalue(),content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        # raise ValidationError(relatedFeatureList)
        return TemplateResponse(request,
                                template,
                                {'featureactionList': featureactionList,
                                 'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                 'data_disclaimer': settings.DATA_DISCLAIMER,
                                 'resultList': resultList,
                                 'startDate': entered_start_date,
                                 'endDate': entered_end_date,
                                 'SelectedResults': int_selectedresultid_ids,
                                 'authenticated': authenticated,
                                 'chartID': chartID, 'chart': chart,
                                 'series': series, 'title2': title2,
                                 'graphType': graphType, 'xAxis': xAxis,
                                 'yAxis': yAxis, 'name_of_units': name_of_units,
                                 'relatedFeatureList': relatedFeatureList,
                                 'SelectedRelatedFeature': selected_relatedfeatid,
                                 'SelectedFeatureAction': selected_featureactionid,
                                 'name': request.user,
                                 'site_title': admin.site.site_title,
                                 'site_header': admin.site.site_header,
                                 'short_title': 'Time Series'}, )

    template = loader.get_template('chart.html')
    selected_relatedfeatid = None
    selected_resultid = None
    if feature_action == 'All':
        selected_featureactionid = 1
        result = Results.objects.filter(featureactionid=selected_featureactionid).first()
        selected_resultid = result.resultid
        selected_relatedfeatid = selected_resultid
    else:
        selected_featureactionid = int(feature_action)

    # relatedfeatureList
    # update_result_on_related_feature
    done = False
    selected_relatedfeatid, done, \
        resultList, selected_resultid = relatedFeaturesFilter(
            request, done, selected_relatedfeatid,
            selected_resultid, feature_action
        )

    if 'SelectedFeatureAction' in request.POST and not done:
        # raise ValidationError(done)
        if not request.POST['SelectedFeatureAction'] == 'All':
            selected_featureactionid = int(request.POST['SelectedFeatureAction'])
            resultList = Results.objects.filter(featureactionid=selected_featureactionid)
            if 'update_result_list' in request.POST:
                pass
        else:
            selected_featureactionid = request.POST['SelectedFeatureAction']
            resultList = Results.objects.filter(result_type="Time series coverage")
    elif not done:
        resultList = Results.objects.filter(featureactionid=selected_featureactionid)

    # find the measurement results series that where selected.
    numresults = resultList.count()
    selectedMResultSeries = []
    for i in range(0, numresults):
        selectionStr = str('selection' + str(i))
        if selectionStr in request.POST:
            # raise ValidationError(request.POST[selectionStr])
            for result in resultList:
                if int(request.POST[selectionStr]) == result.resultid:
                    selectedMResultSeries.append(int(request.POST[selectionStr]))
                    # if 'selection0' in request.POST:
                    # raise ValidationError(request.POST['selection0']
                    # + ' '+ request.POST['selection1'])
                    # selected_resultid = request.POST['selection0']
                    # else:
                    # selected_resultid = 15
    # if no series were selected (like on first load) set the series to some value.
    if len(resultList) > 0 and len(selectedMResultSeries) == 0:
        selectedMResultSeries.append(int(resultList[0].resultid))
    elif len(resultList) == 0 and len(selectedMResultSeries) == 0:
        selectedMResultSeries.append(15)

    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
    else:
        entered_start_date = "2016-01-01"
    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    else:
        entered_end_date = "2016-01-05"
    if entered_end_date == '':
        entered_end_date = "2016-01-05"
    if entered_start_date == '':
        entered_start_date = "2016-01-01"

    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []

    myresultSeries = []
    i = 0
    data = {}

    for selectedMResult in selectedMResultSeries:
        i += 1
        selected_result = Results.objects.filter(resultid=selectedMResult).get()
        selected_results.append(selected_result)
        # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        name_of_sampling_features.append(tmpname)

        tmpname = get_name_of_variable(selected_result)
        if name_of_variables.__len__() > 0:
            namefound = False
            for name in name_of_variables:
                if name == tmpname:
                    namefound = True
            if not namefound:
                name_of_variables.append(tmpname)
            else:
                name_of_variables.append('')
        else:
            name_of_variables.append(tmpname)

        tmpname = get_name_of_units(selected_result)
        if name_of_units.__len__() > 0:
            namefound = False
            for name in name_of_units:
                if name == tmpname:
                    namefound = True
            if not namefound:
                name_of_units.append(tmpname)
            else:
                name_of_units.append('')
        else:
            name_of_units.append(tmpname)

        myresultSeries.append(Timeseriesresultvalues.objects.all().filter(
            ~Q(datavalue__lte=-6999)).filter(
            valuedatetime__gt=entered_start_date).filter(
            valuedatetime__lt=entered_end_date).filter(
            resultid=selectedMResult).order_by('-valuedatetime'))

        data.update({'datavalue' + str(i): []})

    myresultSeriesExport = Timeseriesresultvalues.objects.all() \
        .filter(valuedatetime__gt=entered_start_date) \
        .filter(valuedatetime__lt=entered_end_date) \
        .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
    i = 0

    for myresults in myresultSeries:
        i += 1
        for result in myresults:
            start = datetime(1970, 1, 1)
            delta = result.valuedatetime - start
            mills = delta.total_seconds() * 1000
            if math.isnan(result.datavalue):
                dataval = 'null'
            else:
                dataval = result.datavalue
            if popup == 'Anno':
                data['datavalue' + str(i)].append(
                    {'x': mills, 'y': dataval, 'id': str(result.valueid)})
            else:
                data['datavalue' + str(i)].append(
                    [mills, dataval])
            # data['datavalue' + str(i)].append([mills, result.datavalue])
            # #dumptoMillis(result.valuedatetime)
            # data['datavalue'].extend(tmplist )
            # data['valuedatetime'].append(dumptoMillis(result.valuedatetime))

    # build strings for graph labels
    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    tmpUnit = ''
    tmpVariableName = ''
    tmpLocName = ''
    for name_of_unit, name_of_sampling_feature, name_of_variable in zip(name_of_units,
                                                                        name_of_sampling_features,
                                                                        name_of_variables):
        i += 1
        if i == 1 and not name_of_unit == '':
            seriesStr += name_of_unit
        elif not name_of_unit == '':
            tmpUnit = name_of_unit
            seriesStr += ' - ' + name_of_unit
        if not name_of_variable == '':
            tmpVariableName = name_of_variable
        if not name_of_unit == '':
            tmpUnit = name_of_unit
        if not name_of_sampling_feature == '':
            tmpLocName = name_of_sampling_feature
        series.append(
            {"name": tmpUnit + ' - ' + tmpVariableName + ' - ' + tmpLocName, "yAxis": tmpUnit,
             "data": data['datavalue' + str(i)]})
    i = 0
    name_of_sampling_features = set(name_of_sampling_features)

    for name_of_sampling_feature in name_of_sampling_features:
        i += 1
        if i == 1:
            titleStr += name_of_sampling_feature  # + ', ' +name_of_variable
        else:
            titleStr += ' - ' + name_of_sampling_feature  # +name_of_variable+ ', '

    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter', "zoomType": 'xy'}
    title2 = {"text": titleStr}
    xAxis = {"type": 'datetime', "title": {"text": 'Date'}}
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'scatter'
    actionList = Actions.objects.filter(
        action_type="Observation")  # where the action is not of type estimation
    # assuming an estimate is a single value.
    featureactionList = Featureactions.objects.filter(action__in=actionList)
    relatedFeatureList = Relatedfeatures.objects.distinct(
        'relatedfeatureid')  # .order_by('relatedfeatureid')
    int_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
    csvexport = False
    # if the user hit the export csv button export the measurement results to csv

    if 'export_data' in request.POST:
        # if request.get('export_data'):
        response = exportspreadsheet(request, myresultSeriesExport, False)
        csvexport = True
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
    # response = HttpResponse(myfile.getvalue(),content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    if csvexport:
        return response
    else:
        # raise ValidationError(relatedFeatureList)
        return TemplateResponse(request, template,
                                {'featureactionList': featureactionList,
                                 'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                 'data_disclaimer': settings.DATA_DISCLAIMER, 'resultList': resultList,
                                 'startDate': entered_start_date, 'endDate': entered_end_date,
                                 'SelectedResults': int_selectedresultid_ids,
                                 'authenticated': authenticated,
                                 'chartID': chartID, 'chart': chart, 'series': series,
                                 'title2': title2,
                                 'graphType': graphType, 'xAxis': xAxis, 'yAxis': yAxis,
                                 'name_of_units': name_of_units,
                                 'relatedFeatureList': relatedFeatureList,
                                 'SelectedRelatedFeature': selected_relatedfeatid,
                                 'SelectedFeatureAction': selected_featureactionid,
                                 'name': request.user,
                                 'site_title': admin.site.site_title,
                                 'site_header': admin.site.site_header,
                                 'short_title': 'Time Series'}, )

def groupResultsByVariable(sampling_feature):
    fas = Featureactions.objects.filter(samplingfeatureid=sampling_feature)
    results = Results.objects.filter(featureactionid__in=fas).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 )
    groupedResults = {}

    for result in results:
        # print('id: ' + str(result.featureactionid.featureactionid) +' '+ str(result.featureactionid))
        #if str(result.variableid.variable_name) == 'Water temperature':
        #    print('var code: ' + str(result.variableid.variable_name) + ' var id ' + str(
        #        result.variableid.variableid) + ' unit_type: ' + str(result.unitsid.unit_type) +
        #          ' processing level: ' + str(result.processing_level) + ' id: ' + str(result.resultid))

        seriesname = str(result.variableid.variable_name) + '; units: ' + str(result.unitsid.unitsabbreviation) +\
                     '; ' + str(result.processing_level)

        if str(seriesname) in groupedResults:
            groupedResults[str(seriesname)].append(result.resultid)
        else:
            groupedResults[str(seriesname)] = [result.resultid]

    # print('grouped results')
    deletemes = []
    for groupedResult in groupedResults:
        # print(groupedResult)
        i = 0
        for result in groupedResults[groupedResult]:
            # print(result) #,' : ',groupedResults[groupedResult][result]
            i +=1
        if i == 1:
            deletemes.append(groupedResult)
    for deleteme in deletemes:
        groupedResults.pop(deleteme)
    return groupedResults

def mappopuploader(request, feature_action='NotSet', samplingfeature='NotSet', dataset='NotSet',
                   resultidu='NotSet',
                   startdate='NotSet', enddate='NotSet', popup='NotSet'):
    # print("HERE")
    if not request.user.is_authenticated:
        # return HttpResponseRedirect('../')
        authenticated = False
    else:
        authenticated = True
    if popup == 'NotSet':
        template = loader.get_template('chart2.html')
    else:
        template = loader.get_template('chartpopup.html')
    data_disclaimer = settings.DATA_DISCLAIMER
    useDataset = False
    useSamplingFeature = False
    if dataset == 'NotSet':
        if samplingfeature == 'NotSet':
            feature_action = int(feature_action)
        else:
            samplingfeature = int(samplingfeature)
            useSamplingFeature = True
    else:
        useDataset = True
        dataset = int(dataset)

    if resultidu != 'NotSet':
        pass

    featureActionLocation = None
    featureActionMethod = None
    datasetTitle = None
    featureActions = None
    datasetAbstract = None
    methods = None
    methodsOnly = 'False'
    samplingfeatureid= None
    resultListGrouped = None
    try:
        if not useDataset:
            if useSamplingFeature:
                samplefeature = Samplingfeatures.objects.\
                    filter(samplingfeatureid=samplingfeature).get()
                samplingfeatureid = samplefeature.samplingfeatureid
                featureActions = Featureactions.objects.\
                    filter(samplingfeatureid=samplefeature).\
                    order_by("action__method")
                resultList = Results.objects.filter(featureactionid__in=featureActions
                                                    ).order_by("featureactionid__action__method")
                #.filter(
                #    processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                #)
                actions = Actions.objects.filter(actionid__in=featureActions.values("action"))
                methods = Methods.objects.filter(methodid__in=actions.values("method"))
                featureActionLocation = samplefeature.samplingfeaturename
                resultListGrouped = groupResultsByVariable(samplefeature)
                # print(resultListGrouped)
            else:
                resultList = Results.objects.filter(featureactionid=feature_action
                                                    ).order_by("featureactionid__action__method")
                # .filter(
                # processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display'])
                featureActions = Featureactions.objects.filter(featureactionid=feature_action).get()
                featureActionLocation = featureActions.samplingfeatureid.samplingfeaturename
                samplingfeatureid = featureActions.samplingfeatureid.samplingfeatureid
                featureActionMethod = featureActions.action.method.methodname
                actions = Actions.objects.filter(actionid=featureActions.action.actionid).get()
                methods = Methods.objects.filter(methodid=actions.method.methodid)
                resultListGrouped = groupResultsByVariable(samplingfeatureid)
        else:
            datasetResults = Datasetsresults.objects.filter(datasetid=dataset)
            resultList = Results.objects.filter(resultid__in=datasetResults.values(
                "resultid")).order_by("featureactionid__action__method") #.filter(
                 # processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 #)
            datasetTitle = Datasets.objects.filter(datasetid=dataset).get().datasettitle
            datasetAbstract = Datasets.objects.filter(datasetid=dataset).get().datasetabstract
    except(ObjectDoesNotExist) as e:
        html = "<html><body>No Data Available Yet.</body></html>"
        return HttpResponse(html)
    try:
        StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
        EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
        startdates = Resultextensionpropertyvalues.objects.\
            filter(resultid__in=resultList.values("resultid")).filter(propertyid=StartDateProperty)
        enddates = Resultextensionpropertyvalues.objects.\
            filter(resultid__in=resultList.values("resultid")).filter(propertyid=EndDateProperty)
        realstartdates = []
        realenddates = []
        for startdate in startdates:
            if len(startdate.propertyvalue) == 16:
                realstartdates.append(datetime.strptime(startdate.propertyvalue, "%Y-%m-%d %H:%M"))
            elif len(startdate.propertyvalue) == 19:
                realstartdates.append(datetime.strptime(startdate.propertyvalue, "%Y-%m-%d %H:%M:%S"))
            else:
                realstartdates.append(datetime.strptime(startdate.propertyvalue, "%Y-%m-%d %H:%M:%S.%f"))
        for enddate in enddates:
            if len(enddate.propertyvalue) == 16:
                realenddates.append(datetime.strptime(enddate.propertyvalue, "%Y-%m-%d %H:%M")) #%Y-%m-%d %H:%M
            elif len(enddate.propertyvalue) == 19:
                realenddates.append(datetime.strptime(enddate.propertyvalue, "%Y-%m-%d %H:%M:%S"))
            else:
                realenddates.append(datetime.strptime(enddate.propertyvalue, "%Y-%m-%d %H:%M:%S.%f"))
        startdate = min(realstartdates).strftime('%Y-%m-%d %H:%M')
        enddate = max(realenddates).strftime('%Y-%m-%d %H:%M')
    except (ObjectDoesNotExist) as e:
        try:
            startdate = Timeseriesresultvalues.objects.\
                filter(resultid__in=resultList.values("resultid")).\
                annotate(Min('valuedatetime')).\
                order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
            enddate = Timeseriesresultvalues.objects.\
                filter(resultid__in=resultList.values("resultid")).\
                annotate(Max('valuedatetime')).\
                order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
        except IndexError as e:
            # html = "<html><body>No Data Available Yet.</body></html>"
            # return HttpResponse(html)
            try:
                startdate = Timeseriesresultvalues.objects.\
                    filter(resultid__in=resultList.values("resultid")).\
                    annotate(Min('valuedatetime')).\
                    order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
                enddate = Timeseriesresultvalues.objects.\
                    filter(resultid__in=resultList.values("resultid")).\
                    annotate(Max('valuedatetime')).\
                    order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
                methodsOnly = 'True'
            except IndexError as e:
                html = "<html><body>No time series data available for this site.</body></html>"
                return HttpResponse(html)
    except ValueError as e:
            # html = "<html><body>No Data Available Yet.</body></html>"
            # return HttpResponse(html)
            methodsOnly = 'True'
    for result in resultList:
        try:
            tsr = Timeseriesresults.objects.filter(resultid=result).get()
            result.timeintervalunits = tsr.intendedtimespacingunitsid
            result.timeinterval = tsr.intendedtimespacing
        except:
            pass
    processing_level__in = settings.MAP_CONFIG['result_value_processing_levels_to_display']
    return TemplateResponse(request, template, {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'useSamplingFeature': useSamplingFeature,
                                                'methodsOnly': methodsOnly,
                                                'featureActions': featureActions,
                                                'featureActionMethod': featureActionMethod,
                                                'featureActionLocation': featureActionLocation,
                                                'data_disclaimer': data_disclaimer,
                                                'datasetTitle': datasetTitle,
                                                'samplingfeatureid': samplingfeatureid,
                                                'datasetAbstract': datasetAbstract,
                                                'useDataset': useDataset, 'startDate': startdate,
                                                'endDate': enddate,
                                                'processing_level__in': processing_level__in,
                                                'authenticated': authenticated, 'methods': methods,
                                                'resultList': resultList,
                                                'resultListGrouped': resultListGrouped}, )

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def precision_and_scale(x):
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)

def add_shiftvalues(request):
    shift=None
    error = None
    resultid = None
    shiftvals = None
    lastshiftval = None
    firstshiftval = None
    realshiftvals = []
    response_data = {}
    forwardshift = True
    if 'direction' in request.POST:
        if request.POST['direction'] == 'backward':
            forwardshift = False
    if 'shift' in request.POST:
        shift = Decimal(request.POST['shift'])
        # print(offset)
    if 'shiftvals[]' in request.POST:
        shiftvals = request.POST.getlist('shiftvals[]')
        # print(annotationvals)
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        # print('resultid: ' + str(resultid))

    for rid in resultid:
        intrid = int(rid)
        # print('result id')
        # print(rid)
        # firstdate = shiftvals[0]
        # lastdate = shiftvals[-2]
        idvals = []
        i=0
        for offsetval in shiftvals:
            # print(offsetval)
            # if i % 3 == 0:
            #     datevals.append(datetime.strptime(offsetval, '%Y-%m-%d %H:%M:%S'))
            if i % 3 == 2:
                idvals.append(int(offsetval))
            i += 1
        try:
            order = ''
            if forwardshift:
                order = 'valuedatetime'
            else:
                order = '-valuedatetime'
            tsrvs = Timeseriesresultvalues.objects.filter(resultid=rid).filter(valueid__in=idvals).order_by(order) # .filter(valuedatetime__gte=firstdate).filter(
                # valuedatetime__lte=lastdate).filter(datavalue__in=valstochange).order_by('valuedatetime')
            realshiftvals = tsrvs
        except ObjectDoesNotExist:
            response_data['error'] = 'no values found'
    valcount = realshiftvals.count()
    precision, scale = precision_and_scale(realshiftvals.last().datavalue)
    getcontext().prec = precision
    normshift = shift - Decimal(realshiftvals.last().datavalue)
    shiftval = normshift / valcount
    k = 1
    for tsrv in realshiftvals:
        if k > 1:
            tsrv.datavalue = float(Decimal(Decimal(tsrv.datavalue) + (shiftval*k)))
            tsrv.save()
        # print(tsrv.datavalue)
        k +=1

    return HttpResponse(json.dumps(response_data),content_type='application/json')


def add_offset(request):
    offset=None
    error = None
    resultid = None
    offsetvals = None
    response_data = {}
    if 'offset' in request.POST:
        offset = Decimal(request.POST['offset'])
        # print('offset')
        # print(offset)
    if 'offsetvals[]' in request.POST:
        # THESE VALUES ARE NOT ORDERED CORRECTLY
        offsetvals = request.POST.getlist('offsetvals[]')
        # print(offsetvals)
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        # print('resultid: ' + str(resultid))
    valcount = 0
    i=0
    # datevals = []
    idvals = []
    for offsetval in offsetvals:
        # print(offsetval)
        # if i % 3 == 0:
        #     datevals.append(datetime.strptime(offsetval, '%Y-%m-%d %H:%M:%S'))
        if i % 3 == 2:
            idvals.append(int(offsetval))
        i+=1
    # datevals = sorted(datevals)
    # print(datevals)
    i = 0
    for rid in resultid:

        intrid = int(rid)

        tsrvs = Timeseriesresultvalues.objects.filter(resultid=rid).filter(valueid__in=idvals)# .filter(datavalue__in=valstochange).filter(valuedatetime__gte=firstdate).filter(
            # valuedatetime__lte=lastdate).filter(datavalue__in=valstochange)
        print(tsrvs.query)
        for tsrv in tsrvs:
            tsrv.datavalue = Decimal(tsrv.datavalue) + offset
            tsrv.save()
            # print(tsrv.datavalue)
    response_data['valuesadded'] = valcount
    return HttpResponse(json.dumps(response_data),content_type='application/json')

def add_annotation(request):
    # print('annotate')
    resultid = None
    annotationvals = None
    annotation = None
    setNaNstr = None
    setNaN = False
    cvqualitycode = False
    response_data = {}
    annotationobj = None
    anno = None
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        # print(resultid)
    if 'annotation' in request.POST:
        annotationFromUser = str(request.POST['annotation'])
        response_data['annotation'] = annotationFromUser
        # print(annotation)
    # annotationtype
    if 'cvqualitycode' in request.POST:
        cvqualitycode = str(request.POST['cvqualitycode'])
        # print(cvqualitycode)
        if cvqualitycode == 'Select':
            cvqualitycode = False
    if 'setNaN' in request.POST:
        setNaNstr = str(request.POST['setNaN'])
        if setNaNstr == 'false':
            setNaN = False
        if setNaNstr == 'true':
            setNaN = True
        # print(setNaN)
    if 'annotationvals[]' in request.POST:
        annotationvals = request.POST.getlist('annotationvals[]')
        # print(annotationvals)
    annotationtype = CvAnnotationtype.objects.get(name='Time series result value annotation')
    if cvqualitycode:
        qualitycode = CvQualitycode.objects.get(name=cvqualitycode)
    # annotator = People.objects.filter(personfirstname='Miguel').filter(personlastname='Leon')

    lastannotationval = None
    for rid in resultid:
        intrid = int(rid)
        # print('result id')
        # print(rid)
        idvals = []
        i = 0
        for annotationval in annotationvals:
            # print(offsetval)
            # if i % 3 == 0:
            #     datevals.append(datetime.strptime(offsetval, '%Y-%m-%d %H:%M:%S'))
            if i % 3 == 2:
                idvals.append(int(annotationval))
            i += 1

        # firstdate = annotationvals[0]
        # lastdate = annotationvals[-2]
        # print(firstdate)
        # print(lastdate)
        # tsrvs = Timeseriesresultvalues.objects.filter(resultid=rid).filter(valuedatetime__gte=firstdate).filter(
        #   valuedatetime__lte=lastdate).filter(datavalue__in=valstochange)
        tsrvs = Timeseriesresultvalues.objects.filter(resultid=rid).filter(valueid__in=idvals)
        for tsrv in tsrvs:
            # print(tsrv.datavalue)
            # print(tsrv.valuedatetime)
            if setNaN:
                annotation = annotationFromUser + ' original value was ' + str(tsrv.datavalue)
                # print(annotation)
                if len(annotation) > 499:
                    annotation = annotation[:499]
                try:
                    tsrvanno = Timeseriesresultvalueannotations.objects.filter(valueid=tsrv).get()
                    annotationobj = Annotations.objects.filter(annotationid=tsrvanno.annotationid.annotationid).get()
                    annotationobj.annotationtypecv = annotationtype
                    annotationobj.annotationcode = ''
                    annotationobj.annotationtext = annotation
                    annotationobj.annotationdatetime = datetime.now()
                    annotationobj.annotationutcoffset = 4
                    annotationobj.save()
                except ObjectDoesNotExist:
                    # print('error')
                    #if not annotationobj:
                    #    print('annotation does not exist')
                    annotationobj = Annotations(annotationtypecv=annotationtype, annotationcode='',
                                                annotationtext=annotation, annotationdatetime=datetime.now(),
                                                annotationutcoffset=4)
                    annotationobj.save()
                    tsrvanno = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                annotationid=annotationobj)
                    tsrvanno.save()
                    # print(annotationobj)
                # print(annotation)
                # annotationobj.save()
                tsrv.datavalue = float('nan')
                if cvqualitycode:
                    tsrv.qualitycodecv = qualitycode
                tsrv.save(force_update=True)
                # print(tsrv)
            elif cvqualitycode:
                tsrv.qualitycodecv = qualitycode
                tsrv.save(force_update=True)
            if not setNaN:
                annotation = annotationFromUser
                try:
                    tsrvanno = Timeseriesresultvalueannotations.objects.filter(valueid=tsrv).get()
                    anno = Annotations.objects.filter(annotationid=tsrvanno.annotationid.annotationid).get()
                    anno.annotationtypecv = annotationtype
                    anno.annotationcode = ''
                    anno.annotationtext = annotation
                    anno.annotationdatetime = datetime.now()
                    anno.annotationutcoffset = 4
                    anno.save()
                except ObjectDoesNotExist:
                    # print('error')
                    # if not annotationobj:
                    #print('annotation does not exist')
                    annotationobj = Annotations(annotationtypecv=annotationtype, annotationcode='',
                                                annotationtext=annotation, annotationdatetime=datetime.now(),
                                                annotationutcoffset=4)
                    annotationobj.save()
                    tsrvanno = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                annotationid=annotationobj)
                    tsrvanno.save()
                if cvqualitycode:
                    tsrv.qualitycodecv = qualitycode
                    tsrv.save(force_update=True)
                # try:
            #     tsrvanno = Timeseriesresultvalueannotations.objects.filter(valueid=tsrv).get()
            #     tsrvanno.annotationid = annotationobj
            # except ObjectDoesNotExist:
            #     tsrvanno = Timeseriesresultvalueannotations(valueid=tsrv,
            #                                                 annotationid=annotationobj)
            # tsrvanno.save()
            # print(tsrvanno)
        # tsrvanno.save()
                # print(tsrvanno.valueid)
        #     lastannotationval = annotationval
    # if resultidu != 'NotSet':
    #    resultidu = int(resultidu)
    return HttpResponse(json.dumps(response_data),content_type='application/json')

# def on_raw_message(body):
#    print(body)
def preProcDataLoggerFile(request):
    response_data = {}
    formData = None
    dataloggerfileid = None
    processingCode = None
    databeginson = None
    columnheaderson = None
    check_dates = False
    # print('in view')
    # print(request.POST)
    if 'dataloggerfileid' in request.POST:
        dataloggerfileid = int(request.POST['dataloggerfileid'])
        # print(dataloggerfileid)
    if 'processingCode' in request.POST:
        processingCode = request.POST['processingCode']
        # print(processingCode)
    if 'databeginson' in request.POST:
        databeginson = int(request.POST['databeginson'])
        # print(databeginson)
    if 'columnheaderson' in request.POST:
        columnheaderson = int(request.POST['columnheaderson'])
        # print(columnheaderson)
    if 'check_dates' in request.POST:
        if request.POST['check_dates'] == 'True':
            check_dates = True

    dlf = Dataloggerfiles.objects.get(dataloggerfileid=dataloggerfileid)
    pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=dataloggerfileid)
    linkname = str(dlf.dataloggerfilelinkname())
    fileid = dlf.dataloggerfileid
    out = StringIO()
    try:
        management.call_command('validate_datalogger_file', linkname, str(fileid)
                                , str(databeginson), str(columnheaderson), stdout=out)
        # messages = 'complete '
        messages = out.getvalue()
        response_data['validatemessage'] = str(messages)  # e.with_traceback()
        response = HttpResponse(json.dumps(response_data), content_type='application/json')
    except CommandError as e:
        response_data['error_message'] = str(e) #e.with_traceback()
        response = HttpResponse(json.dumps(response_data), content_type='application/json')
        response.status_code = 400
    return response

# @shared_task
def procDataLoggerFile(request):
    response_data = {}
    formData = None
    dataloggerfileid = None
    processingCode = None
    databeginson = None
    columnheaderson = None
    check_dates=False
    # print('in view')
    # print(request.POST)
    if 'dataloggerfileid' in request.POST:
        dataloggerfileid = int(request.POST['dataloggerfileid'])
        # print(dataloggerfileid)
    if 'processingCode' in request.POST:
        processingCode = request.POST['processingCode']
        # print(processingCode)
    if 'databeginson' in request.POST:
        databeginson = int(request.POST['databeginson'])
        # print(databeginson)
    if 'columnheaderson' in request.POST:
        columnheaderson = int(request.POST['columnheaderson'])
        # print(columnheaderson)
    if 'check_dates' in request.POST:
        if request.POST['check_dates'] =='True':
            check_dates = True
    # print(check_dates)
    # print(dataloggerfileid)

    dlf = Dataloggerfiles.objects.get(dataloggerfileid=dataloggerfileid)
    pdlf = ProcessDataloggerfile.objects.get(dataloggerfileid=dataloggerfileid)
    linkname = str(dlf.dataloggerfilelinkname())
    fileid = dlf.dataloggerfileid
    ftpfile = dlf.dataloggerfiledescription
    ftpparse = urlparse(ftpfile)
    response = None
    try:
        if not pdlf.processingCode == 'locked' and not pdlf.processingCode=='done':
            #  pdlf.processingCode = 'locked'
            #  pdlf.save()
            if len(ftpparse.netloc) > 0:
                ftpfrequencyhours = 24  # re.findall(r'^\D*(\d+)', self.processingCode)[0]
                management.call_command('update_preprocess_process_datalogger_file', linkname, str(fileid)
                                        , str(databeginson), str(columnheaderson),
                                        str(ftpfrequencyhours), False)
            else:
                # print('processdataloggerfile')
                # result = tasks.pdataloggerfile.apply_async((linkname,fileid,databeginson,columnheaderson,check_dates,False))
                management.call_command('ProcessDataLoggerFile', linkname ,str(fileid)
                                        , str(databeginson), str(columnheaderson),
                                        check_dates, False, False)
                # print(result)
                pdlf.processingCode = 'done'
                pdlf.save()
                response = HttpResponse(json.dumps(response_data), content_type='application/json')
    except CommandError as e:
        response_data['error_message'] = str(e) #e.with_traceback()
        response = HttpResponse(json.dumps(response_data), content_type='application/json')
        response.status_code = 400
    #response_data['formData'] = formData


    return response

def addL1timeseries(request):
    resultid = None
    response_data = {}
    createorupdateL1 = None
    pl1 = Processinglevels.objects.get(processinglevelid=2)
    pl0 = Processinglevels.objects.get(processinglevelid=1)
    valuesadded = 0
    tsresultTocopyBulk = []
    if 'createorupdateL1' in request.POST:
        createorupdateL1 = str(request.POST['createorupdateL1'])
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        for result in resultid:
            if createorupdateL1 == "create":
        #print('create')
                resultTocopy = Results.objects.get(resultid=result)
                tsresultTocopy = Timeseriesresults.objects.get(resultid=result)
                resultTocopy.resultid = None
                resultTocopy.processing_level = pl1
                resultTocopy.save()
                tsrvToCopy = Timeseriesresultvalues.objects.filter(resultid=tsresultTocopy)
                tsresultTocopy.resultid = resultTocopy
                tsresultTocopy.save()
                newresult = tsresultTocopy.resultid
                # tsrvToCopy.update(resultid=tsresultTocopy)
                for tsrv in tsrvToCopy:
                    tsrv.resultid = tsresultTocopy
                    try:
                        tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                        tsrv.valueid = None
                        tsrv.save()
                        tsrva.valueid = tsrv
                        # print(tsrv.valueid)
                        tsrva.save()
                    except ObjectDoesNotExist:
                        tsrv.valueid = None
                        tsresultTocopyBulk.append(tsrv)
                newtsrv = Timeseriesresultvalues.objects.bulk_create(tsresultTocopyBulk)

            elif createorupdateL1 == "update":
                print('update')
                tsresultL1 = Timeseriesresults.objects.get(resultid=result)
                resultL1 = Results.objects.get(resultid=result)
                # tsrvL1 = Timeseriesresultvalues.objects.filter(resultid=tsresultL1)
                tsrvAddToL1Bulk = []
                relatedL0result = Results.objects.filter(
                        featureactionid = resultL1.featureactionid).filter(
                        variableid = resultL1.variableid
                    ).filter(unitsid = resultL1.unitsid).filter(
                    processing_level=pl0)

                # newresult = relatedL0result.resultid
                relateL0tsresults = Timeseriesresults.objects.filter(resultid__in= relatedL0result)
                relateL0tsresult = None
                for L0result in relateL0tsresults:
                    if L0result.intendedtimespacing == tsresultL1.intendedtimespacing and L0result.intendedtimespacingunitsid == tsresultL1.intendedtimespacingunitsid:
                        relateL0tsresult =L0result
                tsrvL0 = Timeseriesresultvalues.objects.filter(resultid=relateL0tsresult)
                # print(relateL0tsresult)
                # maxtsrvL1=Timeseriesresultvalues.objects.filter(resultid=relateL1tsresult).annotate(
                #        Max('valuedatetime')). \
                #        order_by('-valuedatetime')
                # print(relateL1tsresult)
                # for r in maxtsrvL1:
                #     print(r)
                print('L1 result')
                print(tsresultL1)

                maxtsrvL0=Timeseriesresultvalues.objects.filter(resultid=relateL0tsresult).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime
                maxtsrvL1=Timeseriesresultvalues.objects.filter(resultid=tsresultL1).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime
                mintsrvL0=Timeseriesresultvalues.objects.filter(resultid=relateL0tsresult).annotate(
                        Min('valuedatetime')). \
                        order_by('valuedatetime')[0].valuedatetime
                mintsrvL1=Timeseriesresultvalues.objects.filter(resultid=tsresultL1).annotate(
                        Min('valuedatetime')). \
                        order_by('valuedatetime')[0].valuedatetime
                # print('max L0')
                # print(maxtsrvL0)
                # print('max L1')
                # print(maxtsrvL1)
                if maxtsrvL1 < maxtsrvL0:
                    tsrvAddToL1 = tsrvL0.filter(valuedatetime__gt=maxtsrvL1)
                    for tsrv in tsrvAddToL1:
                        tsrv.resultid = tsresultL1
                        try:
                            tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                            tsrv.valueid = None
                            tsrv.save()
                            tsrva.valueid = tsrv
                            # print(tsrv.valueid)
                            tsrva.save()
                        except ObjectDoesNotExist:
                            # print('doesnt exist')
                            tsrv.valueid = None
                            tsresultTocopyBulk.append(tsrv)
                if mintsrvL1 > mintsrvL0:
                    tsrvAddToL1 = tsrvL0.filter(valuedatetime__lt=mintsrvL1)
                    for tsrv in tsrvAddToL1:
                        print(tsresultL1)
                        tsrv.resultid = tsresultL1
                        try:
                            tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                            tsrv.valueid = None
                            tsrv.save()
                            tsrva.valueid = tsrv
                            # print(tsrv.valueid)
                            tsrva.save()
                        except ObjectDoesNotExist:
                            tsrv.valueid = None
                            tsresultTocopyBulk.append(tsrv)
                newtsrv = Timeseriesresultvalues.objects.bulk_create(tsresultTocopyBulk)
            valuesadded = newtsrv.__len__()
            print(valuesadded)
            # for tsrv in newtsrv:
            #     print(tsrv.resultid.resultid)
            #     print(tsrv)
            response_data['valuesadded'] = valuesadded
            # response_data['newresultid'] = newresult
            # print(result)
    return HttpResponse(json.dumps(response_data),content_type='application/json')

#another approach
#https://rlskoeser.github.io/2016/03/31/migrating-data-between-databases-with-django/
def createODM2SQLiteFile(request):
    entered_end_date = ''
    entered_start_date = ''
    myresultSeriesExport = []

    if 'exportdata' in request.POST and 'myresultSeriesExport[]' in request.POST:
        selectedMResultSeries = request.POST.getlist('myresultSeriesExport[]')
        myresultSeriesExport = None
        if request.POST['useDates'] == 'true':
            useDates = True
        else:
            useDates = False
        if useDates:
            if 'endDate' in request.POST:
                # print(entered_end_date)
                entered_end_date = request.POST['endDate']
            if 'startDate' in request.POST:
                entered_start_date = request.POST['startDate']
            #Employees.objects.values_list('eng_name', flat=True)
            myresultSeriesExport = Timeseriesresultvalues.objects.all() \
                .filter(valuedatetime__gte=entered_start_date) \
                .filter(valuedatetime__lte=entered_end_date) \
                .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
        else:
            myresultSeriesExport = Timeseriesresultvalues.objects.all() \
                .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
            # emailspreadsheet2(request, myresultSeriesExport, False)
    #management.call_command('dump_object', 'odm2admin.Timeseriesresults', 17160, 17162, kitchensink=True)
    sysout = sys.stdout
    loc = settings.FIXTURE_DIR
    # print(myresultSeriesExport.first())
    random_string = get_random_string(length=5)
    tmpfixture1 = 'tmp'  + '.json' #+ random_string
    sys.stdout = open(loc+ tmpfixture1, 'w')
    tmploc1 = loc+ tmpfixture1
    management.call_command('dump_object', 'odm2admin.Timeseriesresultvalues', myresultSeriesExport.first().valueid, kitchensink=True)
    sys.stdout.close()
    #jsonfile = open(loc+ 'tmp2.json', 'w')
    # i=0
    values = myresultSeriesExport.values_list('valueid', flat=True)
    random_string = get_random_string(length=5)
    # add random string back later
    tmpfixture2 = 'tmp'  + '.json' # + random_string
    sys.stdout = open(loc + tmpfixture2, 'w')
    # sys.stdout = open(loc + 'tmp2.json, 'w')
    tmploc2 = loc+ tmpfixture1
    sys.stdout.write(serializers.serialize("json", myresultSeriesExport[1:], indent=4,use_natural_foreign_keys=False,use_natural_primary_keys=False))
    sys.stdout.close()
    sys.stdout = sysout

    #settings.MAP_CONFIG['result_value_processing_levels_to_display']
    #db_name = exportdb.DATABASES['export']['NAME']
    #print(db_name)
    # print(tmploc1)
    database = ''
    if 'exportdata' in request.POST:
        # print(entered_end_date)
        exportdata = request.POST['exportdata']
        if exportdata == 'true':
            database = 'export'
        if 'publishdata' in request.POST:
            # print(entered_end_date)
            publishdata = request.POST['publishdata']
            if publishdata == 'true':
                database = 'published'
    #management.call_command('loaddata',
    #                        tmploc1 ,database=database)  # ,database='export'
    # print('finished first file')
    #management.call_command('loaddata',
    #                        tmploc2,database=database)
    #export_data.send(sender= Timeseriesresultvalues,tmploc1=tmploc1,tmploc2=tmploc2)
    #management.call_command('create_sqlite_export',tmploc1,tmploc2, settings=exportdb)
    # call('../')
    # print(tmploc1)
    # print(tmploc2)
    dbfilepath = exportdb.DATABASES['default']['NAME']
    path = os.path.dirname(dbfilepath)
    dbfile = os.path.basename(dbfilepath)
    dbfilename = os.path.splitext(dbfile)[0]
    random_string = get_random_string(length=5)
    dbfile2 = path +"/" + dbfilename +  random_string + ".db"
    #command = ['python',  '/home/azureadmin/webapps/ODM2-AdminLCZO/manageexport.py', 'create_sqlite_export', tmploc1, tmploc2]
    command = 'cp ' + dbfilepath + ' ' + str(dbfile2)
    # print(command)
    response = subprocess.check_call(command,shell=True)
    #write an extra settings file instead - have it contain just DATABASES; remove databases from exportdb.py and import new file. 2
    exportdb.DATABASES['default']['NAME'] = dbfile2
    command = settings.BASE_DIR + '/scripts/create_sqlite_file.sh '+ dbfile2 + ' %>> ' + settings.BASE_DIR +'/logging/sqlite_export.log'
    # print(command)
    response = subprocess.check_call(command,shell=True) #
    # print("response")
    # print(response)
    # print(exportdb.DATABASES['default']['NAME'])
    return myresultSeriesExport
    # outfile = loc +'tmp2.json'
    # print(outfile)
    # with open(outfile, 'w') as jsonfile:
    #    json.dump(data, jsonfile)
    #outfile = loc +'tmp2.json'
    #print(outfile)
    #with open(outfile, 'w') as jsonfile:
    #    json.dump(data, jsonfile)

@login_required()
def export_to_hydroshare(request):

    valuestoexport = createODM2SQLiteFile(request)

    export_complete = True
    resource_link = ''
    user = request.user
    # print(request.POST['hydroshareusername'])

    if 'hydroshareusername' in request.POST and 'hydrosharepassword' in request.POST:
        hs_client_id = settings.SOCIAL_AUTH_HYDROSHARE_UP_KEY
        hs_client_secret = settings.SOCIAL_AUTH_HYDROSHARE_UP_SECRET
        username = request.POST['hydroshareusername']
        password =  request.POST['hydrosharepassword']
        auth = HydroShareAuthOAuth2(hs_client_id, hs_client_secret,
                                    username=username, password=password)
    else:
        hs_client_id = settings.SOCIAL_AUTH_HYDROSHARE_KEY
        hs_client_secret = settings.SOCIAL_AUTH_HYDROSHARE_SECRET
        social = user.social_auth.get(provider='hydroshare')
        token = social.extra_data['access_token']
        print(social.extra_data)
        print(token)
        auth = HydroShareAuthOAuth2(hs_client_id, hs_client_secret,
                                     token=social.extra_data)
    #hs = get_oauth_hs(request)
    #userInfo = hs.getUserInfo()
    #
    # token = None
    #if 'code' in request.POST:
    #    print(request.POST['code'])
    #    token = request.POST['code']
    #print('expires in ' + str(token['expires_in']))

    #auth = HydroShareAuthOAuth2(client_id, client_secret,
    #                            username='', password='')
    hs = HydroShare(auth=auth)
    username = hs.getUserInfo()
    # print(username)
    abstracttext = 'ODM2 Admin Result Series ' +  str(valuestoexport.first().resultid)
    entered_start_date = None
    entered_end_date = None
    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
        abstracttext += ' data values from: ' + entered_start_date
    if 'endDate' in request.POST:
    #     # print(entered_end_date)
        entered_end_date = request.POST['endDate']
        abstracttext += ' ending on: ' + entered_end_date
    #
    abstract = abstracttext
    title = 'ODM2 Admin Result Series ' +  str(valuestoexport.first().resultid)
    keywords = ['ODM2']
    rtype = 'GenericResource'
    fpath = exportdb.DATABASES['default']['NAME']
    # # print(fpath)
    # #metadata = '[{"coverage":{"type":"period", "value":{"start":"'+entered_start_date +'", "end":"'+ entered_end_date +'"}}}, {"creator":{"name":"Miguel Leon"}}]'
    metadata = str('[{"coverage":{"type":"period", "value":{"start":"' + entered_start_date +  '", "end":"' + entered_end_date + '"}}}, ' \
                '{"creator":{"name":"' +user.get_full_name() +'"}}]')
    extra_metadata = str('{"key-1": "value-1", "key-2": "value-2"}')
    #
    # #abstract = 'My abstract'
    # #title = 'My resource'
    # #keywords = ('my keyword 1', 'my keyword 2')
    # #rtype = 'GenericResource'
    # #fpath = 'C:/Users/leonmi/Google Drive/ODM2AdminLT2/ODM2SQliteBlank.db'
    # #metadata = '[{"coverage":{"type":"period", "value":{"start":"01/01/2000", "end":"12/12/2010"}}}, {"creator":{"name":"John Smith"}}, {"creator":{"name":"Lisa Miller"}}]'
    # #extra_metadata = '{"key-1": "value-1", "key-2": "value-2"}'
    resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract,
                                          metadata=metadata, extra_metadata=extra_metadata)
    # print(resource_id)
    # for resource in hs.getResourceList():
    #     print(resource)
    return HttpResponse({'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'export_complete': export_complete,
                                                'username' : username,
                                                'resource_link': resource_link,},content_type='application/json')
@login_required()
def email_data_from_graph(request):
    # print('email data')
    emailsent = False
    outEmail = ''
    entered_end_date = ''
    entered_start_date = ''
    myresultSeriesExport = []
    if 'email_data' in request.POST and 'resultidu[]' or 'myresultSeriesExport[]' in request.POST:
        # print(' email data and resultid[]')
        selectedMResultSeries = request.POST.getlist('myresultSeriesExport[]')
        # print(selectedMResultSeries)
        # resultids = request.POST.getlist('resultidu[]')
        # try:
            # print(resultidu)
            # resultidu = [int(selectedMResultSeries)]
        # except TypeError:
         #    resultids = re.findall(r'\d+',request.POST.getlist('myresultSeriesExport[]')) # re.findall(r'\d+',request.POST['myresultSeriesExport[]'])
        resultidu = []
        # mergeResults = 'true'
        for results in selectedMResultSeries:
            ids = re.findall(r'\d+', results)
            for id in ids:
                resultidu.append(int(id))
        # for results in resultids:
        #     ids = re.findall(r'\d+', results)
        #     for id in ids:
        #         resultidu.append(int(reidsults))
        selectedMResultSeries = resultidu
        myresultSeriesExport = None
        if request.POST['useDates'] == 'true':
            useDates = True
        else:
            useDates = False
        if useDates:
            if 'endDate' in request.POST:
                # print(entered_end_date)
                entered_end_date = request.POST['endDate']
            if 'startDate' in request.POST:
                entered_start_date = request.POST['startDate']
            myresultSeriesExport = Timeseriesresultvaluesextwannotations.objects.all() \
                    .filter(valuedatetime__gte=entered_start_date) \
                    .filter(valuedatetime__lte=entered_end_date) \
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
        else:
            myresultSeriesExport = Timeseriesresultvaluesextwannotations.objects.all() \
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
        # print('email spreadsheet')
        emailspreadsheet2(request, myresultSeriesExport, False) # for command str_selectedresultid_ids
        
        # .after_response    
        emailsent=True
    return HttpResponse({'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'emailsent': emailsent,
                                                'outEmail': outEmail,},content_type='application/json')



def hysterisisMetrics(discharge,response):
    hystdict = {}

    return hystdict

# https://bsou.io/posts/color-gradients-with-python
def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])


def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)


def TimeSeriesGraphingShort(request, feature_action='NotSet', samplingfeature='NotSet',
                            dataset='NotSet',dischargeresult='NotSet',
                            resultidu='NotSet', startdate='NotSet', enddate='NotSet',
                            popup='NotSet'):  # ,startdate='',enddate=''
    mergeResults='false'
    authenticated = True
    hystdict = None
    if not request.user.is_authenticated:
        # return HttpResponseRedirect('../')
        authenticated = False
    if popup == 'NotSet':
        template = loader.get_template('chart2.html')
    elif  popup == 'smll':
        template = loader.get_template('chartsmall.html')
    elif popup == 'Anno':
        if not authenticated:
            return HttpResponseRedirect(settings.CUSTOM_TEMPLATE_PATH)
        template = loader.get_template('chartAnnotation.html')
    elif popup == 'hyst':
        if not authenticated:
            return HttpResponseRedirect(settings.CUSTOM_TEMPLATE_PATH)
        template = loader.get_template('hysteresisChart.html')
    else:
        template = loader.get_template('chartpopup.html')
    data_disclaimer = settings.DATA_DISCLAIMER
    map_config = settings.MAP_CONFIG
    useDataset = False
    useSamplingFeature = False
    # samplingfeature = None
    # if 'annotation' in request.POST:
    # pass
    # raise ValidationError(request.POST['annotation'])
    if dataset == 'NotSet':
        if samplingfeature == 'NotSet':
            feature_action = int(feature_action)
        else:
            samplingfeature = int(samplingfeature)
            useSamplingFeature = True
    else:
        useDataset = True
        dataset = int(dataset)

    if resultidu != 'NotSet':
        try:
            # print(resultidu)
            resultidu = [int(resultidu)]
        except:
            resultids = re.findall(r'\d+',resultidu)
            resultidu = []
            mergeResults = 'true'
            for results in resultids:
                resultidu.append(int(results))
    selected_results = []
    name_of_sampling_features = []
    # name_of_variables = []
    name_of_units = []

    myresultSeries = []

    data = {}
    featureActionLocation = None
    featureActionMethod = None
    datasetTitle = None
    datasetAbstract = None
    methods = None
    resultListGrouped = None
    # print(settings.MAP_CONFIG['result_value_processing_levels_to_display'])
    if not useDataset:
        if useSamplingFeature:
            samplefeature = Samplingfeatures.objects.filter(samplingfeatureid=samplingfeature).get()
            feature_actions = Featureactions.objects.filter(samplingfeatureid=samplefeature)
            resultList = Results.objects.filter(featureactionid__in=feature_actions).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid","resultid")
            resultListGrouped = groupResultsByVariable(samplefeature)
            actions = Actions.objects.filter(actionid__in=feature_actions.values("action"))
            methods = Methods.objects.filter(methodid__in=actions.values("method"))
            featureActionLocation = samplefeature.samplingfeaturename
        else:
            resultList = Results.objects.filter(featureactionid=feature_action).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid","resultid")
            featureAction = Featureactions.objects.filter(featureactionid=feature_action).get()
            featureActionLocation = featureAction.samplingfeatureid.samplingfeaturename
            resultListGrouped = groupResultsByVariable(featureAction.samplingfeatureid)
            featureActionMethod = featureAction.action.method.methodname
            action = Actions.objects.filter(actionid=featureAction.action.actionid).get()
            methods = Methods.objects.filter(methodid=action.method.methodid)

    else:
        datasetResults = Datasetsresults.objects.filter(datasetid=dataset)
        resultList = Results.objects.filter(resultid__in=datasetResults.values("resultid")).filter(
             processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
             ).order_by("featureactionid","resultid")
        datasetTitle = Datasets.objects.filter(datasetid=dataset).get().datasettitle
        datasetAbstract = Datasets.objects.filter(datasetid=dataset).get().datasetabstract
    numresults = resultList.count()
    selectedMResultSeries = []
    mergedResultSets = []
    for i in range(0, numresults):
        selectionStr = str('selection' + str(i))
        # when annotating you can only select a single time series
        # with a radio button
        if mergeResults == 'true':
            selectionStr = str('Mergedselection' + str(i))
        if popup == 'Anno':
            selectionStr = str('selection')
        if selectionStr in request.POST:
            # raise ValidationError(request.POST[selectionStr])
            # print(request.POST[selectionStr])
            if mergeResults =='true':
                mergedresults = re.findall('\d+', request.POST[selectionStr])
                mergedResultSets.append(mergedresults)
                for mergedresult in mergedresults:
                    for result in resultList:
                        if int(mergedresult) == result.resultid:
                            selectedMResultSeries.append(int(mergedresult))
            else:
                for result in resultList:
                    if int(request.POST[selectionStr]) == result.resultid:
                        selectedMResultSeries.append(int(request.POST[selectionStr]))
        # if we are annotating we only have a single selection to find
        if popup == 'Anno':
            break
    # selectedMResultSeries = Results.objects.filter(featureactionid=feature_action)
    i = 0
    if selectedMResultSeries.__len__() == 0:
        if resultidu == 'NotSet':
            try:
                selectedMResultSeries.append(resultList[0].resultid)
            except IndexError:
                html = "<html><body>No Data Available Yet.</body></html>"
                return HttpResponse(html)
        else:
            try:
                for resultid in resultidu:
                    selectedMResultSeries.append(resultid)
            except ObjectDoesNotExist:
                html = "<html><body>No Data Available Yet.</body></html>"
                return HttpResponse(html)

    if 'endDate' in request.POST:
        entered_end_date = request.POST['endDate']
    elif not enddate == 'NotSet':
        entered_end_date = enddate
    else:
        entered_end_date = \
            Timeseriesresultvalues.objects.filter(resultid__in=selectedMResultSeries).annotate(
                Max('valuedatetime')).order_by(
                '-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')

    if 'startDate' in request.POST:
        entered_start_date = request.POST['startDate']
    elif not startdate == 'NotSet':
        entered_start_date = startdate
    else:
        # entered_start_date= Measurementresultvalues.objects.
        # filter(resultid__in=selectedMResultSeries).annotate(Min('valuedatetime')).\
        # order_by('valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
        # .annotate(Min('price')).order_by('price')[0]
        datetime_entered_end_date = datetime.strptime(entered_end_date, '%Y-%m-%d %H:%M')
        if popup == 'smll':
            entered_start_date = datetime_entered_end_date - timedelta(
                settings.SENSOR_DASHBOARD['time_series_days'])
        elif popup =='Anno' or popup =='hyst':
            entered_start_date = datetime_entered_end_date - timedelta(
                settings.SENSOR_DASHBOARD['time_series_days'])
        else:
            entered_start_date = datetime_entered_end_date - timedelta(
                map_config['time_series_months'] * 365 / 12)  # .strftime('%Y-%m-%d %H:%M')
        entered_start_date = entered_start_date.strftime('%Y-%m-%d %H:%M')
    if mergeResults == 'false':
        for selectedMResult in selectedMResultSeries:
            i += 1
            selected_result = Results.objects.filter(resultid=selectedMResult).get()
            selected_results.append(selected_result)
            # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

            tmpname = get_name_of_sampling_feature(selected_result)
            name_of_sampling_features.append(tmpname)
            myresultSeries.append(Timeseriesresultvalues.objects.all()
                                  .filter(~Q(datavalue__lte=selected_result.variableid.nodatavalue))
                                  .filter(valuedatetime__gte=entered_start_date)
                                  .filter(valuedatetime__lte=entered_end_date)
                                  .filter(resultid=selectedMResult).order_by('-valuedatetime'))
            data.update({'datavalue' + str(i): []})
    else:
        if len(mergedResultSets) > 0:
            # print(mergedResultSets)
            for mergedResultSet in mergedResultSets:

                i += 1
                selected_result = Results.objects.filter(resultid__in=mergedResultSet).first()
                # print('result set')
                # print(mergedResultSet)
                # print(selected_result)
                selected_results.append(selected_result)
                # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

                tmpname = get_name_of_sampling_feature(selected_result)
                name_of_sampling_features.append(tmpname)
                myresultSeries.append(Timeseriesresultvalues.objects.all()
                                      .filter(~Q(datavalue__lte=selected_result.variableid.nodatavalue))
                                      .filter(valuedatetime__gte=entered_start_date)
                                      .filter(valuedatetime__lte=entered_end_date)
                                      .filter(resultid__in=mergedResultSet).order_by('-valuedatetime'))
                data.update({'datavalue' + str(i): []})
        else:
            i=1
            selected_result = Results.objects.filter(resultid__in=selectedMResultSeries).first()
            selected_results.append(selected_result)
            # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

            tmpname = get_name_of_sampling_feature(selected_result)
            name_of_sampling_features.append(tmpname)
            myresultSeries.append(Timeseriesresultvalues.objects.all()
                                  .filter(~Q(datavalue__lte=selected_result.variableid.nodatavalue))
                                  .filter(valuedatetime__gte=entered_start_date)
                                  .filter(valuedatetime__lte=entered_end_date)
                                  .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime'))
            data.update({'datavalue' + str(i): []})


    i = 0
    annotationsexist = False
    # print(selectedMResultSeries)
    if popup == 'Anno':
        tsrvas = Timeseriesresultvalueannotations.objects.filter(
            valueid__resultid__in=selectedMResultSeries).filter(
            valueid__valuedatetime__gt=entered_start_date).filter(
            valueid__valuedatetime__lt=entered_end_date)
        if tsrvas.count() > 0:
            # print('time series result value annotation count ' + str(tsrvas.count()))
            # (tsrvas.query)
            annotationsexist = True
    #print('series')
    #print(myresultSeries)


    for myresults in myresultSeries:
        i += 1
        resultannotationsexist = False
        print('response count ' + str(myresults.count()))
        # print('1st result')
        # print(myresults[0])
        if popup == 'hyst':
            result = Results
            fa = Featureactions.objects.filter(featureactionid=selected_results[0].featureactionid.featureactionid).get()
            sf = Samplingfeatures.objects.filter(samplingfeatureid=fa.samplingfeatureid.samplingfeatureid).get()
            fas = Featureactions.objects.filter(samplingfeatureid=sf)
            units = Units.objects.filter(unit_type='Volumetric flow rate')
            dischargeRs = None
            if not dischargeresult == 'NotSet':
                dischargeRs = Results.objects.filter(resultid=int(dischargeresult))
            else:
                dischargeRs = Results.objects.filter(featureactionid__in=fas).filter(unitsid__in=units)
            dischargeR = dischargeRs.first()
            dischargeTSR = Timeseriesresults.objects.filter(resultid=dischargeR).get()
            # print(dischargeTSR)
            tsrvdischarge = Timeseriesresultvalues.objects.filter(~Q(datavalue__lte=dischargeR.variableid.nodatavalue))\
                .filter(valuedatetime__gte=entered_start_date)\
                .filter(valuedatetime__lte=entered_end_date)\
                .filter(resultid=dischargeTSR).order_by('-valuedatetime')
            # print(tsrvdischarge.query)
            # print(tsrvdischarge.count())
            hystdict = hysterisisMetrics(tsrvdischarge,myresults)
        if not popup=='hyst':
            for result in myresults:
                start = datetime(1970, 1, 1)
                delta = result.valuedatetime - start
                mills = delta.total_seconds() * 1000
                if math.isnan(result.datavalue):
                    dataval = 'null'
                else:
                    dataval = result.datavalue
                # print(data.keys())
                if popup == 'Anno':
                    data['datavalue' + str(i)].append(
                        {'x': mills, 'y': dataval, 'id': str(result.valueid)})
                else:
                    data['datavalue' + str(i)].append(
                        [mills,dataval])
                if popup == 'Anno':
                    for tsrva in tsrvas:
                        if tsrva.valueid == result:
                            # print('tsrv annotation value id ' + str(tsrva.valueid))
                            if not resultannotationsexist:
                                # print('resultannotationsexist')
                                resultannotationsexist = True
                                data.update({'datavalueannotated' : []})
                            data['datavalueannotated'].append(
                                {'x':mills,'y':dataval,'id':str(result.valueid)})
        else:

            valcount = len(myresults)
            colors = linear_gradient('#BF001B','#00E5C4',n=valcount)# ['#00E5C4','#00E17D','#00DD38','#09D900','#49D500','#86D200','#C2CE00','#CA9900','#C65A00','#C21E00',]
            hexcolors = colors['hex']
            print(valcount)
            k=0

            for result, discharge in zip(myresults,tsrvdischarge):
                if math.isnan(result.datavalue):
                    dataval = 'null'
                else:
                    dataval = result.datavalue
                if math.isnan(discharge.datavalue):
                    dischargeval = 'null'
                else:
                    dischargeval = discharge.datavalue # + " " + str(discharge.valuedatetime)
                    start = datetime(1970, 1, 1)
                    delta = discharge.valuedatetime - start
                    mills = delta.total_seconds() * 1000
                    data['datavalue' + str(i)].append(
                   {'x':dischargeval,'y':dataval,'dateTime':mills,'color':hexcolors[k]}) #  [dischargeval,dataval]
                #if threshold == result.valueid:
                    k+=1

    timeseriesresults = Timeseriesresults.objects.\
        filter(resultid__in=resultList.values("resultid")).\
        order_by("resultid__variableid", "aggregationstatisticcv")
    # build strings for graph labels
    # print('data')
    # print(data)
    i = 0
    seriesStr = ''
    unit = ''
    location = ''
    variable = ''
    aggStatistic = ''
    series = []
    # print('selected result series')
    # print(selectedMResultSeries)
    r = Results.objects.filter(resultid__in=selectedMResultSeries)\
        .order_by("featureactionid","resultid")  # .order_by("unitsid")

    tsrs = Timeseriesresults.objects.filter(resultid__in=selectedMResultSeries)\
        .order_by("resultid__resultid__featureactionid","resultid")
    L1exists = False
    for selectedMResult in r:
        i += 1
        tsr = tsrs.get(resultid=selectedMResult)
        aggStatistic = tsr.aggregationstatisticcv
        unit = selectedMResult.unitsid.unitsabbreviation
        variable = selectedMResult.variableid.variable_name
        location = selectedMResult.featureactionid.samplingfeatureid.samplingfeaturename
        if i == 1 and not unit == '':
            seriesStr += str(unit)
            name_of_units.append(str(unit))
        elif not unit == '':
            seriesStr += ' - ' + str(unit)
            name_of_units.append(str(unit))
        # print('series unit and var')
        # print(str(unit) + ' - ' + str(variable))
        # print(len(mergedResultSets))
        if not popup=='hyst':
            series.append({"name": str(unit) + ' - ' + str(variable) + ' - ' +
                          str(aggStatistic) + ' - ' + str(location), "allowPointSelect": "true", "yAxis": str(unit),
                          "data": data['datavalue' + str(i)], "point": { }})
        else: # build color zones
            vals = len(data['datavalue' + str(i)])
            ii=0
            j=10
            thresholds = []
            # print(vals)
            for datum in data['datavalue' + str(i)]:
                ii+=1
                # print(ii)
                # print(int(round(vals/j)))
                if ii== int(round(vals/j)):
                    j-=1
                    thresholds.append(datum['y'])
            zones = []
            # print(thresholds)
            for ii in range(1, len(thresholds)):
                threshold = thresholds.pop()
                if not threshold == 'null':
                    dict = {'value':float(threshold),'className':'zone-'+str(ii)}
                    zones.append(dict)
            # print('zones')
            # print(zones)
            true = 'true'
            two = 2
            series.append({"name": str(unit) + ' - ' + str(variable) + ' - ' +
                          str(aggStatistic) + ' - ' + str(location), "allowPointSelect": "true", "yAxis": str(unit),
                          "lineWidth":two,"data": data['datavalue' + str(i)], "zones": zones})
            # "plotOptions": {"maker": {"enabled": true},
        if mergeResults =='true' and len(mergedResultSets) <= i:
            break

        if popup == 'Anno':

            relatedtsr = Timeseriesresults.objects.select_related('resultid').filter(
                resultid__featureactionid = selectedMResult.featureactionid).filter(
                resultid__variableid = selectedMResult.variableid
            ).filter(resultid__unitsid = selectedMResult.unitsid).filter(intendedtimespacing = tsr.intendedtimespacing
                                            ).filter(intendedtimespacingunitsid = tsr.intendedtimespacingunitsid)
            relatedresults = Results.objects.filter(resultid__in=relatedtsr)
            print(relatedresults)
            #relatedresults = Results.objects.filter(
            #    featureactionid = selectedMResult.featureactionid).filter(
            #    variableid = selectedMResult.variableid
            #).filter(unitsid = selectedMResult.unitsid)
            for rr in relatedresults:
                if rr.processing_level.processinglevelid ==2:
                    L1exists = True
            if annotationsexist:
                series.append({"name": 'Annotated ' + str(unit) + ' - ' + str(variable) + ' - ' +
                                str(aggStatistic) + ' - ' + str(location), "allowPointSelect": "true", "yAxis": str(unit),
                                "data": data['datavalueannotated'], "point": { }})

    # "point": { "events": {'click': 'selectPointsByClick'}}
    i = 0
    titleStr = ''
    # print(series)
    i = 0
    name_of_sampling_features = set(name_of_sampling_features)

    for name_of_sampling_feature in name_of_sampling_features:
        i += 1
        if i == 1:
            titleStr += name_of_sampling_feature  # + ', ' +name_of_variable
        else:
            titleStr += ' - ' + name_of_sampling_feature  # +name_of_variable+ ', '

    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter', "zoomType": 'xy'}
    title2 = {"text": titleStr}
    graphType = 'scatter'
    if not popup=='hyst':
        xAxis = {"type": 'datetime', "title": {"text": 'Date'}}
    else:
        xAxis = {"title": {"text": 'Discharge'}} # "dateTimeLabelFormats":{}
        chart = {"renderTo": chartID, "type": 'scatter', "zoomType": 'xy'}
        graphType = 'scatter'
    yAxis = {"title": {"text": seriesStr}}


    int_selectedresultid_ids = []
    str_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
        str_selectedresultid_ids.append(str(int_selectedresultid))
    csvexport = False
    cvqualitycode = None
    if popup == 'Anno':
        cvqualitycode = CvQualitycode.objects.all().order_by('definition')

        # csvexport = True
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
        # response = HttpResponse(myfile.getvalue(),content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    # if csvexport:
    #     return response
    # else:
        # raise ValidationError(relatedFeatureList)
    for result in resultList:
        tsr = Timeseriesresults.objects.filter(resultid=result).get()
        result.timeintervalunits = tsr.intendedtimespacingunitsid
        result.timeinterval = tsr.intendedtimespacing

    responsedict = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'startDate': entered_start_date,
                                                'endDate': entered_end_date,
                                                'popup': popup,
                                                'mergeResults':mergeResults,
                                                'resultListGrouped':resultListGrouped,
                                                # 'emailsent': emailsent,
                                                # 'outEmail': outEmail,
                                                'useSamplingFeature': useSamplingFeature,
                                                'featureActionMethod': featureActionMethod,
                                                'featureActionLocation': featureActionLocation,
                                                'cvqualitycode': cvqualitycode,
                                                'data_disclaimer': data_disclaimer,
                                                'datasetTitle': datasetTitle,
                                                'datasetAbstract': datasetAbstract,
                                                'useDataset': useDataset,
                                                'startdate': startdate,
                                                'enddate': enddate,
                                                'L1exists': L1exists,
                                                'SelectedResults': int_selectedresultid_ids,
                                                'authenticated': authenticated,
                                                'methods': methods,
                                                'timeseriesresults': timeseriesresults,
                                                'chartID': chartID, 'chart': chart,
                                                'series': series,
                                                'title2': title2, 'resultList': resultList,
                                                'graphType': graphType, 'xAxis': xAxis,
                                                'yAxis': yAxis,
                                                'name_of_units': name_of_units}
    if hystdict:
        z = hystdict.copy()
        z.update(responsedict)
        responsedict = z
    return TemplateResponse(request, template, responsedict, )


#
# From http://stackoverflow.com/questions/8200342/removing-duplicate-strings-from-a-list-in-python
def removeDupsFromListOfStrings(listOfStrings):
    seen = set()
    result = []
    for item in listOfStrings:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def scatter_plot(request):
    authenticated = True
    if not request.user.is_authenticated:
        authenticated = False
    xVariableSelection = yVariableSelection = fieldarea1 = fieldarea2 = filteredFeatures = None
    xVar = None
    yVar = None
    title = None
    if 'fieldarea1' in request.POST and 'fieldarea2' not in request.POST:
        if not request.POST['fieldarea1'] == 'All':
            fieldarea1 = request.POST['fieldarea1']
            fieldarea1RF = Relatedfeatures.objects.filter(relatedfeatureid=fieldarea1)
            filteredFeatures = Samplingfeatures.objects.filter(
                samplingfeatureid__in=fieldarea1RF.values("samplingfeatureid"))
            fieldarea1 = Samplingfeatures.objects.filter(samplingfeatureid=fieldarea1).get()
    if 'fieldarea1' in request.POST and 'fieldarea2' in request.POST:
        if not request.POST['fieldarea1'] == 'All' and not request.POST['fieldarea2'] == 'All':
            fieldarea1 = request.POST['fieldarea1']
            fieldarea2 = request.POST['fieldarea2']
            fieldareaRF1 = Relatedfeatures.objects.filter(relatedfeatureid=fieldarea1)
            fieldareaRF2 = Relatedfeatures.objects.filter(relatedfeatureid=fieldarea2)
            # fieldareaRF = fieldarea1RF & fieldarea2RF #only sampling features in 1 and 2

            filteredFeatures = Samplingfeatures.objects.filter(
                samplingfeatureid__in=fieldareaRF1.values("samplingfeatureid")) \
                .filter(samplingfeatureid__in=fieldareaRF2.values("samplingfeatureid"))
            fieldarea1 = Samplingfeatures.objects.filter(samplingfeatureid=fieldarea1).get()
            fieldarea2 = Samplingfeatures.objects.filter(samplingfeatureid=fieldarea2).get()
            title = str(fieldarea1.samplingfeaturecode) + " - " + str(
                fieldarea2.samplingfeaturecode) + " : "
    if 'xVariableSelection' and 'yVariableSelection' in request.POST:
        xVariableSelection = request.POST['xVariableSelection']
        yVariableSelection = request.POST['yVariableSelection']
        xVar = Variables.objects.filter(variableid=xVariableSelection).get()
        yVar = Variables.objects.filter(variableid=yVariableSelection).get()
        xVariableSelection = Variables.objects.filter(variableid=xVariableSelection).get()
        yVariableSelection = Variables.objects.filter(variableid=yVariableSelection).get()
        if title:
            title = title + str(xVar.variablecode) + " - " + str(yVar.variablecode)
        else:
            title = str(xVar.variablecode) + " - " + str(yVar.variablecode)
    prv = Profileresults.objects.all()
    # second filter = exclude summary results attached to field areas
    pr = Results.objects.filter(resultid__in=prv).filter(
        ~Q(
            featureactionid__samplingfeatureid__sampling_feature_type="Ecological land "
                                                                      "classification")).filter(
        ~Q(featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
    # variables is the list to pass to the html template
    variables = Variables.objects.filter(variableid__in=pr.values("variableid"))
    fieldareas = Samplingfeatures.objects.filter(
        sampling_feature_type="Ecological land classification")  # Field area
    xlocation = []
    ylocation = []
    xdata = []
    ydata = []
    prvx = prvy = xlocs = ylocs = None
    if xVar and yVar:
        rvx = pr.filter(variableid=xVar).values('resultid')
        prvx = Profileresultvalues.objects.filter(~Q(datavalue=-6999)) \
            .filter(~Q(datavalue=-888.88)).filter(resultid__in=rvx).order_by(
            "resultid__resultid__unitsid",
            "resultid__resultid__featureactionid__samplingfeatureid",
            "zlocation")
        rvy = pr.filter(variableid=yVar).values('resultid')
        prvy = Profileresultvalues.objects.filter(~Q(datavalue=-6999)) \
            .filter(~Q(datavalue=-888.88)).filter(resultid__in=rvy).order_by(
            "resultid__resultid__unitsid",
            "resultid__resultid__featureactionid__samplingfeatureid",
            "zlocation")

        xr = Results.objects.filter(resultid__in=prvx.values("resultid"))
        xfa = Featureactions.objects.filter(featureactionid__in=xr.values("featureactionid"))
        if filteredFeatures:
            xlocs = Samplingfeatures.objects.filter(
                samplingfeatureid__in=xfa.values("samplingfeatureid")).filter(
                samplingfeatureid__in=filteredFeatures)
        else:
            xlocs = Samplingfeatures.objects.filter(
                samplingfeatureid__in=xfa.values("samplingfeatureid"))

        # xlocation = re.sub('[^A-Za-z0-9]+', '', xlocation)
        yr = Results.objects.filter(resultid__in=prvy.values("resultid"))
        yfa = Featureactions.objects.filter(featureactionid__in=yr.values("featureactionid"))
        if filteredFeatures:
            ylocs = Samplingfeatures.objects.filter(
                samplingfeatureid__in=yfa.values("samplingfeatureid")).filter(
                samplingfeatureid__in=filteredFeatures)
        else:
            ylocs = Samplingfeatures.objects.filter(
                samplingfeatureid__in=yfa.values("samplingfeatureid"))
    if prvx and prvx:
        prvx = prvx.filter(resultid__resultid__featureactionid__samplingfeatureid__in=xlocs)
        prvy = prvy.filter(resultid__resultid__featureactionid__samplingfeatureid__in=ylocs)
        for x in prvx:
            xdata.append(
                str(
                    x.datavalue
                ) + ";" + str(
                    x.resultid.resultid.unitsid.unitsabbreviation
                ) + ";" + str(
                    x.zlocation
                ) + ";" + str(
                    x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
                )
            )

            tmpLoc = "{0} {1}-{2} {3};{4};{5};{6};{7}".format(str(
                x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
            ), str(
                x.zlocation - x.zaggregationinterval
            ), str(
                x.zlocation
            ), str(
                x.zlocationunitsid.unitsabbreviation
            ), str(
                x.resultid.resultid.unitsid.unitsabbreviation
            ), str(
                x.zlocation
            ), str(
                x.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
            ), str(
                x.resultid.resultid.unitsid.unitsabbreviation
            ))
            xlocation.append(tmpLoc)

        for y in prvy:
            ydata.append(
                str(y.datavalue) + ";" + str(
                    y.resultid.resultid.unitsid.unitsabbreviation) + ";" + str(y.zlocation) +
                ";" + str(
                    y.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename))
            foundloc = False
            for x in prvx:
                if x.zlocation == y.zlocation or x.resultid.resultid.featureactionid \
                        .samplingfeatureid.samplingfeaturename == y.resultid.resultid \
                        .featureactionid.samplingfeatureid.samplingfeaturename:
                    foundloc = True
                    tmpLoc = "{0} {1}-{2} {3};{4};{5};{6};{7}".format(
                        str(
                            y.resultid.resultid
                            .featureactionid.samplingfeatureid.samplingfeaturename
                        ),
                        str(y.zlocation - y.zaggregationinterval), str(y.zlocation),
                        str(y.zlocationunitsid.unitsabbreviation),
                        str(y.resultid.resultid.unitsid.unitsabbreviation), str(y.zlocation),
                        str(y.resultid.resultid.featureactionid
                            .samplingfeatureid.samplingfeaturename),
                        str(y.resultid.resultid.unitsid.unitsabbreviation)
                    )
            if not foundloc:
                xlocation.append(tmpLoc)
                # xlocation.append(tmpLoc)
    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'scatter', "zoomType": 'xy'}
    title2 = {"text": title}
    # xAxis = {"categories":xAxisCategories,} #"type": 'category',
    # "title": {"text": xAxisCategories},
    yAxis = {"title": {"text": str(yVar)}}
    xAxis = {"title": {"text": str(xVar)}}
    graphType = 'scatter'
    if 'export_data' in request.POST:
        resultValuesSeries = prvx | prvy
        response = exportspreadsheet(request, resultValuesSeries)
        return response
    return TemplateResponse(request, 'soilsscatterplot.html',
                            {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                             'data_disclaimer': settings.DATA_DISCLAIMER,
                             'xVariables': variables, 'yVariables': variables,
                             'authenticated': authenticated,
                             'xVariableSelection': xVariableSelection,
                             'yVariableSelection': yVariableSelection,
                             'fieldarea1': fieldarea1, 'fieldarea2': fieldarea2,
                             'fieldareas': fieldareas,
                             'chartID': chartID, 'chart': chart, 'title2': title2,
                             'graphType': graphType,
                             'yAxis': yAxis, 'xAxis': xAxis, 'xdata': xdata, 'ydata': ydata,
                             'ylocation': ylocation,
                             'xlocation': xlocation, 'name': request.user,
                             'site_title': admin.site.site_title,
                             'site_header': admin.site.site_header,
                             'short_title': 'Soils Scatter Plot'}, )


def exportcitations(request, citations, csv):
    myfile = StringIO()
    first = True
    citationpropvalues = Citationextensionpropertyvalues.objects.filter(
        citationid__in=citations).order_by("propertyid")
    authorheader = Authorlists.objects.filter(citationid__in=citations).order_by(
        "authororder").distinct("authororder")
    # MyTable.objects.extra(select={'int_name': 'CAST(t.name AS INTEGER)'},
    #                  order_by=['int_name'])
    authheadercount = authorheader.__len__()
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
        else:  # endnote instead
            myfile.write(citation.endnoteexport())
        # export authors
        authors = Authorlists.objects.filter(citationid=citation).order_by("authororder")
        authcount = authors.__len__()
        for auth in authors:
            if csv:
                myfile.write(auth.csvoutput())
            else:
                myfile.write(auth.endnoteexport())
        if csv:
            for i in range(0, authheadercount - authcount, 1):
                myfile.write('"",')
        thiscitationpropvalues = citationpropvalues.filter(citationid=citation).order_by(
            "propertyid")
        for matchheader in citationpropheaders:
            headermatched = False
            for citationprop in thiscitationpropvalues:
                headermatched = False
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
        first = False

    if csv:
        response = HttpResponse(myfile.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mycitations.csv"'
    else:
        response = HttpResponse(myfile.getvalue(), content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename="myCitationsEndNoteImport.txt"'

    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def grecaptcha_verify(request):
    if request.method == 'POST':
        response = {}
        data = request.POST
        captcha_rs = data.get('g_recaptcha_response')
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': captcha_rs,
            'remoteip': get_client_ip(request)
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        response["status"] = verify_rs.get("success", False)
        response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
        return response

def emailspreadsheet(request, resultValuesSeries, profileResult=True):
    # if the user hit the export csv button export the measurement results to csv
    response = grecaptcha_verify(request)
    captach_status = response["status"]
    out_email = ''
    entered_start_date =''
    entered_end_date =''
    use_dates =''
    emailsent = False
    if captach_status:
        if 'startDate' in request.POST:
            entered_start_date = request.POST['startDate']
        if 'endDate' in request.POST:
            entered_end_date = request.POST['endDate']
        if 'useDates' in request.POST:
            use_dates = request.POST['useDates']
        if 'outEmail' in request.POST:
            outgoingemail = request.POST['outEmail']
        management.call_command('export_timeseriesresultvaluesextwannotations', outgoingemail,
                                entered_start_date, entered_end_date, use_dates,
                                resultValuesSeries)
        emailsent = True
    return emailsent

# @after_response.enable
def emailspreadsheet2(request, resultValuesSeries, profileResult=True):
    response = grecaptcha_verify(request)
    captach_status = response["status"]
    # captach_status = True
    outgoingemail = ''
    entered_start_date =''
    entered_end_date =''
    use_dates =''
    emailsent = False
    emailtitle = 'your ODM2 Admin data is attached'
    emailtext = 'Attached are results for the following time series: '

    if captach_status:
        # print("captach ok")
        if 'outEmail' in request.POST:
            outgoingemail = request.POST['outEmail']
            # print(outgoingemail)
        tolist = []
        tolist.append(str(outgoingemail))
        # print(tolist)

        myfile = StringIO()
         # raise ValidationError(resultValues)
        k = 0
        variablesAndUnits = []
        variable = ''
        unit = ''
        firstheader = True
        processingCode = None
        lastResult = None
        newResult = None
        resultValuesHeaders = resultValuesSeries.filter(
            ~Q(
                samplingfeaturetypecv="Ecological land classification"  # noqa
            )
        ).filter(
            ~Q(
                samplingfeaturetypecv="Field area"  # noqa
            )
        ).order_by(
             "resultid", "variablecode", "unitsabbreviation",
            "processinglevelcode"
        )
        # .distinct("resultid__resultid__variableid","resultid__resultid__unitsid")
        for myresults in resultValuesHeaders:
            lastResult = newResult
            newResult = myresults
            lastVariable = variable
            variable = myresults.variablecode
            lastUnit = unit
            unit = myresults.unitsabbreviation
            lastProcessingCode = processingCode
            processingCode = myresults.processinglevelcode
            # if not firstheader and firstVar==variable and firstUnit==unit:
            # only add the first instance of each variable, once one repeats your done.
            # break
            if not lastVariable == variable or not lastUnit == unit or not lastProcessingCode == \
                    processingCode or not newResult.resultid == lastResult.resultid:
                variablesAndUnits.append(variable + unit + processingCode +str(newResult.resultid))
                if firstheader:
                    myfile.write(myresults.csvheader())
                    firstheader = False
                myfile.write(myresults.csvheaderShort())
                emailtext = emailtext + ' - ' + str(myresults.email_text())
                # elif not lastUnit==unit:
                # myfile.write(myresults.csvheaderShortUnitOnly())

        if profileResult:
            resultValuesSeries = resultValuesSeries.filter(
                ~Q(
                    resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification"  # noqa
                )
            ).filter(
                ~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area"  # noqa
                   )
            ).order_by(
                "resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
                "resultid__intendedzspacing", "resultid__resultid__variableid",
                "resultid__resultid__unitsid__unitsabbreviation"
            )
        else:
            resultValuesSeries = resultValuesSeries.filter(
                ~Q(samplingfeaturetypecv="Ecological land classification")  # noqa
            ).filter(
                ~Q(samplingfeaturetypecv="Field area"  # noqa
                )
            ).order_by(
                "valuedatetime",
                "resultid",
                "samplingfeaturename",
                "variablecode", "unitsabbreviation",
                "processinglevelcode"
            )
        # myfile.write(lastResult.csvheaderShort())
        # emailtext = emailtext + ' - ' + str(lastResult.email_text())
        myfile.write('\n')

        samplingfeaturename = ''
        lastsamplingfeaturename = ''
        depth = 0
        position = 0
        time = None

        # resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename
        for myresults in resultValuesSeries:
            lastResult = newResult
            # #newResult = myresults
            variable = myresults.variablecode
            unit = myresults.unitsabbreviation
            lastsamplingfeaturename = samplingfeaturename
            samplingfeaturename = myresults.samplingfeaturename
            lastDepth = depth
            processingCode = myresults.processinglevelcode
            if profileResult:
                depth = myresults.resultid.intendedzspacing

                if not k == 0 and (not lastsamplingfeaturename == samplingfeaturename or
                                   not depth == lastDepth):
                    myfile.write('\n')
                    temp = myresults.csvoutput()
                    myfile.write(temp)
                    position = 0
                elif k == 0:
                    temp = myresults.csvoutput()
                    myfile.write(temp)
            else:
                lastTime = time
                time = myresults.valuedatetime
                if not k == 0 and (not lastsamplingfeaturename == samplingfeaturename or
                                   not time == lastTime):
                    myfile.write('\n')
                    temp = myresults.csvoutput()
                    myfile.write(temp)
                    position = 0
                elif k == 0:
                    temp = myresults.csvoutput()
                    myfile.write(temp)
            # else:
            # if variablesAndUnits.index(unicode(variable)+unicode(unit)) ==position:
            for i in range(
                    position,
                    variablesAndUnits.index(variable +
                                            unit +
                                            processingCode+str(myresults.resultid))
            ):
                myfile.write(",")
                myfile.write(",")
                myfile.write(",")
                position += 1
            myfile.write(myresults.csvoutputShort())
            position += 1
            k += 1
        # response = StreamingHttpResponse(myfile.getvalue(), content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
        # print('email!!!!')
        # print(settings.EMAIL_FROM_ADDRESS)
        # print(emailtext)
        # print(tolist)
        email = EmailMessage(emailtitle,emailtext,
                             settings.EMAIL_FROM_ADDRESS, tolist)
        email.attach('mydata.csv', myfile.getvalue(),'text/csv')
        email.send()
        return True
    else:
        # print("captcha not ok")
        return False

def exportspreadsheet(request, resultValuesSeries, profileResult=True):
    # if the user hit the export csv button export the measurement results to csv


    myfile = StringIO.StringIO()
     # raise ValidationError(resultValues)
    k = 0
    variablesAndUnits = []
    variable = ''
    unit = ''
    firstheader = True
    processingCode = None
    resultValuesHeaders = resultValuesSeries.filter(
        ~Q(
            resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification"  # noqa
        )
    ).filter(
        ~Q(
            resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area"  # noqa
        )
    ).order_by(
        "resultid__resultid__variableid", "resultid__resultid__unitsid",
        "resultid__resultid__processing_level__processinglevelcode"
    )
    # .distinct("resultid__resultid__variableid","resultid__resultid__unitsid")
    for myresults in resultValuesHeaders:
        lastVariable = variable
        variable = myresults.resultid.resultid.variableid.variablecode
        lastUnit = unit
        unit = myresults.resultid.resultid.unitsid.unitsabbreviation
        lastProcessingCode = processingCode
        processingCode = myresults.resultid.resultid.processing_level.processinglevelcode
        # if not firstheader and firstVar==variable and firstUnit==unit:
        # only add the first instance of each variable, once one repeats your done.
        # break
        if not lastVariable == variable or not lastUnit == unit or not lastProcessingCode == \
                processingCode:
            variablesAndUnits.append(variable + unit + processingCode)
            if firstheader:
                myfile.write(myresults.csvheader())
                firstheader = False
            myfile.write(myresults.csvheaderShort())
            # elif not lastUnit==unit:
            # myfile.write(myresults.csvheaderShortUnitOnly())
    if profileResult:
        resultValuesSeries = resultValuesSeries.filter(
            ~Q(
                resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification"  # noqa
            )
        ).filter(
            ~Q(resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area"  # noqa
               )
        ).order_by(
            "resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
            "resultid__intendedzspacing", "resultid__resultid__variableid",
            "resultid__resultid__unitsid"
        )
    else:
        resultValuesSeries = resultValuesSeries.filter(
            ~Q(
                resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Ecological land classification")  # noqa
        ).filter(
            ~Q(
                resultid__resultid__featureactionid__samplingfeatureid__sampling_feature_type="Field area"  # noqa
            )
        ).order_by(
            "valuedatetime",
            "resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
            "resultid__resultid__variableid", "resultid__resultid__unitsid",
            "resultid__resultid__processing_level__processinglevelcode"
        )
    # myfile.write(lastResult.csvheaderShort())
    myfile.write('\n')

    samplingFeatureCode = ''

    depth = 0
    position = 0
    time = None

    # resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode
    for myresults in resultValuesSeries:
        variable = myresults.resultid.resultid.variableid.variablecode
        unit = myresults.resultid.resultid.unitsid.unitsabbreviation
        lastSamplingFeatureCode = samplingFeatureCode
        samplingFeatureCode = myresults.resultid.resultid.featureactionid.samplingfeatureid \
            .samplingfeaturecode
        lastDepth = depth
        processingCode = myresults.resultid.resultid.processing_level.processinglevelcode
        if profileResult:
            depth = myresults.resultid.intendedzspacing
            if not k == 0 and (not lastSamplingFeatureCode == samplingFeatureCode or
                               not depth == lastDepth):
                myfile.write('\n')
                temp = myresults.csvoutput()
                myfile.write(temp)
                position = 0
            elif k == 0:
                temp = myresults.csvoutput()
                myfile.write(temp)
        else:
            lastTime = time
            time = myresults.valuedatetime
            if not k == 0 and (not lastSamplingFeatureCode == samplingFeatureCode or
                               not time == lastTime):
                myfile.write('\n')
                temp = myresults.csvoutput()
                myfile.write(temp)
                position = 0
            elif k == 0:
                temp = myresults.csvoutput()
                myfile.write(temp)
        # else:
        # if variablesAndUnits.index(unicode(variable)+unicode(unit)) ==position:
        for i in range(
                position,
                variablesAndUnits.index(variable +
                                        unit +
                                        processingCode)
        ):
            myfile.write(",")
            position += 1
        myfile.write(myresults.csvoutputShort())
        position += 1
        k += 1
    response = StreamingHttpResponse(myfile.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
    # email = EmailMessage(emailtitle,emailtext,
    #                      'leonmi@sas.upenn.edu', tolist)
    # email.attach('mydata.csv', myfile.getvalue(),'text/csv')
    # email.send()
    return response


def graph_data(request, selectedrelatedfeature='NotSet', samplingfeature='NotSet', popup='NotSet'):
    authenticated = True
    if not request.user.is_authenticated:
        authenticated = False
    if popup == 'NotSet':
        template = loader.get_template('chartVariableAndFeature.html')
    else:
        template = loader.get_template('profileresultgraphpopup.html')
    selected_relatedfeatid = 15
    data_disclaimer = settings.DATA_DISCLAIMER
    # relatedfeatureList
    # update_result_on_related_feature

    # need a variables list instead of a results list
    # find the variables for the selected related feature

    if 'SelectedRelatedFeature' in request.POST:
        if not request.POST['SelectedRelatedFeature'] == 'All':
            # relatedFeature = Samplingfeatures.objects.filter(samplingfeatureid=
            # selected_relatedfeatid) #Relatedfeatures.objects.filter(relatedfeatureid=
            # int(selected_relatedfeatid)).distinct('relatedfeatureid')
            selected_relatedfeatid = int(request.POST['SelectedRelatedFeature'])
            # relatedFeature = Samplingfeatures.objects.filter(samplingfeatureid=
            # selected_relatedfeatid)

    elif selectedrelatedfeature != 'NotSet':
        selected_relatedfeatid = int(selectedrelatedfeature)
    else:
        selected_relatedfeatid = 15

    useSamplingFeature = False
    samplingfeaturelabel = None
    if samplingfeature != 'NotSet':
        samplingfeature = int(samplingfeature)
        useSamplingFeature = True
        samplingfeaturelabel = Samplingfeatures.objects.filter(samplingfeatureid=samplingfeature).get()
    # find variables found at the sampling feature
    # need to go through featureaction to get to results

    # need the feature actions for all of the sampling features related to this sampling feature
    if not useSamplingFeature:
        sampling_features = Relatedfeatures.objects.filter(
            relatedfeatureid__exact=selected_relatedfeatid).values(
            'samplingfeatureid')
        samplingfeaturelabel = Samplingfeatures.objects.filter(samplingfeatureid=selected_relatedfeatid).get()
        # select the feature actions for all of the related features.
        feature_actions = Featureactions.objects.filter(samplingfeatureid__in=sampling_features)
    else:
        feature_actions = Featureactions.objects.filter(samplingfeatureid=samplingfeature)

    featureresults = Results.objects.filter(
        featureactionid__in=feature_actions
    ).order_by(
        "variableid", "unitsid"
    ).filter(
        ~Q(featureactionid__samplingfeatureid__sampling_feature_type="Ecological land "
                                                                     "classification")
    ).filter(
        ~Q(featureactionid__samplingfeatureid__sampling_feature_type="Field area"))
    variableList = Variables.objects.filter(variableid__in=featureresults.values("variableid"))

    # find the profile results series for the selected variable
    numvariables = variableList.__len__()
    # raise ValidationError(numvariables)
    selectedMVariableSeries = []
    for i in range(0, numvariables):
        selectionStr = str('selection' + str(i))
        if selectionStr in request.POST:
            # raise ValidationError(request.POST[selectionStr])
            for variable in variableList:
                if int(request.POST[selectionStr]) == variable.variableid:
                    selectedMVariableSeries.append(int(request.POST[selectionStr]))

    # if no series were selected (like on first load) set the series to some value.
    if len(variableList) > 0 and len(selectedMVariableSeries) == 0:
        selectedMVariableSeries.append(int(variableList[0].variableid))
    elif len(variableList) == 0 and len(selectedMVariableSeries) == 0:
        selectedMVariableSeries.append(15)

    selectedMResultsSeries = None
    for variable in selectedMVariableSeries:
        if not selectedMResultsSeries:
            selectedMResultsSeries = featureresults.filter(variableid=variable)
        else:  # concatenante the sets of results for each variable
            selectedMResultsSeries = selectedMResultsSeries | featureresults.filter(
                variableid=variable)
    selected_results = []
    name_of_sampling_features = []
    name_of_variables = []
    name_of_units = []
    unitAndVariable = ''
    i = 0
    data = {}
    resultValuesSeries = None
    # if 'update_result_on_related_feature' in request.POST:
    # raise ValidationError(selectedMResultsSeries)
    # selectedMResultsSeries.order_by("resultid__")

    # these 5 lines sort the results by there z-spacing low to high, then by
    # alphabelitcally by there sampling
    # feature code, luckily Ridge, Slope, Valley are in alphabetical order.
    profileresults = Profileresults.objects.filter(resultid__in=selectedMResultsSeries).order_by(
        "resultid__variableid",
        "resultid__unitsid",
        "intendedzspacing",
        "resultid__featureactionid__samplingfeatureid__samplingfeaturecode")
    sortedResults = list()
    for result in profileresults:
        sortedResults.append(selectedMResultsSeries.get(resultid=result.resultid.resultid))
    selectedMResultsSeries = sortedResults
    for selectedMResult in selectedMResultsSeries:
        i += 1
        selected_result = Results.objects.filter(resultid=selectedMResult.resultid).get()
        # if 'update_result_on_related_feature' in request.POST:
        # raise ValidationError(selected_result)
        selected_results.append(selected_result)
        # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = selected_result.featureactionid.samplingfeatureid.samplingfeaturename # get_name_of_sampling_feature(selected_result)
        tmpLocName = tmpname

        tmpname = selected_result.variableid.variablecode # get_name_of_variable(selected_result)
        unitAndVariable = tmpname
        if name_of_variables.__len__() > 0:
            name_of_variables.append(tmpname)
        else:
            name_of_variables.append(tmpname)
        tmpname = selected_result.unitsid.unitsname # get_name_of_units(selected_result)
        # if(selectedMResult.resultid==2072):
        # raise ValidationError(tmpname)
        unitAndVariable = unitAndVariable + " " + tmpname
        if name_of_units.__len__() > 0:
            name_of_units.append(tmpname)
        else:
            name_of_units.append(tmpname)
        resultValues = Profileresultvalues.objects.all().filter(
            resultid__exact=selectedMResult.resultid)  # .order_by("-zlocation")

        if not resultValuesSeries:
            resultValuesSeries = resultValues
        else:
            resultValuesSeries = resultValuesSeries | resultValues
            # if 'update_result_on_related_feature' in request.POST:
            # raise ValidationError(resultValues)
        for resultValue in resultValues:
            # raise ValidationError(resultValues)
            seriesName = 'datavalue' + unitAndVariable
            tmpLocName = tmpLocName + " Depth " + str(
                resultValue.zlocation - resultValue.zaggregationinterval) + "-" + str(
                resultValue.zlocation) + " " + str(resultValue.zlocationunitsid.unitsabbreviation)
            name_of_sampling_features.append(tmpLocName)
            if seriesName in data:
                if resultValue.datavalue != -6999 and resultValue.datavalue != -888.88:
                    data['datavalue' + unitAndVariable].append(
                        [tmpLocName,
                         resultValue.datavalue])  # tmpUnit +' - '+tmpVariableName +' - '+
                else:
                    data['datavalue' + unitAndVariable].append([tmpLocName, None])
            else:
                data.update({'datavalue' + unitAndVariable: []})
                if resultValue.datavalue != -6999 and resultValue.datavalue != -888.88:
                    data['datavalue' + unitAndVariable].append(
                        [tmpLocName,
                         resultValue.datavalue])  # tmpUnit +' - '+tmpVariableName +' - '+
                else:
                    data['datavalue' + unitAndVariable].append([tmpLocName, None])
                    # data['datavalue' + unitAndVariable].append( resultValue.datavalue)
                    # #get_name_of_variable(selected_result) + " " +
                    # get_name_of_sampling_feature(selected_result) ,
                    # data2.append(resultValue.datavalue)
    # raise ValidationError(data)
    # build strings for graph labels
    i = 0
    seriesStr = ''
    series = []
    titleStr = ''
    tmpUnit = ''
    tmpVariableName = ''
    numberofLocations = len(name_of_sampling_features)

    for name_of_unit, name_of_variable in zip(name_of_units, name_of_variables):
        # raise ValidationError("length of unit names"+ str(len(name_of_units)) +
        # "length of name of variables"+ str(len(name_of_variables)))
        # #get fewer sampling feature names
        i += 1
        lastUnit = tmpUnit
        lastVariableName = tmpVariableName
        tmpVariableName = name_of_variable
        tmpUnit = name_of_unit

        if not name_of_variable == lastVariableName or not name_of_unit == lastUnit:
            update = True
        else:
            update = False

        if i == 1 and not name_of_unit == '':
            seriesStr += name_of_unit
        elif name_of_unit != lastUnit and update:
            # tmpUnit = name_of_unit
            seriesStr += ' - ' + name_of_unit
        lastUnitAndVariable = unitAndVariable
        unitAndVariable = tmpVariableName + " " + tmpUnit
        # raise ValidationError(data['datavalue'+unitAndVariable])
        # raise ValidationError(name_of_unit)
        key = 'datavalue' + unitAndVariable
        if lastUnitAndVariable != unitAndVariable and update and key in data:
            series.append({"name": tmpUnit + ' - ' + tmpVariableName, "yAxis": tmpUnit,
                           #"area": {"cropThreshold": 50000},
                           "data": data[
                               'datavalue' + unitAndVariable]})
            # removewd from name +' - '+ tmpLocName
            if titleStr == '':
                titleStr = tmpVariableName
            else:
                titleStr += ' - ' + tmpVariableName
        elif i == numberofLocations and len(series) == 0 and key in data:
            # raise ValidationError(name_of_unit)
            series.append({"name": tmpUnit + ' - ' + tmpVariableName, "yAxis": tmpUnit,
                           "data": data['datavalue' + unitAndVariable]})
            if titleStr == '':
                titleStr = tmpVariableName
                # titleStr += tmpVariableName
                # series.append(data['datavalue'+str(i)])
    chartID = 'chart_id'
    chart = {"renderTo": chartID, "type": 'column', "zoomType": 'xy'}
    title2 = {"text": titleStr}
    # xAxis = {"categories":xAxisCategories,} #"type":
    # 'category',"title": {"text": xAxisCategories},
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'column'
    withProfileResults = Profileresults.objects.all()
    results = Results.objects.filter(resultid__in=withProfileResults)
    samplefeatid = Featureactions.objects.filter(featureactionid__in=results).values(
        'samplingfeatureid')
    relatedFeatureList = Relatedfeatures.objects.filter(
        samplingfeatureid__in=samplefeatid).distinct(
        'relatedfeatureid')  # .order_by('relatedfeatureid')
    # relatedFeatureList = sorted(relatedFeatureList,
    # key=operator.attrgetter('relatedfeatureid__samplingfeaturecode'))
    # #relatedFeatureList.order_by('relatedfeatureid__samplingfeaturecode')
    int_selectedvariable_ids = []
    for int_selectedvariableid in selectedMVariableSeries:
        int_selectedvariable_ids.append(int(int_selectedvariableid))
    # if the user hit the export csv button export the measurement results to csv
    linkExtProperty = Extensionproperties.objects.filter(propertyname="DatasetFileLink").get()
    datasetresults = Datasetsresults.objects.filter(resultid__in=selectedMResultsSeries)
    datasets = Datasets.objects.filter(datasetid__in=datasetresults.values("datasetid"))
    datasetcitations = Datasetcitations.objects.filter(datasetid__in=datasets)
    citations = Citations.objects.filter(citationid__in=datasetcitations.values("citationid"))

    datasetcitationlinks = {}
    for citation in citations:
        extprop = Citationextensionpropertyvalues.objects.filter(citationid=citation).get(propertyid=linkExtProperty)
        try:
            datasetcitationlinks[citation.title] = extprop.propertyvalue
        except ObjectDoesNotExist:
            datasetcitationlinks[citation.title] = ''
    if 'export_data' in request.POST:
        resultValuesSeries = resultValuesSeries.order_by(
            "resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturecode",
            "resultid__intendedzspacing", "resultid__resultid__variableid",
            "resultid__resultid__unitsid")
        response = exportspreadsheet(request, resultValuesSeries)
        return response
    else:
        # this removes duplicates from a list of strings
        name_of_units = removeDupsFromListOfStrings(name_of_units)
        # raise ValidationError(relatedFeatureList)
        return TemplateResponse(request, template,
                                {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                 'datasetcitationlinks': datasetcitationlinks,
                                 'variableList': variableList,
                                 'SelectedVariables': int_selectedvariable_ids,
                                 'authenticated': authenticated, 'data_disclaimer': data_disclaimer,
                                 'chartID': chartID, 'chart': chart, 'series': series,
                                 'title2': title2, 'graphType': graphType, 'yAxis': yAxis,
                                 'name_of_units': name_of_units,
                                 'samplingfeaturelabel': samplingfeaturelabel,
                                 'relatedFeatureList': relatedFeatureList,
                                 'SelectedRelatedFeature': selected_relatedfeatid,
                                 'name': request.user, 'site_title': admin.site.site_title,
                                 'site_header': admin.site.site_header,
                                 'short_title': 'Soils Data'
                                 }, )