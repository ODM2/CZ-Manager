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
#from odm2testapp.lookups import CvVariableNameLookup
from odm2testapp.models import Variables
from odm2testapp.models import CvVariabletype
from odm2testapp.models import CvVariablename
from odm2testapp.models import CvSpeciation
from odm2testapp.models import Taxonomicclassifiers
from odm2testapp.models import CvTaxonomicclassifiertype
from odm2testapp.models import CvMethodtype
from odm2testapp.models import Samplingfeatures
from odm2testapp.models import CvSamplingfeaturetype
from odm2testapp.models import CvSamplingfeaturegeotype
from odm2testapp.models import CvElevationdatum
from odm2testapp.models import Results
from odm2testapp.models import CvResulttype
from odm2testapp.models import Variables
from odm2testapp.models import Relatedactions
from odm2testapp.models import CvActiontype
from odm2testapp.models import Actions
from odm2testapp.models import Datasets
from odm2testapp.models import Featureactions
from odm2testapp.models import Samplingfeatures
from odm2testapp.models import Organizations
from odm2testapp.models import CvOrganizationtype
from odm2testapp.models import CvRelationshiptype
from odm2testapp.models import CvDatasettypecv
from odm2testapp.models import Affiliations
from odm2testapp.models import People
from odm2testapp.models import Actionby
from odm2testapp.models import Actions
from odm2testapp.models import Dataloggerprogramfiles
from odm2testapp.models import Dataloggerfiles
from odm2testapp.models import Dataloggerfilecolumns
from odm2testapp.models import Methods
from odm2testapp.models import Units
from odm2testapp.models import MeasurementresultvalueFile
from odm2testapp.models import CvUnitstype
from odm2testapp.models import Instrumentoutputvariables
from odm2testapp.models import Equipmentmodels
import cStringIO as StringIO
from ajax_select import make_ajax_field
from .models import Measurementresults
from .models import Measurementresultvalues
#from .views import dataloggercolumnView
from daterange_filter.filter import DateRangeFilter
from chartit import DataPool, Chart
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
#from .admin import MeasurementresultvaluesResource
# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

#a complicated use of search_fields described in ResultsAdminForm

#the following define what fields should be overridden so that dropdown lists can be populated with useful information


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
    list_display =('variable_type','variable_name','speciation')
    search_fields = ['variable_type__name','variable_name__name','speciation__name']


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


def duplicate_results_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.resultid = None
        object.save()
duplicate_results_event.short_description = "Duplicate selected result"

class ResultsAdminForm(ModelForm):
    class Meta:
        model= Results
        fields = '__all__'
class ResultsAdmin(admin.ModelAdmin):
    form=ResultsAdminForm
    list_display = ['resultid','feature_action','variable','processing_level']
    search_fields= ['variable__variable_name__name','variable__variablecode','variable__variabledefinition',
                    'feature_action__sampling_feature__samplingfeaturename',
                    'result_type__name','processing_level__definition']
    actions = [duplicate_results_event]

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
    list_display = ['sampling_feature','action',]
    form=FeatureactionsAdminForm


class DatasetsAdminForm(ModelForm):
    datasetabstract = forms.CharField(max_length=500, widget=forms.Textarea )
    class Meta:
        model= Datasets
        fields = '__all__'
class DatasetsAdmin(admin.ModelAdmin):
    form=DatasetsAdminForm

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
    def method_link(self,obj):
        return u'<a href="%s/">%s</a>'% (obj.methodlink, obj.methodlink)
    method_link.short_description = 'link to method documentation'
    method_link.allow_tags = True

#
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
    change_form_template = './admin/odm2testapp/dataloggerfiles/change_form.html'
    actions = [duplicate_Dataloggerfiles_event]
    #get the data columns related to this data loggerfile and return them to the change view.
    def get_dataloggerfilecolumns(self,object_id):
        DataloggerfilecolumnsList = Dataloggerfilecolumns.objects.filter(dataloggerfileid=object_id)
        return DataloggerfilecolumnsList
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['DataloggerfilecolumnsList'] = self.get_dataloggerfilecolumns(object_id)
        #extra_context['dataloggerfileschange_view'] = DataloggerfilecolumnsAdmin.get_changelist(DataloggerfilecolumnsAdmin)
        return super(DataloggerfilesAdmin, self).change_view(request, object_id,form_url, extra_context=extra_context)



