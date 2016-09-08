import os
# from __future__ import unicode_literals
# from django.forms import HiddenInput  # imported but unused
from django.contrib.gis import forms, admin
# from django.forms import ModelChoiceField  # imported but unused
# from django.forms import FileField  # imported but unused
from django.forms import CharField
from django.forms import TypedChoiceField
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ExportMixin
from django.contrib.admin import SimpleListFilter  # , RelatedFieldListFilter  # imported but unused  # noqa
from django.contrib.gis.geos import GEOSGeometry  # , Point  # imported but unused  # noqa
# from django.db import models   # imported but unused
# from django.contrib.gis.db import models  # imported but unused

# from django.shortcuts import render_to_response  # imported but unused
from .models import Variables
# from .models import CvVariabletype  # imported but unused
# from .models import CvVariablename  # imported but unused
# from .models import CvSpeciation  # imported but unused
from .models import Taxonomicclassifiers
# from .models import CvTaxonomicclassifiertype  # imported but unused
# from .models import CvMethodtype  # imported but unused
from .models import Samplingfeatures
# from .models import CvSamplingfeaturetype  # imported but unused
# from .models import CvSamplingfeaturegeotype  # imported but unused
# from .models import CvElevationdatum  # imported but unused
from .models import Results
# from .models import CvResulttype  # imported but unused
# from .models import Variables  # imported but unused
from .models import Relatedactions
# from .models import CvActiontype  # imported but unused
from .models import Actions
from .models import Datasets
from .models import Featureactions
from .models import Organizations
# from .models import CvOrganizationtype   # imported but unused
# from .models import CvRelationshiptype  # imported but unused
# from .models import CvDatasettypecv  # imported but unused
from .models import Affiliations
from .models import People
from .models import Personexternalidentifiers
from .models import Actionby
from .models import Dataloggerprogramfiles
from .models import Dataloggerfiles
from .models import Dataloggerfilecolumns
from .models import Methods
from .models import Units
from .models import Datasetcitations
from .models import Citations
from .models import Citationextensionpropertyvalues
from .models import Extensionproperties
from .models import Authorlists
from .models import Methodcitations
from .models import MeasurementresultvalueFile
# from .models import CvUnitstype  # imported but unused
from .models import Instrumentoutputvariables
from .models import Equipmentmodels
from .models import Datasetsresults
from .models import Dataquality
from .models import Resultsdataquality
from .models import Samplingfeatureexternalidentifiers
from .models import Externalidentifiersystems
from .models import Citationexternalidentifiers
# from .models import Relatedfeatures  # imported but unused

# from templatesAndSettings.settings import STATIC_URL  # imported but unused
from templatesAndSettings.settings import CUSTOM_TEMPLATE_PATH
# from templatesAndSettings.settings import MEDIA_URL  # imported but unused
from .models import Profileresults
# import cStringIO as StringIO  # imported but unused
# from io import StringIO
from ajax_select import make_ajax_field
# from ajax_select.fields import autoselect_fields_check_can_add  # imported but unused  # noqa
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectField  # , AutoCompleteSelectMultipleField  # imported but unused  # noqa
#  from dal import autocomplete  # imported but unused
from .models import Measurementresults
from .models import Measurementresultvalues
from .models import Profileresultvalues
# from .views import dataloggercolumnView
from daterange_filter.filter import DateRangeFilter
from django.utils.translation import ugettext_lazy as _  # FIXME: This renaming is quite uncommon!  # noqa
# from django.core.exceptions import ValidationError  # imported but unused
import re

# from django.forms.widgets import Textarea  # imported but unused
# from .admin import MeasurementresultvaluesResource
# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

# A complicated use of search_fields described in ResultsAdminForm.

# The following define what fields should be overridden so that dropdown
# lists can be populated with useful information.


def link_list_display_DOI(link):
    match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+", link)
    if not match:
        match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])[[:graph:]])+", link)  # noqa
    if match:
        url = u'<a href="http://dx.doi.org/{0}" target="_blank">{0}</a>'.format
        return url(link)
    else:
        url = u'<a href="{0}" target="_blank">{0}</a>'.format
        return url(link)


class ResultsdataqualityAdminForm(ModelForm):
    class Meta:
        model = Resultsdataquality
        fields = '__all__'


class ResultsdataqualityAdmin(admin.ModelAdmin):
    list_display = ('resultid', 'dataqualityid')
    form = ResultsdataqualityAdminForm


class DataqualityAdminForm(ModelForm):
    class Meta:
        model = Dataquality
        fields = '__all__'


class DataqualityAdmin(admin.ModelAdmin):
    list_display = ('dataqualitytypecv', 'dataqualitycode',
                    'dataqualityvalue', 'dataqualityvalueunitsid')
    form = DataqualityAdminForm


class MethodcitationsAdminForm(ModelForm):
    class Meta:
        model = Methodcitations
        fields = '__all__'


class MethodcitationsAdmin(admin.ModelAdmin):
    list_display = ('method_id', 'method_link',
                    'relationshiptypecv', 'citation_link')
    form = MethodcitationsAdminForm

    def method_link(self, obj):
        url = u'<a href="{}methods/{}/">See Method</a>'.format
        return url(CUSTOM_TEMPLATE_PATH, obj.methodid.methodid)

    def citation_link(self, obj):
        url = u'<a href="{}citations/{}/">{}</a>'.format
        return url(CUSTOM_TEMPLATE_PATH, obj.citationid.citationid,
                   obj.citationid)

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


