#from __future__ import unicode_literals
from django.forms import HiddenInput
from django.contrib import admin
from django.db import models
from django.forms import ModelChoiceField
from django.forms import FileField
from django import forms
from django.forms import  CharField
from django.forms import TypedChoiceField
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import SimpleListFilter, RelatedFieldListFilter

from django.shortcuts import render_to_response
from .models import Variables
from .models import CvVariabletype
from .models import CvVariablename
from .models import CvSpeciation
from .models import Taxonomicclassifiers
from .models import CvTaxonomicclassifiertype
from .models import CvMethodtype
from .models import Samplingfeatures
from .models import CvSamplingfeaturetype
from .models import CvSamplingfeaturegeotype
from .models import CvElevationdatum
from .models import Results
from .models import CvResulttype
from .models import Variables
from .models import Relatedactions
from .models import CvActiontype
from .models import Actions
from .models import Datasets
from .models import Featureactions
from .models import Samplingfeatures
from .models import Organizations
from .models import CvOrganizationtype
from .models import CvRelationshiptype
from .models import CvDatasettypecv
from .models import Affiliations
from .models import People
from .models import Actionby
from .models import Actions
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
from .models import CvUnitstype
from .models import Instrumentoutputvariables
from .models import Equipmentmodels
from .models import Datasetsresults
from .models import Dataquality
from .models import Resultsdataquality

from templatesAndSettings.settings import STATIC_URL
from templatesAndSettings.settings import CUSTOM_TEMPLATE_PATH
from templatesAndSettings.settings import MEDIA_URL
from .models import Profileresults
import cStringIO as StringIO
from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from .models import Measurementresults
from .models import Measurementresultvalues
from .models import Profileresultvalues
#from .views import dataloggercolumnView
from daterange_filter.filter import DateRangeFilter
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import re
#from .admin import MeasurementresultvaluesResource
# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

#a complicated use of search_fields described in ResultsAdminForm

#the following define what fields should be overridden so that dropdown lists can be populated with useful information

def link_list_display_DOI(link):
    match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+", link)
    if not match:
        match = re.match("10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])[[:graph:]])+", link)
    if match:
        return u'<a href="http://dx.doi.org/%s">%s</a>'% (link, link)
    else:
        return u'<a href="%s/">%s</a>'% (link, link)


class ResultsdataqualityAdminForm(ModelForm):
    class Meta:
        model= Resultsdataquality
        fields = '__all__'
class ResultsdataqualityAdmin(admin.ModelAdmin):
    list_display=('resultid', 'dataqualityid')
    form=ResultsdataqualityAdminForm

class DataqualityAdminForm(ModelForm):
    class Meta:
        model= Dataquality
        fields = '__all__'
class DataqualityAdmin(admin.ModelAdmin):
    list_display=('dataqualitytypecv', 'dataqualitycode', 'dataqualityvalue', 'dataqualityvalueunitsid')
    form=DataqualityAdminForm

class MethodcitationsAdminForm(ModelForm):
    class Meta:
        model= Methodcitations
        fields = '__all__'
class MethodcitationsAdmin(admin.ModelAdmin):
    list_display=('method_id','method_link','relationshiptypecv','citation_link')
    form=MethodcitationsAdminForm
    def method_link(self,obj):
        return u'<a href="%smethods/%s/">See Method</a>'% (CUSTOM_TEMPLATE_PATH, obj.methodid.methodid)
    def citation_link(self,obj):
        return u'<a href="%scitations/%s/">%s</a>'% (CUSTOM_TEMPLATE_PATH, obj.citationid.citationid,obj.citationid)
    def method_id(self,obj):
        return obj.methodid
    method_id.short_description = "Method and Citation Link"
    method_link.short_description = 'link to method'
    method_link.allow_tags = True
    citation_link.short_description = 'link to citation'
    citation_link.allow_tags = True

