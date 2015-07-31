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
from odm2testapp.models import CvUnitstype
from .models import Measurementresults
from .models import Measurementresultvalues


# AffiliationsChoiceField(People.objects.all().order_by('personlastname'),Organizations.objects.all().order_by('organizationname'))

class AffiliationsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s "%(obj.personlink)

class MethodsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.methodname)

class ActionByChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.actiondescription)

#custom fields to populate form dropdownlists.
class TermModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.term)

class PersonModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s, %s"%(obj.personlastname, obj.personfirstname)

class VariableNameModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.variablenamecv.term)

class ActionsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.actiontypecv.term)

class OrganizationsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.organizationname)
class programFilesModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.programname)

class SamplingfeaturesModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.samplingfeaturename)
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
    taxonomic_classifier_type= TermModelChoiceField(CvTaxonomicclassifiertype.objects.all().order_by('term'))
    class Meta:
        model= Taxonomicclassifiers
        fields = '__all__'

class TaxonomicclassifiersAdmin(admin.ModelAdmin):
    form=TaxonomicclassifiersAdminForm



class SamplingfeaturesAdminForm(ModelForm):
    samplingfeaturetypecv= TermModelChoiceField(CvSamplingfeaturetype.objects.all().order_by('term'))
    samplingfeaturegeotypecv=TermModelChoiceField(CvSamplingfeaturegeotype.objects.all().order_by('term'))
    elevationdatumcv = TermModelChoiceField(CvElevationdatum.objects.all().order_by('term'))
    class Meta:
        model= Samplingfeatures
        fields = '__all__'
class SamplingfeaturesAdmin(admin.ModelAdmin):
    form=SamplingfeaturesAdminForm


class ResultsAdminForm(ModelForm):
    resulttypecv= TermModelChoiceField(CvResulttype.objects.all().order_by('term'))
    variableid= VariableNameModelChoiceField(Variables.objects.all().order_by('variablenamecv'))
    class Meta:
        model= Results
        fields = '__all__'
class ResultsAdmin(admin.ModelAdmin):
    form=ResultsAdminForm


class RelatedactionsAdminForm(ModelForm):
    actionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    relationshiptypecv= TermModelChoiceField(CvRelationshiptype.objects.all().order_by('term'))
    relatedactionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    class Meta:
        model= Relatedactions
        fields = '__all__'
class RelatedactionsAdmin(admin.ModelAdmin):
    form=RelatedactionsAdminForm

class OrganizationsAdminForm(ModelForm):
    organizationtypecv= TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))
    parentorganizationid =OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Organizations
        fields = '__all__'
class OrganizationsAdmin(admin.ModelAdmin):
    list_display=('organizationname','organizationdescription')
    form=OrganizationsAdminForm


class FeatureactionsAdminForm(ModelForm):
    samplingfeatureid= SamplingfeaturesModelChoiceField(Samplingfeatures.objects.all().order_by('samplingfeaturename'))
    class Meta:
        model= Featureactions
        fields = '__all__'
class FeatureactionsAdmin(admin.ModelAdmin):
    form=FeatureactionsAdminForm


class DatasetsAdminForm(ModelForm):
    datasettypecv= TermModelChoiceField(CvDatasettypecv.objects.all().order_by('term'))
    class Meta:
        model= Datasets
        fields = '__all__'
class DatasetsAdmin(admin.ModelAdmin):
    form=DatasetsAdminForm

class AffiliationsAdminForm(ModelForm):
    #affiliationid = models.AutoField(primary_key=True)
    organizationid= OrganizationsModelChoiceField(Organizations.objects.all().order_by('organizationname'))
    personid = PersonModelChoiceField(People.objects.all().order_by('personlastname'))
    class Meta:
        model= Affiliations
        fields = '__all__'

class AffiliationsAdmin(admin.ModelAdmin):
    form=AffiliationsAdminForm

class ActionsAdminForm(ModelForm):
    methodid= MethodsModelChoiceField(Methods.objects.all().order_by('methodname'))
    actiontypecv= TermModelChoiceField(CvActiontype.objects.all().order_by('term'))
    class Meta:
        model= Actions
        fields = '__all__'
class ActionsAdmin(admin.ModelAdmin):
    form=ActionsAdminForm


class ActionByAdminForm(ModelForm):

    #affiliationid= AffiliationsChoiceField(Affiliations.objects.all().order_by('personlink'))
    #actionid= ActionByChoiceField(Actions.objects.all().order_by('actiondescription'))
    #person__name
    #affiliationsForActionBy= Actionby.objects.filter(Affiliations__affiliationid=affiliationid).values('personlink')

    class Meta:
        model= Actionby
        fields = '__all__'
class ActionByAdmin(admin.ModelAdmin):
    #list_display=('__str__',) #'affiliationid','actionid'
    form=ActionByAdminForm
    #list_select_related = True


class MethodsAdminForm(ModelForm):
    methodtypecv= TermModelChoiceField(CvMethodtype.objects.all().order_by('term'))
    organizationid= OrganizationsModelChoiceField( Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Methods
        fields = '__all__'
class MethodsAdmin(admin.ModelAdmin):
    form=MethodsAdminForm


class DataloggerfilesAdminForm(ModelForm):
    #programid= programFilesModelChoiceField( Dataloggerprogramfiles.objects.all().order_by('programname'))
    class Meta:
        model= Dataloggerfiles
        fields = '__all__'
class DataloggerfilesAdmin(admin.ModelAdmin):
    form=DataloggerfilesAdminForm
from .models import Measurementresults
from .models import Measurementresultvalues

class MeasurementresultsForm(ModelForm):
    #programid= programFilesModelChoiceField( Dataloggerprogramfiles.objects.all().order_by('programname'))
    class Meta:
        model= Measurementresults
        fields = '__all__'

class MeasurementresultvaluesForm(ModelForm):
    #programid= programFilesModelChoiceField( Dataloggerprogramfiles.objects.all().order_by('programname'))
    class Meta:
        model= Measurementresultvalues
        fields = '__all__'

class UnitsAdminForm(ModelForm):
    #programid= programFilesModelChoiceField( Dataloggerprogramfiles.objects.all().order_by('programname'))
    #unitstypecv = CvUnitstype.objects.all().order_by('term')
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

