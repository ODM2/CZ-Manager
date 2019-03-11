# from __future__ import unicode_literals
# import compiler

import os
import stat
import subprocess
import sys
import datetime as datetime
from django.utils.crypto import get_random_string
from django.core import management
from django.core import serializers
from django.core.management import settings
from templatesAndSettings.settings import exportdb
from django.http import HttpResponse
from hs_restclient import HydroShare, HydroShareAuthOAuth2
# from odm2admin.tasks import create_sqlite_export_celery

from django.contrib.gis import forms, admin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django.core.management import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CharField
from django.forms import ModelForm
from django.forms import TypedChoiceField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html, format_html_join
from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportActionModelAdmin
from django.db.models import Max
from .management.commands.ProcessDataLoggerFile import updateStartDateEndDate
from .models import Actionby, Specimens
from .models import Actions
from .models import Affiliations
from .models import Authorlists
from .models import Citationextensionpropertyvalues
from .models import Citationexternalidentifiers
from .models import Citations
from .models import CvQualitycode
from .models import CvSitetype
from .models import Dataloggerfilecolumns
from .models import Dataloggerfiles
from .models import Dataloggerprogramfiles
from .models import Dataquality
from .models import Datasetcitations
from .models import Datasets
from .models import Datasetsresults
from .models import Equipmentmodels
from .models import Extensionproperties
from .models import Externalidentifiersystems
from .models import Featureactions
from .models import Instrumentoutputvariables
from .models import MeasurementresultvalueFile
from .models import Methodcitations
from .models import Methods
from .models import Organizations
from .models import People
from .models import Personexternalidentifiers
from .models import Profileresults
from .models import Processinglevels
from .models import ProcessDataloggerfile
from .models import Relatedactions
from .models import Relatedfeatures
from .models import Relatedresults
from .models import Results
from .models import Resultextensionpropertyvalues
from .models import Resultsdataquality
from .models import Samplingfeatureextensionpropertyvalues
from .models import Samplingfeatureexternalidentifiers
from .models import Samplingfeatures
from .models import Spatialreferences
from .models import Taxonomicclassifiers
from .models import Timeseriesresults
from .models import Timeseriesresultvalues
from .models import Units
from .models import Sites
from .models import Variables
from .models import Resultderivationequations
from .models import Derivationequations
from .models import CvCensorcode
# from io import StringIO
from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField

from .models import Measurementresults
from .models import Measurementresultvalues
from .models import Profileresultvalues
# from .views import dataloggercolumnView
from daterange_filter.filter import DateRangeFilter
import re

from .readonlyadmin import ReadOnlyAdmin
from .listfilters import SamplingFeatureTypeListFilter
# import pyproj

# from .admin import MeasurementresultvaluesResource
# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),
# Organizations.objects.all().order_by('organizationname'))

# a complicated use of search_fields described in ResultsAdminForm

# the following define what fields should be overridden so that
# dropdown lists can be populated with useful information

def link_list_display_DOI(link):
    if link:
        match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+", link)
        if not match:
            match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])[[:graph:]])+", link)

        if match:
            return format_html('<a href="http://dx.doi.org/%s" target="_blank">%s</a>' % (link, link))
        else:
            return format_html('<a href="%s" target="_blank">%s</a>' % (link, link))
    else:
        return format_html('<a href="%s" target="_blank">%s</a>' % (link, link))


class variablesInLine(admin.StackedInline):
    model = Variables

class actionByInLine(admin.StackedInline):
    model = Actionby
    extra = 0
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('actionid',
                       'affiliationid',
                       'isactionlead',
                       'roledescription',
                       )

        }),
    )

class ReadOnlyActionByInLine(actionByInLine):
    readonly_fields = actionByInLine.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False

class unitsInLine(admin.StackedInline):
    model = Units
    # fieldsets = (
    #     ('Details', {
    #         'classes': ('collapse',),
    #         'fields': ('unitsid',
    #                    'unit_type',
    #                    'unitsabbreviation',
    #                    'unitsname',
    #                    'unitslink',
    #                    )
    #
    #     }),
    # )
    extra = 0


class FeatureActionsInline(admin.StackedInline): # AjaxSelectAdminStackedInline
    model = Featureactions
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('featureactionid',
                       'samplingfeatureid',
                       'action',
                       )

        }),
    )
    extra = 0


class ReadOnlyFeatureActionsInline(FeatureActionsInline):
    readonly_fields = FeatureActionsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class CitationextensionpropertyvalueInline(admin.StackedInline):
    model = Citationextensionpropertyvalues
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('citationid',
                       'propertyid',
                       'propertyvalue',)
        }),
    )
    extra = 6


class ReadOnlyCitationextensionpropertyvalueInline(CitationextensionpropertyvalueInline):
    readonly_fields = CitationextensionpropertyvalueInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class resultsInLine(admin.StackedInline):
    model = Results


# Resultsdataquality AdminForm
class ResultsdataqualityAdminForm(ModelForm):
    resultid = make_ajax_field(Datasetsresults, 'resultid',
                               'result_lookup')

    class Meta:
        model = Resultsdataquality
        fields = ['dataqualityid', 'bridgeid', 'resultid']


class ResultsdataqualityAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Resultsdataquality._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ResultsdataqualityAdminForm
    inlines_list = list()

    list_display = ('resultid', 'dataqualityid')



class DatasetsresultsInlineAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='A data result',
                                       label='Data result',show_help_text =None)

    class Meta:
        model = Datasetsresults
        fields = ['datasetid', 'bridgeid', 'resultid']

class DatasetsResultsInline(admin.StackedInline):
    model = Datasetsresults
    form = DatasetsresultsInlineAdminForm
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('datasetid', 'bridgeid', 'resultid'
                       )
        }),
    )
    extra = 0

class ReadOnlyDatasetsResultsInline(DatasetsResultsInline):
    readonly_fields = DatasetsResultsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False

class DatasetsresultsAdminForm(ModelForm):
    resultid = make_ajax_field(Datasetsresults, 'resultid',
                               'result_lookup')

    class Meta:
        model = Datasetsresults
        fields = ['datasetid', 'bridgeid', 'resultid']


class DatasetsresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Datasetsresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DatasetsresultsAdminForm
    inlines_list = list()


class DataqualityAdminForm(ModelForm):
    class Meta:
        model = Dataquality
        fields = '__all__'


class DataqualityAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Dataquality._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DataqualityAdminForm
    inlines_list = list()

    list_display = ('dataqualitytypecv',
                    'dataqualitycode',
                    'dataqualityvalue',
                    'dataqualityvalueunitsid')


class MethodcitationsAdminForm(ModelForm):
    class Meta:
        model = Methodcitations
        fields = '__all__'


class MethodcitationsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Methodcitations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = MethodcitationsAdminForm
    inlines_list = list()

    list_display = ('method_id', 'method_link', 'relationshiptypecv', 'citation_link')

    def method_link(self, obj):
        return format_html('<a href="%smethods/%s/">See Method</a>' % (settings.CUSTOM_TEMPLATE_PATH,
                                                            obj.methodid.methodid))

    def citation_link(self, obj):
        return format_html('<a href="%scitations/%s/">%s</a>' % (settings.CUSTOM_TEMPLATE_PATH,
                                                      obj.citationid.citationid,
                                                      obj.citationid))

    def method_id(self, obj):
        return obj.methodid

    method_id.short_description = "Method and Citation Link"
    method_link.short_description = 'link to method'
    method_link.allow_tags = True
    citation_link.short_description = 'link to citation'
    citation_link.allow_tags = True


class AuthorlistsAdminForm(ModelForm):
    class Meta:
        model = Authorlists
        fields = '__all__'


class AuthorlistsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Authorlists._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = AuthorlistsAdminForm
    inlines_list = list()

    list_display = ('personid', 'citationid')


class DatasetcitationsAdminForm(ModelForm):
    class Meta:
        model = Datasetcitations
        fields = '__all__'


class DatasetcitationsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Datasetcitations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DatasetcitationsAdminForm
    inlines_list = list()

    list_display = ('datasetid', 'relationshiptypecv', 'citationid')


class InstrumentoutputvariablesInline(admin.StackedInline):
    model = Instrumentoutputvariables
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('instrumentoutputvariableid',
                       'modelid',
                       'variableid',
                       'instrumentmethodid',
                       'instrumentresolution',
                       'instrumentaccuracy',
                       'instrumentrawoutputunitsid',)
        }),
    )
    extra = 0


class ReadOnlyInstrumentoutputvariablesInline(InstrumentoutputvariablesInline):
    readonly_fields = InstrumentoutputvariablesInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class authorlistInline(admin.StackedInline):
    model = Authorlists
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('personid',
                       'authororder',)
        }),
    )
    extra = 0


class ReadOnlyauthorlistInline(authorlistInline):
    readonly_fields = authorlistInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class CitationsAdminForm(ModelForm):
    title = forms.CharField(max_length=255, widget=forms.Textarea, label="Publication Title")

    class Meta:
        model = Citations
        fields = '__all__'


class DOIInline(admin.StackedInline):
    model = Citationexternalidentifiers
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('bridgeid',
                       'citationid',
                       'externalidentifiersystemid',
                       'citationexternalidentifier',
                       'citationexternalidentifieruri')
        }),
    )
    extra = 0


class ReadOnlyDOIInline(DOIInline):
    readonly_fields = DOIInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class CitationsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Citations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyauthorlistInline,
                             ReadOnlyDOIInline,
                             ReadOnlyCitationextensionpropertyvalueInline]

    # For admin users
    form = CitationsAdminForm
    inlines_list = [authorlistInline, DOIInline, CitationextensionpropertyvalueInline]

    list_display = ('primary_author', 'publicationyear',
                    'title', 'other_author',
                    'publisher', 'doi',
                    'citation_link')
    list_display_links = ['title']
    search_fields = ['title', 'publisher',
                     'publicationyear', 'authorlists__personid__personfirstname',
                     'authorlists__personid__personlastname']

    def citation_link(self, obj):
        return link_list_display_DOI(obj.citationlink)

    def doi(self, obj):
        external_id = Citationexternalidentifiers.objects.get(citationid=obj.citationid)
        return format_html('<a href="http://dx.doi.org/{0}" target="_blank">{0}</a>'.format(
            external_id.citationexternalidentifier))

    def primary_author(self, obj):
        author_list = Authorlists.objects.filter(citationid=obj.citationid)
        first_author = author_list.get(authororder=1)
        return "{0}, {1}".format(first_author.personid.personlastname,
                                 first_author.personid.personfirstname)

    def other_author(self, obj):
        list_et_al = list()
        author_list = Authorlists.objects.filter(citationid=obj.citationid)
        for author in author_list:
            if author.authororder != 1:
                list_et_al.append(
                    "{0}, {1}".format(author.personid.personlastname,
                                      author.personid.personfirstname))
        return "; ".join(list_et_al)

    doi.allow_tags = True
    citation_link.short_description = 'link to citation'
    other_author.short_description = 'Other Authors'
    citation_link.allow_tags = True
    # primary_author.admin_order_field = 'authorlists__personid__personlastname'


