import re

from django import forms
from django.contrib.admin import SimpleListFilter
from django.contrib.gis import forms, admin
from django.contrib.gis.geos import GEOSGeometry
from django.forms import CharField
from django.forms import ModelForm
from django.forms import TypedChoiceField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy
from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportActionModelAdmin

from templatesAndSettings.settings import CUSTOM_TEMPLATE_PATH
from .models import Actionby
from .models import Actions
from .models import Affiliations
from .models import Authorlists
from .models import Citationextensionpropertyvalues
from .models import Citationexternalidentifiers
from .models import Citations
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
from .models import Measurementresults
from .models import MeasurementresultvalueFile
from .models import Measurementresultvalues
from .models import Methodcitations
from .models import Methods
from .models import Organizations
from .models import People
from .models import Personexternalidentifiers
from .models import Profileresults
from .models import Profileresultvalues
from .models import Relatedactions
from .models import Results
from .models import Resultsdataquality
from .models import Samplingfeatureexternalidentifiers
from .models import Samplingfeatures
from .models import Taxonomicclassifiers
from .models import Units
from .models import Variables
from .models import Relatedfeatures
from .models import Processinglevels
from .models import ProcessDataloggerfile

# from io import StringIO
from ajax_select import make_ajax_field
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectField

# from .views import dataloggercolumnView
from daterange_filter.filter import DateRangeFilter
from readonlyadmin import ReadOnlyAdmin


# Organizations AdminForm
class OrganizationsAdminForm(ModelForm):
    # organizationtypecv= TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))
    # parentorganizationid =OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
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
        return u'<a href={0} target="_blank">{0}</a>'.format(org.organizationlink)

    organization_link.allow_tags = True


# Affilitions AdminForm
class AffiliationsResource(resources.ModelResource):
    class Meta:
        model = Affiliations
        fields = ('organizationid__organizationname', 'personid__personfirstname', 'personid__personlastname',
                  'isprimaryorganizationcontact',
                  'primaryemail')
        export_order = ['organizationid__organizationname', 'personid__personfirstname', 'personid__personlastname',
                        'isprimaryorganizationcontact', 'primaryemail']


class AffiliationsAdminForm(ModelForm):
    class Meta:
        model = Affiliations
        fields = '__all__'
        export_order = ['organizationname', 'personfirstname', 'personlastname', 'isprimaryorganizationcontact',
                        'primaryemail']


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
        'organizationname', 'personfirstname', 'personlastname', 'isprimaryorganizationcontact', 'primaryemail')

    def organizationname(self, obj):
        return obj.organizationid.organizationname

    def personfirstname(self, obj):
        return obj.personid.personfirstname

    def personlastname(self, obj):
        return obj.personid.personlastname


# People AdminForm
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


class PeopleAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in People._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyAffiliationInline, ReadOnlyORCIDInline]

    # For admin users
    form = PeopleAdminForm
    inlines_list = [AffiliationInLine, ORCIDInLine]

    search_fields = ['personfirstname', 'personlastname', 'personexternalidentifiers__personexternalidentifier',
                     'affiliations__organizationid__organizationname']
    list_display = ('personlastname', 'personfirstname', 'orcid', 'affiliation')
    save_as = True

    def orcid(self, obj):
        external_id = Personexternalidentifiers.objects.get(personid=obj.personid)
        return u'<a href="http://orcid.org/{0}" target="_blank">{0}</a>'.format(external_id.personexternalidentifier)

    def affiliation(self, obj):
        org = Organizations.objects.filter(affiliations__personid_id=obj.personid)
        name_list = list()
        for org_name in org:
            if org_name.organizationlink:
                name_list.append(
                    u'<a href="{0}" target="_blank">{1}</a>'.format(org_name.organizationlink,
                                                                    org_name.organizationname))
            else:
                name_list.append(
                    u'{0}'.format(org_name.organizationname))
                # if org_name.parentorganizationid:
                #     if org_name.organizationlink:
                #         name_list.append(u'<a href="{0}" target="_blank">{1}, {2}</a>'.format(org_name.organizationlink,
                #                                                                               org_name.organizationname,
                #                                                                               org_name.parentorganizationid.organizationname))
                #     else:
                #         name_list.append(u'{0}, {1}'.format(org_name.organizationname,
                #                                               org_name.parentorganizationid.organizationname))
                # else:
                #     if org_name.organizationlink:
                #         name_list.append(
                #             u'<a href="{0}" target="_blank">{1}</a>'.format(org_name.organizationlink, org_name.organizationname))
                #     else:
                #         name_list.append(
                #             u'{0}'.format(org_name.organizationname))

        return u'; '.join(name_list)

    orcid.allow_tags = True
    affiliation.allow_tags = True


