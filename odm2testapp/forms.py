#from __future__ import unicode_literals
from django.forms import ModelForm
from django.forms import HiddenInput
from django.contrib import admin
from django.db import models
from django.forms import ModelChoiceField
import django.forms
from django.forms import FileField
from .forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response

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
from odm2testapp.models import Methods
from odm2testapp.models import Units
from odm2testapp.models import MeasurementresultvalueFile
from odm2testapp.models import CvUnitstype
from .models import Measurementresults
from .models import Measurementresultvalues



# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

#a complicated use of search_fields described in ResultsAdminForm

#the following define what fields should be overridden so that dropdown lists can be populated with useful information
class VariablesAdminForm(ModelForm):
    #variabletypecv= TermModelChoiceField(CvVariabletype.objects.all().order_by('term'))
   # variablenamecv= TermModelChoiceField(CvVariablename.objects.all().order_by('term'))
    #speciationcv= TermModelChoiceField(CvSpeciation.objects.all().order_by('term'))

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
    class Meta:
        model= Samplingfeatures
        fields = '__all__'
class SamplingfeaturesAdmin(admin.ModelAdmin):
    form=SamplingfeaturesAdminForm
    search_fields = ['sampling_feature_type__name','sampling_feature_geo_type__name','samplingfeaturename','samplingfeaturecode']


class ResultsAdminForm(ModelForm):
    class Meta:
        model= Results
        fields = '__all__'
class ResultsAdmin(admin.ModelAdmin):
    form=ResultsAdminForm
    list_display = ['feature_action','processing_level']
    search_fields= ['variable__variable_name__name','feature_action__sampling_feature__samplingfeaturename',
                    'result_type__name','processing_level__definition__name']

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
    form=FeatureactionsAdminForm


class DatasetsAdminForm(ModelForm):
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

    class Meta:
        model= Actions
        fields = '__all__'
class ActionsAdmin(admin.ModelAdmin):
    list_display=('action_type','method')
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
    #methodtypecv= TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))
    #organizationid= OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Methods
        fields = '__all__'
class MethodsAdmin(admin.ModelAdmin):
    form=MethodsAdminForm


class DataloggerfilesAdminForm(ModelForm):
    class Meta:
        model= Dataloggerfiles
        fields = '__all__'
class DataloggerfilesAdmin(admin.ModelAdmin):
    form=DataloggerfilesAdminForm


class MeasurementresultsForm(ModelForm):
    class Meta:
        model= Measurementresults
        fields = '__all__'

class MeasurementresultvaluesAdminForm(ModelForm):
    class Meta:
        model= Measurementresultvalues
        fields = '__all__'
class MeasurementresultvaluesAdmin(admin.ModelAdmin):
    form=MeasurementresultvaluesAdminForm
    list_display = ['datavalue','valuedatetime','resultid','feature_action_link'] #,'resultid__feature_action__name', 'resultid__variable__name'
    list_display_links = ['resultid','feature_action_link']
    search_fields= ['resultid__resultid__feature_action__sampling_feature__samplingfeaturename','resultid__resultid__variable__variable_name__name',
                    'resultid__resultid__variable__variable_type__name']
    def feature_action_link(self,obj):
        return u'<a href="/admin/odm2testapp/featureactions/%s/">%s</a>' % (obj.resultid.resultid.feature_action.featureactionid,obj.resultid.resultid.feature_action)
    feature_action_link.short_description = 'feature action'
    feature_action_link.allow_tags = True
    feature_action_link.admin_order_field = 'resultid__resultid__feature_action__sampling_feature'
    #get_feature_action = 'resultid__resultid__feature_action'

class MeasurementresultvalueFileForm(ModelForm):
    class Meta:
        model= MeasurementresultvalueFile
        fields = '__all__'



class UnitsAdminForm(ModelForm):
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

