import cStringIO as StringIO
import math
import json
import time
from datetime import datetime
from datetime import timedelta
from time import mktime
from django import template
from django.contrib import admin
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.mail import EmailMessage
from django.core import mail
from django.core.management import settings
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import management
# from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
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
from .models import Datasets
from .models import Datasetsresults
from .models import Featureactions
from .models import Methods
from .models import People
from .models import Processinglevels
from .models import Profileresults
from .models import Profileresultvalues
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
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated():
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][1]['title']}
        return TemplateResponse(request, 'AddSensor.html', context)
    else:
        return HttpResponseRedirect('../')


def chartIndex(request):
    if request.user.is_authenticated():
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][5]['title']}
        return TemplateResponse(request, 'chartIndex.html', context)
    else:
        return HttpResponseRedirect('../')


# chartIndex
def AddProfile(request):
    if request.user.is_authenticated():
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][2]['title']}
        return TemplateResponse(request, 'AddProfile.html', context)
    else:
        return HttpResponseRedirect('../')


def RecordAction(request):
    if request.user.is_authenticated():
        context = {'prefixpath': settings.CUSTOM_TEMPLATE_PATH, 'name': request.user,
                   'authenticated': True, 'site_title': admin.site.site_title,
                   'site_header': admin.site.site_header,
                   'short_title': settings.ADMIN_SHORTCUTS[0]['shortcuts'][3]['title']}
        return TemplateResponse(request, 'RecordAction.html', context)
    else:
        return HttpResponseRedirect('../')


def ManageCitations(request):
    if request.user.is_authenticated():
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
        featureactionid=selected_result.values('featureactionid'))
    title_sampling_feature = Samplingfeatures.objects.filter(
        samplingfeatureid=title_feature_action.values('samplingfeatureid'))
    s = str(title_sampling_feature.values_list('samplingfeaturename', flat=True))
    name_of_sampling_feature = s.split('\'')[1]
    return name_of_sampling_feature


def get_name_of_variable(selected_result):
    title_variables = Variables.objects.filter(variableid=selected_result.values('variableid'))
    s = str(title_variables.values_list('variablecode', flat=True))
    name_of_variable = s.split('\'')[1]
    return name_of_variable


def get_name_of_units(selected_result):
    title_units = Units.objects.filter(unitsid=selected_result.values('unitsid'))
    s = str(title_units.values_list('unitsname', flat=True))
    name_of_units = s.split('\'')[1]
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
    if request.user.is_authenticated():
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
        features = Samplingfeatures.objects.all()
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
            site = Sites.objects.get(samplingfeatureid=sf.samplingfeatureid)
            feat.update({
                'sitetype': site.sitetypecv.name,
                'sitetypeurl': site.sitetypecv.sourcevocabularyuri
            })

        # Get Specimen Attr
        if sf.sampling_feature_type.name == 'Specimen':
            specimen = Specimens.objects.get(samplingfeatureid=sf.samplingfeatureid)
            feat.update({
                'specimentype': specimen.specimentypecv.name,
                'specimentypeurl': specimen.specimentypecv.sourcevocabularyuri,
                'specimenmedium': specimen.specimenmediumcv.name,
                'specimenmediumurl': specimen.specimenmediumcv.sourcevocabularyuri,
            })
        # Get Relations
        relationship = get_relations(sf)
        if relationship['siblings'] == [] or relationship['siblings'] is None \
                and relationship['parents'] == [] or relationship['parents'] is None \
                and relationship['children'] == [] or relationship['children'] is None:
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