class CitationextensionpropertyvaluesAdminForm(ModelForm):
    propertyvalue = forms.CharField(max_length=255, widget=forms.Textarea)

    class Meta:
        model = Citationextensionpropertyvalues
        fields = '__all__'


class CitationextensionpropertyvaluesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Citationextensionpropertyvalues._meta.get_fields() if
                     not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = CitationextensionpropertyvaluesAdminForm
    inlines_list = list()

    list_display = ('citationid', 'propertyid', 'propertyvalue')


class ExtensionpropertiesAdminForm(ModelForm):
    propertydescription = forms.CharField(max_length=255, widget=forms.Textarea,
                                          label="Property description")

    class Meta:
        model = Extensionproperties
        fields = '__all__'


class ExtensionpropertiesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Extensionproperties._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ExtensionpropertiesAdminForm
    inlines_list = list()

    list_display = ('propertyname', 'propertydescription', 'propertydatatypecv', 'propertyunitsid')


class VariablesAdminForm(ModelForm):
    # variabletypecv= TermModelChoiceField(CvVariabletype.objects.all().order_by('term'))
    # variablenamecv= TermModelChoiceField(CvVariablename.objects.all().order_by('term'))
    # speciationcv= TermModelChoiceField(CvSpeciation.objects.all().order_by('term'))
    # make these fields ajax type ahead fields with links to odm2 controlled vocabulary
    variable_type = AutoCompleteSelectField('cv_variable_type', required=True,
                                            label='variable type')
    #AutoCompleteSelectField('featureaction_lookup', required=True, help_text='',
    #                                          label='Sampling feature action')
    variable_name = AutoCompleteSelectField('cv_variable_name', required=True,
                                            label = 'variable name')
    #make_ajax_field(Variables, 'variable_name', 'cv_variable_name')
    variabledefinition = forms.CharField(max_length=500, widget=forms.Textarea)
    # variable_type = make_ajax_field(Variables,'variable_type','cv_variable_type')
    speciation = make_ajax_field(Variables, 'speciation', 'cv_speciation')

    variable_name.help_text = format_html('view variable names here <a href="http://vocabulary.odm2.org/' \
                              'variablename/" target="_blank">' \
                              'http://vocabulary.odm2.org/variablename/</a>')
    variable_name.allow_tags = True
    variable_type.help_text = format_html('view variable types here <a href="http://vocabulary.odm2.org/' \
                              'variabletype/" target="_blank" >' \
                              'http://vocabulary.odm2.org/variabletype/</a>')
    variable_type.allow_tags = True
    speciation.help_text = format_html('view variable types here <a href="http://vocabulary.odm2.org/' \
                           'speciation/" target="_blank" >' \
                           'http://vocabulary.odm2.org/speciation/</a>')
    speciation.allow_tags = True

    class Meta:
        model = Variables
        fields = '__all__'


class VariablesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Variables._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = VariablesAdminForm
    inlines_list = list()

    list_display = ('variablecode',
                    'variable_name_linked',
                    'variable_type_linked',
                    'speciation_linked')
    search_fields = ['variable_type__name',
                     'variable_name__name',
                     'variablecode',
                     'speciation__name']
    save_as = True
    def variable_name_linked(self, obj):
        if obj.variable_name:
            return format_html('<a href="http://vocabulary.odm2.org/variablename/{0}" target=' \
                   '"_blank">{1}</a>'.format(obj.variable_name.term, obj.variable_name.name))

    variable_name_linked.short_description = 'Variable Name'
    variable_name_linked.allow_tags = True

    def variable_type_linked(self, obj):
        if obj.variable_type:
            return format_html('<a href="http://vocabulary.odm2.org/variabletype/{0}" target=' \
                   '"_blank">{1}</a>'.format(obj.variable_type.term, obj.variable_type.name))

    variable_type_linked.short_description = 'Variable Type'
    variable_type_linked.allow_tags = True

    def speciation_linked(self, obj):
        if obj.speciation:
            return format_html('<a href="http://vocabulary.odm2.org/speciation/{0}" target=' \
                   '"_blank">{1}</a>'.format(obj.speciation.term, obj.speciation.name))

    speciation_linked.short_description = 'Speciation'
    speciation_linked.allow_tags = True


class TaxonomicclassifiersAdminForm(ModelForm):
    taxonomic_classifier_type = make_ajax_field(Taxonomicclassifiers, 'taxonomic_classifier_type',
                                                'cv_taxonomic_classifier_type',show_help_text =None)
    taxonomic_classifier_type.help_text = u'A vocabulary for describing types of taxonomies ' \
                                          u'from which descriptive terms used ' \
                                          u'in an ODM2 database have been drawn. ' \
                                          u'Taxonomic classifiers provide a way to classify' \
                                          u' Results and Specimens according to terms ' \
                                          u'from a formal taxonomy. Check ' \
                                          u'<a href="http://vocabulary.odm2.org/' \
                                          u'taxonomicclassifiertype/" target="_blank">' \
                                          u'http://vocabulary.odm2.org/' \
                                          u'taxonomicclassifiertype/</a> for more info'
    taxonomic_classifier_type.allow_tags = True

    class Meta:
        model = Taxonomicclassifiers
        fields = '__all__'


class TaxonomicclassifiersAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Taxonomicclassifiers._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = TaxonomicclassifiersAdminForm
    inlines_list = list()

    search_fields = ['taxonomicclassifiername', 'taxonomicclassifiercommonname',
                     'taxonomicclassifierdescription', 'taxonomic_classifier_type__name']

class SitesAdminForm(ModelForm):
    samplingfeatureid = AutoCompleteSelectField('sampling_feature_lookup', required=True, help_text='',
                                              label='Sampling feature',show_help_text =None)
    class Meta:
        model = Sites
        fields = '__all__'

class SitesAdmin(admin.ModelAdmin):
    form = SitesAdminForm
    search_fields = ['samplingfeatureid__samplingfeaturename','samplingfeatureid__samplingfeaturecode'
        , 'samplingfeatureid__samplingfeaturedescription']
    list_display = ('samplingfeatureid', 'sitetypecv','latitude', 'longitude', 'spatialreferenceid')
    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


class SpatialreferencesAdminForm(ModelForm):
    class Meta:
        model = Spatialreferences
        fields = '__all__'

class SpatialreferencesAdmin(admin.ModelAdmin):
    form = SpatialreferencesAdminForm
    search_fields = ['srscode','srsname', 'srsdescription']
    list_display = ('srscode', 'srsname','srsdescription', 'srslink')
    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups



class SamplingfeatureexternalidentifiersAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatureexternalidentifiers
        fields = '__all__'


class SamplingfeatureexternalidentifiersAdmin(admin.ModelAdmin):
    form = SamplingfeatureexternalidentifiersAdminForm
    search_fields = ['samplingfeatureexternalidentifier']
    list_display = ('samplingfeatureexternalidentifier', 'samplingfeatureexternalidentifieruri')
    save_as = True
    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups
#
# class SamplingfeaturesFormset(forms.models.BaseInlineFormSet):
#     def clean(self):
#         super(SamplingfeaturesFormset, self).clean()
#         # make sure deadline is set
#         for form in self.forms:
#          if not form.is_valid():
#             return #other errors exist, so don't bother
#          samplingfeaturetype = form.cleaned_data['sampling_feature_type']
#          sitetypecv = form.cleaned_data['Sitetypecv']
#          if form.cleaned_data and not form.cleaned_data.get('DELETE') \
#              and samplingfeaturetype=='Site' and sitetypecv==None :
#             raise ValidationError('If sampling feature is of type site it must have a related site,'+
#                                   ' see inline forms below')


class SamplingfeaturesAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatures
        # formset = SamplingfeaturesFormset
        fields = ['sampling_feature_type', 'samplingfeaturecode', 'samplingfeaturename',
                  'samplingfeaturedescription', 'sampling_feature_geo_type', 'featuregeometrywkt',
                  'featuregeometry',
                  'elevation_m', 'elevation_datum']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            if instance.featuregeometry:
                feat = instance.featuregeometrywkt()
                initial = kwargs.get('initial', {})
                initial['featuregeometrywkt'] = '{}'.format(feat)
                kwargs['initial'] = initial
        super(SamplingfeaturesAdminForm, self).__init__(*args, **kwargs)

    featuregeometrywkt = forms.CharField(
        help_text="feature geometry (to add a point format is POINT(lon lat)" +
                  " where lon and lat are in decimal degrees. If you don't want to add a "
                  "location" + " leave default value of POINT(0 0).", label='Featuregeometrywkt',
        widget=forms.Textarea, required=False)
    featuregeometrywkt.initial = GEOSGeometry("POINT(0 0)")

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')
    sampling_feature_type.help_text = u'A vocabulary for describing the type of SamplingFeature. ' \
                                      u'Many different SamplingFeature types can be represented ' \
                                      u'in ODM2. SamplingFeatures of type Site and Specimen ' \
                                      u'will be the most common, ' \
                                      u'but many different types of varying levels of ' \
                                      u'complexity can be used. ' \
                                      u'details for individual values ' \
                                      u'here: <a href="http://vocabulary.odm2.org/' \
                                      u'samplingfeaturetype/" target="_blank">http://vocabulary.' \
                                      u'odm2.org/samplingfeaturetype/</a>'
    sampling_feature_type.allow_tags = True

    samplingfeaturedescription = CharField(max_length=5000, label="feature description",
                                           widget=forms.Textarea,
                                           required=False)

    sampling_feature_geo_type = make_ajax_field(Samplingfeatures, 'sampling_feature_geo_type',
                                                'cv_sampling_feature_geo_type')
    sampling_feature_geo_type.help_text = u'A vocabulary for describing the geospatial feature ' \
                                          u'type associated with a SamplingFeature. ' \
                                          u'For example, Site SamplingFeatures are ' \
                                          u'represented as ' \
                                          u'points. ' \
                                          u'In ODM2, each SamplingFeature may have only one ' \
                                          u'geospatial type, ' \
                                          u'but a geospatial types may range from ' \
                                          u'simple points to ' \
                                          u'a complex polygons ' \
                                          u'or even three dimensional volumes. ' \
                                          u'details for individual values ' \
                                          u'here: <a href="http://vocabulary.odm2.org/' \
                                          u'samplingfeaturegeotype/" ' \
                                          u'target="_blank">http://vocabulary.odm2.org/' \
                                          u'samplingfeaturegeotype/</a>'
    sampling_feature_geo_type.allow_tags = True
    sampling_feature_geo_type.required = False

    elevation_datum = make_ajax_field(Samplingfeatures, 'elevation_datum',
                                      'cv_elevation_datum')
    elevation_datum.help_text = u'A vocabulary for describing vertical datums. ' \
                                u'Vertical datums are used in ODM2 to specify the ' \
                                u'origin for elevations ' \
                                u'assocated with SamplingFeatures.' \
                                u'details for individual values ' \
                                u'here: <a href="http://vocabulary.odm2.org/elevationdatum/" ' \
                                u'target="_blank">http://vocabulary.odm2.org/elevationdatum/</a>'
    elevation_datum.allow_tags = True
    # featuregeometry is not working in production I think GDAL_DATA setting is needed but I'm not sure what to point
    # it to. This was not working well in either case though.
    # featuregeometry = forms.PointField(label='Featuregeometry',
    #                                    widget=forms.OSMWidget(), required=False)

    # featuregeometry.initial = GEOSGeometry("POINT(0 0)")