class AuthorlistsAdminForm(ModelForm):
    class Meta:
        model= Authorlists
        fields = '__all__'
class AuthorlistsAdmin(admin.ModelAdmin):
    list_display=('personid','citationid')
    form=AuthorlistsAdminForm

class DatasetcitationsAdminForm(ModelForm):
    class Meta:
        model= Datasetcitations
        fields = '__all__'
class DatasetcitationsAdmin(admin.ModelAdmin):
    list_display=('datasetid','relationshiptypecv','citationid')
    form=DatasetcitationsAdminForm


class CitationsAdminForm(ModelForm):
    class Meta:
        model= Citations
        fields = '__all__'
class CitationsAdmin(admin.ModelAdmin):
    list_display=('title','publisher','publicationyear', 'citation_link')
    form=CitationsAdminForm
    search_fields = ['title','publisher','publicationyear','authorlists__personid__personfirstname', 'authorlists__personid__personlastname']
    def citation_link(self,obj):
       return link_list_display_DOI(obj.citationlink)
    citation_link.short_description = 'link to citation'
    citation_link.allow_tags = True

class CitationextensionpropertyvaluesAdminForm(ModelForm):
    propertyvalue = forms.CharField(max_length=255, widget=forms.Textarea )
    class Meta:
        model=Citationextensionpropertyvalues
        fields = '__all__'

class CitationextensionpropertyvaluesAdmin(admin.ModelAdmin):
    list_display=('citationid','propertyid','propertyvalue')
    form=CitationextensionpropertyvaluesAdminForm


class ExtensionpropertiesAdminForm(ModelForm):
    propertydescription = forms.CharField(max_length=255, widget=forms.Textarea, label="Property description")
    class Meta:
        model= Extensionproperties
        fields = '__all__'
class ExtensionpropertiesAdmin(admin.ModelAdmin):
    list_display=('propertyname','propertydescription','propertydatatypecv', 'propertyunitsid')
    form=ExtensionpropertiesAdminForm


class VariablesAdminForm(ModelForm):
    #variabletypecv= TermModelChoiceField(CvVariabletype.objects.all().order_by('term'))
   # variablenamecv= TermModelChoiceField(CvVariablename.objects.all().order_by('term'))
    #speciationcv= TermModelChoiceField(CvSpeciation.objects.all().order_by('term'))
    #make these fields ajax type ahead fields with links to odm2 controlled vocabulary
    variable_name = make_ajax_field(Variables,'variable_name','cv_variable_name')
    variabledefinition = forms.CharField(max_length=500, widget=forms.Textarea )
    #variable_type = make_ajax_field(Variables,'variable_type','cv_variable_type')
    speciation = make_ajax_field(Variables,'speciation','cv_speciation')
    class Meta:
        model=Variables
        fields = '__all__'

       
class VariablesAdmin(admin.ModelAdmin):
    form=VariablesAdminForm
    list_display =('variable_type','variable_name','variablecode','speciation')
    search_fields = ['variable_type__name','variable_name__name','variablecode','speciation__name']


class TaxonomicclassifiersAdminForm(ModelForm):
    class Meta:
        model= Taxonomicclassifiers
        fields = '__all__'

class TaxonomicclassifiersAdmin(admin.ModelAdmin):
    form=TaxonomicclassifiersAdminForm
    search_fields = ['taxonomicclassifiername','taxonomicclassifiercommonname',
                     'taxonomicclassifierdescription','taxonomic_classifier_type__name']



class SamplingfeaturesAdminForm(ModelForm):
    featuregeometry = CharField(label="feature geometry (to add a point format is POINT(long, lat)"+
                                    " where long and lat are in decimal degrees. If you don't want to add a location"+
                                      " leave default value of POINT(0 0).",
                                    max_length=500, widget=forms.Textarea(),) #attrs={'readonly':'readonly'}
    samplingfeaturedescription = CharField(max_length=500, label= "feature description", widget=forms.Textarea, required=False)
    featuregeometry.initial = "POINT(0 0)"
    featuregeometry.required=False
    class Meta:
        model= Samplingfeatures
        fields = '__all__'