def get_relations(s):
    pf = Relatedfeatures.objects.filter(samplingfeatureid_id=s.samplingfeatureid)
    cf = Relatedfeatures.objects.filter(relatedfeatureid_id=s.samplingfeatureid)
    sibsf = None
    parents = None
    children = None
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
    if not request.user.is_authenticated():
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
        enddt = time.strptime(end_date, "%Y-%m-%d %H:%M")
        dt = datetime.fromtimestamp(mktime(enddt))
        last_day_previous_month = dt - timedelta(days=30)
        entered_start_date = last_day_previous_month.strftime('%Y-%m-%d %H:%M')
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
        enddt = time.strptime(end_date, "%Y-%m-%d %H:%M")
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
        selected_result = Results.objects.filter(resultid=selectedMResult)
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
        selected_result = Results.objects.filter(resultid=selectedMResult)
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
            data['datavalue' + str(i)].append([mills, dataval])
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


def mappopuploader(request, feature_action='NotSet', samplingfeature='NotSet', dataset='NotSet',
                   resultidu='NotSet',
                   startdate='NotSet', enddate='NotSet', popup='NotSet'):
    if not request.user.is_authenticated():
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
    try:
        if not useDataset:
            if useSamplingFeature:
                samplefeature = Samplingfeatures.objects.\
                    filter(samplingfeatureid=samplingfeature).get()
                featureActions = Featureactions.objects.\
                    filter(samplingfeatureid=samplefeature).\
                    order_by("action__method")
                resultList = Results.objects.filter(featureactionid__in=featureActions)\
                     .filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid__action__method")
                actions = Actions.objects.filter(actionid__in=featureActions.values("action"))
                methods = Methods.objects.filter(methodid__in=actions.values("method"))
                featureActionLocation = samplefeature.samplingfeaturename
            else:
                resultList = Results.objects.filter(featureactionid=feature_action)\
                    .filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid__action__method")
                featureActions = Featureactions.objects.filter(featureactionid=feature_action).get()
                featureActionLocation = featureActions.samplingfeatureid.samplingfeaturename
                featureActionMethod = featureActions.action.method.methodname
                actions = Actions.objects.filter(actionid=featureActions.action.actionid).get()
                methods = Methods.objects.filter(methodid=actions.method.methodid)
        else:
            datasetResults = Datasetsresults.objects.filter(datasetid=dataset)
            resultList = Results.objects.filter(resultid__in=datasetResults.values(
                "resultid")).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid__action__method")
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
            realstartdates.append(datetime.strptime(startdate.propertyvalue, "%Y-%m-%d %H:%M"))
        for enddate in enddates:
            realenddates.append(datetime.strptime(enddate.propertyvalue, "%Y-%m-%d %H:%M"))
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
        except IndexError:
            # html = "<html><body>No Data Available Yet.</body></html>"
            # return HttpResponse(html)
            methodsOnly = 'True'
    except ValueError:
            # html = "<html><body>No Data Available Yet.</body></html>"
            # return HttpResponse(html)
            methodsOnly = 'True'

    return TemplateResponse(request, template, {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'useSamplingFeature': useSamplingFeature,
                                                'methodsOnly': methodsOnly,
                                                'featureActions': featureActions,
                                                'featureActionMethod': featureActionMethod,
                                                'featureActionLocation': featureActionLocation,
                                                'data_disclaimer': data_disclaimer,
                                                'datasetTitle': datasetTitle,
                                                'datasetAbstract': datasetAbstract,
                                                'useDataset': useDataset, 'startDate': startdate,
                                                'endDate': enddate,
                                                'authenticated': authenticated, 'methods': methods,
                                                'resultList': resultList}, )

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_annotation(request):
    # print('annotate')
    resultid = None
    annotationvals = None
    annotation = None
    setNaNstr = None
    setNaN = False
    cvqualitycode = None
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        # print(resultid)
    if 'annotation' in request.POST:
        annotation = str(request.POST['annotation'])
        # print(annotation)
    # annotationtype
    if 'cvqualitycode' in request.POST:
        cvqualitycode = str(request.POST['cvqualitycode'])
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
    annotationobj = Annotations(annotationtypecv= annotationtype, annotationcode='',
                                annotationtext=annotation, annotationdatetime=datetime.now(),
                                annotationutcoffset=4)
    annotationobj.save()
    lastannotationval = None
    for rid in resultid:
        intrid = int(rid)
        for annotationval in annotationvals:
            if is_number(annotationval):
                floatval = float(annotationval)
                try:
                    tsrvquery = Timeseriesresultvalues.objects.filter(resultid=intrid).filter(
                        valuedatetime=lastannotationval).filter(datavalue=floatval)
                    # print(tsrvquery.query)
                    tsrv = tsrvquery.get()
                    if setNaN:
                        annotation += ' original value was ' + str(tsrv.datavalue)
                        annotationobj = Annotations(annotationtypecv= annotationtype, annotationcode='',
                                                    annotationtext=annotation,
                                                    annotationdatetime=datetime.now(),
                                                    annotationutcoffset=4)
                        annotationobj.save()
                        tsrv.datavalue = float('nan')
                        tsrv.qualitycodecv = qualitycode
                        tsrv.save()
                    elif cvqualitycode:
                        tsrv.qualitycodecv = qualitycode
                        tsrv.save()
                    tsrvanno = Timeseriesresultvalueannotations(valueid=tsrv,
                                                                annotationid=annotationobj)
                    tsrvanno.save()
                except ObjectDoesNotExist:
                    print('no matching time series result value for query')
                    print(tsrvquery.query)
                # tsrvanno.save()
                # print(tsrvanno.valueid)
            lastannotationval = annotationval
    # if resultidu != 'NotSet':
    #    resultidu = int(resultidu)
    return HttpResponse({'prefixpath': settings.CUSTOM_TEMPLATE_PATH, },content_type='application/json')