class AuthorlistsAdmin(admin.ModelAdmin):
    list_display = ('personid', 'citationid')
    form = AuthorlistsAdminForm


class DatasetcitationsAdminForm(ModelForm):
    class Meta:
        model = Datasetcitations
        fields = '__all__'


class DatasetcitationsAdmin(admin.ModelAdmin):
    list_display = ('datasetid', 'relationshiptypecv', 'citationid')
    form = DatasetcitationsAdminForm


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


class CitationsAdminForm(ModelForm):
    title = forms.CharField(max_length=255, widget=forms.Textarea,
                            label="Publication Title")

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


class CitationsAdmin(admin.ModelAdmin):
    list_display = ('primary_author', 'publicationyear', 'title',
                    'other_author', 'publisher', 'doi', 'citation_link')
    list_display_links = ['title']
    inlines = [authorlistInline, DOIInline]
    form = CitationsAdminForm
    search_fields = ['title', 'publisher', 'publicationyear',
                     'authorlists__personid__personfirstname',
                     'authorlists__personid__personlastname']

    def citation_link(self, obj):
        return link_list_display_DOI(obj.citationlink)

    def doi(self, obj):
        external_id = Citationexternalidentifiers.objects.get(
            citationid=obj.citationid
        )
        url = u'<a href="http://dx.doi.org/{0}" target="_blank">{0}</a>'.format
        return url(external_id.citationexternalidentifier)

    def primary_author(self, obj):
        self.author_list = Authorlists.objects.filter(
            citationid=obj.citationid
        )
        first_author = self.author_list.get(authororder=1)
        return "{0}, {1}".format(first_author.personid.personlastname,
                                 first_author.personid.personfirstname)

    def other_author(self, obj):
        list_et_al = list()
        for author in self.author_list:
            if author.authororder != 1:
                list_et_al.append(
                    "{0}, {1}".format(author.personid.personlastname,
                                      author.personid.personfirstname)
                )
        return "; ".join(list_et_al)

    doi.allow_tags = True
    citation_link.short_description = 'link to citation'
    other_author.short_description = 'Other Authors'
    citation_link.allow_tags = True
    # primary_author.admin_order_field = 'authorlists__personid__personlastname'  # noqa


class CitationextensionpropertyvaluesAdminForm(ModelForm):
    propertyvalue = forms.CharField(max_length=255, widget=forms.Textarea)

    class Meta:
        model = Citationextensionpropertyvalues
        fields = '__all__'


class CitationextensionpropertyvaluesAdmin(admin.ModelAdmin):
    list_display = ('citationid', 'propertyid', 'propertyvalue')
    form = CitationextensionpropertyvaluesAdminForm


class ExtensionpropertiesAdminForm(ModelForm):
    propertydescription = forms.CharField(max_length=255,
                                          widget=forms.Textarea,
                                          label="Property description")

    class Meta:
        model = Extensionproperties
        fields = '__all__'


class ExtensionpropertiesAdmin(admin.ModelAdmin):
    list_display = ('propertyname', 'propertydescription',
                    'propertydatatypecv', 'propertyunitsid')
    form = ExtensionpropertiesAdminForm


class VariablesAdminForm(ModelForm):
    # variabletypecv= TermModelChoiceField(CvVariabletype.objects.all().order_by('term'))  # noqa
    # variablenamecv= TermModelChoiceField(CvVariablename.objects.all().order_by('term'))  # noqa
    # speciationcv= TermModelChoiceField(CvSpeciation.objects.all().order_by('term'))  # noqa
    # make these fields ajax type ahead fields with links to odm2 controlled vocabulary  # noqa
    variable_type = make_ajax_field(Variables, 'variable_type', 'cv_variable_type')  # noqa
    variable_name = make_ajax_field(Variables, 'variable_name', 'cv_variable_name')  # noqa
    variabledefinition = forms.CharField(max_length=500, widget=forms.Textarea)
    # variable_type = make_ajax_field(Variables,'variable_type','cv_variable_type')  # noqa
    speciation = make_ajax_field(Variables, 'speciation', 'cv_speciation')

    variable_name.help_text = u'view variable names here <a href="http://vocabulary.odm2.org/variablename/" target="_blank">http://vocabulary.odm2.org/variablename/</a>'  # noqa
    variable_name.allow_tags = True
    variable_type.help_text = u'view variable types here <a href="http://vocabulary.odm2.org/variabletype/" target="_blank" >http://vocabulary.odm2.org/variabletype/</a>'  # noqa
    variable_type.allow_tags = True
    speciation.help_text = u'view variable types here <a href="http://vocabulary.odm2.org/speciation/" target="_blank" >http://vocabulary.odm2.org/speciation/</a>'  # noqa
    speciation.allow_tags = True

    class Meta:
        model = Variables
        fields = '__all__'