class SitesInline(admin.StackedInline):
    model = Sites
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('samplingfeatureid',
                       'sitetypecv',
                       'latitude',
                       'longitude',
                       'spatialreferenceid',
                       )
        }),
    )
    max_num = 1
    extra = 0
    min_num = 1


class ReadOnlySitesInline(SitesInline):
    readonly_fields = SitesInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class SpecimensInline(admin.StackedInline):
    model = Specimens
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('samplingfeatureid',
                       'specimentypecv',
                       'specimenmediumcv',
                       'isfieldspecimen',
                       )
        }),
    )
    max_num = 1
    extra = 0
    min_num = 1


class ReadOnlySpecimenInline(SpecimensInline):
    readonly_fields = SpecimensInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class IGSNInline(admin.StackedInline):
    model = Samplingfeatureexternalidentifiers
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('bridgeid',
                       'samplingfeatureid',
                       'externalidentifiersystemid',
                       'samplingfeatureexternalidentifier',
                       'samplingfeatureexternalidentifieruri',
                       )
        }),
    )
    max_num = 1
    extra = 0


class ReadOnlyIGSNInline(IGSNInline):
    readonly_fields = IGSNInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False

class SamplingfeatureextensionpropertiesInline(admin.StackedInline):
    model = Samplingfeatureextensionpropertyvalues
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('bridgeid',
                       'samplingfeatureid',
                       'propertyid',
                       'propertyvalue',
                       )
        }),
    )
    max_num = 2
    extra = 0


class ReadOnlySamplingfeatureextensionpropertiesInline(IGSNInline):
    readonly_fields = SamplingfeatureextensionpropertiesInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class SamplingfeaturesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Samplingfeatures._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [
        ReadOnlyFeatureActionsInline,
        ReadOnlyIGSNInline,
        ReadOnlySitesInline,
        ReadOnlySpecimenInline
    ]

    form = SamplingfeaturesAdminForm
    inlines_list = [
        FeatureActionsInline,
        IGSNInline,
        SamplingfeatureextensionpropertiesInline,
        SitesInline,
        SpecimensInline
    ]

    def get_formsets_with_inlines(self, request, obj=None):
        """
        Yields formsets and the corresponding inlines.
        """
        if obj:
            if obj.sampling_feature_type.name == 'Site':
                filtinline = [item for item in self.get_inline_instances(request, obj)
                              if item.verbose_name != 'Specimen']
            elif obj.sampling_feature_type.name == 'Specimen':
                filtinline = [item for item in self.get_inline_instances(request, obj)
                              if item.verbose_name != 'Site']
            else:
                filtinline = self.get_inline_instances(request, obj)[:-2]

            for inline in filtinline:
                yield inline.get_formset(request, obj), inline
        else:
            for inline in self.get_inline_instances(request, obj):
                yield inline.get_formset(request, obj), inline

    search_fields = ['sampling_feature_type__name', 'sampling_feature_geo_type__name',
                     'samplingfeaturename',
                     'samplingfeaturecode', 'samplingfeatureid',
                     'samplingfeatureexternalidentifiers__samplingfeatureexternalidentifier']

    list_display = (
        'samplingfeaturecode', 'samplingfeaturename', 'sampling_feature_type_linked',
        'samplingfeaturedescription',
        'igsn',
        'dataset_code')
    readonly_fields = ('samplingfeatureuuid',)

    list_filter = (SamplingFeatureTypeListFilter,)

    # your own processing
    def save_model(self, request, obj, form, change):
        # for example:
        obj.featuregeometry = '%s' % form.cleaned_data['featuregeometrywkt']
        obj.save()

    save_as = True

    def igsn(self, obj):
        external_id = Samplingfeatureexternalidentifiers.objects.get(
            samplingfeatureid=obj.samplingfeatureid)
        return format_html('<a href="https://app.geosamples.org/sample/igsn/{0}" ' \
               'target="_blank">{0}</a>'.format(external_id.samplingfeatureexternalidentifier))

    igsn.allow_tags = True

    def dataset_code(self, obj):
        fid = Featureactions.objects.filter(samplingfeatureid=obj.samplingfeatureid)
        ds = Datasets.objects.filter(datasetsresults__resultid__featureactionid__in=fid).distinct()
        ds_list = list()
        for d in ds:
            ds_list.append(d.datasetcode)
        return ", ".join(ds_list)

    def sampling_feature_type_linked(self, obj):
        if obj.sampling_feature_type:
            return format_html('<a href="http://vocabulary.odm2.org/samplingfeaturetype/{0}" ' \
                   'target="_blank">{1}</a>'.format(obj.sampling_feature_type.term,
                                                     obj.sampling_feature_type.name))

    sampling_feature_type_linked.short_description = 'Sampling feature / location type'
    sampling_feature_type_linked.allow_tags = True

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


# class SamplingfeaturesAdmin(admin.OSMGeoAdmin):
#     form = SamplingfeaturesAdminForm
#     inlines = [FeatureActionsInline, IGSNInline]
#     search_fields = ['sampling_feature_type__name', 'sampling_feature_geo_type__name',
#                      'samplingfeaturename',
#                      'samplingfeaturecode', 'samplingfeatureid',
#                      'samplingfeatureexternalidentifiers__samplingfeatureexternalidentifier']
#
#     list_display = (
#         'samplingfeaturecode', 'samplingfeaturename', 'sampling_feature_type_linked',
#         'samplingfeaturedescription',
#         'igsn',
#         'dataset_code')
#     readonly_fields = ('samplingfeatureuuid',)
#
#     # your own processing
#     def save_model(self, request, obj, form, change):
#         # for example:
#         obj.featuregeometry = '%s' % form.cleaned_data['featuregeometrywkt']
#         obj.save()
#
#     save_as = True
#
#     def igsn(self, obj):
#         external_id = Samplingfeatureexternalidentifiers.objects.get(
#             samplingfeatureid=obj.samplingfeatureid)
#         return u'<a href="https://app.geosamples.org/sample/igsn/{0}" ' \
#                u'target="_blank">{0}</a>'.format(external_id.samplingfeatureexternalidentifier)
#
#     igsn.allow_tags = True
#
#     @staticmethod
#     def dataset_code(obj):
#         fid = Featureactions.objects.filter(samplingfeatureid=obj.samplingfeatureid)
#         ds = Datasets.objects.filter(datasetsresults__resultid__featureactionid__in=fid).
# distinct()
#         ds_list = list()
#         for d in ds:
#             ds_list.append(d.datasetcode)
#         return ", ".join(ds_list)
#
#     def sampling_feature_type_linked(self, obj):
#         if obj.sampling_feature_type:
#             return u'<a href="http://vocabulary.odm2.org/samplingfeaturetype/{0}" ' \
#                    u'target="_blank">{1}</a>'.format(obj.sampling_feature_type.term,
#                                                      obj.sampling_feature_type.name)
#
#     sampling_feature_type_linked.short_description = 'Sampling Feature Type'
#     sampling_feature_type_linked.allow_tags = True


def duplicate_results_event(ModelAdmin, request, queryset):
    for obj in queryset:
        obj.resultid = None
        obj.save()


duplicate_results_event.short_description = "Duplicate selected result"


#
# class FeatureactionsField(ajax_select.make_ajax_field):
#     def to_python(self, value):
#         featureactioniduni= self.data['featureactionid']
#         for faiduni in featureactioniduni.split("-"):
#              if faiduni.isdigit():
#                  featureactionid = faiduni
#                  continue
#         featureaction = Featureactions.objects.filter(featureactionid=featureactionid)
#         self.data['featureactionid'] = featureaction
#         return featureaction


class TimeseriesresultsInline(admin.StackedInline):
    model = Timeseriesresults
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('resultid',
                       'xlocation',
                       'xlocationunitsid',
                       'ylocation',
                       'ylocationunitsid',
                       'zlocation',
                       'zlocationunitsid',
                       'spatialreferenceid',
                       'intendedtimespacing',
                       'intendedtimespacingunitsid',
                       'aggregationstatisticcv',
                       )
        }),
    )
    extra = 0


class ReadOnlyTimeseriesresultsInline(TimeseriesresultsInline):
    readonly_fields = TimeseriesresultsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class MeasurementResultsInline(admin.StackedInline):
    model = Measurementresults
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('resultid',
                       'xlocation',
                       'xlocationunitsid',
                       'ylocation',
                       'ylocationunitsid',
                       'zlocation',
                       'zlocationunitsid',
                       'spatialreferenceid',
                       'censorcodecv',
                       'qualitycodecv',
                       'aggregationstatisticcv',
                       'timeaggregationinterval',
                       'timeaggregationintervalunitsid',

                       )
        }),
    )
    extra = 0