class SamplingfeaturesAdmin(admin.ModelAdmin):
    form=SamplingfeaturesAdminForm
    search_fields = ['sampling_feature_type__name','sampling_feature_geo_type__name','samplingfeaturename','samplingfeaturecode']
    save_as = True

def duplicate_results_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.resultid = None
        object.save()
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

class ResultsAdminForm(ModelForm):
    #featureactionid = make_ajax_field(Featureactions,'featureactionid','featureaction_lookup',max_length=500)
    featureactionid = AutoCompleteSelectField('featureaction_lookup', required=True, help_text='',label='Sampling feature action')
    def clean_featureactionid(self):
          featureactioniduni= self.data['featureactionid']
          featureactionid = None
          for faiduni in featureactioniduni.split("-"):
              if faiduni.isdigit():
                  featureactionid = faiduni
                  continue
          featureaction = Featureactions.objects.filter(featureactionid=featureactionid).get()
          return featureaction
    class Meta:
        model= Results
        fields = '__all__'
    #make_ajax_field doesn't work with the add + green plus on the field

        #widgets = {
        #     'featureactionid': autocomplete.ModelSelect2(url='featueactions-autocomplete')
        # }
#The user can click, a popup window lets them create a new object, they click save, the popup closes and the AjaxSelect field is set.
#Your Admin must inherit from AjaxSelectAdmin
#http://django-ajax-selects.readthedocs.org/en/latest/Admin-add-popup.html
class ResultsAdmin(AjaxSelectAdmin): # admin.ModelAdmin
    form=ResultsAdminForm
    list_display = ['resultid','featureactionid','variableid','processing_level']
    search_fields= ['variableid__variable_name__name','variableid__variablecode','variableid__variabledefinition',
                    'featureactionid__samplingfeatureid__samplingfeaturename',
                    'result_type__name','processing_level__definition']
    actions = [duplicate_results_event]
    save_as = True

    #def get_form(self, request, obj=None, **kwargs):
      #form = super(ResultsAdmin, self).get_form(request, obj, **kwargs)
      #autoselect_fields_check_can_add(form, self.model, request.user)
      #raise ValidationError(form)
      #return form
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
    #actionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    #relationshiptypecv= TermModelChoiceField(CvRelationshiptype.objects.all().order_by('term'))
    #relatedactionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    class Meta:
        model= Relatedactions
        fields = '__all__'
class RelatedactionsAdmin(admin.ModelAdmin):
    form=RelatedactionsAdminForm

class OrganizationsAdminForm(ModelForm):
    #organizationtypecv= TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))
    #parentorganizationid =OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Organizations
        fields = '__all__'
class OrganizationsAdmin(admin.ModelAdmin):
    list_display=('organizationname','organizationdescription')
    form=OrganizationsAdminForm



class FeatureactionsAdminForm(ModelForm):
    class Meta:
        model= Featureactions
        fields = '__all__'
class FeatureactionsAdmin(admin.ModelAdmin):
    list_display = ['samplingfeatureid','action',]
    form=FeatureactionsAdminForm
    save_as = True
    search_fields=['action__method__methodname','samplingfeatureid__samplingfeaturename']

class DatasetsAdminForm(ModelForm):
    datasetabstract = forms.CharField(max_length=500, widget=forms.Textarea )
    class Meta:
        model= Datasets
        fields = '__all__'