# Variables AdminForm
class VariablesAdminForm(ModelForm):
    # make these fields ajax type ahead fields with links to odm2 controlled vocabulary
    variable_type = make_ajax_field(Variables, 'variable_type', 'cv_variable_type')
    variable_name = make_ajax_field(Variables, 'variable_name', 'cv_variable_name')
    variabledefinition = forms.CharField(max_length=500, widget=forms.Textarea)
    # variable_type = make_ajax_field(Variables,'variable_type','cv_variable_type')
    speciation = make_ajax_field(Variables, 'speciation', 'cv_speciation')

    variable_name.help_text = u'view variable names here <a href="http://vocabulary.odm2.org/variablename/" target="_blank">http://vocabulary.odm2.org/variablename/</a>'
    variable_name.allow_tags = True
    variable_type.help_text = u'view variable types here <a href="http://vocabulary.odm2.org/variabletype/" target="_blank" >http://vocabulary.odm2.org/variabletype/</a>'
    variable_type.allow_tags = True
    speciation.help_text = u'view variable types here <a href="http://vocabulary.odm2.org/speciation/" target="_blank" >http://vocabulary.odm2.org/speciation/</a>'
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

    list_display = ('variablecode', 'variable_name_linked', 'variable_type_linked', 'speciation_linked')
    search_fields = ['variable_type__name', 'variable_name__name', 'variablecode', 'speciation__name']

    def variable_name_linked(self, obj):
        if obj.variable_name:
            return u'<a href="http://vocabulary.odm2.org/variablename/{0}" target="_blank">{1}</a>'.format(
                obj.variable_name.term, obj.variable_name.name)

    variable_name_linked.short_description = 'Variable Name'
    variable_name_linked.allow_tags = True

    def variable_type_linked(self, obj):
        if obj.variable_type:
            return u'<a href="http://vocabulary.odm2.org/variabletype/{0}" target="_blank">{1}</a>'.format(
                obj.variable_type.term, obj.variable_type.name)

    variable_type_linked.short_description = 'Variable Type'
    variable_type_linked.allow_tags = True

    def speciation_linked(self, obj):
        if obj.speciation:
            return u'<a href="http://vocabulary.odm2.org/speciation/{0}" target="_blank">{1}</a>'.format(
                obj.speciation.term, obj.speciation.name)

    speciation_linked.short_description = 'Speciation'
    speciation_linked.allow_tags = True


# Units AdminForm
class UnitsAdminForm(ModelForm):
    unit_type = make_ajax_field(Units, 'unit_type', 'cv_unit_type')
    unit_type.help_text = u'A vocabulary for describing the type of the Unit or the more general quantity that the Unit ' \
                          u'represents. View unit type details here <a href="http://vocabulary.odm2.org/unitstype/" ' \
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


# Taxonomicclassifiers AdminForm
class TaxonomicclassifiersAdminForm(ModelForm):
    taxonomic_classifier_type = make_ajax_field(Taxonomicclassifiers, 'taxonomic_classifier_type',
                                                'cv_taxonomic_classifier_type')
    taxonomic_classifier_type.help_text = u'A vocabulary for describing types of taxonomies from which descriptive terms used ' \
                                          u'in an ODM2 database have been drawn. Taxonomic classifiers provide a way to classify' \
                                          u' Results and Specimens according to terms from a formal taxonomy. Check ' \
                                          u'<a href="http://vocabulary.odm2.org/taxonomicclassifiertype/" target="_blank">' \
                                          u'http://vocabulary.odm2.org/taxonomicclassifiertype/</a>  for more info'
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