class ReadOnlyMeasurementResultsInline(MeasurementResultsInline):
    readonly_fields = MeasurementResultsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class ProfileResultsInline(admin.StackedInline):
    model = Profileresults
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('resultid',
                       'xlocation',
                       'xlocationunitsid',
                       'ylocation',
                       'ylocationunitsid',
                       'spatialreferenceid',
                       'intendedzspacing',
                       'intendedzspacingunitsid',
                       'intendedtimespacing',
                       'intendedtimespacingunitsid',
                       'aggregationstatisticcv',

                       )
        }),
    )
    extra = 0


class ReadOnlyProfileResultsInline(ProfileResultsInline):
    readonly_fields = ProfileResultsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ResultsAdminForm(ModelForm):
    # featureactionid = make_ajax_field(Featureactions,'featureactionid','featureaction_lookup',
    # max_length=500)
    featureactionid = AutoCompleteSelectField('featureaction_lookup', required=True, help_text='',
                                              label='Sampling feature / location action',show_help_text =None)

    def clean_featureactionid(self):
        featureactioniduni = self.data['featureactionid']
        featureactionid = None
        for faiduni in featureactioniduni.split("-"):
            if faiduni.isdigit():
                featureactionid = faiduni
                continue
        featureaction = Featureactions.objects.filter(featureactionid=featureactionid).get()
        return featureaction

    class Meta:
        model = Results
        fields = '__all__'
        # make_ajax_field doesn't work with the add + green plus on the field

        # widgets = {
        #     'featureactionid': autocomplete.ModelSelect2(url='featueactions-autocomplete')
        # }


# The user can click, a popup window lets them create a new object, they click save,
# the popup closes and the AjaxSelect field is set.
# Your Admin must inherit from AjaxSelectAdmin
# http://django-ajax-selects.readthedocs.org/en/latest/Admin-add-popup.html
class ResultsAdmin(ReadOnlyAdmin):  # admin.ModelAdmin
    # The user can click, a popup window lets them create a new object,
    # they click save, the popup closes and the AjaxSelect field is set.
    # http://django-ajax-selects.readthedocs.org/en/latest/Admin-add-popup.html
    # For readonly usergroup
    user_readonly = [p.name for p in Results._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyTimeseriesresultsInline,
                             ReadOnlyMeasurementResultsInline,
                             ReadOnlyProfileResultsInline]

    # For admin users
    form = ResultsAdminForm
    inlines_list = [TimeseriesresultsInline, MeasurementResultsInline, ProfileResultsInline]

    list_display = ['resultid', 'featureactionid', 'variableid', 'processing_level']
    search_fields = ['variableid__variable_name__name', 'variableid__variablecode',
                     'variableid__variabledefinition',
                     'featureactionid__samplingfeatureid__samplingfeaturename',
                     'result_type__name', 'processing_level__definition']

    actions = [duplicate_results_event]
    save_as = True

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)

        if self.__user_is_readonly(request):
            actions = list()

        return actions

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


class RelatedactionsAdminForm(ModelForm):
    # actionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    # relationshiptypecv= TermModelChoiceField(CvRelationshiptype.objects.all().order_by('term'))
    # relatedactionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    class Meta:
        model = Relatedactions
        fields = '__all__'


class RelatedactionsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Relatedactions._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = RelatedactionsAdminForm
    inlines_list = list()


class OrganizationsAdminForm(ModelForm):
    # organizationtypecv= TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))
    # parentorganizationid =OrganizationsModelChoiceField( Organizations.objects.all().
    # order_by('organizationname'))
    class Meta:
        model = Organizations
        fields = '__all__'


class OrganizationsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Organizations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = OrganizationsAdminForm
    inlines_list = list()

    list_display = ('organizationname', 'organizationdescription', 'organization_link')

    def organization_link(self, org):
        return format_html('<a href={0} target="_blank">{0}</a>'.format(org.organizationlink))

    organization_link.allow_tags = True


class SamplingFeaturesInline(admin.StackedInline):
    model = Samplingfeatures
    extra = 0

class ActionsInline(admin.StackedInline):
    model = Actions
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('actionid',
                       'action_type',
                       'method',
                       'begindatetime',
                       'begindatetimeutcoffset',
                       'enddatetime',
                       'enddatetimeutcoffset',
                       'actiondescription',
                       'actionfilelink',
                       )

        }),
    )
    extra = 0


class ReadOnlyActionsInline(ActionsInline):
    readonly_fields = ActionsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class DerivationequationsAdminForm(ModelForm):
    derivationequation = CharField(max_length=255, label="derivation equation",
                                   widget=forms.Textarea,
                                   help_text='use python snytax if you are using this equation to derive new' +
                            'values in ODM2 Admin as shown here' +
                            ' https://en.wikibooks.org/wiki/Python_Programming/Basic_Math' +
                            ' this currently supports 1 derived from field which should be x in the equation.' +
                            ' the derived value must be stored in a variable y')

    class Meta:
        model = Derivationequations
        fields = '__all__'

class DerivationequationsAdmin(ReadOnlyAdmin):
    user_readonly = [p.name for p in Derivationequations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()
    inlines_list = list()
    # For admin users
    form = DerivationequationsAdminForm
    list_display = ['derivationequation', ]
    # list_display_links = None
    save_as = True
    search_fields = ['derivationequationid','derivationequation']


class ResultderivationequationsAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result that is a product of this derivation equation',
                                       label='Data result',show_help_text =None)
    class Meta:
        model = Resultderivationequations
        fields = '__all__'