class DatasetsAdmin(admin.ModelAdmin):
    form=DatasetsAdminForm
    def get_datasetsresults(self,object_id):
        datasetResults = Datasetsresults.objects.filter(datasetid=object_id)
        #raise ValidationError(datasetResults)
        return datasetResults
    def get_results(self,object_id):
        ids = []
        datasetResults = Datasetsresults.objects.filter(datasetid=object_id)
        for result in datasetResults:
                ids += [result.resultid.resultid]
        resultsList = Results.objects.filter(resultid__in=ids)
        #raise ValidationError(datasetResults)
        #return queryset.filter(resultid__in=ids)
        return resultsList
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DatasetResultsList'] = self.get_datasetsresults(object_id)
        extra_context['ResultsList'] = self.get_results(object_id)
        extra_context['prefixpath'] = CUSTOM_TEMPLATE_PATH
        return super(DatasetsAdmin, self).change_view(request, object_id,form_url, extra_context=extra_context)

class AffiliationsAdminForm(ModelForm):

    class Meta:
        model= Affiliations
        fields = '__all__'

class AffiliationsAdmin(admin.ModelAdmin):
    form=AffiliationsAdminForm

class ActionsAdminForm(ModelForm):
    actiondescription = CharField(max_length=500, label= "Action description", widget=forms.Textarea, required=False)
    class Meta:
        model= Actions
        fields = '__all__'
class ActionsAdmin(admin.ModelAdmin):
    list_display=('action_type','method','begindatetime')
    list_display_links =('action_type','method')
    search_fields=['action_type__name','method__methodname']#,
    form=ActionsAdminForm


class ActionByAdminForm(ModelForm):
    class Meta:
        model= Actionby
        fields = '__all__'
class ActionByAdmin(admin.ModelAdmin):
    list_display=('affiliationid','actionid')
    list_display_links =('affiliationid','actionid')#
    form=ActionByAdminForm
    #list_select_related = True


class MethodsAdminForm(ModelForm):
    methoddescription = CharField(max_length=500, label= "Method description", widget=forms.Textarea, required=False)

    #methodtypecv= TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))
    #organizationid= OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Methods
        fields = '__all__'
class MethodsAdmin(admin.ModelAdmin):
    list_display=('methodname','methodtypecv','method_link')
    list_display_links = ['methodname','method_link']
    form=MethodsAdminForm
    #DOI matching reg expresion came from http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
    def method_link(self,obj):
        return link_list_display_DOI(obj.methodlink)
    method_link.short_description = 'link to method documentation'
    method_link.allow_tags = True

def duplicate_Dataloggerfiles_event(ModelAdmin, request, queryset):
     for dataloggerfile in queryset:
         fileid = dataloggerfile.dataloggerfileid
         filecolumns= Dataloggerfilecolumns.objects.filter(dataloggerfileid=fileid)
         dataloggerfile.dataloggerfileid = None
         dataloggerfile.save()
         #save will assign new dataloggerfileid
         fileid = dataloggerfile.dataloggerfileid
         for columns in filecolumns:
             columns.dataloggerfilecolumnid = None
             columns.dataloggerfileid = dataloggerfile
             columns.save()


duplicate_Dataloggerfiles_event.short_description = "Duplicate selected datalogger file along with columns"

class DataloggerfilesAdminForm(ModelForm):
    class Meta:
        model= Dataloggerfiles
        fields = '__all__'
class DataloggerfilesAdmin(admin.ModelAdmin):
    form=DataloggerfilesAdminForm
    change_form_template = './admin/ODM2CZOData/dataloggerfiles/change_form.html'
    actions = [duplicate_Dataloggerfiles_event]
    #get the data columns related to this data loggerfile and return them to the change view.
    def get_dataloggerfilecolumns(self,object_id):
        DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.filter(dataloggerfileid=object_id)
        return DataloggerfilecolumnsList
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DataloggerfilecolumnsList'] = self.get_dataloggerfilecolumns(object_id)
        extra_context['prefixpath'] = CUSTOM_TEMPLATE_PATH
        #extra_context['dataloggerfileschange_view'] = DataloggerfilecolumnsAdmin.get_changelist(DataloggerfilecolumnsAdmin)
        return super(DataloggerfilesAdmin, self).change_view(request, object_id,form_url, extra_context=extra_context)



