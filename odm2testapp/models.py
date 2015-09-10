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
from uuidfield import UUIDField
from django.db import models
from odm2testsite.settings import MEDIA_ROOT
#from django.contrib.gis.db import models
import csv
import io
import binascii
import unicodedata
from io import TextIOWrapper
from django.conf import settings
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
import time
#from django.forms import ModelFormWithFileField
#from .forms import DataloggerprogramfilesAdminForm
#from odm2testapp.forms import VariablesForm
from odm2testsite.settings import MEDIA_ROOT
#from django.contrib.gis.db import models
import csv
import io
import binascii
import unicodedata
from io import TextIOWrapper
from django.core.exceptions import ValidationError
import itertools
from django.utils.translation import ugettext as _

def handle_uploaded_file(f,id):
    destination = io.open(MEDIA_ROOT + '/resultvalues/' + f.name +'.csv', 'wb+')
    # data = open(f)
    for chunk in f.chunks():

        destination.write(chunk)
        #Measurementresultvalues

    destination.close()
    try:
        with io.open(MEDIA_ROOT + '/resultvalues/' + f.name +'.csv', 'rt', encoding='ascii') as f:
            reader = csv.reader(f)
            for row in reader:
                #raise ValidationError(row) #print the current row
                dateT = time.strptime(row[0],"%m/%d/%Y %H:%M")#'1/1/2013 0:10
                datestr = time.strftime("%Y-%m-%d %H:%M",dateT)
                Measurementresultvalues(resultid=id,datavalue=row[1],valuedatetime=datestr,valuedatetimeutcoffset=4).save()
    except IndexError:
        raise ValidationError('encountered a problem with row '+row)

def process_datalogger_file(f,fileid):
    try:
        with io.open(MEDIA_ROOT +  f.name , 'rt', encoding='ascii') as f:
            #reader = csv.reader(f)
            reader, reader2 = itertools.tee(csv.reader(f))
            columnsinCSV = len(next(reader2))
            rowColumnMap = list()
            DataloggerfilecolumnSet = Dataloggerfilecolumns.objects.filter(dataloggerfileid=fileid.dataloggerfileid)
            i=0
            numCols=DataloggerfilecolumnSet.count()
            if numCols == 0:
                raise ValidationError(_('This file has no dataloggerfilecolumns associated with it. '), code='noDataloggerfilecolumns')
            if not numCols == columnsinCSV:
                 raise ValidationError(_('The number of columns in the '+ str(columnsinCSV) +' csv file do not match the number of'+
                                       ' dataloggerfilecolumns '+ str(numCols) + ' associated with the dataloggerfile in the database. '), code='ColumnMisMatch')
            for row in reader:
                #map the column objects to the column in the file assumes first row in file contains columnlabel.
                if i==0:

                    for dloggerfileColumns in DataloggerfilecolumnSet:
                        foundColumn=False
                        for j in range(numCols):
                            #raise ValidationError(" in file " + row[j] + " in obj column label "+dloggerfileColumns.columnlabel)
                            if row[j] == dloggerfileColumns.columnlabel:
                                foundColumn=True
                                dloggerfileColumns.columnnum = j
                                rowColumnMap += [dloggerfileColumns]
                        if not foundColumn:
                             raise ValidationError(_('Cannot find a column in the CSV matching the dataloggerfilecolumn '+
                                                     str(dloggerfileColumns.columnlabel) ), code='ColumnMisMatch')
                        #if you didn't find a matching name for this column amoung the dloggerfileColumns raise error

                else:

                    #assume date is first column for the moment
                    dateT = time.strptime(row[0],"%m/%d/%Y %H:%M")#'1/1/2013 0:10
                    datestr = time.strftime("%Y-%m-%d %H:%M",dateT)
                    #for each column in the data table
                    #raise ValidationError("".join(str(rowColumnMap)))
                    for colnum in rowColumnMap:
                        #x[0] for x in my_tuples
                        #colnum[0] = column number, colnum[1] = dataloggerfilecolumn object

                        if not colnum.columnnum ==0:
                            #raise ValidationError("result: " + str(colnum.resultid) + " datavalue "+
                                                  #str(row[colnum.columnnum])+ " dateTime " + datestr)
                            #thisresultid = colnum.resultid #result.values('resultid')

                            measurementresult = Measurementresults.objects.filter(resultid= colnum.resultid)
                            if  measurementresult.count() == 0:
                                raise ValidationError(_('No Measurement results for column ' + colnum.columnlabel + ' Add measurement results for'+
                                                  'each column ' ))
                            #only one measurement result is allowed per result
                            for mresults in measurementresult:
                                Measurementresultvalues(resultid=mresults
                                        ,datavalue=row[colnum.columnnum],
                                        valuedatetime=datestr,valuedatetimeutcoffset=4).save()

                            #row[0] is this column object
                i+=1

                #read columns Add measurement result values for each column
                #dateT = time.strptime(row[0],"%m/%d/%Y %H:%M")#'1/1/2013 0:10
                #datestr = time.strftime("%Y-%m-%d %H:%M",dateT)
                #Measurementresultvalues(resultid=programid,datavalue=row[1],valuedatetime=datestr,valuedatetimeutcoffset=4).save()
    except IndexError:
        raise ValidationError('encountered a problem with row '+row)



class Actionannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    annotationid = models.ForeignKey('Annotations', db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'actionannotations'


class Actionby(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions',verbose_name="action", db_column='actionid')
    affiliationid = models.ForeignKey('Affiliations',verbose_name="person by affiliation", db_column='affiliationid')
    isactionlead = models.BooleanField(verbose_name="is lead person on action")
    roledescription = models.CharField(max_length=500,verbose_name="person's role on this action", blank=True)
    #def affiliationsForActionBy(self):
        #return self.affiliationid.objects.all().order_by('personlink')
    def __str__(self):
        s = str(self.actionid)
        if self.affiliationid:
            s += '- {0}'.format(self.affiliationid)
        if self.roledescription:
            s += '- {0},'.format(self.roledescription)
        return s
    class Meta:
        managed = False
        db_table = 'actionby'
        verbose_name='action by'
        verbose_name_plural='action by'


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
    action_type = models.ForeignKey('CvActiontype',
            help_text= "A vocabulary for describing the type of actions performed in making observations. Depending" +
            " on the action type, the action may or may not produce an observation result. view action type "+
            "details here http://vocabulary.odm2.org/actiontype/",db_column='actiontypecv')
    method = models.ForeignKey('Methods', db_column='methodid')
    begindatetime = models.DateTimeField(verbose_name='begin date time')
    begindatetimeutcoffset = models.IntegerField(verbose_name='begin date time clock off set (from GMT)', default=4)
    enddatetime = models.DateTimeField(verbose_name='end date time',blank=True, null=True)
    enddatetimeutcoffset = models.IntegerField(verbose_name='end date time clock off set (from GMT)', default=4)
    actiondescription = models.CharField(verbose_name='action description',max_length=500, blank=True)
    actionfilelink = models.CharField(verbose_name='action file link',max_length=255, blank=True)
    def __str__(self):
        s = str(self.action_type)
        if self.method:
           s += '- {0},'.format(self.method)
        #if self.actiondescription:
            #s += '- {0},'.format(self.actiondescription)
        return s
    class Meta:
        managed = False
        db_table = 'actions'
        verbose_name='action'


class Affiliations(models.Model):
    affiliationid = models.AutoField(primary_key=True)
    personid = models.ForeignKey('People', verbose_name='person', db_column='personid')
    organizationid = models.ForeignKey('Organizations', verbose_name='organization', db_column='organizationid', blank=True, null=True)
    isprimaryorganizationcontact = models.NullBooleanField(verbose_name='primary organization contact? ')
    affiliationstartdate = models.DateField(verbose_name="When affiliation began ")
    affiliationenddate = models.DateField(verbose_name="When affiliation ended",blank=True, null=True)
    primaryphone = models.CharField(verbose_name="primary phone",max_length=50, blank=True)
    primaryemail = models.CharField(verbose_name="primary email",max_length=255)
    primaryaddress = models.CharField(verbose_name="primary address", max_length=255, blank=True)
    personlink = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s = str(self.personid)
        if self.organizationid:
            s += '- {0},'.format(self.organizationid)
        return s
    class Meta:
        managed = False
        db_table = 'affiliations'
        verbose_name='affiliation (relate people and organizations)'
        verbose_name_plural='affiliation (relate people and organizations)'


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
        ordering = ['title']


class CvActiontype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s = str(self.term)
        if self.name:
            s += ' - {0}'.format(self.name)
        #if self.definition:
        #    s += ' - {0},'.format(self.definition)
        return s
    class Meta:
        managed = False
        db_table = 'cv_actiontype'
        ordering = ['term','name']


class CvAggregationstatistic(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0}'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_aggregationstatistic'
        ordering = ['term','name']



class CvAnnotationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_annotationtype'
        ordering = ['term','name']


class CvCensorcode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0}'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_censorcode'
        ordering = ['term','name']



class CvDataqualitytype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_dataqualitytype'
        ordering = ['term','name']


class CvDatasettypecv(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_datasettypecv'
        ordering = ['term','name']


class CvDirectivetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_directivetype'
        ordering = ['term','name']


class CvElevationdatum(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_elevationdatum'
        verbose_name='elevation datum'
        ordering = ['term','name']


class CvEquipmenttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_equipmenttype'
        ordering = ['term','name']


class CvMethodtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0}'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_methodtype'
        ordering = ['term','name']


class CvOrganizationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0}'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_organizationtype'
        ordering = ['term','name']


class CvPropertydatatype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_propertydatatype'
        ordering = ['term','name']


class CvQualitycode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0}'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_qualitycode'
        ordering = ['term','name']



class CvReferencematerialmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_referencematerialmedium'
        ordering = ['term','name']


class CvRelationshiptype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_relationshiptype'
        ordering = ['term','name']


class CvResulttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_resulttype'
        ordering = ['term','name']


class CvMedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_medium'
        ordering = ['term','name']



class CvSamplingfeaturegeotype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_samplingfeaturegeotype'
        verbose_name='sampling feature geo type'
        ordering = ['term','name']


class CvSamplingfeaturetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_samplingfeaturetype'
        verbose_name='sampling feature type'
        ordering = ['term','name']


class CvSitetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_sitetype'
        ordering = ['term','name']


class CvSpatialoffsettype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'cv_spatialoffsettype'
        ordering = ['term','name']


class CvSpeciation(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_speciation'
        ordering = ['term','name']


class CvSpecimenmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_specimenmedium'
        ordering = ['term','name']


class CvSpecimentype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_specimentype'
        ordering = ['term','name']


class CvStatus(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_status'
        ordering = ['term','name']


class CvTaxonomicclassifiertype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_taxonomicclassifiertype'
        ordering = ['term','name']
        verbose_name="taxonomic classifier"


class CvUnitstype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_unitstype'
        ordering = ['term','name']


class CvVariablename(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s
    class Meta:
        managed = False
        db_table = 'cv_variablename'
        ordering = ['term','name']



class CvVariabletype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        s=str(self.term)
        s += '- {0},'.format(self.name)
        return s

    class Meta:
        managed = False
        db_table = 'cv_variabletype'
        ordering = ['term','name']


class Dataloggerfilecolumns(models.Model):
    dataloggerfilecolumnid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results',verbose_name="result", db_column='resultid', blank=True, null=True)
    dataloggerfileid = models.ForeignKey('Dataloggerfiles', verbose_name="data logger file", db_column='dataloggerfileid')
    instrumentoutputvariableid = models.ForeignKey('Instrumentoutputvariables',
                                verbose_name="instrument output variable", db_column='instrumentoutputvariableid')
    columnlabel = models.CharField(verbose_name="column label", max_length=50)
    columndescription = models.CharField(verbose_name = "column description", max_length=500, blank=True)
    measurementequation = models.CharField(verbose_name="measurement equation", max_length=255, blank=True)
    scaninterval = models.FloatField(verbose_name="scan interval (time)", blank=True, null=True)
    scanintervalunitsid = models.ForeignKey('Units', verbose_name="scan interval units",
                    related_name='relatedScanIntervalUnitsid', db_column='scanintervalunitsid', blank=True, null=True)
    recordinginterval = models.FloatField(verbose_name="recording interval",blank=True, null=True)
    recordingintervalunitsid = models.ForeignKey('Units',verbose_name="recording interval units",
    related_name='relatedRecordingintervalunitsid', db_column='recordingintervalunitsid', blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, verbose_name="aggregation statistic",
                                               db_column='aggregationstatisticcv', blank=True, null=True)
    def __str__(self):
        s=str(self.dataloggerfileid)
        s += '- {0},'.format(self.columnlabel)
        s += '- {0},'.format(self.columndescription)
        s += '- {0},'.format(self.resultid)
        return s
    class Meta:
        managed = False
        db_table = 'dataloggerfilecolumns'
        verbose_name='data logger file column'


class Dataloggerfiles(models.Model):
    dataloggerfileid = models.AutoField(primary_key=True)
    programid = models.ForeignKey('Dataloggerprogramfiles', db_column='programid')
    dataloggerfilename = models.CharField(max_length=255)
    dataloggerfiledescription = models.CharField(max_length=500, blank=True)
    #dataloggerfilelink = models.CharField(max_length=255, blank=True)
    dataloggerfilelink = models.FileField(upload_to='dataloggerfiles') #upload_to='.'
    def __str__(self):
        s=str(self.dataloggerfilename)
        return s
    class Meta:
        managed = False
        db_table = 'dataloggerfiles'
        verbose_name='data logger file'



class ProcessDataloggerfile(models.Model):
    processdataloggerfileid = models.AutoField(primary_key=True)
    dataloggerfileid = models.ForeignKey('dataloggerfiles',help_text="CAUTION dataloggerfilecolumns must be setup" +
                                         ", the date and time stamp is expected to be the first column, "+
                                         " column names are expected to be in first row only and must match "+
                                         "the column name in associated dataloggerfilecolumns. Data begins on row 2.",
                                         verbose_name='data logger file', db_column='dataloggerfileid')
    processingCode = models.CharField(max_length=255, verbose_name='processing code', default="0")
    date_processed = models.DateTimeField(auto_now=True)
    def __str__(self):
        s=str(self.dataloggerfileid)
        s += '- Processed on  {0}'.format(self.date_processed)
        return s
    class Meta:
        managed = True
        db_table = 'processdataloggerfile'
        verbose_name= 'process data logger file'
    def save(self, *args, **kwargs):
        process_datalogger_file(self.dataloggerfileid.dataloggerfilelink,self.dataloggerfileid)
        super(ProcessDataloggerfile, self).save(*args, **kwargs)
    # def get_actions(self, request):
    #     #Disable delete
    #     actions = super(ProcessDataloggerfile, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions
    # def has_delete_permission(self, request, obj=None):
    #     return False


class Dataloggerprogramfiles(models.Model):
    programid = models.AutoField(primary_key=True)
    affiliationid = models.ForeignKey(Affiliations, db_column='affiliationid')
    programname = models.CharField(max_length=255)
    programdescription = models.CharField(max_length=500, blank=True)
    programversion = models.CharField(max_length=50, blank=True)
    #programfilelink = models.CharField(max_length=255, blank=True)
    programfilelink = models.FileField(upload_to='dataloggerprogramfiles') #+ '/' + programname.__str__() settings.MEDIA_ROOT upload_to='/upfiles/'
    def __str__(self):
        s=str(self.programname)
        s += '- Version {0}'.format(self.programversion)
        return s
    class Meta:
        managed = False
        db_table = 'dataloggerprogramfiles'
        verbose_name= 'data logger program file'



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
    datasetuuid = UUIDField(auto=True)
    datasettypecv = models.ForeignKey(CvDatasettypecv, verbose_name="dataset type", db_column='datasettypecv')
    datasetcode = models.CharField(verbose_name="dataset code", max_length=50)
    datasettitle = models.CharField(verbose_name="dataset title", max_length=255)
    datasetabstract = models.CharField(verbose_name = "dataset abstract", max_length=500)
    def __str__(self):
        s = str(self.datasetcode)
        if self.datasettitle:
            s += ' - {0}'.format(self.datasettitle)
        return s
    class Meta:
        managed = False
        db_table = 'datasets'
        verbose_name= 'dataset'


class Datasetsresults(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, verbose_name="dataset",db_column='datasetid')
    resultid = models.ForeignKey('Results',verbose_name="add the dataset to the result", db_column='resultid')
    def __str__(self):
        s = str(self.datasetid)
        if self.resultid:
            s += ' - {0}'.format(self.resultid)
        return s
    class Meta:
        managed = False
        db_table = 'datasetsresults'
        verbose_name='dataset result'


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
    modelmanufacturerid = models.ForeignKey('Organizations', verbose_name="model manufacturer",
                                            db_column='modelmanufacturerid')
    modelpartnumber = models.CharField(max_length=50, blank=True, verbose_name="model part number")
    modelname = models.CharField(max_length=255, verbose_name="model name")
    modeldescription = models.CharField(max_length=500, blank=True,null=True, verbose_name="model description")
    isinstrument = models.BooleanField(verbose_name="Is this an instrument?")
    modelspecificationsfilelink = models.CharField(max_length=255,
                                verbose_name="link to manual for equipment", blank=True)
    modellink = models.CharField(max_length=255, verbose_name="link to website for model", blank=True)
    def __str__(self):
        s=str(self.modelname)
        if self.modelpartnumber:
            s += '- {0}'.format(self.modelpartnumber)
        return s
    class Meta:
        managed = False
        db_table = 'equipmentmodels'
        verbose_name="equipment model"


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
    sampling_feature = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    action = models.ForeignKey(Actions, db_column='actionid')
    def __str__(self):
        s=str(self.sampling_feature)
        s += '- {0}'.format(self.action)
        return s
    class Meta:
        managed = False
        db_table = 'featureactions'
        verbose_name='sampling feature action (link sampling features and actions)'
        verbose_name_plural='sampling feature action (link sampling features and actions)'


class Instrumentoutputvariables(models.Model):
    instrumentoutputvariableid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey(Equipmentmodels,verbose_name="equipment model", db_column='modelid')
    variableid = models.ForeignKey('Variables',verbose_name="variable", db_column='variableid')
    instrumentmethodid = models.ForeignKey('Methods',verbose_name="instrument method", db_column='instrumentmethodid')
    instrumentresolution = models.CharField(max_length=255, verbose_name="instrument resolution", blank=True)
    instrumentaccuracy = models.CharField(max_length=255, verbose_name="instrument accuracy", blank=True)
    instrumentrawoutputunitsid = models.ForeignKey('Units', related_name='+',verbose_name="instrument raw output unit",
                                                   db_column='instrumentrawoutputunitsid')
    def __str__(self):
        s=str(self.modelid)
        s += '- {0}'.format(self.variableid)
        return s
    class Meta:
        managed = False
        db_table = 'instrumentoutputvariables'
        verbose_name="instrument output variable"


class Maintenanceactions(models.Model):
    actionid = models.ForeignKey(Actions, db_column='actionid', primary_key=True)
    isfactoryservice = models.BooleanField()
    maintenancecode = models.CharField(max_length=50, blank=True)
    maintenancereason = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'maintenanceactions'


class Measurementresults(models.Model):
    resultid = models.ForeignKey('Results', verbose_name="Result Series",db_column='resultid', primary_key=True)
    xlocation = models.FloatField(verbose_name="x location",blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units',verbose_name="x location units", related_name='relatedXlocationUnits',  db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True,verbose_name="y location", null=True)
    ylocationunitsid = models.ForeignKey('Units',verbose_name="y location units", related_name='relatedYlocationUnits',  db_column='ylocationunitsid', blank=True, null=True)
    zlocation = models.FloatField(blank=True, verbose_name="z location", null=True)
    zlocationunitsid = models.ForeignKey('Units', verbose_name="z location units",related_name='relatedZlocationUnits', db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', verbose_name="spatial reference", db_column='spatialreferenceid', blank=True, null=True)
    censorcodecv = models.ForeignKey(CvCensorcode, verbose_name="censor code", db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, verbose_name="quality code", db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic, verbose_name="aggregation statistic", db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField(verbose_name="time aggregation interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units',verbose_name="time aggregation interval unit", related_name='+', db_column='timeaggregationintervalunitsid')
    def __str__(self):
        s=str(self.resultid)
        s += '- {0}'.format(self.qualitycodecv)
        return s
    class Meta:
        managed = False
        db_table = 'measurementresults'
        ordering = ['censorcodecv','resultid']
        verbose_name='measurement result'


class Measurementresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Measurementresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = 'measurementresultvalueannotations'

import re
class Measurementresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Measurementresults, verbose_name='result',db_column='resultid')
    datavalue = models.FloatField(verbose_name='data value')
    valuedatetime = models.DateTimeField(verbose_name='value date time')
    valuedatetimeutcoffset = models.IntegerField(verbose_name='value date time UTC offset', default=4)
    def __str__(self):
        s=str(self.resultid)
        s += '- {0}'.format(str(self.datavalue))
        s += '- {0}'.format(self.valuedatetime)
        return s
    def csvoutput(self):
        s = str(self.valueid)
        s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        #temp = str(self.resultid).translate(' ', ',')
        temp = re.sub('[,]', '', str(self.resultid))
        s += ', {0} \n'.format(temp)
        return s
    class Meta:
        managed = False
        db_table = 'measurementresultvalues'
        verbose_name='measurement result value'




class MeasurementresultvalueFile(models.Model):
    valueFileid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Measurementresults, verbose_name='result',db_column='resultid')
    valueFile = models.FileField(upload_to='resultvalues', verbose_name="value file ")
    def __str__(self):
        s=str(self.resultid)
        return s
    class Meta:
        db_table = 'Measurementresultvaluefile'
        verbose_name='measurement result value file'
    def save(self, *args, **kwargs):
        handle_uploaded_file(self.valueFile.file,self.resultid)
        super(MeasurementresultvalueFile, self).save(*args, **kwargs)


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
    methodtypecv = models.ForeignKey(CvMethodtype,verbose_name='method type',
            help_text="A vocabulary for describing types of Methods associated with creating observations. " +
                      "MethodTypes correspond with ActionTypes in ODM2. An Action must be performed using an " +
                      "appropriate MethodType - e.g., a specimen collection Action should be associated with a "+
                      "specimen collection method. details for individual values " +
                      "here: http://vocabulary.odm2.org/methodtype/", db_column='methodtypecv')
    methodcode = models.CharField(verbose_name='method code',max_length=50)
    methodname = models.CharField(verbose_name='method name',max_length=255)
    methoddescription = models.CharField(verbose_name='method description', max_length=500, blank=True)
    methodlink = models.CharField(verbose_name='web link for method', max_length=255, blank=True)
    organizationid = models.ForeignKey('Organizations', verbose_name='organization', db_column='organizationid', blank=True, null=True)
    def __str__(self):
        s = str(self.methodcode)
        if self.methodtypecv:
            s += ', {0}'.format(self.methodtypecv)
        return s
    class Meta:
        managed = False
        db_table = 'methods'
        verbose_name='method'


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
    organizationtypecv = models.ForeignKey( CvOrganizationtype, verbose_name="organization type", db_column='organizationtypecv')
    organizationcode = models.CharField(verbose_name="organization code", max_length=50)
    organizationname = models.CharField(verbose_name="organization name", max_length=255)
    organizationdescription = models.CharField(verbose_name="organization description", max_length=500, blank=True)
    organizationlink = models.CharField(verbose_name="organization web link", max_length=255, blank=True)
    parentorganizationid = models.ForeignKey('self',verbose_name="parent organization", db_column='parentorganizationid',blank=True, null=True, default=1)
    def __str__(self):
        s = str(self.organizationcode)
        if self.organizationname:
            s += ', {0}'.format(self.organizationname)
        return s
    class Meta:
        managed = False
        db_table = 'organizations'
        verbose_name='organization'


class People(models.Model):
    personid = models.AutoField(primary_key=True)
    personfirstname = models.CharField(max_length=255)
    personmiddlename = models.CharField(max_length=255, blank=True)
    personlastname = models.CharField(max_length=255)
    def __str__(self):
        s = str(self.personlastname)
        if self.personfirstname:
            s += ', {0}'.format(self.personfirstname)
        return s
    class Meta:
        managed = False
        db_table = 'people'
        verbose_name='people'
        verbose_name_plural='people'


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
    processinglevelcode = models.CharField(verbose_name='processing level code',max_length=50)
    definition = models.CharField(max_length=500, blank=True)
    explanation = models.CharField(max_length=500, blank=True)
    def __str__(self):
        s = str(self.processinglevelcode)
        if self.definition:
            s += ', {0}'.format(self.definition)
        return s
    class Meta:
        managed = False
        db_table = 'processinglevels'
        verbose_name='processing level'


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
    actionid = models.ForeignKey(Actions,verbose_name='action', db_column='actionid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, verbose_name='relationship type', db_column='relationshiptypecv')
    relatedactionid = models.ForeignKey(Actions, verbose_name='related action',related_name='RelatedActions',db_column='relatedactionid')
    def __str__(self):
        s = str(self.actionid)
        if self.relationshiptypecv:
            s += ', {0}'.format(self.relationshiptypecv)
        if self.relatedactionid:
            s += ', {0}'.format(self.relatedactionid)
        return s
    class Meta:
        managed = False
        db_table = 'relatedactions'
        verbose_name='related action (associates one action with another)'
        verbose_name_plural='related action (associates one action with another)'


class Relatedannotations(models.Model):
    relationid = models.AutoField(primary_key=True)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedannotationid = models.ForeignKey(Annotations,related_name='RelatedAnnotations', db_column='relatedannotationid')

    class Meta:
        managed = False
        db_table = 'relatedannotations'


class Relatedcitations(models.Model):
    relationid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey(Citations, db_column='citationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedcitationid = models.ForeignKey(Citations,related_name='RelatedCitations', db_column='relatedcitationid')

    class Meta:
        managed = False
        db_table = 'relatedcitations'


class Relateddatasets(models.Model):
    relationid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, db_column='datasetid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relateddatasetid = models.ForeignKey(Datasets, related_name='relatedDataset',db_column='relateddatasetid')
    versioncode = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = 'relateddatasets'


class Relatedequipment(models.Model):
    relationid = models.AutoField(primary_key=True)
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedequipmentid = models.ForeignKey(Equipment, related_name='RelatedEquipment', db_column='relatedequipmentid')
    relationshipstartdatetime = models.DateTimeField()
    relationshipstartdatetimeutcoffset = models.IntegerField()
    relationshipenddatetime = models.DateTimeField(blank=True, null=True)
    relationshipenddatetimeutcoffset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatedequipment'


class Relatedfeatures(models.Model):
    relationid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', verbose_name="first feature", db_column='samplingfeatureid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, verbose_name= "relationship type", db_column='relationshiptypecv')
    relatedfeatureid = models.ForeignKey('Samplingfeatures', verbose_name="second feature", related_name='RelatedFeatures', db_column='relatedfeatureid')
    spatialoffsetid = models.ForeignKey('Spatialoffsets',verbose_name="spatial offset", db_column='spatialoffsetid', blank=True, null=True)
    def __str__(self):
        s = str(self.samplingfeatureid)
        s +=  ' - {0}'.format(self.relationshiptypecv)
        s += ' - {0}'.format(self.relatedfeatureid)
        return s
    class Meta:
        managed = False
        db_table = 'relatedfeatures'
        verbose_name= 'relate two feature'


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
    relatedresultid = models.ForeignKey('Results', related_name='RelatedResult', db_column='relatedresultid')
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
    resultuuid = UUIDField(auto=True)
    feature_action = models.ForeignKey( Featureactions,related_name="feature_actions",verbose_name="sampling feature action", db_column='featureactionid')
    result_type = models.ForeignKey(CvResulttype,verbose_name='result type', db_column='resulttypecv')
    variable = models.ForeignKey('Variables', verbose_name='variable', db_column='variableid')
    unitsid = models.ForeignKey('Units', verbose_name='units', related_name='+', db_column='unitsid')
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers', verbose_name='taxonomic classifier', db_column='taxonomicclassifierid',blank=True, null=True)
    processing_level = models.ForeignKey(Processinglevels, db_column='processinglevelid')
    resultdatetime = models.DateTimeField(verbose_name='result date time',blank=True, null=True)
    resultdatetimeutcoffset = models.BigIntegerField(verbose_name='result date time UTC offset', default=4, null=True)
    #validdatetime>> Date and time for which the result is valid (e.g., for a forecast result).
    # Should probably be expressed as a duration
    validdatetime = models.DateTimeField(verbose_name= 'valid date time- Date and time for which the result is valid', blank=True, null=True)
    validdatetimeutcoffset = models.BigIntegerField(verbose_name='valid date time UTC offset', default=4, null=True)
    statuscv = models.ForeignKey(CvStatus, verbose_name='status',db_column='statuscv', blank=True, null=True)
    sampledmediumcv = models.ForeignKey(CvMedium, verbose_name= 'sampled medium', db_column='sampledmediumcv', blank=True, null=True)
    valuecount = models.IntegerField(verbose_name='number of recorded values')
    #def __unicode__(self):
    #    return u'%s - %s' % (self.resultid, self.feature_action)
    def __str__(self):
        #s = str(self.resultid)
        s = '{0}'.format(self.variable)
        s+='- {0}'.format(self.feature_action)
        s += '- ID: {0}'.format(self.resultid)
        #if self.result_type:
            #s += ', {0}'.format(self.result_type)
        return s
    class Meta:
        managed = False
        db_table = 'results'
        verbose_name='result'
        ordering = ["variable"]


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
    def __str__(self):
        s = str(self.samplingfeatureid)
        if self.annotationid:
            s += ', {0}'.format(self.annotationid)
        return s
    class Meta:
        managed = False
        db_table = 'samplingfeatureannotations'


class Samplingfeatureextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)
    def __str__(self):
        s = str(self.samplingfeatureid)
        if self.propertyvalue:
            s += '- {0}'.format(self.propertyvalue)
        return s
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
    samplingfeatureuuid = UUIDField(auto=True)
    sampling_feature_type = models.ForeignKey(CvSamplingfeaturetype, db_column='samplingfeaturetypecv')
    samplingfeaturecode = models.CharField(verbose_name='sampling feature code',max_length=50)
    samplingfeaturename = models.CharField(verbose_name='sampling feature name',max_length=255, blank=True, null=True)
    samplingfeaturedescription = models.CharField(verbose_name='sampling feature description', max_length=500, blank=True)
    sampling_feature_geo_type = models.ForeignKey(CvSamplingfeaturegeotype,db_column='samplingfeaturegeotypecv', default= "Point", null=True)
    featuregeometry = models.TextField(verbose_name='feature geometry',blank=True, null=True)  #GeometryField This field type is a guess.
    elevation_m = models.FloatField(verbose_name='elevation',blank=True, null=True)
    elevation_datum = models.ForeignKey(CvElevationdatum, db_column='elevationdatumcv', blank=True, null=True)
    def __str__(self):
        s = str(self.samplingfeaturecode)
        s += '- {0} '.format(self.sampling_feature_type)
        if self.samplingfeaturename:
            s += '- {0},'.format(self.samplingfeaturename)
        return s
    class Meta:
        managed = False
        db_table = 'samplingfeatures'
        verbose_name='sampling feature'


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

# I needed to add a sequence and set it as the default for the primary key to make the Taxonomic Classifiers class work
# this is the SQL

# CREATE SEQUENCE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
#   INCREMENT 1
#   MINVALUE 2
#   MAXVALUE 9223372036854775807
#   START 3
#   CACHE 1;
# ALTER TABLE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
#   OWNER TO postgres;

#ALTER TABLE odm2.taxonomicclassifiers
 #  ALTER COLUMN taxonomicclassifierid SET DEFAULT nextval('odm2.taxonomicclassifiers_taxonomicclassifiersid_seq'::regclass);

class Taxonomicclassifiers(models.Model):
    taxonomicclassifierid = models.AutoField(primary_key=True)
    taxonomic_classifier_type = models.ForeignKey(CvTaxonomicclassifiertype, db_column='taxonomicclassifiertypecv',
                    help_text="A vocabulary for describing types of taxonomies from which descriptive terms used "+
                              "in an ODM2 database have been drawn. Taxonomic classifiers provide a way to classify"+
                              " Results and Specimens according to terms from a formal taxonomy.. Check "+
                              "http://vocabulary.odm2.org/taxonomicclassifiertype/  for more info")
    taxonomicclassifiername = models.CharField(verbose_name='taxonomic classifier name', max_length=255)
    taxonomicclassifiercommonname = models.CharField(verbose_name='taxonomic classifier common name',max_length=255, blank=True)
    taxonomicclassifierdescription = models.CharField(verbose_name='taxonomic classifier description',max_length=500, blank=True)
    parent_taxonomic_classifier = models.ForeignKey('self', db_column='parenttaxonomicclassifierid', blank=True, null=True)
    def __str__(self):
        s = str(self.taxonomicclassifiername)
        if self.taxonomicclassifiercommonname:
            s += ', {0}'.format(self.taxonomicclassifiercommonname)
        return s
    class Meta:
        managed = False
        db_table = 'taxonomicclassifiers'
        verbose_name='taxonomic classifier'


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
    unit_type = models.ForeignKey(CvUnitstype,
            help_text="A vocabulary for describing the type of the Unit or the more general quantity that the Unit " +
                      "represents. View unit type details here http://vocabulary.odm2.org/unitstype/"
            ,db_column='unitstypecv')
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    unitsname = models.CharField(verbose_name='unit name',max_length=255)
    unitslink = models.CharField(verbose_name='reference for the unit (web link)',max_length=255, blank=True)
    def __str__(self):
        s = str(self.unitsabbreviation)
        if self.unitsname:
            s += ', {0}'.format(self.unitsname)
        return s
    class Meta:
        managed = False
        db_table = 'units'
        verbose_name='unit'


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
    variable_type = models.ForeignKey(CvVariabletype,
        help_text="view variable types here http://vocabulary.odm2.org/variabletype/ ", db_column='variabletypecv')
    #variabletypecv = models.ModelChoiceField(CvVariabletype, db_column='variabletypecv')
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    variable_name = models.ForeignKey(CvVariablename,
        help_text="view variable names here http://vocabulary.odm2.org/variablename/", db_column='variablenamecv')
    variabledefinition = models.CharField(verbose_name='variable definition', max_length=500, blank=True)
    #variabledefinition.name = 'variable_definition'
    speciation = models.ForeignKey(CvSpeciation, db_column='speciationcv', blank=True, null=True)
    nodatavalue = models.FloatField(verbose_name='no data value')
    def __str__(self):
        s = str(self.variablecode)
        if self.variabledefinition:
            s += ', {0}'.format(self.variabledefinition)[:20]
        return s
    class Meta:
        managed = False
        db_table = 'variables'
        verbose_name='variable'
    