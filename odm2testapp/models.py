#C:\ODM2\odm2testsite\odm2testsite\templates
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib import admin
from django.utils.html import format_html
#from odm2testapp.forms import VariablesForm




class Actionannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    annotationid = models.ForeignKey('Annotations', db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'actionannotations'


class Actionby(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    affiliationid = models.ForeignKey('Affiliations', db_column='affiliationid')
    #affiliationpersonlink= models.CharField(max_length=500, blank=True)
    #Membership.objects.filter(person__name="x").select_related('person', depth=1)
    isactionlead = models.BooleanField()
    roledescription = models.CharField(max_length=500, blank=True)
    #def affiliationsForActionBy(self):
        #return self.affiliationid.objects.all().order_by('personlink')
    class Meta:
        managed = False
        db_table = 'actionby'


class Actiondirectives(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    directiveid = models.ForeignKey('Directives', db_column='directiveid')

    class Meta:
        managed = False
        db_table = 'actiondirectives'


class Actionextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    propertyid = models.ForeignKey('Extensionproperties', db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'actionextensionpropertyvalues'


class Actions(models.Model):
    actionid = models.AutoField(primary_key=True)
    actiontypecv = models.ForeignKey('CvActiontype', db_column='actiontypecv')
    methodid = models.ForeignKey('Methods', db_column='methodid')
    begindatetime = models.DateTimeField()
    begindatetimeutcoffset = models.IntegerField()
    enddatetime = models.DateTimeField(blank=True, null=True)
    enddatetimeutcoffset = models.IntegerField(blank=True, null=True)
    actiondescription = models.CharField(max_length=500, blank=True)
    actionfilelink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'actions'


class Affiliations(models.Model):
    affiliationid = models.AutoField(primary_key=True)
    personid = models.ForeignKey('People', db_column='personid')
    organizationid = models.ForeignKey('Organizations', db_column='organizationid', blank=True, null=True)
    isprimaryorganizationcontact = models.NullBooleanField()
    affiliationstartdate = models.DateField()
    affiliationenddate = models.DateField(blank=True, null=True)
    primaryphone = models.CharField(max_length=50, blank=True)
    primaryemail = models.CharField(max_length=255)
    primaryaddress = models.CharField(max_length=255, blank=True)
    personlink = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s = str(self.personlink)
        if self.primaryemail:
            s += ', {0}'.format(self.primaryemail)
        return s
    class Meta:
        managed = False
        db_table = 'affiliations'


class Annotations(models.Model):
    annotationid = models.AutoField(primary_key=True)
    annotationtypecv = models.ForeignKey('CvAnnotationtype', db_column='annotationtypecv')
    annotationcode = models.CharField(max_length=50, blank=True)
    annotationtext = models.CharField(max_length=500)
    annotationdatetime = models.DateTimeField(blank=True, null=True)
    annotationutcoffset = models.IntegerField(blank=True, null=True)
    annotationlink = models.CharField(max_length=255, blank=True)
    annotatorid = models.ForeignKey('People', db_column='annotatorid', blank=True, null=True)
    citationid = models.ForeignKey('Citations', db_column='citationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotations'


class Authorlists(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', db_column='citationid')
    personid = models.ForeignKey('People', db_column='personid')
    authororder = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'authorlists'


class Calibrationactions(models.Model):
    actionid = models.ForeignKey(Actions, db_column='actionid', primary_key=True)
    calibrationcheckvalue = models.FloatField(blank=True, null=True)
    instrumentoutputvariableid = models.ForeignKey('Instrumentoutputvariables', db_column='instrumentoutputvariableid')
    calibrationequation = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'calibrationactions'


class Calibrationreferenceequipment(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Calibrationactions, db_column='actionid')
    equipmentid = models.ForeignKey('Equipment', db_column='equipmentid')

    class Meta:
        managed = False
        db_table = 'calibrationreferenceequipment'


class Calibrationstandards(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Calibrationactions, db_column='actionid')
    referencematerialid = models.ForeignKey('Referencematerials', db_column='referencematerialid')

    class Meta:
        managed = False
        db_table = 'calibrationstandards'


class Categoricalresults(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.IntegerField(blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.IntegerField(blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.IntegerField(blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid', blank=True, null=True)
    qualitycodecv = models.ForeignKey('CvQualitycode', db_column='qualitycodecv')

    class Meta:
        managed = False
        db_table = 'categoricalresults'


class Categoricalresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Categoricalresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'categoricalresultvalueannotations'


class Categoricalresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Categoricalresults, db_column='resultid')
    datavalue = models.CharField(max_length=255)
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'categoricalresultvalues'


class Citationextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', db_column='citationid')
    propertyid = models.ForeignKey('Extensionproperties', db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'citationextensionpropertyvalues'


class Citationexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', db_column='citationid')
    externalidentifiersystemid = models.ForeignKey('Externalidentifiersystems', db_column='externalidentifiersystemid')
    citationexternalidentifer = models.CharField(max_length=255)
    citationexternalidentiferuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'citationexternalidentifiers'


class Citations(models.Model):
    citationid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publicationyear = models.IntegerField()
    citationlink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'citations'


class CvActiontype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_actiontype'


class CvAggregationstatistic(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_aggregationstatistic'


class CvAnnotationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_annotationtype'


class CvCensorcode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_censorcode'


class CvDataqualitytype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_dataqualitytype'


class CvDatasettypecv(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_datasettypecv'


class CvDirectivetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_directivetype'


class CvElevationdatum(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_elevationdatum'


class CvEquipmenttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_equipmenttype'


class CvMethodtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_methodtype'


class CvOrganizationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_organizationtype'


class CvPropertydatatype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_propertydatatype'


class CvQualitycode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_qualitycode'


class CvReferencematerialmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_referencematerialmedium'


class CvRelationshiptype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_relationshiptype'


class CvResulttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_resulttype'


class CvSampledmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_sampledmedium'


class CvSamplingfeaturegeotype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_samplingfeaturegeotype'


class CvSamplingfeaturetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_samplingfeaturetype'


class CvSitetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_sitetype'


class CvSpatialoffsettype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_spatialoffsettype'


class CvSpeciation(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_speciation'


class CvSpecimenmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_specimenmedium'


class CvSpecimentype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_specimentype'


class CvStatus(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_status'


class CvTaxonomicclassifiertype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_taxonomicclassifiertype'


class CvUnitstype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_unitstype'


class CvVariablename(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_variablename'


class CvVariabletype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return self.term
    
    class Meta:
        managed = False
        db_table = 'cv_variabletype'


class Dataloggerfilecolumns(models.Model):
    dataloggerfilecolumnid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid', blank=True, null=True)
    dataloggerfileid = models.ForeignKey('Dataloggerfiles', db_column='dataloggerfileid')
    instrumentoutputvariableid = models.ForeignKey('Instrumentoutputvariables', db_column='instrumentoutputvariableid')
    columnlabel = models.CharField(max_length=50)
    columndescription = models.CharField(max_length=500, blank=True)
    measurementequation = models.CharField(max_length=255, blank=True)
    scaninterval = models.FloatField(blank=True, null=True)
    scanintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='scanintervalunitsid', blank=True, null=True)
    recordinginterval = models.FloatField(blank=True, null=True)
    recordingintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='recordingintervalunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataloggerfilecolumns'


class Dataloggerfiles(models.Model):
    dataloggerfileid = models.AutoField(primary_key=True)
    programid = models.ForeignKey('Dataloggerprogramfiles', db_column='programid')
    dataloggerfilename = models.CharField(max_length=255)
    dataloggerfiledescription = models.CharField(max_length=500, blank=True)
    dataloggerfilelink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'dataloggerfiles'


class Dataloggerprogramfiles(models.Model):
    programid = models.AutoField(primary_key=True)
    affiliationid = models.ForeignKey(Affiliations, db_column='affiliationid')
    programname = models.CharField(max_length=255)
    programdescription = models.CharField(max_length=500, blank=True)
    programversion = models.CharField(max_length=50, blank=True)
    programfilelink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'dataloggerprogramfiles'


class Dataquality(models.Model):
    dataqualityid = models.AutoField(primary_key=True)
    dataqualitytypecv = models.ForeignKey(CvDataqualitytype, db_column='dataqualitytypecv')
    dataqualitycode = models.CharField(max_length=255)
    dataqualityvalue = models.FloatField(blank=True, null=True)
    dataqualityvalueunitsid = models.ForeignKey('Units', related_name='+', db_column='dataqualityvalueunitsid', blank=True, null=True)
    dataqualitydescription = models.CharField(max_length=500, blank=True)
    dataqualitylink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'dataquality'


class Datasetcitations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey('Datasets', db_column='datasetid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    citationid = models.ForeignKey(Citations, db_column='citationid')

    class Meta:
        managed = False
        db_table = 'datasetcitations'


class Datasets(models.Model):
    datasetid = models.AutoField(primary_key=True)
    datasetuuid = models.TextField()  # This field type is a guess.
    datasettypecv = models.ForeignKey(CvDatasettypecv, db_column='datasettypecv')
    datasetcode = models.CharField(max_length=50)
    datasettitle = models.CharField(max_length=255)
    datasetabstract = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'datasets'


class Datasetsresults(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, db_column='datasetid')
    resultid = models.ForeignKey('Results', db_column='resultid')

    class Meta:
        managed = False
        db_table = 'datasetsresults'


class Derivationequations(models.Model):
    derivationequationid = models.AutoField(primary_key=True)
    derivationequation = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'derivationequations'


class Directives(models.Model):
    directiveid = models.AutoField(primary_key=True)
    directivetypecv = models.ForeignKey(CvDirectivetype, db_column='directivetypecv')
    directivedescription = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'directives'


class Equipment(models.Model):
    equipmentid = models.AutoField(primary_key=True)
    equipmentcode = models.CharField(max_length=50)
    equipmentname = models.CharField(max_length=255)
    equipmenttypecv = models.ForeignKey(CvEquipmenttype, db_column='equipmenttypecv')
    equipmentmodelid = models.ForeignKey('Equipmentmodels', db_column='equipmentmodelid')
    equipmentserialnumber = models.CharField(max_length=50)
    equipmentownerid = models.ForeignKey('People', db_column='equipmentownerid')
    equipmentvendorid = models.ForeignKey('Organizations', db_column='equipmentvendorid')
    equipmentpurchasedate = models.DateTimeField()
    equipmentpurchaseordernumber = models.CharField(max_length=50, blank=True)
    equipmentdescription = models.CharField(max_length=500, blank=True)
    equipmentdocumentationlink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'equipment'


class Equipmentannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'equipmentannotations'


class Equipmentmodels(models.Model):
    equipmentmodelid = models.AutoField(primary_key=True)
    modelmanufacturerid = models.ForeignKey('Organizations', db_column='modelmanufacturerid')
    modelpartnumber = models.CharField(max_length=50, blank=True)
    modelname = models.CharField(max_length=255)
    modeldescription = models.CharField(max_length=500, blank=True)
    isinstrument = models.BooleanField()
    modelspecificationsfilelink = models.CharField(max_length=255, blank=True)
    modellink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'equipmentmodels'


class Equipmentused(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid')
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')

    class Meta:
        managed = False
        db_table = 'equipmentused'


class Extensionproperties(models.Model):
    propertyid = models.AutoField(primary_key=True)
    propertyname = models.CharField(max_length=255)
    propertydescription = models.CharField(max_length=500, blank=True)
    propertydatatypecv = models.ForeignKey(CvPropertydatatype, db_column='propertydatatypecv')
    propertyunitsid = models.ForeignKey('Units', related_name='+',  db_column='propertyunitsid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extensionproperties'


class Externalidentifiersystems(models.Model):
    externalidentifiersystemid = models.AutoField(primary_key=True)
    externalidentifiersystemname = models.CharField(max_length=255)
    identifiersystemorganizationid = models.ForeignKey('Organizations', db_column='identifiersystemorganizationid')
    externalidentifiersystemdescription = models.CharField(max_length=500, blank=True)
    externalidentifiersystemurl = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'externalidentifiersystems'


class Featureactions(models.Model):
    featureactionid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    actionid = models.ForeignKey(Actions, db_column='actionid')

    class Meta:
        managed = False
        db_table = 'featureactions'


class Instrumentoutputvariables(models.Model):
    instrumentoutputvariableid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey(Equipmentmodels, db_column='modelid')
    variableid = models.ForeignKey('Variables', db_column='variableid')
    instrumentmethodid = models.ForeignKey('Methods', db_column='instrumentmethodid')
    instrumentresolution = models.CharField(max_length=255, blank=True)
    instrumentaccuracy = models.CharField(max_length=255, blank=True)
    instrumentrawoutputunitsid = models.ForeignKey('Units', related_name='+',  db_column='instrumentrawoutputunitsid')

    class Meta:
        managed = False
        db_table = 'instrumentoutputvariables'


class Maintenanceactions(models.Model):
    actionid = models.ForeignKey(Actions, db_column='actionid', primary_key=True)
    isfactoryservice = models.BooleanField()
    maintenancecode = models.CharField(max_length=50, blank=True)
    maintenancereason = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'maintenanceactions'


class Measurementresults(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+',  db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+',  db_column='ylocationunitsid', blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid', blank=True, null=True)
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'measurementresults'


class Measurementresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Measurementresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'measurementresultvalueannotations'


class Measurementresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Measurementresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'measurementresultvalues'


class Methodannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'methodannotations'


class Methodcitations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    citationid = models.ForeignKey(Citations, db_column='citationid')

    class Meta:
        managed = False
        db_table = 'methodcitations'


class Methodextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'methodextensionpropertyvalues'


class Methodexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    methodexternalidentifier = models.CharField(max_length=255)
    methodexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'methodexternalidentifiers'


class Methods(models.Model):
    methodid = models.AutoField(primary_key=True)
    methodtypecv = models.ForeignKey(CvMethodtype, db_column='methodtypecv')
    methodcode = models.CharField(max_length=50)
    methodname = models.CharField(max_length=255)
    methoddescription = models.CharField(max_length=500, blank=True)
    methodlink = models.CharField(max_length=255, blank=True)
    organizationid = models.ForeignKey('Organizations', db_column='organizationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'methods'


class Modelaffiliations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey('Models', db_column='modelid')
    affiliationid = models.ForeignKey(Affiliations, db_column='affiliationid')
    isprimary = models.BooleanField()
    roledescription = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'modelaffiliations'


class Models(models.Model):
    modelid = models.AutoField(primary_key=True)
    modelcode = models.CharField(max_length=50)
    modelname = models.CharField(max_length=255)
    modeldescription = models.CharField(max_length=500, blank=True)
    version = models.CharField(max_length=255, blank=True)
    modellink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'models'


class Organizations(models.Model):
    organizationid = models.AutoField(primary_key=True)
    organizationtypecv = models.ForeignKey(CvOrganizationtype, db_column='organizationtypecv')
    organizationcode = models.CharField(max_length=50)
    organizationname = models.CharField(max_length=255)
    organizationdescription = models.CharField(max_length=500, blank=True)
    organizationlink = models.CharField(max_length=255, blank=True)
    parentorganizationid = models.ForeignKey('self', db_column='parentorganizationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organizations'


class People(models.Model):
    personid = models.AutoField(primary_key=True)
    personfirstname = models.CharField(max_length=255)
    personmiddlename = models.CharField(max_length=255, blank=True)
    personlastname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'people'


class Personexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    personid = models.ForeignKey(People, db_column='personid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    personexternalidentifier = models.CharField(max_length=255)
    personexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'personexternalidentifiers'


class Pointcoverageresults(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid', blank=True, null=True)
    intendedxspacing = models.FloatField(blank=True, null=True)
    intendedxspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedxspacingunitsid', blank=True, null=True)
    intendedyspacing = models.FloatField(blank=True, null=True)
    intendedyspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedyspacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pointcoverageresults'


class Pointcoverageresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Pointcoverageresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'pointcoverageresultvalueannotations'


class Pointcoverageresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Pointcoverageresults, db_column='resultid')
    datavalue = models.BigIntegerField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    xlocation = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid')
    ylocation = models.FloatField()
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')

    class Meta:
        managed = False
        db_table = 'pointcoverageresultvalues'


class Processinglevels(models.Model):
    processinglevelid = models.AutoField(primary_key=True)
    processinglevelcode = models.CharField(max_length=50)
    definition = models.CharField(max_length=500, blank=True)
    explanation = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'processinglevels'


class Profileresults(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid', blank=True, null=True)
    intendedzspacing = models.FloatField(blank=True, null=True)
    intendedzspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedzspacingunitsid', blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtimespacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'profileresults'


class Profileresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Profileresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'profileresultvalueannotations'


class Profileresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Profileresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    zlocation = models.FloatField()
    zaggregationinterval = models.FloatField()
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'profileresultvalues'


class Referencematerialexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    referencematerialid = models.ForeignKey('Referencematerials', db_column='referencematerialid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    referencematerialexternalidentifier = models.CharField(max_length=255)
    referencematerialexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'referencematerialexternalidentifiers'


class Referencematerials(models.Model):
    referencematerialid = models.AutoField(primary_key=True)
    referencematerialmediumcv = models.ForeignKey(CvReferencematerialmedium, db_column='referencematerialmediumcv')
    referencematerialorganizationid = models.ForeignKey(Organizations, db_column='referencematerialorganizationid')
    referencematerialcode = models.CharField(max_length=50)
    referencemateriallotcode = models.CharField(max_length=255, blank=True)
    referencematerialpurchasedate = models.DateTimeField(blank=True, null=True)
    referencematerialexpirationdate = models.DateTimeField(blank=True, null=True)
    referencematerialcertificatelink = models.CharField(max_length=255, blank=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referencematerials'


class Referencematerialvalues(models.Model):
    referencematerialvalueid = models.AutoField(primary_key=True)
    referencematerialid = models.ForeignKey(Referencematerials, db_column='referencematerialid')
    referencematerialvalue = models.FloatField()
    referencematerialaccuracy = models.FloatField(blank=True, null=True)
    variableid = models.ForeignKey('Variables', db_column='variableid')
    unitsid = models.ForeignKey('Units', related_name='+', db_column='unitsid')
    citationid = models.ForeignKey(Citations, db_column='citationid')

    class Meta:
        managed = False
        db_table = 'referencematerialvalues'


class Relatedactions(models.Model):
    relationid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedactionid = models.ForeignKey(Actions, related_name='Related actions',db_column='relatedactionid')

    class Meta:
        managed = False
        db_table = 'relatedactions'


class Relatedannotations(models.Model):
    relationid = models.AutoField(primary_key=True)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedannotationid = models.ForeignKey(Annotations,related_name='Related annotations', db_column='relatedannotationid')

    class Meta:
        managed = False
        db_table = 'relatedannotations'


class Relatedcitations(models.Model):
    relationid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey(Citations, db_column='citationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedcitationid = models.ForeignKey(Citations,related_name='Related citations', db_column='relatedcitationid')

    class Meta:
        managed = False
        db_table = 'relatedcitations'


class Relateddatasets(models.Model):
    relationid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, db_column='datasetid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relateddatasetid = models.ForeignKey(Datasets, related_name='related dataset',db_column='relateddatasetid')
    versioncode = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = 'relateddatasets'


class Relatedequipment(models.Model):
    relationid = models.AutoField(primary_key=True)
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedequipmentid = models.ForeignKey(Equipment, related_name='Related equipment', db_column='relatedequipmentid')
    relationshipstartdatetime = models.DateTimeField()
    relationshipstartdatetimeutcoffset = models.IntegerField()
    relationshipenddatetime = models.DateTimeField(blank=True, null=True)
    relationshipenddatetimeutcoffset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatedequipment'


class Relatedfeatures(models.Model):
    relationid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedfeatureid = models.ForeignKey('Samplingfeatures', related_name='Related features', db_column='relatedfeatureid')
    spatialoffsetid = models.ForeignKey('Spatialoffsets', db_column='spatialoffsetid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatedfeatures'


class Relatedmodels(models.Model):
    relatedid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey(Models, db_column='modelid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedmodelid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'relatedmodels'


class Relatedresults(models.Model):
    relationid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedresultid = models.ForeignKey('Results', related_name='related result', db_column='relatedresultid')
    versioncode = models.CharField(max_length=50, blank=True)
    relatedresultsequencenumber = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatedresults'


class Resultannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')
    begindatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'resultannotations'


class Resultderivationequations(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    derivationequationid = models.ForeignKey(Derivationequations, db_column='derivationequationid')

    class Meta:
        managed = False
        db_table = 'resultderivationequations'


class Resultextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'resultextensionpropertyvalues'


class Resultnormalizationvalues(models.Model):
    resultid = models.ForeignKey('Results', db_column='resultid', primary_key=True)
    normalizedbyreferencematerialvalueid = models.ForeignKey(Referencematerialvalues, db_column='normalizedbyreferencematerialvalueid')

    class Meta:
        managed = False
        db_table = 'resultnormalizationvalues'


class Results(models.Model):
    resultid = models.AutoField(primary_key=True)
    resultuuid = models.TextField()  # This field type is a guess.
    featureactionid = models.ForeignKey(Featureactions, db_column='featureactionid')
    resulttypecv = models.ForeignKey(CvResulttype, db_column='resulttypecv')
    variableid = models.ForeignKey('Variables', db_column='variableid')
    unitsid = models.ForeignKey('Units', related_name='+', db_column='unitsid')
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers', db_column='taxonomicclassifierid', blank=True, null=True)
    processinglevelid = models.ForeignKey(Processinglevels, db_column='processinglevelid')
    resultdatetime = models.DateTimeField(blank=True, null=True)
    resultdatetimeutcoffset = models.BigIntegerField(blank=True, null=True)
    validdatetime = models.DateTimeField(blank=True, null=True)
    validdatetimeutcoffset = models.BigIntegerField(blank=True, null=True)
    statuscv = models.ForeignKey(CvStatus, db_column='statuscv', blank=True, null=True)
    sampledmediumcv = models.ForeignKey(CvSampledmedium, db_column='sampledmediumcv')
    valuecount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'results'


class Resultsdataquality(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Results, db_column='resultid')
    dataqualityid = models.ForeignKey(Dataquality, db_column='dataqualityid')

    class Meta:
        managed = False
        db_table = 'resultsdataquality'


class Samplingfeatureannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'samplingfeatureannotations'


class Samplingfeatureextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'samplingfeatureextensionpropertyvalues'


class Samplingfeatureexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    samplingfeatureexternalidentifier = models.CharField(max_length=255)
    samplingfeatureexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'samplingfeatureexternalidentifiers'


class Samplingfeatures(models.Model):
    samplingfeatureid = models.AutoField(primary_key=True)
    samplingfeatureuuid = models.TextField()  # This field type is a guess.
    samplingfeaturetypecv = models.ForeignKey(CvSamplingfeaturetype, db_column='samplingfeaturetypecv')
    samplingfeaturecode = models.CharField(max_length=50)
    samplingfeaturename = models.CharField(max_length=255, blank=True)
    samplingfeaturedescription = models.CharField(max_length=500, blank=True)
    samplingfeaturegeotypecv = models.ForeignKey(CvSamplingfeaturegeotype, db_column='samplingfeaturegeotypecv', blank=True, null=True)
    featuregeometry = models.TextField(blank=True)  # This field type is a guess.
    elevation_m = models.FloatField(blank=True, null=True)
    elevationdatumcv = models.ForeignKey(CvElevationdatum, db_column='elevationdatumcv', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'samplingfeatures'


class Sectionresults(models.Model):
    resultid = models.ForeignKey(Results, db_column='resultid', primary_key=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid', blank=True, null=True)
    intendedxspacing = models.FloatField(blank=True, null=True)
    intendedxspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedxspacingunitsid', blank=True, null=True)
    intendedzspacing = models.FloatField(blank=True, null=True)
    intendedzspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedzspacingunitsid', blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtimespacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'sectionresults'


class Sectionresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Sectionresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'sectionresultvalueannotations'


class Sectionresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Sectionresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.BigIntegerField()
    valuedatetimeutcoffset = models.BigIntegerField()
    xlocation = models.FloatField()
    xaggregationinterval = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid')
    zlocation = models.BigIntegerField()
    zaggregationinterval = models.FloatField()
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'sectionresultvalues'


class Simulations(models.Model):
    simulationid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid')
    simulationname = models.CharField(max_length=255)
    simulationdescription = models.CharField(max_length=500, blank=True)
    simulationstartdatetime = models.DateTimeField()
    simulationstartdatetimeutcoffset = models.IntegerField()
    simulationenddatetime = models.DateTimeField()
    simulationenddatetimeutcoffset = models.IntegerField()
    timestepvalue = models.FloatField()
    timestepunitsid = models.IntegerField()
    inputdatasetid = models.IntegerField(blank=True, null=True)
    modelid = models.ForeignKey(Models, db_column='modelid')

    class Meta:
        managed = False
        db_table = 'simulations'


class Sites(models.Model):
    samplingfeatureid = models.ForeignKey(Samplingfeatures, db_column='samplingfeatureid', primary_key=True)
    sitetypecv = models.ForeignKey(CvSitetype, db_column='sitetypecv')
    latitude = models.FloatField()
    longitude = models.FloatField()
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid')

    class Meta:
        managed = False
        db_table = 'sites'


class Spatialoffsets(models.Model):
    spatialoffsetid = models.AutoField(primary_key=True)
    spatialoffsettypecv = models.ForeignKey(CvSpatialoffsettype, db_column='spatialoffsettypecv')
    offset1value = models.FloatField()
    offset1unitid = models.ForeignKey('Units', related_name='+', db_column='offset1unitid')
    offset2value = models.FloatField(blank=True, null=True)
    offset2unitid = models.ForeignKey('Units', related_name='+', db_column='offset2unitid', blank=True, null=True)
    offset3value = models.FloatField(blank=True, null=True)
    offset3unitid = models.ForeignKey('Units', related_name='+', db_column='offset3unitid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatialoffsets'


class Spatialreferenceexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    spatialreferenceexternalidentifier = models.CharField(max_length=255)
    spatialreferenceexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'spatialreferenceexternalidentifiers'


class Spatialreferences(models.Model):
    spatialreferenceid = models.AutoField(primary_key=True)
    srscode = models.CharField(max_length=50, blank=True)
    srsname = models.CharField(max_length=255)
    srsdescription = models.CharField(max_length=500, blank=True)
    srslink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'spatialreferences'


class Specimenbatchpostions(models.Model):
    featureactionid = models.ForeignKey(Featureactions, db_column='featureactionid', primary_key=True)
    batchpositionnumber = models.IntegerField()
    batchpositionlabel = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'specimenbatchpostions'


class Specimens(models.Model):
    samplingfeatureid = models.ForeignKey(Samplingfeatures, db_column='samplingfeatureid', primary_key=True)
    specimentypecv = models.ForeignKey(CvSpecimentype, db_column='specimentypecv')
    specimenmediumcv = models.ForeignKey(CvSpecimenmedium, db_column='specimenmediumcv')
    isfieldspecimen = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'specimens'


class Specimentaxonomicclassifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey(Specimens, db_column='samplingfeatureid')
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers', db_column='taxonomicclassifierid')
    citationid = models.ForeignKey(Citations, db_column='citationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'specimentaxonomicclassifiers'


class Spectraresults(models.Model):
    resultid = models.ForeignKey(Results, db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid', blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid', blank=True, null=True)
    intendedwavelengthspacing = models.FloatField(blank=True, null=True)
    intendedwavelengthspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedwavelengthspacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'spectraresults'


class Spectraresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Spectraresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'spectraresultvalueannotations'


class Spectraresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Spectraresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    excitationwavelength = models.FloatField()
    emissionwavelength = models.FloatField()
    wavelengthunitsid = models.ForeignKey('Units', related_name='+', db_column='wavelengthunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'spectraresultvalues'


class Taxonomicclassifierexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers', db_column='taxonomicclassifierid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    taxonomicclassifierexternalidentifier = models.CharField(max_length=255)
    taxonomicclassifierexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'taxonomicclassifierexternalidentifiers'


class Taxonomicclassifiers(models.Model):
    taxonomicclassifierid = models.AutoField(primary_key=True)
    taxonomicclassifiertypecv = models.ForeignKey(CvTaxonomicclassifiertype, db_column='taxonomicclassifiertypecv')
    taxonomicclassifiername = models.CharField(max_length=255)
    taxonomicclassifiercommonname = models.CharField(max_length=255, blank=True)
    taxonomicclassifierdescription = models.CharField(max_length=500, blank=True)
    parenttaxonomicclassifierid = models.ForeignKey('self', db_column='parenttaxonomicclassifierid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxonomicclassifiers'


class Timeseriesresults(models.Model):
    resultid = models.ForeignKey(Results, db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid', blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid', blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtimespacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'timeseriesresults'


class Timeseriesresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Timeseriesresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'timeseriesresultvalueannotations'


class Timeseriesresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Timeseriesresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'timeseriesresultvalues'


class Trajectoryresults(models.Model):
    resultid = models.ForeignKey(Results, db_column='resultid', primary_key=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid', blank=True, null=True)
    intendedtrajectoryspacing = models.FloatField(blank=True, null=True)
    intendedtrajectoryspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtrajectoryspacingunitsid', blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtimespacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'trajectoryresults'


class Trajectoryresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Trajectoryresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'trajectoryresultvalueannotations'


class Trajectoryresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Trajectoryresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    xlocation = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid')
    ylocation = models.FloatField()
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid')
    zlocation = models.FloatField()
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid')
    trajectorydistance = models.FloatField()
    trajectorydistanceaggregationinterval = models.FloatField()
    trajectorydistanceunitsid = models.ForeignKey('Units', related_name='+', db_column='trajectorydistanceunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'trajectoryresultvalues'


class Transectresults(models.Model):
    resultid = models.ForeignKey(Results, db_column='resultid', primary_key=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid', blank=True, null=True)
    intendedtransectspacing = models.FloatField(blank=True, null=True)
    intendedtransectspacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtransectspacingunitsid', blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+', db_column='intendedtimespacingunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = 'transectresults'


class Transectresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Transectresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'transectresultvalueannotations'


class Transectresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Transectresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.DateTimeField()
    xlocation = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid')
    ylocation = models.FloatField()
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid')
    transectdistance = models.FloatField()
    transectdistanceaggregationinterval = models.FloatField()
    transectdistanceunitsid = models.ForeignKey('Units', related_name='+', db_column='transectdistanceunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+', db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = 'transectresultvalues'


class Units(models.Model):
    unitsid = models.AutoField(primary_key=True)
    unitstypecv = models.ForeignKey(CvUnitstype, db_column='unitstypecv')
    unitsabbreviation = models.CharField(max_length=50)
    unitsname = models.CharField(max_length=255)
    unitslink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'units'


class Variableextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'variableextensionpropertyvalues'


class Variableexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems, db_column='externalidentifiersystemid')
    variableexternalidentifer = models.CharField(max_length=255)
    variableexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'variableexternalidentifiers'



class Variables(models.Model):
    #form = VariablesForm
    variableid = models.AutoField(primary_key=True)
    variabletypecv = models.ForeignKey(CvVariabletype, db_column='variabletypecv')
    #variabletypecv = models.ModelChoiceField(CvVariabletype, db_column='variabletypecv')
    variablecode = models.CharField(max_length=50)
    variablenamecv = models.ForeignKey(CvVariablename, db_column='variablenamecv')
    variabledefinition = models.CharField(max_length=500, blank=True)
    speciationcv = models.ForeignKey(CvSpeciation, db_column='speciationcv', blank=True, null=True)
    nodatavalue = models.FloatField()



    class Meta:
        managed = False
        db_table = 'variables'
    