class VariablesAdmin(admin.ModelAdmin):
    form = VariablesAdminForm
    list_display = ('variablecode', 'variable_name_linked',
                    'variable_type_linked', 'speciation_linked')
    search_fields = ['variable_type__name', 'variable_name__name',
                     'variablecode', 'speciation__name']

    def variable_name_linked(self, obj):
        if obj.variable_name:
            url = u'<a href="http://vocabulary.odm2.org/variablename/{0}" target="_blank">{1}</a>'.format  # noqa
            return url(obj.variable_name.term, obj.variable_name.name)
    variable_name_linked.short_description = 'Variable Name'
    variable_name_linked.allow_tags = True

    def variable_type_linked(self, obj):
        if obj.variable_type:
            url = '<a href="http://vocabulary.odm2.org/variabletype/{0}" target="_blank">{1}</a>'.format  # noqa
            return url(obj.variable_type.term, obj.variable_type.name)

    variable_type_linked.short_description = 'Variable Type'
    variable_type_linked.allow_tags = True

    def speciation_linked(self, obj):
        if obj.speciation:
            url = u'<a href="http://vocabulary.odm2.org/speciation/{0}" target="_blank">{1}</a>'.format  # noqa
            return url(obj.speciation.term, obj.speciation.name)

    speciation_linked.short_description = 'Speciation'
    speciation_linked.allow_tags = True


class TaxonomicclassifiersAdminForm(ModelForm):
    taxonomic_classifier_type = make_ajax_field(
        Taxonomicclassifiers,
        'taxonomic_classifier_type',
        'cv_taxonomic_classifier_type')
    taxonomic_classifier_type.help_text = u'''
    A vocabulary for describing types of taxonomies from which descriptive terms used in an ODM2 database have been drawn.
    Taxonomic classifiers provide a way to classify Results and Specimens according to terms from a formal taxonomy.
    Check <a href="http://vocabulary.odm2.org/taxonomicclassifiertype/" target="_blank">
    http://vocabulary.odm2.org/taxonomicclassifiertype/</a> for more info.
    '''  # noqa
    taxonomic_classifier_type.allow_tags = True

    class Meta:
        model = Taxonomicclassifiers
        fields = '__all__'


class TaxonomicclassifiersAdmin(admin.ModelAdmin):
    form = TaxonomicclassifiersAdminForm
    search_fields = ['taxonomicclassifiername',
                     'taxonomicclassifiercommonname',
                     'taxonomicclassifierdescription',
                     'taxonomic_classifier_type__name']


class SamplingfeatureexternalidentifiersAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatureexternalidentifiers
        fields = '__all__'


class SamplingfeatureexternalidentifiersAdmin(admin.ModelAdmin):
    form = SamplingfeatureexternalidentifiersAdminForm
    search_fields = ['samplingfeatureexternalidentifier']
    list_display = ('samplingfeatureexternalidentifier',
                    'samplingfeatureexternalidentifieruri')
    save_as = True


class SamplingfeaturesAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatures
        fields = [
            'sampling_feature_type',
            'samplingfeaturecode',
            'samplingfeaturename',
            'samplingfeaturedescription',
            'sampling_feature_geo_type',
            'featuregeometrywkt',
            'featuregeometry',
            'elevation_m',
            'elevation_datum'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            feat = instance.featuregeometrywkt()
            initial = kwargs.get('initial', {})
            initial['featuregeometrywkt'] = '{}'.format(feat)
            kwargs['initial'] = initial
        super(SamplingfeaturesAdminForm, self).__init__(*args, **kwargs)

    help_text = """Feature geometry (to add a point format is POINT(lat, lon)
        where long and lat are in decimal degrees.
        If you don't want to add a location use default value of POINT(0 0)."""

    featuregeometrywkt = forms.CharField(
        help_text=help_text,
        label='Featuregeometrywkt',
        widget=forms.Textarea, required=False)
    featuregeometrywkt.initial = GEOSGeometry("POINT(0 0)")

    sampling_feature_type = make_ajax_field(
        Samplingfeatures,
        'sampling_feature_type', 'cv_sampling_feature_type'
    )
    sampling_feature_type.help_text = u'''A vocabulary for describing the type of SamplingFeature.
    Many different SamplingFeature types can be represented in ODM2.
    SamplingFeatures of type Site and Specimen will be the most common,
    but many different types of varying levels of complexity can be used.
    Details for individual values here: <a href="http://vocabulary.odm2.org/samplingfeaturetype/" target="_blank">http://vocabulary.odm2.org/samplingfeaturetype/</a>
    '''  # noqa
    sampling_feature_type.allow_tags = True

    samplingfeaturedescription = CharField(max_length=5000,
                                           label="feature description",
                                           widget=forms.Textarea,
                                           required=False)

    sampling_feature_geo_type = make_ajax_field(Samplingfeatures,
                                                'sampling_feature_geo_type',
                                                'cv_sampling_feature_geo_type')
    sampling_feature_geo_type.help_text = u'''
    A vocabulary for describing the geospatial feature type associated with a SamplingFeature.
    For example, Site SamplingFeatures are represented as points.
    In ODM2, each SamplingFeature may have only one geospatial type,
    but a geospatial types may range from simple points to a complex polygons or even three dimensional volumes.
    Details for individual values here: <a href="http://vocabulary.odm2.org/samplingfeaturegeotype/"'target="_blank">http://vocabulary.odm2.org/samplingfeaturegeotype/</a>
    '''  # noqa
    sampling_feature_geo_type.allow_tags = True
    sampling_feature_geo_type.required = False

    elevation_datum = make_ajax_field(Samplingfeatures,
                                      'elevation_datum',
                                      'cv_elevation_datum')
    elevation_datum.help_text = u'''
    A vocabulary for describing vertical datums.
    Vertical datums are used in ODM2 to specify the origin for elevations assocated with SamplingFeatures.
    Details for individual values here: <a href="http://vocabulary.odm2.org/elevationdatum/"target="_blank">http://vocabulary.odm2.org/elevationdatum/</a>
    '''  # noqa
    elevation_datum.allow_tags = True
    featuregeometry = forms.PointField(label='Featuregeometry',
                                       widget=forms.OpenLayersWidget(),
                                       required=False)

    featuregeometry.initial = GEOSGeometry("POINT(0 0)")


class IGSNInline(admin.StackedInline):
    model = Samplingfeatureexternalidentifiers
    extra = 0


class SamplingfeaturesAdmin(admin.OSMGeoAdmin):
    form = SamplingfeaturesAdminForm
    inlines = [IGSNInline]
    search_fields = [
        'sampling_feature_type__name',
        'sampling_feature_geo_type__name',
        'samplingfeaturename',
        'samplingfeaturecode',
        'samplingfeatureid',
        'samplingfeatureexternalidentifiers__samplingfeatureexternalidentifier'
    ]

    list_display = (
        'samplingfeaturecode',
        'samplingfeaturename',
        'sampling_feature_type_linked',
        'samplingfeaturedescription',
        'igsn',
        'dataset_code'
    )
    readonly_fields = ('samplingfeatureuuid',)

    # Your own processing.
    def save_model(self, request, obj, form, change):
        # For example:
        obj.featuregeometry = '%s' % form.cleaned_data['featuregeometrywkt']
        obj.save()

    save_as = True

    def igsn(self, obj):
        external_id = Samplingfeatureexternalidentifiers.objects.get(
            samplingfeatureid=obj.samplingfeatureid
        )
        url = u'<a href="https://app.geosamples.org/sample/igsn/{0}" target="_blank">{0}</a>'.format  # noqa
        return url(external_id.samplingfeatureexternalidentifier)

    igsn.allow_tags = True

    def dataset_code(self, obj):
        fid = Featureactions.objects.filter(
            samplingfeatureid=obj.samplingfeatureid
        )
        ds = Datasets.objects.filter(
            datasetsresults__resultid__featureactionid__in=fid
        ).distinct()
        ds_list = list()
        for d in ds:
            ds_list.append(d.datasetcode)
        return ", ".join(ds_list)

    def sampling_feature_type_linked(self, obj):
        if obj.sampling_feature_type:
            url = u'<a href="http://vocabulary.odm2.org/samplingfeaturetype/{0}" target="_blank">{1}</a>'.format  # noqa
            return url(obj.sampling_feature_type.term,
                       obj.sampling_feature_type.name)

    sampling_feature_type_linked.short_description = 'Sampling Feature Type'
    sampling_feature_type_linked.allow_tags = True


def duplicate_results_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.resultid = None
        object.save()


duplicate_results_event.short_description = "Duplicate selected result"


# class FeatureactionsField(ajax_select.make_ajax_field):
#     def to_python(self, value):
#         featureactioniduni= self.data['featureactionid']
#         for faiduni in featureactioniduni.split("-"):
#              if faiduni.isdigit():
#                  featureactionid = faiduni
#                  continue
#        featureaction = Featureactions.objects.filter(
#            featureactionid=featureactionid
#        )
#         self.data['featureactionid'] = featureaction
#         return featureaction

class ResultsAdminForm(ModelForm):
    # featureactionid = make_ajax_field(Featureactions, 'featureactionid', 'featureaction_lookup', max_length=500)  # noqa
    featureactionid = AutoCompleteSelectField('featureaction_lookup',
                                              required=True,
                                              help_text='',
                                              label='Sampling feature action')

    def clean_featureactionid(self):
        featureactioniduni = self.data['featureactionid']
        featureactionid = None
        for faiduni in featureactioniduni.split("-"):
            if faiduni.isdigit():
                featureactionid = faiduni
                continue
        featureaction = Featureactions.objects.filter(
            featureactionid=featureactionid
        ).get()
        return featureaction

    class Meta:
        model = Results
        fields = '__all__'
        # make_ajax_field doesn't work with the add + green plus on the field

        # widgets = {
        #     'featureactionid': autocomplete.ModelSelect2(url='featueactions-autocomplete')  # noqa
        # }


# The user can click, a popup window lets them create a new object,
# they click save, the popup closes and the AjaxSelect field is set.
# Your Admin must inherit from AjaxSelectAdmin
# http://django-ajax-selects.readthedocs.org/en/latest/Admin-add-popup.html
class ResultsAdmin(AjaxSelectAdmin):  # admin.ModelAdmin
    form = ResultsAdminForm
    list_display = [
        'resultid',
        'featureactionid',
        'variableid',
        'processing_level'
    ]
    search_fields = [
        'variableid__variable_name__name',
        'variableid__variablecode',
        'variableid__variabledefinition',
        'featureactionid__samplingfeatureid__samplingfeaturename',
        'result_type__name', 'processing_level__definition'
    ]
    actions = [duplicate_results_event]
    save_as = True

    # def get_form(self, request, obj=None, **kwargs):
    # form = super(ResultsAdmin, self).get_form(request, obj, **kwargs)
    # autoselect_fields_check_can_add(form, self.model, request.user)
    # raise ValidationError(form)
    # return form
    # def save_model(self, request, obj, form, change):
    #     featureactionidstr = request.featureactionid
    #     featureactionid = None
    #     for featureactionidstr in str.split():
    #         if featureactionidstr.isdigit():
    #             featureactionid = featureactionidstr
    #             continue
    #     raise ValidationError(featureactionid)
    #     obj.featureactionid = featureactionid
    #     obj.save()


class RelatedactionsAdminForm(ModelForm):
    # actionid = ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))  # noqa
    # relationshiptypecv = TermModelChoiceField(CvRelationshiptype.objects.all().order_by('term'))  # noqa
    # relatedactionid = ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))  # noqa
    class Meta:
        model = Relatedactions
        fields = '__all__'


class RelatedactionsAdmin(admin.ModelAdmin):
    form = RelatedactionsAdminForm


class OrganizationsAdminForm(ModelForm):
    # organizationtypecv = TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))  # noqa
    # parentorganizationid = OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))  # noqa
    class Meta:
        model = Organizations
        fields = '__all__'


class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('organizationname',
                    'organizationdescription',
                    'organization_link')
    form = OrganizationsAdminForm

    def organization_link(self, org):
        url = u'<a href={0} target="_blank">{0}</a>'.format
        return url(org.organizationlink)

    organization_link.allow_tags = True


class FeatureactionsAdminForm(ModelForm):
    class Meta:
        model = Featureactions
        fields = '__all__'


class FeatureactionsAdmin(admin.ModelAdmin):
    list_display = ['samplingfeatureid', 'action', ]
    form = FeatureactionsAdminForm
    save_as = True
    search_fields = ['action__method__methodname',
                     'samplingfeatureid__samplingfeaturename']


class DatasetsAdminForm(ModelForm):
    datasetabstract = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Datasets
        fields = '__all__'


class DatasetsAdmin(admin.ModelAdmin):
    form = DatasetsAdminForm
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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DatasetResultsList'] = self.get_datasetsresults(object_id)  # noqa
        extra_context['ResultsList'] = self.get_results(object_id)
        extra_context['prefixpath'] = CUSTOM_TEMPLATE_PATH
        return super(DatasetsAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context
        )


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
    action_type.help_text = u'''
    A vocabulary for describing the type of actions performed in making observations.
    Depending on the action type, the action may or may not produce an observation result.
    View action type details here <a href="http://vocabulary.odm2.org/actiontype/" target="_blank">http://vocabulary.odm2.org/actiontype/</a>
    '''  # noqa
    action_type.allow_tags = True

    class Meta:
        model = Actions
        fields = '__all__'


class ActionsAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'method', 'begindatetime', 'enddatetime')
    list_display_links = ('action_type',)
    search_fields = ['action_type__name', 'method__methodname']  # ,
    form = ActionsAdminForm