def addL1timeseries(request):
    resultid = None
    response_data = {}
    createorupdateL1 = None
    pl1 = Processinglevels.objects.get(processinglevelid=2)
    valuesadded = 0
    tsresultTocopyBulk = []
    if 'createorupdateL1' in request.POST:
        createorupdateL1 = str(request.POST['createorupdateL1'])
    if 'resultidu[]' in request.POST:
        resultid = request.POST.getlist('resultidu[]')
        for result in resultid:
            if createorupdateL1 == "create":
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
                        print(tsrv.valueid)
                        tsrva.save()
                    except ObjectDoesNotExist:
                        tsrv.valueid = None
                        tsresultTocopyBulk.append(tsrv)
                newtsrv = Timeseriesresultvalues.objects.bulk_create(tsresultTocopyBulk)
            elif createorupdateL1 == "update":
                tsresultL0 = Timeseriesresults.objects.get(resultid=result)
                resultL0 = Results.objects.get(resultid=result)
                tsrvL0 = Timeseriesresultvalues.objects.filter(resultid=tsresultL0)
                tsrvAddToL1Bulk = []
                relatedL1result = Results.objects.filter(
                        featureactionid = resultL0.featureactionid).filter(
                        variableid = resultL0.variableid
                    ).filter(unitsid = resultL0.unitsid).get(
                    processing_level=pl1)
                newresult = relatedL1result.resultid
                relateL1tsresult = Timeseriesresults.objects.filter(resultid= relatedL1result).get()
                # print(relateL1tsresult)
                # maxtsrvL1=Timeseriesresultvalues.objects.filter(resultid=relateL1tsresult).annotate(
                #        Max('valuedatetime')). \
                #        order_by('-valuedatetime')
                # print(relateL1tsresult)
                # for r in maxtsrvL1:
                #     print(r)

                maxtsrvL1=Timeseriesresultvalues.objects.filter(resultid=relateL1tsresult).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime
                maxtsrvL0=Timeseriesresultvalues.objects.filter(resultid=tsresultL0).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime
                mintsrvL1=Timeseriesresultvalues.objects.filter(resultid=relateL1tsresult).annotate(
                        Min('valuedatetime')). \
                        order_by('valuedatetime')[0].valuedatetime
                mintsrvL0=Timeseriesresultvalues.objects.filter(resultid=tsresultL0).annotate(
                        Min('valuedatetime')). \
                        order_by('valuedatetime')[0].valuedatetime
                if maxtsrvL1 < maxtsrvL0:
                    tsrvAddToL1 = tsrvL0.filter(valuedatetime__gt=maxtsrvL1)
                    for tsrv in tsrvAddToL1:
                        tsrv.resultid = relateL1tsresult
                        try:
                            tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                            tsrv.valueid = None
                            tsrv.save()
                            tsrva.valueid = tsrv
                            print(tsrv.valueid)
                            tsrva.save()
                        except ObjectDoesNotExist:
                            tsrv.valueid = None
                            tsresultTocopyBulk.append(tsrv)
                if mintsrvL1 > mintsrvL0:
                    tsrvAddToL1 = tsrvL0.filter(valuedatetime__lt=mintsrvL1)
                    for tsrv in tsrvAddToL1:
                        tsrv.resultid = relateL1tsresult
                        try:
                            tsrva = Timeseriesresultvalueannotations.objects.get(valueid = tsrv.valueid)
                            tsrv.valueid = None
                            tsrv.save()
                            tsrva.valueid = tsrv
                            print(tsrv.valueid)
                            tsrva.save()
                        except ObjectDoesNotExist:
                            tsrv.valueid = None
                            tsresultTocopyBulk.append(tsrv)
                newtsrv = Timeseriesresultvalues.objects.bulk_create(tsrvAddToL1Bulk)
            valuesadded = newtsrv.__len__()
            response_data['valuesadded'] = valuesadded
            # response_data['newresultid'] = newresult
            # print(result)
    return HttpResponse(json.dumps(response_data),content_type='application/json')

