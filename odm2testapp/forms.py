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
from django.forms import ModelChoiceField

class VariableModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%(obj.term)

class VariablesAdminForm(ModelForm):
    variabletypecv= VariableModelChoiceField(CvVariabletype.objects.all().order_by('term'))
    variablenamecv= VariableModelChoiceField(CvVariablename.objects.all().order_by('term'))
    speciationcv= VariableModelChoiceField(CvSpeciation.objects.all().order_by('term'))
    class Meta:
        model=Variables
       
class VariablesAdmin(admin.ModelAdmin):
    form=VariablesAdminForm

class TaxonomicclassifiersAdminForm(ModelForm):
    taxonomicclassifiertypecv= VariableModelChoiceField(CvTaxonomicclassifiertype.objects.all().order_by('term'))
    class Meta:
        model= Taxonomicclassifiers

class TaxonomicclassifiersAdmin(admin.ModelAdmin):
    form=TaxonomicclassifiersAdminForm


class SamplingfeaturesAdminForm(ModelForm):
    samplingfeaturetypecv= VariableModelChoiceField(CvSamplingfeaturetype.objects.all().order_by('term'))
    samplingfeaturegeotypecv=VariableModelChoiceField(CvSamplingfeaturegeotype.objects.all().order_by('term'))
    elevationdatumcv = VariableModelChoiceField(CvElevationdatum.objects.all().order_by('term'))
    class Meta:
        model= Samplingfeatures

class SamplingfeaturesAdmin(admin.ModelAdmin):
    form=SamplingfeaturesAdminForm