def duplicate_Dataloggerfilecolumns_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.dataloggerfilecolumnid = None
        object.save()
duplicate_Dataloggerfilecolumns_event.short_description = "Duplicate selected datalogger file columns"

class DataloggerfilecolumnsAdminForm(ModelForm):
    resultid =AutoCompleteSelectField('result_lookup', required=True, help_text='result to extend as a soil profile result',label='Result')
    def clean_resultid(self):
      resultiduni= self.data['resultid']
      resultid = None
      for riduni in resultiduni.split("-"):
          if riduni.isdigit():
              resultid = riduni
              continue
      result = Results.objects.filter(resultid=resultid).get()
      return result
    class Meta:
        model= Dataloggerfilecolumns
        fields = '__all__'
class DataloggerfilecolumnsAdmin(admin.ModelAdmin):
    form=DataloggerfilecolumnsAdminForm
    list_display = ['columnlabel', 'resultid','dataloggerfileid']
    actions = [duplicate_Dataloggerfilecolumns_event]
    search_fields= ['columnlabel','dataloggerfileid__dataloggerfilename',
                    'resultid__variableid__variable_name__name',]
    save_as = True

class MeasurementResultFilter(SimpleListFilter):
    title = _('data values loaded')
    parameter_name = 'resultValuesPresent'

    def lookups(self, request, model_admin):
        mrs = Measurementresults.objects.values('resultid', 'resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                                                'resultid__variableid__variable_name__name')
        #need to make a custom list with feature name and variable name.
        resultidlist =  [ ( p['resultid'], '{0} {1}'.format(
            p['resultid__featureactionid__samplingfeatureid__samplingfeaturename'],
            p['resultid__variableid__variable_name__name'] ),) for p in mrs ]

        return resultidlist

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        valuesPresent = Measurementresults.objects.filter(resultid=self.value())
        #values = Measurementresultvalues.objects.filter(resultid=self.value()).distinct()
        resultsWCount = Results.objects.raw("SELECT results.*, count(measurementresultvalues.resultid) as valuecount2 " +
                                       "from odm2.results "+
                                       "left join odm2.measurementresultvalues " +
                                       "on (results.resultid = measurementresultvalues.resultid) " +
                                       "group by "+
                                       "results.resultid")
        ids = []
        for mresults in valuesPresent:
            resultid = str(mresults.resultid) #mresults.value_list('resultid')
            resultid= resultid.split(':')[1]
            resultid=  resultid.strip()
            resultid = long(resultid)
            #raise ValidationError(resultid)
            for resultwCount in resultsWCount:
                valuecount2= resultwCount.valuecount2
                #raise ValidationError(resultwCount.resultid)
                if resultid == resultwCount.resultid and valuecount2 > 0:
                     ids += [resultwCount.resultid]
                     #raise ValidationError(ids)

        #valuesPresent = [p.resultid for p in resultsWCount]
        return queryset.filter(resultid__in=ids)

#for soil sampling profiles with depths
class ProfileresultsAdminForm(ModelForm):
    #resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid =AutoCompleteSelectField('result_lookup', required=True, help_text='result to extend as a soil profile result',label='Result')
    #this processes the user input into the form.
    def clean_resultid(self):
      resultiduni= self.data['resultid']
      resultid = None
      for riduni in resultiduni.split("-"):
          if riduni.isdigit():
              resultid = riduni
              continue
      result = Results.objects.filter(resultid=resultid).get()
      return result

    class Meta:
        model =Profileresults
        fields='__all__'
class ProfileresultsAdmin(AjaxSelectAdmin):

    form = ProfileresultsAdminForm
    list_display = ['intendedzspacing','intendedzspacingunitsid','aggregationstatisticcv','resultid',]
    list_display_links = ['intendedzspacing','intendedzspacingunitsid','aggregationstatisticcv','resultid',]
    search_fields= ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                    'resultid__variableid__variable_name__name','resultid__unitsid__unitsname',
                    'resultid__variableid__variable_type__name']
    save_as = True