# Methods AdminForm
class MethodsAdminForm(ModelForm):
    methoddescription = CharField(max_length=5000, label="Method description", widget=forms.Textarea,
                                  required=False)
    methodtypecv = make_ajax_field(Methods, 'methodtypecv', 'cv_method_type')
    methodtypecv.help_text = u'A vocabulary for describing types of Methods associated with creating observations. ' \
                             u'MethodTypes correspond with ActionTypes in ODM2. An Action must be performed using an ' \
                             u'appropriate MethodType - e.g., a specimen collection Action should be associated with a ' \
                             u'specimen collection method. details for individual values ' \
                             u'here: <a href="http://vocabulary.odm2.org/methodtype/" target="_blank">http://vocabulary.odm2.org/methodtype/</a>'
    methodtypecv.allow_tags = True

    # methodtypecv= TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))
    # organizationid= OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model = Methods
        fields = '__all__'


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


class MethodsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Methods._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyActionsInline]

    # For admin users
    form = MethodsAdminForm
    inlines_list = [ActionsInline]

    list_display = ('methodname', 'method_type_linked', 'method_link')
    list_display_links = ['methodname']

    # DOI matching reg expresion came from http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
    def method_link(self, obj):
        return link_list_display_doi(obj.methodlink)

    method_link.short_description = 'link to method documentation'
    method_link.allow_tags = True

    def method_type_linked(self, obj):
        if obj.methodtypecv:
            return u'<a href="http://vocabulary.odm2.org/methodtype/{0}" target="_blank">{1}</a>'.format(
                obj.methodtypecv.term, obj.methodtypecv.name)

    method_type_linked.short_description = 'Method Type'
    method_type_linked.allow_tags = True


# Actions AdminForm
class ActionsAdminForm(ModelForm):
    actiondescription = CharField(max_length=5000, label="Action description", widget=forms.Textarea,
                                  required=False)
    action_type = make_ajax_field(Actions, 'action_type', 'cv_action_type')
    action_type.help_text = u'A vocabulary for describing the type of actions performed in making observations. Depending' \
                            u' on the action type, the action may or may not produce an observation result. view action type ' \
                            u'details here <a href="http://vocabulary.odm2.org/actiontype/" target="_blank">http://vocabulary.odm2.org/actiontype/</a>'
    action_type.allow_tags = True

    class Meta:
        model = Actions
        fields = '__all__'


class FeatureActionsInline(admin.StackedInline):
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


class ActionsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Actions._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyFeatureActionsInline]

    # For admin users
    form = ActionsAdminForm
    inlines_list = [FeatureActionsInline]

    list_display = ('action_type', 'method', 'begindatetime', 'enddatetime')
    list_display_links = ('action_type',)
    search_fields = ['action_type__name', 'method__methodname']  # ,


# Relatedactions AdminForm
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


# Actionby AdminForm
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