class ResultderivationequationsAdmin(ReadOnlyAdmin):
    user_readonly = [p.name for p in Resultderivationequations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()
    inlines_list = list()
    # For admin users
    form = ResultderivationequationsAdminForm
    list_display = ['resultid', 'derivationequationid', ]
    save_as = True
    search_fields = [ 'resultid__variableid__variable_name__name',
                     'resultid__variableid__variablecode',
                     'resultid__variableid__variabledefinition',
                     'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'derivationequationid__derivationequation']

def create_derived_values_event(ModelAdmin, request, queryset):
     StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
     EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
     qualitycode = CvQualitycode.objects.filter(name="Good").get()
     censorcode = CvCensorcode.objects.filter(name="Not censored").get()
     bulktimeseriesvalues = []
     for relatedresults in queryset:
        resultidtoderive = relatedresults.resultid #16678
        tsrtoderive = Timeseriesresults.objects.get(resultid=resultidtoderive.resultid)
        relatedresult = relatedresults.relatedresultid
        relationshipType = relatedresults.relationshiptypecv
        if not relationshipType.name == 'Is derived from':
            raise forms.ValidationError("relationship type is not \'Is derived from\'")
        try:
            derivedenddaterepv = Resultextensionpropertyvalues.objects.filter(resultid=resultidtoderive.resultid).filter(
                propertyid=EndDateProperty).get()
            derivedenddate= derivedenddaterepv.propertyvalue
            derivedstartdaterepv = Resultextensionpropertyvalues.objects.filter(resultid=resultidtoderive.resultid).filter(
            propertyid=StartDateProperty).get()
            derivedstartdate = derivedstartdaterepv.propertyvalue
        except ObjectDoesNotExist:
            derivedenddate='1800-01-01 00:00'
            derivedstartdate='1800-01-01 00:00'
        # values to derive from more recent then last derived value
        fromvalues = Timeseriesresultvalues.objects.filter(resultid=relatedresult.resultid
                            ).filter(valuedatetime__gt=derivedenddate)
        # raise forms.ValidationError("derived end date: " + derivedenddate.propertyvalue +
        #                            " derived resultid: " + str(resultidtoderive.resultid))
        resultequation = Resultderivationequations.objects.filter(resultid=resultidtoderive.resultid).get()
        equation = Derivationequations.objects.filter(derivationequationid=resultequation.derivationequationid.derivationequationid).get()
        equationvalue = equation.derivationequation
        y = 0
        for vals in fromvalues:
            x = vals.datavalue
            d = dict(locals(), **globals())
            # exec equationvalue in d
            exec(equationvalue, d,d)
            derivedvalue =  d["y"]
            # raise forms.ValidationError('original value: ' + str(x) + ' new value: ' + str(derivedvalue))
            tsrv = Timeseriesresultvalues(
                resultid=tsrtoderive,
                datavalue=derivedvalue,
                valuedatetime=vals.valuedatetime,
                valuedatetimeutcoffset=4,
                censorcodecv=censorcode,
                qualitycodecv=qualitycode,
                timeaggregationinterval=tsrtoderive
                .intendedtimespacing,
                timeaggregationintervalunitsid=tsrtoderive
                .intendedtimespacingunitsid)
            bulktimeseriesvalues.append(tsrv)
        Timeseriesresultvalues.objects.bulk_create(bulktimeseriesvalues)
        tsrvb = len(bulktimeseriesvalues)
        newenddate = Timeseriesresultvalues.objects.filter(resultid=resultidtoderive.resultid).annotate(
                        Max('valuedatetime')). \
                        order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M')
        updateStartDateEndDate(resultidtoderive, derivedstartdate, newenddate)
        messages.info(request,str(tsrvb) + " Derived time series values succesfully created, ending on "+str(newenddate))

create_derived_values_event.short_description = "create derived values based " \
                                                    " on this relationship"


class RelatedresultsAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result',
                                       label='Data result' ,show_help_text =None)
    relatedresultid = AutoCompleteSelectField('result_lookup', required=True,
                                              help_text='resulted related to first result',
                                              label='Related data result' ,show_help_text =None)
    class Meta:
        model = Relatedresults
        fields = '__all__'

class RelatedresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup

    user_readonly = [p.name for p in Relatedresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()
    # For admin users
    form = RelatedresultsAdminForm
    inlines_list = list()
    actions = [create_derived_values_event]
    list_display = ['resultid', 'relationshiptypecv', 'relatedresultid',  'versioncode',
                    'relatedresultsequencenumber']
    save_as = True
    search_fields = ['resultid__variableid__variable_name__name',
                     'resultid__variableid__variablecode',
                     'resultid__variableid__variabledefinition',
                     'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'relatedresultid__variableid__variable_name__name',
                     'relatedresultid__variableid__variablecode',
                     'relatedresultid__variableid__variabledefinition',
                     'relatedresultid__featureactionid__samplingfeatureid__samplingfeaturename']

class FeatureactionsAdminForm(ModelForm):
    samplingfeatureid = AutoCompleteSelectField('sampling_feature_lookup', required=True, help_text='',
                                              label='Sampling feature',show_help_text =None)
    class Meta:
        model = Featureactions
        fields = '__all__'


class FeatureactionsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Featureactions._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = FeatureactionsAdminForm
    inlines_list = list()

    list_display = ['samplingfeatureid', 'action', ]
    save_as = True
    search_fields = ['action__method__methodname', 'samplingfeatureid__samplingfeaturename']


def createODM2SQLiteFile(results, dataset,request, username, password):
    myresultSeriesExport = []

    # for result in results:
    # emailspreadsheet2(request, myresultSeriesExport, False)
    # management.call_command('dump_object', 'odm2admin.Timeseriesresults', 17160, 17162, kitchensink=True)
    sysout = sys.stdout
    loc = settings.FIXTURE_DIR
    # print(myresultSeriesExport.first())
    startdate = None
    enddate = None
    site = None
    lastsite = None
    fixturecount = 0
    # print('looping results')
    for result in results:
        myresultSeriesExport = Timeseriesresultvalues.objects.filter(resultid=result.resultid).order_by('valuedatetime')
        # print('result count for:')
        # print(result)
        # print(myresultSeriesExport.count())
        fixturecount += 1
        tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
        sys.stdout = open(loc + tmpfixture1, 'w')
        management.call_command('dump_object', 'odm2admin.CvOrganizationtype', '*', kitchensink=False)
        sys.stdout.close()

        fixturecount += 1
        tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
        sys.stdout = open(loc + tmpfixture1, 'w')
        if myresultSeriesExport.count() > 0:
            startdate = myresultSeriesExport.first().valuedatetime
            enddate = myresultSeriesExport.last().valuedatetime
            management.call_command('dump_object', 'odm2admin.Timeseriesresultvalues',
                                    myresultSeriesExport.first().valueid, kitchensink=True)
            # site = Sites.objects.filter(samplingfeatureid=result.featureactionid.samplingfeatureid).get()
            # if not site == lastsite:
            #     sys.stdout.close()
            #     sys.stdout = sysout
            #     print(site)
            #     print(site.samplingfeatureid.samplingfeatureid)
            #     print(fixturecount)
            #     fixturecount += 1
            #     tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
            #     print(tmpfixture1)
            #     sys.stdout = open(loc + tmpfixture1, 'w')
            #     management.call_command('dump_object', 'odm2admin.Sites', '*', kitchensink=True)
            #
            # sys.stdout.close()
            # lastsite = site
        else:
            myresultSeriesExport = Profileresultvalues.objects.filter(resultid=result.resultid)
            # print(myresultSeriesExport.first().valueid)
            # print(myresultSeriesExport.first())
            if myresultSeriesExport.count() > 0:
                management.call_command('dump_object', 'odm2admin.Profileresultvalues',
                                        myresultSeriesExport.first().valueid, kitchensink=True)
        sys.stdout.close()



    fixturecount += 1
    tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
    sys.stdout = open(loc + tmpfixture1, 'w')
    management.call_command('dump_object', 'odm2admin.Datasets', dataset.datasetid, kitchensink=False)
    sys.stdout.close()

    fixturecount += 1
    tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
    sys.stdout = open(loc + tmpfixture1, 'w')
    management.call_command('dump_object', 'odm2admin.Sites', '*', kitchensink=False)
    sys.stdout.close()

    fixturecount += 1
    tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
    sys.stdout = open(loc + tmpfixture1, 'w')
    # codes = CvCensorcode.objects.all()
    management.call_command('dump_object', 'odm2admin.CvCensorcode',
                            '*', kitchensink=False)
    sys.stdout.close()

    fixturecount += 1
    tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
    sys.stdout = open(loc + tmpfixture1, 'w')
    management.call_command('dump_object', 'odm2admin.CvQualitycode',
                            '*', kitchensink=False)

    sys.stdout.close()

    for result in results:
        fixturecount += 1
        tmpfixture1 = 'tmp' + str(fixturecount) + '.json'  # + random_string
        sys.stdout = open(loc + tmpfixture1, 'w')
        myresultSeriesExport = Timeseriesresultvalues.objects.filter(resultid=result.resultid)
        if myresultSeriesExport.count() > 0:
            sys.stdout.write(serializers.serialize("json", myresultSeriesExport[1:], indent=4,
                                                   use_natural_foreign_keys=False, use_natural_primary_keys=False))
        else:
            myresultSeriesExport = Profileresultvalues.objects.filter(resultid=result.resultid)
            if myresultSeriesExport.count() > 0:
                sys.stdout.write(
                    serializers.serialize("json", myresultSeriesExport[1:], indent=4, use_natural_foreign_keys=False,
                                          use_natural_primary_keys=False))
        sys.stdout.close()
    sys.stdout = sysout

    # settings.MAP_CONFIG['result_value_processing_levels_to_display']
    # db_name = exportdb.DATABASES['export']['NAME']
    # print(db_name)
    # print(tmploc1)
    database = ''

    # management.call_command('loaddata',
    #                        tmploc1 ,database=database)  # ,database='export'
    # print('finished first file')
    # management.call_command('loaddata',
    #                        tmploc2,database=database)
    # export_data.send(sender= Timeseriesresultvalues,tmploc1=tmploc1,tmploc2=tmploc2)
    # management.call_command('create_sqlite_export',tmploc1,tmploc2, settings=exportdb)
    # call('../')
    # print(tmploc1)
    # print(tmploc2)
    dbfilepath = settings.TEMPLATE_DIR + '/ODM2SQliteBlank.sqlite'  # exportdb.DATABASES['default']['NAME']
    path = os.path.dirname(dbfilepath)
    dbfile = os.path.basename(dbfilepath)
    dbfilename = os.path.splitext(dbfile)[0]
    random_string = get_random_string(length=5)
    dbfilename2 = dbfilename + random_string + ".sqlite"
    dbfile2 = path + "/" + dbfilename + random_string + ".sqlite"
    # command = ['python',  '/home/azureadmin/webapps/ODM2-AdminLCZO/manageexport.py', 'create_sqlite_export', tmploc1, tmploc2]
    command = 'cp ' + dbfilepath + ' ' + dbfile2

    response = subprocess.check_call(command, shell=True)
    # write an extra settings file instead - have it contain just DATABASES; remove databases from exportdb.py and import new file. 2
    # exportdb.DATABASES['export']['NAME'] = dbfile2
    # print(sys.path)
    # oldexportdb = path + '/templatesAndSettings/settings/exportdb.py'
    # copyexportdb = path + '/templatesAndSettings/settings/exportdbold.py'
    # command = 'cp ' + oldexportdb + ' ' + copyexportdb

    # response = subprocess.check_call(command, shell=True)
    # sys.stdout = open(oldexportdb)
    command = 'cp ' + dbfilepath + ' ' + str(dbfile2)
    # exportsettings = "DATABASES = { \n" + \
    #                  "'default': { \n" + \
    #                  "'ENGINE': 'django.db.backends.sqlite3','NAME':'" + settings.TEMPLATE_DIR + dbfile2 + "',}, 'export': {'ENGINE': 'django.db.backends.sqlite3','NAME':'" + settings.TEMPLATE_DIR + dbfile2 + "',}}"
    # print(exportsettings)
    sys.stdout = sysout
    sys.stdout = open(path + '/templatesAndSettings/scripts/create_sqlite_file2.sh', 'w')
    # / home / miguelcleon / webapps / odm2admin2 / manageexport.py
    # create_sqlite_export
    # sys.stdout = sysout
    commandstring = '#!/usr/bin/env bash \n'

    commandstring += settings.PYTHON_EXEC + ' '  # sys.executable

    commandstring += path + '/manageexport.py'
    commandstring += ' create_sqlite_export2 '
    commandstring += dbfile2 + ' '
    fixturelist = []
    for x in range(1, fixturecount + 1):
        tmpfixture1 = 'tmp' + str(x) + '.json'  # + random_string
        commandstring += loc + tmpfixture1 + ' '
        fixturelist.append(loc + tmpfixture1)

    commandstring += ' > ' + path + '/templatesAndSettings/logging/sqlite_export.log \n'
    print(commandstring)
    user = request.user.get_full_name()

    try:
        startdate = datetime.datetime.strptime(str(startdate), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    except ValueError:
        startdate = datetime.datetime.strptime(str(startdate), '%Y-%m-%d %H:%M:%S.$f').strftime('%Y-%m-%d')
    try:
        enddate = datetime.datetime.strptime(str(enddate), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    except ValueError:
        enddate = datetime.datetime.strptime(str(enddate), '%Y-%m-%d %H:%M:%S.$f').strftime('%Y-%m-%d')

    hydrosharecommand = settings.PYTHON_EXEC + ' '  # sys.executable

    hydrosharecommand += path + "/manageexport.py"
    hydrosharecommand += " create_hydroshare_resource '" + username + "' '" + password + "' '" +\
                         user + "' '" + dataset.datasettitle + "' '" + startdate + "' '" + enddate +\
                         "' " + dbfile2 + " " + dbfilename2
    hydrosharecommand += ' > ' + path + '/templatesAndSettings/logging/hydroshare_export.log \n'
    print(hydrosharecommand)
    # cpcommand = 'cp ' + copyexportdb  + ' ' +  oldexportdb
    # print(cpcommand)
    command = path + '/templatesAndSettings/scripts/create_sqlite_file2.sh'  # + dbfile2 + ' %>> ' + settings.BASE_DIR +'/logging/sqlite_export.log'
    st = os.stat(command)
    sys.stdout = sysout
    try:
        os.chmod(command, st.st_mode | stat.S_IEXEC)
    except OSError as e:
        print(e)
        pass
    # print(command)
    sys.stdout = sysout
    print(commandstring)
    # instead of running the .sh file here use incrontab to check if the file create_sqlite_file2.sh changed and execute it.

    args = [command]
    # os.execv('sudo bash',args) # command_path
    # os.execv(settings.PYTHON_EXEC, [settings.PYTHON_EXEC] +commandstring)
    # print("response")
    # print(response)
    # command = 'cp ' + copyexportdb + ' ' + oldexportdb

    # response = subprocess.check_call(command,shell=True)
    # print(exportdb.DATABASES['default']['NAME'])

    return myresultSeriesExport, startdate, enddate, fixturecount, dbfile2, dbfilename2


def export_to_hydroshare(request, results, datasets):
    username = None
    password = None
    auth = None

    if 'hydroshareUsername' in request.POST and 'hydrosharePassword' in request.POST:
        hs_client_id = settings.SOCIAL_AUTH_HYDROSHARE_UP_KEY
        hs_client_secret = settings.SOCIAL_AUTH_HYDROSHARE_UP_SECRET
        username = request.POST['hydroshareUsername']
        password = request.POST['hydrosharePassword']
        auth = HydroShareAuthOAuth2(hs_client_id, hs_client_secret,
                                    username=username, password=password)

    valuestoexport, startdate, enddate, \
    fixturecount, dbfiletoupload, dbfilename2 = createODM2SQLiteFile(
        results, datasets, request, username, password)
    # print(username)
    # print(password)
    export_complete = True
    resource_link = ''
    messages.info(request,'request in being processed. It may take a few minutes' +\
                          ', or longer depending on the size of your dataset, for your Hydroshare resource to appear. ')
    return HttpResponse({'prefixpath': settings.CUSTOM_TEMPLATE_PATH,
                         'export_complete': export_complete,
                         'username': username,
                         'resource_link': resource_link, }, content_type='application/json')


def publish_dataset_to_hydroshare(ModelAdmin, request, queryset):
    results = None
    for dataset in queryset:
        relateddatasetresults = Datasetsresults.objects.filter(datasetid=dataset)
        results = Results.objects.filter(resultid__in=relateddatasetresults.values('resultid'))
        print('result count')
        print(results.count())
        export_to_hydroshare(request, results, dataset)


publish_dataset_to_hydroshare.short_description = "export dataset results as a hydroshare resource. "


class DatasetsAdminForm(ModelForm):
    datasetabstract = forms.CharField(max_length=5000, widget=forms.Textarea)


    class Meta:
        model = Datasets
        fields = '__all__'


class DatasetsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Datasets._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyDatasetsResultsInline]
    actions = [publish_dataset_to_hydroshare]

    # For admin users
    form = DatasetsAdminForm
    inlines_list = [DatasetsResultsInline]

    list_display = ['datasetcode', 'datasettitle', 'datasettypecv']

    def get_datasetsresults(self, object_id):
        datasetResults = Datasetsresults.objects.filter(datasetid=object_id)
        # raise ValidationError(datasetResults)
        return datasetResults

    def get_results(self, object_id):
        ids = []
        datasetResults = Datasetsresults.objects.filter(datasetid=object_id)
        for result in datasetResults:
            ids += [result.resultid.resultid]
        resultsList = Results.objects.filter(resultid__in=ids)
        # raise ValidationError(datasetResults)
        # return queryset.filter(resultid__in=ids)
        return resultsList

    # What is this for?
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DatasetResultsList'] = self.get_datasetsresults(object_id)
        extra_context['ResultsList'] = self.get_results(object_id)
        extra_context['prefixpath'] = settings.CUSTOM_TEMPLATE_PATH
        return super(DatasetsAdmin, self).change_view(request, object_id, form_url,
                                                      extra_context=extra_context)


# class AffiliationsAdminForm(ModelForm):
#     class Meta:
#         model = Affiliations
#         fields = '__all__'
#
#
# class AffiliationsAdmin(admin.ModelAdmin):
#     form = AffiliationsAdminForm


class ActionsAdminForm(ModelForm):
    actiondescription = CharField(max_length=5000, label="Action description",
                                  widget=forms.Textarea, required=False)
    action_type = make_ajax_field(Actions, 'action_type', 'cv_action_type')
    action_type.help_text = u'A vocabulary for describing the type of actions performed in ' \
                            u'making observations. Depending' \
                            u' on the action type, the action may or may not produce an ' \
                            u'observation result. view action type ' \
                            u'details here <a href="http://vocabulary.odm2.org/actiontype/" ' \
                            u'target="_blank">http://vocabulary.odm2.org/actiontype/</a>'
    action_type.allow_tags = True

    class Meta:
        model = Actions
        fields = '__all__'


class ActionsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Actions._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyFeatureActionsInline]

    # For admin users
    form = ActionsAdminForm
    inlines_list = [FeatureActionsInline, actionByInLine]

    def method_link(self, obj):
        return format_html('<a href="{0}methods/{1}/">{2}</a>'.format(settings.CUSTOM_TEMPLATE_PATH,
                                                            obj.method.methodid, obj.method.methodname))


    list_display = ('action_type', 'method_link', 'begindatetime', 'enddatetime')
    list_display_links = ('action_type',)
    search_fields = ['action_type__name', 'method__methodname']  # ,

    method_link.short_description = 'Method'
    method_link.allow_tags = True
    save_as = True

class ActionByAdminForm(ModelForm):
    class Meta:
        model = Actionby
        fields = '__all__'


class ActionByAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Actionby._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ActionByAdminForm
    inlines_list = list()

    list_display = ('actionid', 'affiliationid')
    # list_display_links = ('affiliationid', 'actionid')
    # list_select_related = True


class MethodsAdminForm(ModelForm):
    methoddescription = CharField(max_length=5000, label="Method description",
                                  widget=forms.Textarea, required=False)
    methodtypecv = make_ajax_field(Methods, 'methodtypecv', 'cv_method_type')
    methodtypecv.help_text = u'A vocabulary for describing types of Methods associated ' \
                             u'with creating observations. ' \
                             u'MethodTypes correspond with ActionTypes in ODM2. ' \
                             u'An Action must be performed using an ' \
                             u'appropriate MethodType - e.g., a specimen collection ' \
                             u'Action should be associated with a ' \
                             u'specimen collection method. details for individual values ' \
                             u'here: <a href="http://vocabulary.odm2.org/methodtype/" ' \
                             u'target="_blank">http://vocabulary.odm2.org/methodtype/</a>'
    methodtypecv.allow_tags = True

    # methodtypecv= TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))
    # organizationid= OrganizationsModelChoiceField( Organizations.objects.all().
    # order_by('organizationname'))
    class Meta:
        model = Methods
        fields = '__all__'


class MethodsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Methods._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyActionsInline]

    # For admin users
    form = MethodsAdminForm
    inlines_list = [ActionsInline]

    list_display = ('methodname', 'method_type_linked', 'method_link')
    list_display_links = ['methodname']

    # DOI matching reg expresion came from http://stackoverflow.com/questions/27910/
    # finding-a-doi-in-a-document-or-page
    def method_link(self, obj):
        return link_list_display_DOI(obj.methodlink)

    method_link.short_description = 'link to method documentation'
    method_link.allow_tags = True

    def method_type_linked(self, obj):
        if obj.methodtypecv:
            return format_html('<a href="http://vocabulary.odm2.org/methodtype/{0}" target=' \
                   '"_blank">{1}</a>'.format(obj.methodtypecv.term, obj.methodtypecv.name))

    method_type_linked.short_description = 'Method Type'
    method_type_linked.allow_tags = True


def duplicate_Dataloggerfiles_event(ModelAdmin, request, queryset):
    for dataloggerfile in queryset:
        fileid = dataloggerfile.dataloggerfileid
        filecolumns = Dataloggerfilecolumns.objects.filter(dataloggerfileid=fileid)
        dataloggerfile.dataloggerfileid = None
        dataloggerfile.save()
        # save will assign new dataloggerfileid
        for columns in filecolumns:
            columns.dataloggerfilecolumnid = None
            columns.dataloggerfileid = dataloggerfile
            columns.save()


duplicate_Dataloggerfiles_event.short_description = "Duplicate selected datalogger " \
                                                    "file along with columns"


class DataLoggerFileColumnsInlineAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='A data result',
                                       label='Data result',show_help_text =None)

    class Meta:
        model = Dataloggerfilecolumns
        fields = '__all__'


