#from __future__ import unicode_literals
from django.forms import ModelForm
from django.contrib import admin
from django.db import models
from odm2testapp.models import Variables
from odm2testapp.models import CvVariabletype
from odm2testapp.models import CvVariablename
from odm2testapp.models import CvSpeciation
from odm2testapp.models import Taxonomicclassifiers
from odm2testapp.models import CvTaxonomicclassifiertype
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
from odm2testapp.models import Organizations
from odm2testapp.models import CvOrganizationtype
from odm2testapp.models import CvRelationshiptype

from django.forms import ModelChoiceField

class TermModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.term)

class VariableNameModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.variablenamecv.term)

class ActionsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.actiontypecv.term)

class OrganizationsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.organizationname)

class VariablesAdminForm(ModelForm):
    variabletypecv= TermModelChoiceField(CvVariabletype.objects.all().order_by('term'))
    variablenamecv= TermModelChoiceField(CvVariablename.objects.all().order_by('term'))
    speciationcv= TermModelChoiceField(CvSpeciation.objects.all().order_by('term'))
    class Meta:
        model=Variables
       
class VariablesAdmin(admin.ModelAdmin):
    form=VariablesAdminForm

class TaxonomicclassifiersAdminForm(ModelForm):
    taxonomicclassifiertypecv= TermModelChoiceField(CvTaxonomicclassifiertype.objects.all().order_by('term'))
    class Meta:
        model= Taxonomicclassifiers

class TaxonomicclassifiersAdmin(admin.ModelAdmin):
    form=TaxonomicclassifiersAdminForm


class SamplingfeaturesAdminForm(ModelForm):
    samplingfeaturetypecv= TermModelChoiceField(CvSamplingfeaturetype.objects.all().order_by('term'))
    samplingfeaturegeotypecv=TermModelChoiceField(CvSamplingfeaturegeotype.objects.all().order_by('term'))
    elevationdatumcv = TermModelChoiceField(CvElevationdatum.objects.all().order_by('term'))
    class Meta:
        model= Samplingfeatures

class SamplingfeaturesAdmin(admin.ModelAdmin):
    form=SamplingfeaturesAdminForm


class ResultsAdminForm(ModelForm):
    resulttypecv= TermModelChoiceField(CvResulttype.objects.all().order_by('term'))
    variableid= VariableNameModelChoiceField(Variables.objects.all().order_by('variablenamecv'))
    class Meta:
        model= Results

class ResultsAdmin(admin.ModelAdmin):
    form=ResultsAdminForm


class RelatedactionsAdminForm(ModelForm):
    actionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    relationshiptypecv= TermModelChoiceField(CvRelationshiptype.objects.all().order_by('term'))
    relatedactionid= ActionsModelChoiceField(Actions.objects.all().order_by('begindatetime'))
    class Meta:
        model= Relatedactions

class RelatedactionsAdmin(admin.ModelAdmin):
    form=RelatedactionsAdminForm

class OrganizationsAdminForm(ModelForm):
    organizationtypecv= TermModelChoiceField(CvOrganizationtype.objects.all().order_by('term'))
    #parentorganizationid = TermModelChoiceField(Organizations.objects.all().order_by('organizationname'))
    class Meta:
        model= Organizations

class OrganizationsAdmin(admin.ModelAdmin):
    form=OrganizationsAdminForm