# Samplingfeatures AdminForm
class SamplingfeaturesAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatures
        fields = ['sampling_feature_type', 'samplingfeaturecode', 'samplingfeaturename',
                  'samplingfeaturedescription', 'sampling_feature_geo_type', 'featuregeometrywkt', 'featuregeometry',
                  'elevation_m', 'elevation_datum']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            feat = instance.featuregeometrywkt()
            initial = kwargs.get('initial', {})
            initial['featuregeometrywkt'] = '{}'.format(feat)
            initial['map'] = '{}'.format(feat)
            kwargs['initial'] = initial
        super(SamplingfeaturesAdminForm, self).__init__(*args, **kwargs)

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type', 'cv_sampling_feature_type')
    sampling_feature_type.help_text = u'A vocabulary for describing the type of SamplingFeature. ' \
                                      u'Many different SamplingFeature types can be represented in ODM2. ' \
                                      u'SamplingFeatures of type Site and Specimen will be the most common, ' \
                                      u'but many different types of varying levels of complexity can be used. ' \
                                      u'details for individual values ' \
                                      u'here: <a href="http://vocabulary.odm2.org/samplingfeaturetype/" target="_blank">http://vocabulary.odm2.org/samplingfeaturetype/</a>'
    sampling_feature_type.allow_tags = True

    samplingfeaturedescription = CharField(max_length=5000, label="feature description", widget=forms.Textarea,
                                           required=False)

    sampling_feature_geo_type = make_ajax_field(Samplingfeatures, 'sampling_feature_geo_type',
                                                'cv_sampling_feature_geo_type')
    sampling_feature_geo_type.help_text = u'A vocabulary for describing the geospatial feature type associated with a SamplingFeature. ' \
                                          u'For example, Site SamplingFeatures are represented as points. ' \
                                          u'In ODM2, each SamplingFeature may have only one geospatial type, ' \
                                          u'but a geospatial types may range from simple points to a complex polygons ' \
                                          u'or even three dimensional volumes. ' \
                                          u'details for individual values ' \
                                          u'here: <a href="http://vocabulary.odm2.org/samplingfeaturegeotype/" ' \
                                          u'target="_blank">http://vocabulary.odm2.org/samplingfeaturegeotype/</a>'
    sampling_feature_geo_type.allow_tags = True
    sampling_feature_geo_type.required = False

    elevation_datum = make_ajax_field(Samplingfeatures, 'elevation_datum',
                                      'cv_elevation_datum')
    elevation_datum.help_text = u'A vocabulary for describing vertical datums. ' \
                                u'Vertical datums are used in ODM2 to specify the origin for elevations ' \
                                u'assocated with SamplingFeatures.' \
                                u'details for individual values ' \
                                u'here: <a href="http://vocabulary.odm2.org/elevationdatum/" ' \
                                u'target="_blank">http://vocabulary.odm2.org/elevationdatum/</a>'
    elevation_datum.allow_tags = True
    featuregeometrywkt = forms.CharField(help_text="feature geometry (to add a point format is POINT(lat, lon)" +
                                                   " where long and lat are in decimal degrees. If you don't want to add a location" +
                                                   " leave default value of POINT(0 0).", label='Featuregeometrywkt',
                                         widget=forms.Textarea(attrs={'readonly': False}), required=False)


    featuregeometrywkt.initial = GEOSGeometry("POINT(0 0)")
    featuregeometry = forms.PointField(label='Featuregeometry',
                                       widget=forms.OpenLayersWidget(), required=False)

    featuregeometry.initial = GEOSGeometry("POINT(0 0)")


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


class SamplingfeaturesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Samplingfeatures._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyFeatureActionsInline, ReadOnlyIGSNInline]

    form = SamplingfeaturesAdminForm
    inlines_list = [FeatureActionsInline, IGSNInline]

    search_fields = ['sampling_feature_type__name', 'sampling_feature_geo_type__name', 'samplingfeaturename',
                     'samplingfeaturecode', 'samplingfeatureid',
                     'samplingfeatureexternalidentifiers__samplingfeatureexternalidentifier']

    list_display = (
        'samplingfeaturecode', 'samplingfeaturename', 'sampling_feature_type_linked', 'samplingfeaturedescription',
        'igsn',
        'dataset_code')
    readonly_fields = ('samplingfeatureuuid',)

    # your own processing
    def save_model(self, request, obj, form, change):
        # for example:
        obj.featuregeometry = '%s' % form.cleaned_data['featuregeometrywkt']
        obj.save()

    save_as = True

    def igsn(self, obj):
        external_id = Samplingfeatureexternalidentifiers.objects.get(samplingfeatureid=obj.samplingfeatureid)
        return u'<a href="https://app.geosamples.org/sample/igsn/{0}" target="_blank">{0}</a>'.format(
            external_id.samplingfeatureexternalidentifier)

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
            return u'<a href="http://vocabulary.odm2.org/samplingfeaturetype/{0}" target="_blank">{1}</a>'.format(
                obj.sampling_feature_type.term, obj.sampling_feature_type.name)

    sampling_feature_type_linked.short_description = 'Sampling Feature Type'
    sampling_feature_type_linked.allow_tags = True

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups

# Relatedfeatures AdminForm
class RelatedfeaturesAdminForm(ModelForm):
    class Meta:
        model = Relatedfeatures
        fields = '__all__'


class RelatedfeaturesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Relatedfeatures._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = RelatedactionsAdminForm
    inlines_list = list()