class ProfileresultvaluesResource(resources.ModelResource):
    class Meta:
        model = Profileresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'zlocation','zlocationunitsid','zaggregationinterval','resultid__resultid__variableid__variable_name',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename','valuedatetime',
                  'resultid__resultid__unitsid__unitsname','datavalue')
        export_order = ('valueid', 'datavalue','zlocation','zlocationunitsid','zaggregationinterval',
        'resultid__resultid__variableid__variable_name','resultid__resultid__unitsid__unitsname','resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename','valuedatetime')


class ProfileresultsvaluesAdminForm(ModelForm):
    #resultid = make_ajax_field(Profileresults,'resultid','profileresult_lookup')
    resultid =AutoCompleteSelectField('profileresult_lookup', required=True, help_text='',label='Profile Result')
    def clean_resultid(self):
      resultiduni= self.data['resultid']
      resultid = None
      for riduni in resultiduni.split("-"):
          if riduni.isdigit():
              resultid = riduni
              continue
      result = Profileresults.objects.filter(resultid=resultid).get()
      return result
    class Meta:
        model= Profileresultvalues
        fields = '__all__'
class ProfileresultsvaluesAdmin(ImportExportActionModelAdmin, AjaxSelectAdmin):
    form=ProfileresultsvaluesAdminForm
    resource_class = ProfileresultvaluesResource
    list_display = ['datavalue','zlocation','zlocationunitsid','zaggregationinterval','valuedatetime','resultid',] #'resultid','featureactionid_link','resultid__featureactionid__name', 'resultid__variable__name'
    list_display_links = ['resultid',] #'featureactionid_link'
    search_fields= ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename','zaggregationinterval',
                    'resultid__resultid__variableid__variable_name__name','resultid__resultid__unitsid__unitsname',
                    'resultid__resultid__variableid__variable_type__name', ]



class MeasurementresultsAdminForm(ModelForm):
    #resultid = make_ajax_field(Results,'resultid','result_lookup')
    resultid =AutoCompleteSelectField('result_lookup', required=True, help_text='',label='Result')
     #this processes the user input into the form.
    def clean_resultid(self):
      resultiduni= self.data['resultid']
      resultid = None
      for riduni in resultiduni.split("-"):
          if riduni.isdigit():
              resultid = riduni
              continue
      result = Results.objects.filter(resultid=resultid).get()
      return result

    class Meta:
        model= Measurementresults
        fields = '__all__'
class MeasurementresultsAdmin(AjaxSelectAdmin):
    form=MeasurementresultsAdminForm
    list_display = ('resultid','censorcodecv','data_link')
    list_display_links = ('resultid','data_link')
    #def resultvalues_valuedatetime(self,obj):
    #    mrv = Measurementresultvalues.objects.filter(resultid= obj.resultid)
    #    return mrv.values('valuedatetime')
    #gl = OrderDetail.objects.filter(order__order_date__range=('2015-02-02','2015-03-10'))
    list_filter = [MeasurementResultFilter, ] #('resultid__valuedatetime', DateRangeFilter),
    save_as = True
    search_fields= ['resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                    'resultid__variableid__variable_name__name',
                    'resultid__variableid__variable_type__name']
    def data_link(self,obj):
        return u'<a href="%sfeatureactions/%s/">%s</a>' % (CUSTOM_TEMPLATE_PATH, obj.resultid.featureactionid.featureactionid, obj.resultid.featureactionid)


    data_link.short_description = 'sampling feature action'
    data_link.allow_tags = True

    #resultValues = Measurementresultvalues.objects.filter(resultid=)