class ActionByAdminForm(ModelForm):
    class Meta:
        model = Actionby
        fields = '__all__'


class ActionByAdmin(admin.ModelAdmin):
    list_display = ('actionid', 'affiliationid')
    # list_display_links = ('affiliationid', 'actionid')  #
    form = ActionByAdminForm
    # list_select_related = True


class MethodsAdminForm(ModelForm):
    methoddescription = CharField(max_length=5000, label="Method description",
                                  widget=forms.Textarea, required=False)
    methodtypecv = make_ajax_field(Methods, 'methodtypecv', 'cv_method_type')
    methodtypecv.help_text = u'''
    A vocabulary for describing types of Methods associated with creating observations.
    MethodTypes correspond with ActionTypes in ODM2.
    An Action must be performed using an appropriate MethodType - e.g., a specimen collection Action should be associated with a
    specimen collection method.
    Details for individual values here: <a href="http://vocabulary.odm2.org/methodtype/" target="_blank">http://vocabulary.odm2.org/methodtype/</a>
    '''  # noqa
    methodtypecv.allow_tags = True

    # methodtypecv = TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))  # noqa
    # organizationid = OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))  # noqa
    class Meta:
        model = Methods
        fields = '__all__'


class MethodsAdmin(admin.ModelAdmin):
    list_display = ('methodname', 'method_type_linked', 'method_link')
    list_display_links = ['methodname']
    form = MethodsAdminForm

    # DOI matching reg expression came from http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page  # noqa
    def method_link(self, obj):
        return link_list_display_DOI(obj.methodlink)

    method_link.short_description = 'link to method documentation'
    method_link.allow_tags = True

    def method_type_linked(self, obj):
        if obj.methodtypecv:
            url = u'<a href="http://vocabulary.odm2.org/methodtype/{0}" target="_blank">{1}</a>'.format  # noqa
            return url(obj.methodtypecv.term, obj.methodtypecv.name)

    method_type_linked.short_description = 'Method Type'
    method_type_linked.allow_tags = True


def duplicate_Dataloggerfiles_event(ModelAdmin, request, queryset):
    for dataloggerfile in queryset:
        fileid = dataloggerfile.dataloggerfileid
        filecolumns = Dataloggerfilecolumns.objects.filter(
            dataloggerfileid=fileid
        )
        dataloggerfile.dataloggerfileid = None
        dataloggerfile.save()
        # Save will assign new dataloggerfileid.
        fileid = dataloggerfile.dataloggerfileid
        for columns in filecolumns:
            columns.dataloggerfilecolumnid = None
            columns.dataloggerfileid = dataloggerfile
            columns.save()