# FeatureActions AdminForm
class FeatureactionsAdminForm(ModelForm):

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


# Results AdminForm
class ResultsAdminForm(ModelForm):
    # featureactionid = make_ajax_field(Featureactions,'featureactionid','featureaction_lookup',max_length=500)
    featureactionid = AutoCompleteSelectField('featureaction_lookup', required=True, help_text='',
                                              label='Sampling feature action')

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


def duplicate_results_event(request, queryset):
    for object in queryset:
        object.resultid = None
        object.save()

duplicate_results_event.short_description = "Duplicate selected result"


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


class ResultsAdmin(ReadOnlyAdmin):  # admin.ModelAdmin
    # The user can click, a popup window lets them create a new object,
    # they click save, the popup closes and the AjaxSelect field is set.
    # http://django-ajax-selects.readthedocs.org/en/latest/Admin-add-popup.html
    # For readonly usergroup
    user_readonly = [p.name for p in Results._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyMeasurementResultsInline, ReadOnlyProfileResultsInline]

    # For admin users
    form = ResultsAdminForm
    inlines_list = [MeasurementResultsInline, ProfileResultsInline]

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


# Datasets AdminForm
class DatasetsAdminForm(ModelForm):
    datasetabstract = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Datasets
        fields = '__all__'


class DatasetsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Datasets._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DatasetsAdminForm
    inlines_list = list()

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
        extra_context['prefixpath'] = CUSTOM_TEMPLATE_PATH
        return super(DatasetsAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


# Datasetsresult AdminForm
class DatasetsresultsAdminForm(ModelForm):
    resultid = make_ajax_field(Datasetsresults, 'resultid',
                                                'result_lookup')
    class Meta:
        model = Datasetsresults
        fields = ['datasetid','bridgeid', 'resultid']


class DatasetsresultsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Datasetsresults._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DatasetsresultsAdminForm
    inlines_list = list()


# ProcessingLevels AdminForm
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


# Measurementresults AdminForm
class MeasurementresultsAdminForm(ModelForm):
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup', required=True, help_text='', label='Result')

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


class MeasurementResultFilter(SimpleListFilter):
    title = ugettext_lazy('data values loaded')
    parameter_name = 'resultValuesPresent'

    def lookups(self, request, model_admin):
        mrs = Measurementresults.objects.values('resultid',
                                                'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                                                'resultid__variableid__variable_name__name')
        # need to make a custom list with feature name and variable name.
        resultidlist = [(p['resultid'], '{0} {1}'.format(
            p['resultid__featureactionid__samplingfeatureid__samplingfeaturename'],
            p['resultid__variableid__variable_name__name']),) for p in mrs]

        return resultidlist

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        valuesPresent = Measurementresults.objects.filter(resultid=self.value())
        # values = Measurementresultvalues.objects.filter(resultid=self.value()).distinct()
        resultsWCount = Results.objects.raw(
            "SELECT results.*, count(measurementresultvalues.resultid) as valuecount2 " +
            "from odm2.results " +
            "left join odm2.measurementresultvalues " +
            "on (results.resultid = measurementresultvalues.resultid) " +
            "group by " +
            "results.resultid")
        ids = []
        for mresults in valuesPresent:
            resultid = str(mresults.resultid)  # mresults.value_list('resultid')
            resultid = resultid.split(':')[1]
            resultid = resultid.strip()
            resultid = long(resultid)
            # raise ValidationError(resultid)
            for resultwCount in resultsWCount:
                valuecount2 = resultwCount.valuecount2
                # raise ValidationError(resultwCount.resultid)
                if resultid == resultwCount.resultid and valuecount2 > 0:
                    ids += [resultwCount.resultid]
                    # raise ValidationError(ids)

        # valuesPresent = [p.resultid for p in resultsWCount]
        return queryset.filter(resultid__in=ids)


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
    list_filter = [MeasurementResultFilter, ]  # ('resultid__valuedatetime', DateRangeFilter),
    save_as = True
    search_fields = ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__variableid__variable_name__name',
                     'resultid__variableid__variable_type__name']

    def data_link(self, obj):
        return u'<a href="%sfeatureactions/%s/">%s</a>' % (
            CUSTOM_TEMPLATE_PATH, obj.resultid.featureactionid.featureactionid, obj.resultid.featureactionid)

    data_link.short_description = 'sampling feature action'
    data_link.allow_tags = True

        # resultValues = Measurementresultvalues.objects.filter(resultid=)


# Measurementresultvalues AdminForm
class MeasurementresultvaluesResource(resources.ModelResource):

    class Meta:
        model = Measurementresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'resultid__resultid__variableid__variable_name', 'resultid__resultid__unitsid__unitsname',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename', 'valuedatetime',
                  'datavalue', 'resultid__timeaggregationinterval', 'resultid__timeaggregationintervalunitsid')
        export_order = ('valueid', 'valuedatetime', 'datavalue', 'resultid__timeaggregationinterval',
                        'resultid__timeaggregationintervalunitsid', 'resultid__resultid__variableid__variable_name',
                        'resultid__resultid__unitsid__unitsname',
                        'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',)


class MeasurementresultvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Measurementresults,'resultid','measurementresult_lookup') #
    resultid = AutoCompleteSelectField('measurementresult_lookup', required=True, help_text='', label='Result')

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
    user_readonly = [p.name for p in Measurementresultvalues._meta.get_fields() if not p.one_to_many]
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
        MeasurementResultFilter,

    )
    list_display = ['datavalue', 'valuedatetime',
                    'resultid']  # 'resultid','featureactionid_link','resultid__featureactionid__name', 'resultid__variable__name'
    list_display_links = ['resultid', ]  # 'featureactionid_link'
    search_fields = ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__resultid__variableid__variable_name__name',
                     'resultid__resultid__variableid__variable_type__name']

    def feature_action_link(self, obj):
        return u'<a href="/admin/ODM2CZOData/featureactions/%s/">%s</a>' % (
            obj.resultid.resultid.featureactionid.featureactionid, obj.resultid.resultid.featureactionid)

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
    #         response['Content-Disposition'] = 'attachment; filename="'+ name_of_sampling_feature+'-'+ name_of_variable +'.csv"'
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


# MeasurementresultvalueFile AdminForm
class MeasurementresultvalueFileAdminForm(ModelForm):

    class Meta:
        model = MeasurementresultvalueFile
        fields = '__all__'


class MeasurementresultvalueFileAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in MeasurementresultvalueFile._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProcessingLevelsAdminForm
    inlines_list = list()


# Profileresults AdminForm
class ProfileresultsAdminForm(ModelForm):
    # for soil sampling profiles with depths
    # resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result to extend as a soil profile result', label='Result')

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

    list_display = ['intendedzspacing', 'intendedzspacingunitsid', 'aggregationstatisticcv', 'resultid', ]
    list_display_links = ['intendedzspacing', 'intendedzspacingunitsid', 'aggregationstatisticcv', 'resultid', ]
    search_fields = ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                     'resultid__variableid__variable_name__name', 'resultid__unitsid__unitsname',
                     'resultid__variableid__variable_type__name']
    save_as = True