class DataLoggerFileColumnsInline(admin.StackedInline):
    model = Dataloggerfilecolumns
    form = DataLoggerFileColumnsInlineAdminForm
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('dataloggerfilecolumnid',
                       'resultid',
                       'dataloggerfileid',
                       'instrumentoutputvariableid',
                       'columnlabel',
                       'columndescription',
                       'measurementequation',
                       'scaninterval',
                       'scanintervalunitsid',
                       'recordinginterval',
                       'recordingintervalunitsid',
                       'aggregationstatisticcv',
                       )

        }),
    )
    extra = 0


class ReadOnlyDataLoggerFileColumnsInline(DataLoggerFileColumnsInline):
    readonly_fields = DataLoggerFileColumnsInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class DataloggerfilesAdminForm(ModelForm):
    class Meta:
        model = Dataloggerfiles
        fields = '__all__'


class DataloggerfilesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Dataloggerfiles._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyDataLoggerFileColumnsInline]

    # For admin users
    form = DataloggerfilesAdminForm
    inlines_list = [DataLoggerFileColumnsInline]

    actions = [duplicate_Dataloggerfiles_event]
    list_display = ['dataloggerfilename', 'dataloggerfiledescription',]
    search_fields = ['dataloggerfilename', 'dataloggerfiledescription', 'programid__programname',
                     'programid__programname', ]
    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)

        if self.__user_is_readonly(request):
            actions = list()

        return actions

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


def duplicate_Dataloggerfilecolumns_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.dataloggerfilecolumnid = None
        object.save()


duplicate_Dataloggerfilecolumns_event.short_description = "Duplicate selected " \
                                                          "datalogger file columns"


class DataloggerfilecolumnsAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result related to this column',
                                       label='Data result',show_help_text =None)

    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Results.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Dataloggerfilecolumns
        fields = '__all__'


class DataloggerfilecolumnsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Dataloggerfilecolumns._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DataloggerfilecolumnsAdminForm
    inlines_list = list()

    list_display = ['columnlabel', 'resultid', 'dataloggerfileid']
    actions = [duplicate_Dataloggerfilecolumns_event]
    search_fields = ['columnlabel', 'dataloggerfileid__dataloggerfilename',
                     'resultid__variableid__variable_name__name', ]
    save_as = True

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)

        if self.__user_is_readonly(request):
            actions = list()

        return actions

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups



class ProcessDataloggerfileAdminForm(ModelForm):
    class Meta:
        model = ProcessDataloggerfile
        fields = '__all__'


class ProcessDataloggerfileAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in ProcessDataloggerfile._meta.get_fields() if
                     not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProcessDataloggerfileAdminForm
    inlines_list = list()


# class MeasurementResultFilter(SimpleListFilter):
#     title = ugettext_lazy('data values loaded')
#     parameter_name = 'resultValuesPresent'
#
#     def lookups(self, request, model_admin):
#         mrs = Measurementresults.objects.values('resultid',
#                                                 'resultid__featureactionid__samplingfeatureid
# __samplingfeaturename',
#                                                 'resultid__variableid__variable_name__name')
#         # need to make a custom list with feature name and variable name.
#         resultidlist = [(p['resultid'], '{0} {1}'.format(
#             p['resultid__featureactionid__samplingfeatureid__samplingfeaturename'],
#             p['resultid__variableid__variable_name__name']),) for p in mrs]
#
#         return resultidlist
#
#     def queryset(self, request, queryset):
#         if not self.value():
#             return queryset
#         valuesPresent = Measurementresults.objects.filter(resultid=self.value())
#         # values = Measurementresultvalues.objects.filter(resultid=self.value()).distinct()
#         resultsWCount = Results.objects.raw(
#             "SELECT results.*, count(measurementresultvalues.resultid) as valuecount2 " +
#             "from odm2.results " +
#             "left join odm2.measurementresultvalues " +
#             "on (results.resultid = measurementresultvalues.resultid) " +
#             "group by " +
#             "results.resultid")
#         ids = []
#         for mresults in valuesPresent:
#             resultid = str(mresults.resultid)  # mresults.value_list('resultid')
#             resultid = resultid.split(':')[1]
#             resultid = resultid.strip()
#             resultid = int(resultid)
#             # raise ValidationError(resultid)
#             for resultwCount in resultsWCount:
#                 valuecount2 = resultwCount.valuecount2
#                 # raise ValidationError(resultwCount.resultid)
#                 if resultid == resultwCount.resultid and valuecount2 > 0:
#                     ids += [resultwCount.resultid]
#                     # raise ValidationError(ids)
#
#         # valuesPresent = [p.resultid for p in resultsWCount]
#         return queryset.filter(resultid__in=ids)


# for soil sampling profiles with depths
class ProfileresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result to extend as a soil profile result',
                                       label='Data result')

    # this processes the user input into the form.
    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Results.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Profileresults
        fields = '__all__'


class ProfileresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Profileresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProfileresultsAdminForm
    inlines_list = list()

    list_display = ['intendedzspacing', 'intendedzspacingunitsid', 'aggregationstatisticcv',
                    'resultid', ]
    list_display_links = ['intendedzspacing', 'intendedzspacingunitsid', 'aggregationstatisticcv',
                          'resultid', ]
    search_fields = ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__variableid__variable_name__name', 'resultid__unitsid__unitsname',
                     'resultid__variableid__variable_type__name']
    save_as = True


class ProfileresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Profileresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'zlocation', 'zlocationunitsid', 'zaggregationinterval',
                  'resultid__resultid__variableid__variable_name',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                  'valuedatetime',
                  'resultid__resultid__unitsid__unitsname', 'datavalue')
        export_order = (
            'valueid', 'datavalue', 'zlocation', 'zlocationunitsid', 'zaggregationinterval',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__unitsid__unitsname',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
            'valuedatetime')


class ProfileresultsvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Profileresults,'resultid','profileresult_lookup')
    resultid = AutoCompleteSelectField('profileresult_lookup', required=True, help_text='',
                                       label='Profile Result')

    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Profileresults.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Profileresultvalues
        fields = '__all__'


class ProfileresultsvaluesAdmin(ImportExportActionModelAdmin, ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Profileresultvalues._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProfileresultsvaluesAdminForm
    inlines_list = list()

    resource_class = ProfileresultvaluesResource
    list_display = ['datavalue', 'zlocation', 'zlocationunitsid', 'zaggregationinterval',
                    'valuedatetime',
                    'resultid', ]  # 'resultid','featureactionid_link',
    # 'resultid__featureactionid__name', 'resultid__variable__name'
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'zaggregationinterval',
                     'resultid__resultid__variableid__variable_name__name',
                     'resultid__resultid__unitsid__unitsname',
                     'resultid__resultid__variableid__variable_type__name', ]

    def changelist_view(self, request, extra_context=None):
        if self.__user_is_readonly(request):
            self.change_list_template = None
        else:
            self.change_list_template = 'admin/import_export/change_list_import.html'
        return super(ProfileresultsvaluesAdmin, self).changelist_view(
            request, extra_context=extra_context)

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


# Relatedfeatures AdminForm
class RelatedfeaturesAdminForm(ModelForm):
    samplingfeatureid = AutoCompleteSelectField('sampling_feature_lookup', required=True, help_text='',
                                              label='first sampling feature',show_help_text =None)
    relatedfeatureid = AutoCompleteSelectField('sampling_feature_lookup', required=True, help_text='',
                                              label='second sampling feature',show_help_text =None)
    class Meta:
        model = Relatedfeatures
        fields = '__all__'


class RelatedfeaturesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Relatedfeatures._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = RelatedfeaturesAdminForm
    inlines_list = list()


class ProcessingLevelsAdminForm(ModelForm):
    class Meta:
        model = Processinglevels
        fields = '__all__'


class ProcessingLevelsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Processinglevels._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProcessingLevelsAdminForm
    inlines_list = list()


class MeasurementresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup', required=True, help_text='',
                                       label='Data result')

    # this processes the user input into the form.
    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Results.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Measurementresults
        fields = '__all__'


class MeasurementresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Measurementresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = MeasurementresultsAdminForm
    inlines_list = list()

    list_display = ('resultid', 'censorcodecv', 'data_link')
    list_display_links = ('resultid', 'data_link')
    # def resultvalues_valuedatetime(self,obj):
    #    mrv = Measurementresultvalues.objects.filter(resultid= obj.resultid)
    #    return mrv.values('valuedatetime')
    # gl = OrderDetail.objects.filter(order__order_date__range=('2015-02-02','2015-03-10'))
    # list_filter = [MeasurementResultFilter, ]  # ('resultid__valuedatetime', DateRangeFilter),
    save_as = True
    search_fields = ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__variableid__variable_name__name',
                     'resultid__variableid__variable_type__name']

    def data_link(self, obj):
        return format_html('<a href="%sfeatureactions/%s/">%s</a>' % (
            settings.CUSTOM_TEMPLATE_PATH, obj.resultid.featureactionid.featureactionid,
            obj.resultid.featureactionid))

    data_link.short_description = 'sampling feature /site action'
    data_link.allow_tags = True

    # resultValues = Measurementresultvalues.objects.filter(resultid=)


class MeasurementresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Measurementresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'resultid__resultid__variableid__variable_name',
                  'resultid__resultid__unitsid__unitsname',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                  'valuedatetime',
                  'datavalue', 'resultid__timeaggregationinterval',
                  'resultid__timeaggregationintervalunitsid')
        export_order = (
            'valueid', 'valuedatetime', 'datavalue', 'resultid__timeaggregationinterval',
            'resultid__timeaggregationintervalunitsid',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__unitsid__unitsname',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',)


class TimeseriesresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup', required=True, help_text='',
                                       label='Data result')

    # this processes the user input into the form.
    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Results.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Timeseriesresults
        fields = '__all__'


class TimeseriesresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Timeseriesresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = TimeseriesresultsAdminForm
    inlines_list = list()

    list_display = ('resultid', 'intendedtimespacing', 'intendedtimespacingunitsid', 'data_link')
    list_display_links = ('resultid', 'data_link')
    # def resultvalues_valuedatetime(self,obj):
    #    mrv = Measurementresultvalues.objects.filter(resultid= obj.resultid)
    #    return mrv.values('valuedatetime')
    # gl = OrderDetail.objects.filter(order__order_date__range=('2015-02-02','2015-03-10'))
    # list_filter = [MeasurementResultFilter, ]  # ('resultid__valuedatetime', DateRangeFilter),
    save_as = True
    search_fields = ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__variableid__variable_name__name',
                     'resultid__variableid__variable_type__name']

    def data_link(self, obj):
        return format_html('<a href="%sfeatureactions/%s/">%s</a>' % (
            settings.CUSTOM_TEMPLATE_PATH, obj.resultid.featureactionid.featureactionid,
            obj.resultid.featureactionid))

    data_link.short_description = 'sampling feature / site action'
    data_link.allow_tags = True


class TimeseriesresultvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Measurementresults,'resultid','measurementresult_lookup') #
    resultid = AutoCompleteSelectField('timeseriesresult_lookup', required=True, help_text='',
                                       label='Result')

    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Timeseriesresults.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Timeseriesresultvalues
        fields = '__all__'


class TimeseriesresultvaluesAdmin(ImportExportActionModelAdmin, ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Timeseriesresultvalues._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = TimeseriesresultvaluesAdminForm
    inlines_list = list()

    list_filter = (
        ('valuedatetime', DateRangeFilter),
        # MeasurementResultFilter,

    )
    list_display = ['datavalue', 'valuedatetime',
                    'resultid']
    # 'resultid','featureactionid_link','resultid__featureactionid__name',
    # 'resultid__variable__name'
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__resultid__variableid__variable_name__name',
                     'resultid__resultid__variableid__variable_type__name']

    def feature_action_link(self, obj):
        return format_html('<a href="/admin/ODM2CZOData/featureactions/%s/">%s</a>' % (
            obj.resultid.resultid.featureactionid.featureactionid,
            obj.resultid.resultid.featureactionid))

    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__featureactionid__samplingfeatureid'

    # get_feature_action = 'resultid__resultid__feature_action'
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #
    #     if request.REQUEST.get('export_data'):
    #         csvexport=True
    #         myMeasurementResults = Measurementresultvalues.objects.all().filter()
    #         myfile = StringIO.StringIO()
    #         for mresults in myMeasurementResults:
    #             myfile.write(mresults.csvoutput())
    #         response = HttpResponse(myfile.getvalue(),content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+
    # '-'+ name_of_variable +'.csv"'
    #         extra_context = response
    #     return super(MeasurementresultvaluesAdmin, self).change_view(request, object_id,
    #         form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        if self.__user_is_readonly(request):
            self.change_list_template = None
        else:
            self.change_list_template = 'admin/import_export/change_list_import.html'
        return super(TimeseriesresultvaluesAdmin, self).changelist_view(
            request, extra_context=extra_context)

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


class MeasurementresultvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Measurementresults,'resultid','measurementresult_lookup') #
    resultid = AutoCompleteSelectField('measurementresult_lookup', required=True, help_text='',
                                       label='Result')

    def clean_resultid(self):
        resultiduni = self.data['resultid']
        resultid = None
        for riduni in resultiduni.split("-"):
            if riduni.isdigit():
                resultid = riduni
                continue
        result = Measurementresults.objects.filter(resultid=resultid).get()
        return result

    class Meta:
        model = Measurementresultvalues
        fields = '__all__'


class MeasurementresultvaluesAdmin(ImportExportActionModelAdmin, ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Measurementresultvalues._meta.get_fields() if
                     not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = MeasurementresultvaluesAdminForm
    inlines_list = list()

    # MeasurementresultvaluesResource is for exporting values to different file types.
    # resource_class uses django-import-export
    resource_class = MeasurementresultvaluesResource

    # date time filter and list of results you can filter on
    list_filter = (
        ('valuedatetime', DateRangeFilter),
        # MeasurementResultFilter,

    )
    list_display = ['datavalue', 'valuedatetime',
                    'resultid']  # 'resultid','featureactionid_link',
    # 'resultid__featureactionid__name', 'resultid__variable__name'
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__resultid__variableid__variable_name__name',
                     'resultid__resultid__variableid__variable_type__name']

    def feature_action_link(self, obj):
        return format_html('<a href="/admin/ODM2CZOData/featureactions/%s/">%s</a>' % (
            obj.resultid.resultid.featureactionid.featureactionid,
            obj.resultid.resultid.featureactionid))

    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__featureactionid__samplingfeatureid'

    # get_feature_action = 'resultid__resultid__feature_action'
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #
    #     if request.REQUEST.get('export_data'):
    #         csvexport=True
    #         myMeasurementResults = Measurementresultvalues.objects.all().filter()
    #         myfile = StringIO.StringIO()
    #         for mresults in myMeasurementResults:
    #             myfile.write(mresults.csvoutput())
    #         response = HttpResponse(myfile.getvalue(),content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+
    # '-'+ name_of_variable +'.csv"'
    #         extra_context = response
    #     return super(MeasurementresultvaluesAdmin, self).change_view(request, object_id,
    #         form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        if self.__user_is_readonly(request):
            self.change_list_template = None
        else:
            self.change_list_template = 'admin/import_export/change_list_import.html'
        return super(MeasurementresultvaluesAdmin, self).changelist_view(
            request, extra_context=extra_context)

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


class MeasurementresultvalueFileAdminForm(ModelForm):
    class Meta:
        model = MeasurementresultvalueFile
        fields = '__all__'


class MeasurementresultvalueFileAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in MeasurementresultvalueFile._meta.get_fields() if
                     not p.one_to_many]  # noqa
    user_readonly_inlines = list()

    # For admin users
    form = ProcessingLevelsAdminForm
    inlines_list = list()


class UnitsAdminForm(ModelForm):
    unit_type = make_ajax_field(Units, 'unit_type', 'cv_units_type')
    unit_type.help_text = u'A vocabulary for describing the type of the Unit or ' \
                          u'the more general quantity that the Unit ' \
                          u'represents. View unit type details here ' \
                          u'<a href="http://vocabulary.odm2.org/unitstype/" ' \
                          u'target="_blank">http://vocabulary.odm2.org/unitstype/</a>'
    unit_type.allow_tags = True

    class Meta:
        model = Units
        fields = '__all__'


class UnitsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Units._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = UnitsAdminForm
    inlines_list = list()

    search_fields = ['unit_type__name', 'unitsabbreviation', 'unitsname']
    list_display = ['unitsabbreviation', 'unitsname', 'unit_type']


class DataloggerprogramfilesAdminForm(ModelForm):
    @staticmethod
    def upload_file(request):
        if request.method == 'POST':
            form = DataloggerprogramfilesAdminForm(request.POST, request.FILES)
            if form.is_valid():
                # file is saved
                form.save()
                return HttpResponseRedirect('/success/url/')
        else:
            form = DataloggerprogramfilesAdminForm()
        return render(request, 'upload.html', {'form': form})

    class Meta:
        model = Dataloggerprogramfiles
        fields = '__all__'


class DataloggerprogramfilesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Dataloggerprogramfiles._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DataloggerprogramfilesAdminForm
    inlines_list = list()


class InstrumentoutputvariablesAdminForm(ModelForm):
    class Meta:
        model = Instrumentoutputvariables
        fields = '__all__'


class InstrumentoutputvariablesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Instrumentoutputvariables._meta.get_fields() if
                     not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = InstrumentoutputvariablesAdminForm
    inlines_list = list()
    search_fields = ['variableid__variable_name__name', 'variableid__variablecode', 'modelid__modelname',
                     'variableid__variable_type__name','instrumentmethodid__methodname',
                     'instrumentrawoutputunitsid__unitsname']
    list_display = ['modelid','variableid', 'instrumentmethodid', 'instrumentrawoutputunitsid']


class EquipmentmodelsAdminForm(ModelForm):
    modeldescription = CharField(max_length=5000, label="model description", widget=forms.Textarea)
    # change from a check box to a yes no choice with radio buttons.
    isinstrument = TypedChoiceField(label="Is this an instrument?",
                                    coerce=lambda x: x == 'True',
                                    choices=((False, 'Yes'), (True, 'No')),
                                    widget=forms.RadioSelect
                                    )

    class Meta:
        model = Equipmentmodels
        fields = '__all__'


class EquipmentmodelsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Equipmentmodels._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyInstrumentoutputvariablesInline]

    # For admin users
    form = EquipmentmodelsAdminForm
    inlines_list = [InstrumentoutputvariablesInline]


class PeopleAdminForm(ModelForm):
    class Meta:
        model = People
        fields = '__all__'


class ORCIDInLine(admin.StackedInline):
    model = Personexternalidentifiers
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('bridgeid',
                       'personid',
                       'externalidentifiersystemid',
                       'personexternalidentifier',
                       'personexternalidentifieruri',
                       )

        }),
    )
    max_num = 1
    extra = 0
    verbose_name = 'ORCID'


class AffiliationInLine(admin.StackedInline):
    model = Affiliations
    fieldsets = (
        ('Details', {
            'classes': ('collapse',),
            'fields': ('affiliationid',
                       'personid',
                       'organizationid',
                       'isprimaryorganizationcontact',
                       'affiliationstartdate',
                       'affiliationenddate',
                       'primaryphone',
                       'primaryemail',
                       'primaryaddress',
                       'personlink',)

        }),
    )
    extra = 0


class AffiliationsResource(resources.ModelResource):
    class Meta:
        model = Affiliations
        # import_id_fields = ('valueid',)
        fields = (
            'organizationid__organizationname', 'personid__personfirstname',
            'personid__personlastname',
            'isprimaryorganizationcontact',
            'primaryemail')
        export_order = ['organizationid__organizationname', 'personid__personfirstname',
                        'personid__personlastname',
                        'isprimaryorganizationcontact', 'primaryemail']


class ReadOnlyAffiliationInline(AffiliationInLine):
    readonly_fields = AffiliationInLine.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class ReadOnlyORCIDInline(ORCIDInLine):
    readonly_fields = ORCIDInLine.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class AffiliationsAdminForm(ModelForm):
    class Meta:
        model = Affiliations
        fields = '__all__'
        export_order = ['organizationname', 'personfirstname', 'personlastname',
                        'isprimaryorganizationcontact',
                        'primaryemail']
        # ordering = ['-primaryemail']


class AffiliationsAdmin(ExportMixin, ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Affiliations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = AffiliationsAdminForm
    inlines_list = list()
    resource_class = AffiliationsResource
    search_fields = ['organizationid__organizationname', 'organizationid__organizationtypecv__name',
                     'organizationid__organizationcode',
                     'personid__personfirstname', 'personid__personlastname']
    list_display = (
        'organizationname', 'personfirstname', 'personlastname', 'isprimaryorganizationcontact',
        'primaryemail')

    def organizationname(self, obj):
        return obj.organizationid.organizationname

    def personfirstname(self, obj):
        return obj.personid.personfirstname

    def personlastname(self, obj):
        return obj.personid.personlastname


class PeopleAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in People._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyAffiliationInline, ReadOnlyORCIDInline]

    # For admin users
    form = PeopleAdminForm
    inlines_list = [AffiliationInLine, ORCIDInLine]

    search_fields = ['personfirstname', 'personlastname',
                     'personexternalidentifiers__personexternalidentifier',
                     'affiliations__organizationid__organizationname']
    list_display = ('personlastname', 'personfirstname', 'orcid', 'affiliation')
    save_as = True

    def orcid(self, obj):
        external_id = Personexternalidentifiers.objects.get(personid=obj.personid)
        return format_html('<a href="http://orcid.org/{0}" target="_blank">{0}</a>'.format(
            external_id.personexternalidentifier))

    def affiliation(self, obj):
        org = Organizations.objects.filter(affiliations__personid_id=obj.personid)
        name_list = list()
        for org_name in org:
            if org_name.organizationlink:
                name_list.append(
                    format_html('<a href="{0}" target="_blank">{1}</a>'.format(org_name.organizationlink,
                                                                    org_name.organizationname)))
            else:
                name_list.append(
                    format_html('{0}'.format(org_name.organizationname)))

        return format_html('; '.join(name_list))

    orcid.allow_tags = True
    affiliation.allow_tags = True


class ExternalidentifiersystemForm(ModelForm):
    class Meta:
        model = Externalidentifiersystems
        fields = '__all__'


class ExternalidentifiersystemAdmin(ReadOnlyAdmin):
    # For admin users
    form = ExternalidentifiersystemForm
    inlines_list = list()

    # For readonly users
    user_readonly = [p.name for p in Externalidentifiersystems._meta.get_fields() if
                     not p.one_to_many]
    user_readonly_inlines = list()
    