duplicate_Dataloggerfiles_event.short_description = "Duplicate selected datalogger file along with columns"  # noqa


class DataloggerfilesAdminForm(ModelForm):
    class Meta:
        model = Dataloggerfiles
        fields = '__all__'


class DataloggerfilesAdmin(admin.ModelAdmin):
    form = DataloggerfilesAdminForm
    change_form_template = os.path.join(os.curdir, 'admin', 'ODM2CZOData',
                                        'dataloggerfiles', 'change_form.html')
    actions = [duplicate_Dataloggerfiles_event]

    # Get the data columns related to this data loggerfile
    # and return them to the change view.
    def get_dataloggerfilecolumns(self, object_id):
        DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.filter(
            dataloggerfileid=object_id
        )
        return DataloggerfilecolumnsList

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DataloggerfilecolumnsList'] = self.get_dataloggerfilecolumns(object_id)  # noqa
        extra_context['prefixpath'] = CUSTOM_TEMPLATE_PATH
        # extra_context['dataloggerfileschange_view'] = DataloggerfilecolumnsAdmin.get_changelist(DataloggerfilecolumnsAdmin)  # noqa
        return super(DataloggerfilesAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)  # noqa


def duplicate_Dataloggerfilecolumns_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.dataloggerfilecolumnid = None
        object.save()


duplicate_Dataloggerfilecolumns_event.short_description = "Duplicate selected datalogger file columns"  # noqa


class DataloggerfilecolumnsAdminForm(ModelForm):
    resultid = AutoCompleteSelectField(
        'result_lookup',
        required=True,
        help_text='result to extend as a soil profile result',
        label='Result'
    )

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


class DataloggerfilecolumnsAdmin(admin.ModelAdmin):
    form = DataloggerfilecolumnsAdminForm
    list_display = ['columnlabel', 'resultid', 'dataloggerfileid']
    actions = [duplicate_Dataloggerfilecolumns_event]
    search_fields = ['columnlabel', 'dataloggerfileid__dataloggerfilename',
                     'resultid__variableid__variable_name__name', ]
    save_as = True


class MeasurementResultFilter(SimpleListFilter):
    title = _('data values loaded')
    parameter_name = 'resultValuesPresent'

    def lookups(self, request, model_admin):
        mrs = Measurementresults.objects.values(
            'resultid',
            'resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
            'resultid__variableid__variable_name__name'
        )
        # Need to make a custom list with feature name and variable name.
        resultidlist = [(p['resultid'], '{0} {1}'.format(
            p['resultid__featureactionid__samplingfeatureid__samplingfeaturename'],  # noqa
            p['resultid__variableid__variable_name__name']),) for p in mrs]

        return resultidlist

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        valuesPresent = Measurementresults.objects.filter(resultid=self.value())  # noqa
        # values = Measurementresultvalues.objects.filter(resultid=self.value()).distinct()  # noqa
        resultsWCount = Results.objects.raw(
            "SELECT results.*, count(measurementresultvalues.resultid) as valuecount2 " +  # noqa
            "from odm2.results " +
            "left join odm2.measurementresultvalues " +
            "on (results.resultid = measurementresultvalues.resultid) " +
            "group by " +
            "results.resultid")
        ids = []
        for mresults in valuesPresent:
            resultid = str(mresults.resultid)  # mresults.value_list('resultid')  # noqa
            resultid = resultid.split(':')[1]
            resultid = resultid.strip()
            resultid = int(resultid)
            # raise ValidationError(resultid)
            for resultwCount in resultsWCount:
                valuecount2 = resultwCount.valuecount2
                # raise ValidationError(resultwCount.resultid)
                if resultid == resultwCount.resultid and valuecount2 > 0:
                    ids += [resultwCount.resultid]
                    # raise ValidationError(ids)

        # valuesPresent = [p.resultid for p in resultsWCount]
        return queryset.filter(resultid__in=ids)


# For soil sampling profiles with depths.
class ProfileresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField(
        'result_lookup',
        required=True,
        help_text='result to extend as a soil profile result',
        label='Result'
    )

    # This processes the user input into the form.
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


class ProfileresultsAdmin(AjaxSelectAdmin):
    form = ProfileresultsAdminForm
    list_display = [
        'intendedzspacing',
        'intendedzspacingunitsid',
        'aggregationstatisticcv',
        'resultid',
    ]
    list_display_links = [
        'intendedzspacing',
        'intendedzspacingunitsid',
        'aggregationstatisticcv',
        'resultid',
    ]
    search_fields = [
        'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
        'resultid__variableid__variable_name__name',
        'resultid__unitsid__unitsname',
        'resultid__variableid__variable_type__name'
    ]
    save_as = True


class ProfileresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Profileresultvalues
        import_id_fields = ('valueid',)
        fields = (
            'valueid',
            'zlocation',
            'zlocationunitsid',
            'zaggregationinterval',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
            'valuedatetime',
            'resultid__resultid__unitsid__unitsname',
            'datavalue'
        )
        export_order = (
            'valueid',
            'datavalue',
            'zlocation',
            'zlocationunitsid',
            'zaggregationinterval',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__unitsid__unitsname',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
            'valuedatetime'
        )


class ProfileresultsvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Profileresults,'resultid','profileresult_lookup')  # noqa
    resultid = AutoCompleteSelectField('profileresult_lookup',
                                       required=True,
                                       help_text='',
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


class ProfileresultsvaluesAdmin(ImportExportActionModelAdmin, AjaxSelectAdmin):
    form = ProfileresultsvaluesAdminForm
    resource_class = ProfileresultvaluesResource
    list_display = [
        'datavalue',
        'zlocation',
        'zlocationunitsid',
        'zaggregationinterval',
        'valuedatetime',
        'resultid',
    ]  # 'resultid','featureactionid_link','resultid__featureactionid__name', 'resultid__variable__name'  # noqa
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = [
        'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
        'zaggregationinterval',
        'resultid__resultid__variableid__variable_name__name',
        'resultid__resultid__unitsid__unitsname',
        'resultid__resultid__variableid__variable_type__name',
    ]


class MeasurementresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup',
                                       required=True,
                                       help_text='',
                                       label='Result')

    # This processes the user input into the form.
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


class MeasurementresultsAdmin(AjaxSelectAdmin):
    form = MeasurementresultsAdminForm
    list_display = ('resultid', 'censorcodecv', 'data_link')
    list_display_links = ('resultid', 'data_link')
    # def resultvalues_valuedatetime(self,obj):
    #    mrv = Measurementresultvalues.objects.filter(resultid= obj.resultid)
    #    return mrv.values('valuedatetime')
    # gl = OrderDetail.objects.filter(order__order_date__range=('2015-02-02','2015-03-10'))  # noqa
    list_filter = [MeasurementResultFilter, ]  # ('resultid__valuedatetime', DateRangeFilter),  # noqa
    save_as = True
    search_fields = [
        'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
        'resultid__variableid__variable_name__name',
        'resultid__variableid__variable_type__name'
    ]

    def data_link(self, obj):
        url = u'<a href="{}featureactions/{}/">{}</a>'.format
        return url(CUSTOM_TEMPLATE_PATH,
                   obj.resultid.featureactionid.featureactionid,
                   obj.resultid.featureactionid)

    data_link.short_description = 'sampling feature action'
    data_link.allow_tags = True

    # resultValues = Measurementresultvalues.objects.filter(resultid=)


class MeasurementresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Measurementresultvalues
        import_id_fields = ('valueid',)
        fields = (
            'valueid',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__unitsid__unitsname',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
            'valuedatetime',
            'datavalue',
            'resultid__timeaggregationinterval',
            'resultid__timeaggregationintervalunitsid'
        )
        export_order = (
            'valueid',
            'valuedatetime',
            'datavalue',
            'resultid__timeaggregationinterval',
            'resultid__timeaggregationintervalunitsid',
            'resultid__resultid__variableid__variable_name',
            'resultid__resultid__unitsid__unitsname',
            'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
        )


class MeasurementresultvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Measurementresults,'resultid','measurementresult_lookup')  # noqa
    resultid = AutoCompleteSelectField('measurementresult_lookup',
                                       required=True,
                                       help_text='',
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


class MeasurementresultvaluesAdmin(ImportExportActionModelAdmin,
                                   AjaxSelectAdmin):
    form = MeasurementresultvaluesAdminForm
    # MeasurementresultvaluesResource is for exporting
    # values to different file types.
    # resource_class uses django-import-export.
    resource_class = MeasurementresultvaluesResource
    # Date time filter and list of results you can filter on.
    list_filter = (
        ('valuedatetime', DateRangeFilter),
        MeasurementResultFilter,

    )
    list_display = [
        'datavalue',
        'valuedatetime',
        'resultid'
    ]  # 'resultid', 'featureactionid_link', 'resultid__featureactionid__name', 'resultid__variable__name'  # noqa
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = [
        'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',  # noqa
        'resultid__resultid__variableid__variable_name__name',
        'resultid__resultid__variableid__variable_type__name'
    ]

    def feature_action_link(self, obj):
        url = u'<a href="/admin/ODM2CZOData/featureactions/{}/">{}</a>'.format
        return url(obj.resultid.resultid.featureactionid.featureactionid,
                   obj.resultid.resultid.featureactionid)

    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__featureactionid__samplingfeatureid'  # noqa
    # get_feature_action = 'resultid__resultid__feature_action'
    # def change_view(self, request, object_id, form_url='', extra_context=None):  # noqa
    #
    #     if request.REQUEST.get('export_data'):
    #         csvexport=True
    #         myMeasurementResults = Measurementresultvalues.objects.all().filter()  # noqa
    #         myfile = StringIO.StringIO()
    #         for mresults in myMeasurementResults:
    #             myfile.write(mresults.csvoutput())
    #         response = HttpResponse(myfile.getvalue(),content_type='text/csv')  # noqa
    #         response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+'-'+ name_of_variable +'.csv"'  # noqa
    #         extra_context = response
    #     return super(MeasurementresultvaluesAdmin, self).change_view(request, object_id,  # noqa
    #         form_url, extra_context=extra_context)


class MeasurementresultvalueFileForm(ModelForm):
    class Meta:
        model = MeasurementresultvalueFile
        fields = '__all__'


class UnitsAdminForm(ModelForm):
    unit_type = make_ajax_field(Units, 'unit_type', 'cv_unit_type')
    unit_type.help_text = u'''
    A vocabulary for describing the type of the Unit or the more general quantity that the Unit represents.
    View unit type details here <a href="http://vocabulary.odm2.org/unitstype/"target="_blank">http://vocabulary.odm2.org/unitstype/</a>
    '''  # noqa
    unit_type.allow_tags = True

    class Meta:
        model = Units
        fields = '__all__'


class UnitsAdmin(admin.ModelAdmin):
    form = UnitsAdminForm
    search_fields = ['unit_type__name', 'unitsabbreviation', 'unitsname']
    list_display = ['unitsabbreviation', 'unitsname', 'unit_type']


class DataloggerprogramfilesAdminForm(ModelForm):
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


class DataloggerprogramfilesAdmin(admin.ModelAdmin):
    form = DataloggerprogramfilesAdminForm


class InstrumentoutputvariablesAdminForm(ModelForm):
    class Meta:
        model = Instrumentoutputvariables
        fields = '__all__'


class InstrumentoutputvariablesAdmin(admin.ModelAdmin):
    form = InstrumentoutputvariablesAdminForm


class EquipmentmodelsAdminForm(ModelForm):
    modeldescription = CharField(max_length=5000,
                                 label="model description",
                                 widget=forms.Textarea)
    # Change from a check box to a yes no choice with radio buttons.
    isinstrument = TypedChoiceField(label="Is this an instrument?",
                                    coerce=lambda x: x == 'True',
                                    choices=((False, 'Yes'), (True, 'No')),
                                    widget=forms.RadioSelect
                                    )

    class Meta:
        model = Equipmentmodels
        fields = '__all__'


class EquipmentmodelsAdmin(admin.ModelAdmin):
    form = EquipmentmodelsAdminForm


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
            'organizationid__organizationname',
            'personid__personfirstname',
            'personid__personlastname',
            'isprimaryorganizationcontact',
            'primaryemail'
        )
        export_order = [
            'organizationid__organizationname',
            'personid__personfirstname',
            'personid__personlastname',
            'isprimaryorganizationcontact',
            'primaryemail'
        ]