# Profileresultvalues AdminForm
class ProfileresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Profileresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'zlocation', 'zlocationunitsid', 'zaggregationinterval',
                  'resultid__resultid__variableid__variable_name',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename', 'valuedatetime',
                  'resultid__resultid__unitsid__unitsname', 'datavalue')
        export_order = ('valueid', 'datavalue', 'zlocation', 'zlocationunitsid', 'zaggregationinterval',
                        'resultid__resultid__variableid__variable_name', 'resultid__resultid__unitsid__unitsname',
                        'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                        'valuedatetime')


class ProfileresultvaluesAdminForm(ModelForm):
    # resultid = make_ajax_field(Profileresults,'resultid','profileresult_lookup')
    resultid = AutoCompleteSelectField('profileresult_lookup', required=True, help_text='', label='Profile Result')

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


class ProfileresultvaluesAdmin(ImportExportActionModelAdmin, ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Profileresultvalues._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProfileresultvaluesAdminForm
    inlines_list = list()

    resource_class = ProfileresultvaluesResource
    list_display = ['datavalue', 'zlocation', 'zlocationunitsid', 'zaggregationinterval', 'valuedatetime',
                    'resultid', ]  # 'resultid','featureactionid_link','resultid__featureactionid__name', 'resultid__variable__name'
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
        return super(ProfileresultvaluesAdmin, self).changelist_view(
            request, extra_context=extra_context)

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


# Citations AdminForm
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


class ReadOnlyDOIInline(DOIInline):
    readonly_fields = DOIInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class ReadOnlyauthorlistInline(authorlistInline):
    readonly_fields = authorlistInline.fieldsets[0][1]['fields']
    can_delete = False

    def has_add_permission(self, request):
        return False


class CitationsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Citations._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyauthorlistInline, ReadOnlyDOIInline]

    # For admin users
    form = CitationsAdminForm
    inlines_list = [authorlistInline, DOIInline]

    list_display = (
    'primary_author', 'publicationyear', 'title', 'other_author', 'publisher', 'doi', 'citation_link')
    list_display_links = ['title']
    search_fields = ['title', 'publisher', 'publicationyear', 'authorlists__personid__personfirstname',
                     'authorlists__personid__personlastname']

    def citation_link(self, obj):
        return link_list_display_doi(obj.citationlink)

    def doi(self, obj):
        external_id = Citationexternalidentifiers.objects.get(citationid=obj.citationid)
        return u'<a href="http://dx.doi.org/{0}" target="_blank">{0}</a>'.format(
            external_id.citationexternalidentifier)

    def primary_author(self, obj):
        self.author_list = Authorlists.objects.filter(citationid=obj.citationid)
        first_author = self.author_list.get(authororder=1)
        return "{0}, {1}".format(first_author.personid.personlastname, first_author.personid.personfirstname)

    def other_author(self, obj):
        list_et_al = list()
        for author in self.author_list:
            if author.authororder != 1:
                list_et_al.append(
                    "{0}, {1}".format(author.personid.personlastname, author.personid.personfirstname))
        return "; ".join(list_et_al)

    doi.allow_tags = True
    citation_link.short_description = 'link to citation'
    other_author.short_description = 'Other Authors'
    citation_link.allow_tags = True
    # primary_author.admin_order_field = 'authorlists__personid__personlastname'


# Authorlist AdminForm
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


# Datasetcitations AdminForm
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


# Methodcitations AdminForm
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
        return u'<a href="%smethods/%s/">See Method</a>' % (CUSTOM_TEMPLATE_PATH, obj.methodid.methodid)

    def citation_link(self, obj):
        return u'<a href="%scitations/%s/">%s</a>' % (
        CUSTOM_TEMPLATE_PATH, obj.citationid.citationid, obj.citationid)

    def method_id(self, obj):
        return obj.methodid

    method_id.short_description = "Method and Citation Link"
    method_link.short_description = 'link to method'
    method_link.allow_tags = True
    citation_link.short_description = 'link to citation'
    citation_link.allow_tags = True


# Extentsionsproperties AdminForm
class ExtensionpropertiesAdminForm(ModelForm):
    propertydescription = forms.CharField(max_length=255, widget=forms.Textarea, label="Property description")

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


# Citationextensionpropertyvalues AdminForm
class CitationextensionpropertyvaluesAdminForm(ModelForm):
    propertyvalue = forms.CharField(max_length=255, widget=forms.Textarea)

    class Meta:
        model = Citationextensionpropertyvalues
        fields = '__all__'


class CitationextensionpropertyvaluesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Citationextensionpropertyvalues._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = CitationextensionpropertyvaluesAdminForm
    inlines_list = list()

    list_display = ('citationid', 'propertyid', 'propertyvalue')


# Dataloggerprogramfiles AdminForm
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


class DataloggerprogramfilesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Dataloggerprogramfiles._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = DataloggerprogramfilesAdminForm
    inlines_list = list()


# Dataloggerfiles AdminForm
def duplicate_Dataloggerfiles_event(request, queryset):
    for dataloggerfile in queryset:
        fileid = dataloggerfile.dataloggerfileid
        filecolumns = Dataloggerfilecolumns.objects.filter(dataloggerfileid=fileid)
        dataloggerfile.dataloggerfileid = None
        dataloggerfile.save()
        # save will assign new dataloggerfileid
        fileid = dataloggerfile.dataloggerfileid
        for columns in filecolumns:
            columns.dataloggerfilecolumnid = None
            columns.dataloggerfileid = dataloggerfile
            columns.save()

duplicate_Dataloggerfiles_event.short_description = "Duplicate selected datalogger file along with columns"

class DataLoggerFileColumnsInlineAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result to extend as a soil profile result', label='Result')

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

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)

        if self.__user_is_readonly(request):
            actions = list()

        return actions

    @staticmethod
    def __user_is_readonly(request):
        groups = [x.name for x in request.user.groups.all()]
        return "readonly" in groups