class MeasurementresultvaluesResource(resources.ModelResource):

    class Meta:
        model = Measurementresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'resultid__resultid__variableid__variable_name','resultid__resultid__unitsid__unitsname',
                  'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename','valuedatetime',
                  'datavalue','resultid__timeaggregationinterval','resultid__timeaggregationintervalunitsid')
        export_order = ('valueid', 'valuedatetime','datavalue','resultid__timeaggregationinterval',
        'resultid__timeaggregationintervalunitsid', 'resultid__resultid__variableid__variable_name',
        'resultid__resultid__unitsid__unitsname',
        'resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',)

class MeasurementresultvaluesAdminForm(ModelForm):
    #resultid = make_ajax_field(Measurementresults,'resultid','measurementresult_lookup') #
    resultid =AutoCompleteSelectField('measurementresult_lookup', required=True, help_text='',label='Result')
    def clean_resultid(self):
      resultiduni= self.data['resultid']
      resultid = None
      for riduni in resultiduni.split("-"):
          if riduni.isdigit():
              resultid = riduni
              continue
      result = Measurementresults.objects.filter(resultid=resultid).get()
      return result

    class Meta:
        model= Measurementresultvalues
        fields = '__all__'
class MeasurementresultvaluesAdmin(ImportExportActionModelAdmin, AjaxSelectAdmin):
    form=MeasurementresultvaluesAdminForm
    #MeasurementresultvaluesResource is for exporting values to different file types.
    #resource_class uses django-import-export
    resource_class = MeasurementresultvaluesResource
    #date time filter and list of results you can filter on
    list_filter = (
         ('valuedatetime', DateRangeFilter),
        MeasurementResultFilter,

    )
    list_display = ['datavalue','valuedatetime','resultid'] #'resultid','featureactionid_link','resultid__featureactionid__name', 'resultid__variable__name'
    list_display_links = ['resultid',] #'featureactionid_link'
    search_fields= ['resultid__resultid__featureactionid__samplingfeatureid__samplingfeaturename',
                    'resultid__resultid__variableid__variable_name__name',
                    'resultid__resultid__variableid__variable_type__name']
    def feature_action_link(self,obj):
        return u'<a href="/admin/ODM2CZOData/featureactions/%s/">%s</a>' % (obj.resultid.resultid.featureactionid.featureactionid,obj.resultid.resultid.featureactionid)
    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__featureactionid__samplingfeatureid'
    #get_feature_action = 'resultid__resultid__feature_action'
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


class MeasurementresultvalueFileForm(ModelForm):
    class Meta:
        model= MeasurementresultvalueFile
        fields = '__all__'



class UnitsAdminForm(ModelForm):
    unit_type = make_ajax_field(Units,'unit_type','cv_unit_type')
    class Meta:
        model= Units
        fields = '__all__'
class UnitsAdmin(admin.ModelAdmin):
    form=UnitsAdminForm
    search_fields = ['units_type__name','unitsabbreviation__name','unitsname__name']

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
        model= Dataloggerprogramfiles
        fields = '__all__'

class DataloggerprogramfilesAdmin(admin.ModelAdmin):
    form=DataloggerprogramfilesAdminForm



class InstrumentoutputvariablesAdminForm(ModelForm):
    class Meta:
        model= Instrumentoutputvariables
        fields = '__all__'
class InstrumentoutputvariablesAdmin(admin.ModelAdmin):
    form=InstrumentoutputvariablesAdminForm



class EquipmentmodelsAdminForm(ModelForm):
    modeldescription = CharField(max_length=500, label= "model description", widget=forms.Textarea)
    #change from a check box to a yes no choice with radio buttons.
    isinstrument = TypedChoiceField( label="Is this an instrument?",
                   coerce=lambda x: x == 'True',
                   choices=((False, 'Yes'), (True, 'No')),
                   widget=forms.RadioSelect
                )
    class Meta:
        model= Equipmentmodels
        fields = '__all__'
class EquipmentmodelsAdmin(admin.ModelAdmin):
    form=EquipmentmodelsAdminForm