class AffiliationsAdminForm(ModelForm):

    class Meta:
        model = Affiliations
        fields = '__all__'
        export_order = [
            'organizationname',
            'personfirstname',
            'personlastname',
            'isprimaryorganizationcontact',
            'primaryemail'
        ]
        # ordering = ['-primaryemail']


class AffiliationsAdmin(ExportMixin, admin.ModelAdmin):
    form = AffiliationsAdminForm
    resource_class = AffiliationsResource
    search_fields = [
        'organizationid__organizationname',
        'organizationid__organizationtypecv__name',
        'organizationid__organizationcode',
        'personid__personfirstname',
        'personid__personlastname'
    ]
    list_display = (
        'organizationname',
        'personfirstname',
        'personlastname',
        'isprimaryorganizationcontact',
        'primaryemail'
    )

    def organizationname(self, obj):
        return obj.organizationid.organizationname

    def personfirstname(self, obj):
        return obj.personid.personfirstname

    def personlastname(self, obj):
        return obj.personid.personlastname


class PeopleAdmin(admin.ModelAdmin):
    form = PeopleAdminForm
    inlines = [AffiliationInLine, ORCIDInLine]
    search_fields = [
        'personfirstname',
        'personlastname',
        'personexternalidentifiers__personexternalidentifier',
        'affiliations__organizationid__organizationname'
    ]
    list_display = (
        'personlastname',
        'personfirstname',
        'orcid',
        'affiliation'
    )
    save_as = True

    def orcid(self, obj):
        external_id = Personexternalidentifiers.objects.get(personid=obj.personid)  # noqa
        url = u'<a href="http://orcid.org/{0}" target="_blank">{0}</a>'.format
        return url(external_id.personexternalidentifier)

    def affiliation(self, obj):
        org = Organizations.objects.filter(affiliations__personid_id=obj.personid)  # noqa
        name_list = list()
        url = u'<a href="{0}" target="_blank">{1}</a>'.format
        for org_name in org:
            if org_name.organizationlink:
                name_list.append(url(org_name.organizationlink,
                                     org_name.organizationname))
            else:
                name_list.append(
                    u'{0}'.format(org_name.organizationname))
            # if org_name.parentorganizationid:
            #     if org_name.organizationlink:
            #         name_list.append(u'<a href="{0}" target="_blank">{1}, {2}</a>'.format(org_name.organizationlink, # noqa
            #                                                                               org_name.organizationname,  # noqa
            #                                                                               org_name.parentorganizationid.organizationname))  # noqa
            #     else:
            #         name_list.append(u'{0}, {1}'.format(org_name.organizationname,  # noqa
            #                                               org_name.parentorganizationid.organizationname))
            # else:
            #     if org_name.organizationlink:
            #         name_list.append(
            #             u'<a href="{0}" target="_blank">{1}</a>'.format(org_name.organizationlink, org_name.organizationname))  # noqa
            #     else:
            #         name_list.append(
            #             u'{0}'.format(org_name.organizationname))

        return u'; '.join(name_list)

    orcid.allow_tags = True
    affiliation.allow_tags = True


class ExternalidentifiersystemForm(ModelForm):
    class Meta:
        model = Externalidentifiersystems
        fields = '__all__'


class ExternalidentifiersystemAdmin(admin.ModelAdmin):
    form = ExternalidentifiersystemForm