def duplicate_Dataloggerfilecolumns_event(ModelAdmin, request, queryset):
    for object in queryset:
        object.dataloggerfilecolumnid = None
        object.save()
duplicate_Dataloggerfilecolumns_event.short_description = "Duplicate selected datalogger file columns"

class DataloggerfilecolumnsAdminForm(ModelForm):
    class Meta:
        model= Dataloggerfilecolumns
        fields = '__all__'
class DataloggerfilecolumnsAdmin(admin.ModelAdmin):
    form=DataloggerfilecolumnsAdminForm
    list_display = ['columnlabel', 'resultid','dataloggerfileid']
    actions = [duplicate_Dataloggerfilecolumns_event]
    search_fields= ['columnlabel','dataloggerfileid__dataloggerfilename',
                    'resultid__variable__variable_name__name',]
    save_as = True

class MeasurementResultFilter(SimpleListFilter):
    title = _('data values loaded')
    parameter_name = 'resultValuesPresent'

    def lookups(self, request, model_admin):
        mrs = Measurementresults.objects.values('resultid', 'resultid__feature_action__sampling_feature__samplingfeaturename',
                                                'resultid__variable__variable_name__name')
        #need to make a custom list with feature name and variable name.
        resultidlist =  [ ( p['resultid'], '{0} {1}'.format(
            p['resultid__feature_action__sampling_feature__samplingfeaturename'],
            p['resultid__variable__variable_name__name'] ),) for p in mrs ]

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


class MeasurementresultsAdminForm(ModelForm):
    class Meta:
        model= Measurementresults
        fields = '__all__'
class MeasurementresultsAdmin(admin.ModelAdmin):
    form=MeasurementresultsAdminForm
    list_filter = [MeasurementResultFilter, ]
    list_display = ['resultid','censorcodecv','data_link']
    list_display_links = ['resultid','censorcodecv','data_link']
    save_as = True
    def data_link(self,obj):
        return u'<a href="/admin/odm2testapp/featureactions/%s/">%s</a>' % (obj.resultid.feature_action.featureactionid, obj.resultid.feature_action)
    data_link.short_description = 'feature action'
    data_link.allow_tags = True
    search_fields= ['resultid__feature_action__sampling_feature__samplingfeaturename',
                    'resultid__variable__variable_name__name',
                    'resultid__variable__variable_type__name']
    #resultValues = Measurementresultvalues.objects.filter(resultid=)



class MeasurementresultvaluesResource(resources.ModelResource):

    class Meta:
        model = Measurementresultvalues
        import_id_fields = ('valueid',)
        fields = ('valueid', 'resultid__resultid__variable__variable_name',
                  'resultid__resultid__feature_action__sampling_feature__samplingfeaturename','valuedatetime','datavalue',)
        export_order = ('valueid', 'valuedatetime','datavalue',
        'resultid__resultid__variable__variable_name','resultid__resultid__feature_action__sampling_feature__samplingfeaturename',)

class MeasurementresultvaluesAdminForm(ModelForm):
    class Meta:
        model= Measurementresultvalues
        fields = '__all__'
class MeasurementresultvaluesAdmin(ImportExportActionModelAdmin):
    form=MeasurementresultvaluesAdminForm

    #MeasurementresultvaluesResource is for exporting values to different file types.
    #resource_class uses django-import-export
    resource_class = MeasurementresultvaluesResource

    #date time filter and list of results you can filter on
    list_filter = (
         ('valuedatetime', DateRangeFilter),
        MeasurementResultFilter,

    )
    list_display = ['datavalue','valuedatetime','resultid'] #'resultid','feature_action_link','resultid__feature_action__name', 'resultid__variable__name'
    list_display_links = ['resultid',] #'feature_action_link'
    search_fields= ['resultid__resultid__feature_action__sampling_feature__samplingfeaturename',
                    'resultid__resultid__variable__variable_name__name',
                    'resultid__resultid__variable__variable_type__name']
    def feature_action_link(self,obj):
        return u'<a href="/admin/odm2testapp/featureactions/%s/">%s</a>' % (obj.resultid.resultid.feature_action.featureactionid,obj.resultid.resultid.feature_action)
    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__feature_action__sampling_feature'
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