# Dataloggerfilecolumns AdminForm
def duplicate_Dataloggerfilecolumns_event(request, queryset):
    for object in queryset:
        object.dataloggerfilecolumnid = None
        object.save()

duplicate_Dataloggerfilecolumns_event.short_description = "Duplicate selected datalogger file columns"


class DataloggerfilecolumnsAdminForm(ModelForm):
    resultid = AutoCompleteSelectField('result_lookup', required=True,
                                       help_text='result to extend as a soil profile result', label='Result')

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


# ProcessDataloggerfile AdminForm
class ProcessDataloggerfileAdminForm(ModelForm):

    class Meta:
        model = ProcessDataloggerfile
        fields = '__all__'


class ProcessDataloggerfileAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in ProcessDataloggerfile._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = ProcessDataloggerfileAdminForm
    inlines_list = list()


# Instrumentoutputvariables AdminForm
class InstrumentoutputvariablesAdminForm(ModelForm):

    class Meta:
        model = Instrumentoutputvariables
        fields = '__all__'


class InstrumentoutputvariablesAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Instrumentoutputvariables._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()

    # For admin users
    form = InstrumentoutputvariablesAdminForm
    inlines_list = list()

# Equipmentmodels AdminForm
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


class EquipmentmodelsAdmin(ReadOnlyAdmin):
    # For readonly usergroup
    user_readonly = [p.name for p in Equipmentmodels._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = [ReadOnlyInstrumentoutputvariablesInline]

    # For admin users
    form = EquipmentmodelsAdminForm
    inlines_list = [InstrumentoutputvariablesInline]


# Dataquality AdminForm
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

    list_display = ('dataqualitytypecv', 'dataqualitycode', 'dataqualityvalue', 'dataqualityvalueunitsid')


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


# Externalidentifiersystem AdminForm
class ExternalidentifiersystemForm(ModelForm):
    class Meta:
        model = Externalidentifiersystems
        fields = '__all__'


class ExternalidentifiersystemAdmin(ReadOnlyAdmin):
    # For admin users
    form = ExternalidentifiersystemForm
    inlines_list = list()

    # For readonly users
    user_readonly = [p.name for p in Externalidentifiersystems._meta.get_fields() if not p.one_to_many]
    user_readonly_inlines = list()
###############################################################
# from .admin import MeasurementresultvaluesResource
# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

# a complicated use of search_fields described in ResultsAdminForm

# the following define what fields should be overridden so that dropdown lists can be populated with useful information

def link_list_display_doi(link):
    match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+", link)
    if not match:
        match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])[[:graph:]])+", link)
    if match:
        return u'<a href="http://dx.doi.org/%s" target="_blank">%s</a>' % (link, link)
    else:
        return u'<a href="%s" target="_blank">%s</a>' % (link, link)


class variablesInLine(admin.StackedInline):
    model = Variables


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


class resultsInLine(admin.StackedInline):
    model = Results


class SamplingfeatureexternalidentifiersAdminForm(ModelForm):
    class Meta:
        model = Samplingfeatureexternalidentifiers
        fields = '__all__'


class SamplingfeatureexternalidentifiersAdmin(admin.ModelAdmin):
    form = SamplingfeatureexternalidentifiersAdminForm
    search_fields = ['samplingfeatureexternalidentifier']
    list_display = ('samplingfeatureexternalidentifier', 'samplingfeatureexternalidentifieruri')
    save_as = True


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



class SamplingFeaturesInline(admin.StackedInline):
    model = Samplingfeatures
    extra = 0