def email_data_from_graph(request):
    emailsent = False
    outEmail = ''
    entered_end_date = ''
    entered_start_date = ''
    myresultSeriesExport = []
    if 'email_data' in request.POST and 'myresultSeriesExport[]' in request.POST:
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
            myresultSeriesExport = Timeseriesresultvaluesextwannotations.objects.all() \
                    .filter(valuedatetime__gte=entered_start_date) \
                    .filter(valuedatetime__lte=entered_end_date) \
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
        else:
            myresultSeriesExport = Timeseriesresultvaluesextwannotations.objects.all() \
                    .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
        emailspreadsheet2(request, myresultSeriesExport, False) # for command str_selectedresultid_ids
        
        # .after_response    
        emailsent=True
    return HttpResponse({'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'emailsent': emailsent,
                                                'outEmail': outEmail,},content_type='application/json')

def TimeSeriesGraphingShort(request, feature_action='NotSet', samplingfeature='NotSet',
                            dataset='NotSet',
                            resultidu='NotSet', startdate='NotSet', enddate='NotSet',
                            popup='NotSet'):  # ,startdate='',enddate=''
    authenticated = True
    if not request.user.is_authenticated():
        # return HttpResponseRedirect('../')
        authenticated = False
    if popup == 'NotSet':
        template = loader.get_template('chart2.html')
    elif popup == 'Anno':
        if not authenticated:
            return HttpResponseRedirect(settings.CUSTOM_TEMPLATE_PATH)
        template = loader.get_template('chartAnnotation.html')
    else:
        template = loader.get_template('chartpopup.html')
    data_disclaimer = settings.DATA_DISCLAIMER
    map_config = settings.MAP_CONFIG
    useDataset = False
    useSamplingFeature = False
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
        resultidu = int(resultidu)

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
    # print(settings.MAP_CONFIG['result_value_processing_levels_to_display'])
    if not useDataset:
        if useSamplingFeature:
            samplefeature = Samplingfeatures.objects.filter(samplingfeatureid=samplingfeature).get()
            feature_actions = Featureactions.objects.filter(samplingfeatureid=samplefeature)
            resultList = Results.objects.filter(featureactionid__in=feature_actions).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid","resultid")
            actions = Actions.objects.filter(actionid__in=feature_actions.values("action"))
            methods = Methods.objects.filter(methodid__in=actions.values("method"))
            featureActionLocation = samplefeature.samplingfeaturename
        else:
            resultList = Results.objects.filter(featureactionid=feature_action).filter(
                 processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                 ).order_by("featureactionid","resultid")
            featureAction = Featureactions.objects.filter(featureactionid=feature_action).get()
            featureActionLocation = featureAction.samplingfeatureid.samplingfeaturename
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
    for i in range(0, numresults):
        selectionStr = str('selection' + str(i))
        # when annotating you can only select a single time series
        # with a radio button
        if popup == 'Anno':
            selectionStr = str('selection')
        if selectionStr in request.POST:
            # raise ValidationError(request.POST[selectionStr])
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
                Results.objects.filter(resultid=int(resultidu)).filter(
                   processing_level__in=settings.MAP_CONFIG['result_value_processing_levels_to_display']
                ).get()
                selectedMResultSeries.append(int(resultidu))
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
        entered_start_date = datetime_entered_end_date - timedelta(
            map_config['time_series_months'] * 365 / 12)  # .strftime('%Y-%m-%d %H:%M')
        entered_start_date = entered_start_date.strftime('%Y-%m-%d %H:%M')
    for selectedMResult in selectedMResultSeries:
        i += 1
        selected_result = Results.objects.filter(resultid=selectedMResult)
        selected_results.append(selected_result)
        # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        name_of_sampling_features.append(tmpname)
        myresultSeries.append(Timeseriesresultvalues.objects.all()
                              .filter(~Q(datavalue__lte=-6999))
                              .filter(valuedatetime__gt=entered_start_date)
                              .filter(valuedatetime__lt=entered_end_date)
                              .filter(resultid=selectedMResult).order_by('-valuedatetime'))

        data.update({'datavalue' + str(i): []})
    # myresultSeriesExport = None
    # if 'useDates' in request.POST:
    #     use_dates = request.POST['useDates']
    #     myresultSeriesExport = Timeseriesresultvaluesext.objects.all() \
    #             .filter(valuedatetime__gte=entered_start_date) \
    #             .filter(valuedatetime__lte=entered_end_date) \
    #             .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
    #
    # else:
    #     myresultSeriesExport = Timeseriesresultvaluesext.objects.all() \
    #             .filter(resultid__in=selectedMResultSeries).order_by('-valuedatetime')
    # if the user hit the export csv button export the measurement results to csv
    # emailsent = False
    # outEmail = ''
    # if 'outEmail' in request.POST:
    #         outEmail = request.POST['outEmail']
    # if 'email_data' in request.POST:
    #     emailspreadsheet2.after_response(request, myresultSeriesExport, False) # for command str_selectedresultid_ids
    #     emailsent=True

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
    for myresults in myresultSeries:
        i += 1
        resultannotationsexist = False
        for result in myresults:
            start = datetime(1970, 1, 1)
            delta = result.valuedatetime - start
            mills = delta.total_seconds() * 1000
            if math.isnan(result.datavalue):
                dataval = 'null'
            else:
                dataval = result.datavalue
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
                        [mills,dataval])
               #{"x": mills, "y": dataval, "z": str(result.valueid)})  # dumptoMillis(result.valuedatetime)
            # data['datavalue'].extend(tmplist )
            # data['valuedatetime'].append(dumptoMillis(result.valuedatetime))

    timeseriesresults = Timeseriesresults.objects.\
        filter(resultid__in=resultList.values("resultid")).\
        order_by("resultid__variableid", "aggregationstatisticcv")
    # build strings for graph labels

    i = 0
    seriesStr = ''
    unit = ''
    location = ''
    variable = ''
    aggStatistic = ''
    series = []
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
        series.append({"name": str(unit) + ' - ' + str(variable) + ' - ' +
                      str(aggStatistic) + ' - ' + str(location), "allowPointSelect": "true", "yAxis": str(unit),
                      "data": data['datavalue' + str(i)]})

        if popup == 'Anno':
            relatedresults = Results.objects.filter(
                featureactionid = selectedMResult.featureactionid).filter(
                variableid = selectedMResult.variableid
            ).filter(unitsid = selectedMResult.unitsid)
            for rr in relatedresults:
                if rr.processing_level.processinglevelid ==2:
                    L1exists = True
            if annotationsexist:
                series.append({"name": 'Annotated ' + str(unit) + ' - ' + str(variable) + ' - ' +
                                str(aggStatistic) + ' - ' + str(location), "allowPointSelect": "false", "yAxis": str(unit),
                                "data": data['datavalueannotated']})
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
    xAxis = {"type": 'datetime', "title": {"text": 'Date'}}
    yAxis = {"title": {"text": seriesStr}}
    graphType = 'scatter'

    int_selectedresultid_ids = []
    str_selectedresultid_ids = []
    for int_selectedresultid in selectedMResultSeries:
        int_selectedresultid_ids.append(int(int_selectedresultid))
        str_selectedresultid_ids.append(str(int_selectedresultid))
    csvexport = False
    cvqualitycode = None
    if popup == 'Anno':
        cvqualitycode = CvQualitycode.objects.all()

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
    return TemplateResponse(request, template, {'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                                                'startDate': entered_start_date,
                                                'endDate': entered_end_date,
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
                                                'name_of_units': name_of_units}, )


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
    if not request.user.is_authenticated():
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
    myfile = StringIO.StringIO()
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

        myfile = StringIO.StringIO()
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
        emailtext = emailtext + ' - ' + str(lastResult.email_text())
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
                position += 1
            myfile.write(myresults.csvoutputShort())
            position += 1
            k += 1
        # response = StreamingHttpResponse(myfile.getvalue(), content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
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
    if not request.user.is_authenticated():
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
    if samplingfeature != 'NotSet':
        samplingfeature = int(samplingfeature)
        useSamplingFeature = True
    # find variables found at the sampling feature
    # need to go through featureaction to get to results

    # need the feature actions for all of the sampling features related to this sampling feature
    if not useSamplingFeature:
        sampling_features = Relatedfeatures.objects.filter(
            relatedfeatureid__exact=selected_relatedfeatid).values(
            'samplingfeatureid')
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
        selected_result = Results.objects.filter(resultid=selectedMResult.resultid)
        # if 'update_result_on_related_feature' in request.POST:
        # raise ValidationError(selected_result)
        selected_results.append(selected_result)
        # name_of_sampling_features.append(get_name_of_sampling_feature(selected_result))

        tmpname = get_name_of_sampling_feature(selected_result)
        tmpLocName = tmpname

        tmpname = get_name_of_variable(selected_result)
        unitAndVariable = tmpname
        if name_of_variables.__len__() > 0:
            name_of_variables.append(tmpname)
        else:
            name_of_variables.append(tmpname)
        tmpname = get_name_of_units(selected_result)
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
                                 'variableList': variableList,
                                 'SelectedVariables': int_selectedvariable_ids,
                                 'authenticated': authenticated, 'data_disclaimer': data_disclaimer,
                                 'chartID': chartID, 'chart': chart, 'series': series,
                                 'title2': title2, 'graphType': graphType, 'yAxis': yAxis,
                                 'name_of_units': name_of_units,
                                 'relatedFeatureList': relatedFeatureList,
                                 'SelectedRelatedFeature': selected_relatedfeatid,
                                 'name': request.user, 'site_title': admin.site.site_title,
                                 'site_header': admin.site.site_header,
                                 'short_title': 'Soils Data'}, )
