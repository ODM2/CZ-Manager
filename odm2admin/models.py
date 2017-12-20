﻿# C:\ODM2\odm2testsite\odm2testsite\templates
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify,
# and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

import time

from django.db import models
from django.db.models import UUIDField
from django.core import management
from django.core.exceptions import ValidationError
from django.core.management import settings
from django.contrib.gis.geos import GEOSGeometry
# from django.forms import ModelFormWithFileField
# from .forms import DataloggerprogramfilesAdminForm
# from odm2testapp.forms import VariablesForm
# from django.contrib.gis.db import models
import csv
import io
from urlparse import urlparse
import uuid
from django.contrib.gis.db import models as gis_models
import re

def handle_uploaded_file(f, id):
    destination = io.open(settings.MEDIA_ROOT + '/resultvalues/' + f.name + '.csv', 'wb+')
    # data = open(f)
    for chunk in f.chunks():
        destination.write(chunk)
        # Measurementresultvalues

    destination.close()
    try:
        with io.open(settings.MEDIA_ROOT + '/resultvalues/' + f.name + '.csv', 'rt', encoding='ascii') as f:
            reader = csv.reader(f)
            for row in reader:
                # raise ValidationError(row) #print the current row
                dateT = time.strptime(row[0], "%m/%d/%Y %H:%M")  # '1/1/2013 0:10
                datestr = time.strftime("%Y-%m-%d %H:%M", dateT)
                Measurementresultvalues(resultid=id, datavalue=row[1], valuedatetime=datestr,
                                        valuedatetimeutcoffset=4).save()
    except IndexError:
        raise ValidationError('encountered a problem with row ' + row)


def buildCitation(s, self):
    result = None
    if hasattr(self.resultid, 'resultid'):
        result = self.resultid.resultid
    else:
        result = Results.objects.get(resultid=self.resultid)
    datasetresults = Datasetsresults.objects.filter(resultid=result)
    dsCitations = Datasetcitations.objects.filter(datasetid__in=datasetresults.values("datasetid"))
    citations = Citations.objects.filter(citationid__in=dsCitations.values("citationid"))

    authcount = 0
    if citations.count() == 0:
        s += ','
        return s
    for citation in citations:
        citedauthors = Authorlists.objects.filter(citationid=citation.citationid).order_by(
            "authororder")
        citedpersons = People.objects.filter(personid__in=citedauthors.values("personid"))
        for citedauthor in citedauthors:
            for author in citedpersons:
                if citedauthor.personid.personid == author.personid:
                    if authcount == 0:
                        s += ',\" {0}'.format(author.personlastname)
                    else:
                        s += ' {0}'.format(author.personlastname)

                    authcount += 1
                    if authcount == citedpersons.count():
                        s += ' {0}.'.format(author.personfirstname)
                    else:
                        s += ' {0},'.format(author.personfirstname)
        s += ' {0}'.format(citation.title)
        s += '. {0}'.format(citation.publisher)
        s += ', {0}'.format(citation.publicationyear)
        s += ' DOI: {0}\"'.format(citation.citationlink)  # doesn't work not sure why
    return s


class Actionannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    annotationid = models.ForeignKey('Annotations', db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."actionannotations'


class Actionby(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', verbose_name="action", db_column='actionid')
    affiliationid = models.ForeignKey('Affiliations', verbose_name="person by affiliation",
                                      db_column='affiliationid')
    isactionlead = models.BooleanField(verbose_name="is lead person on action")
    roledescription = models.CharField(max_length=5000, verbose_name="person's role on this action",
                                       blank=True)

    def __unicode__(self):
        s = u"%s" % self.actionid
        if self.affiliationid:
            s += u"- %s" % self.affiliationid
        if self.roledescription:
            s += u"- %s" % self.roledescription
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."actionby'
        verbose_name = 'action by'
        verbose_name_plural = 'action by'


class Actiondirectives(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    directiveid = models.ForeignKey('Directives', db_column='directiveid')

    class Meta:
        managed = False
        db_table = r'odm2"."actiondirectives'


class Actionextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey('Actions', db_column='actionid')
    propertyid = models.ForeignKey('Extensionproperties', db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = r'odm2"."actionextensionpropertyvalues'


class Actions(models.Model):
    actionid = models.AutoField(primary_key=True)
    action_type = models.ForeignKey('CvActiontype',
                                    help_text='A vocabulary for describing the type of actions '
                                              'performed in making observations. Depending'
                                              ' on the action type, the action may or may not '
                                              'produce an observation result. view action type '
                                              'details here http://vocabulary.odm2.org/actiontype/',
                                    db_column='actiontypecv')
    method = models.ForeignKey('Methods', db_column='methodid')
    begindatetime = models.DateTimeField(verbose_name='begin date time')
    begindatetimeutcoffset = models.IntegerField(
        verbose_name='begin date time clock off set (from GMT)', default=4)
    enddatetime = models.DateTimeField(verbose_name='end date time', blank=True, null=True)
    enddatetimeutcoffset = models.IntegerField(
        verbose_name='end date time clock off set (from GMT)', default=4)
    actiondescription = models.CharField(verbose_name='action description', max_length=5000,
                                         blank=True)
    actionfilelink = models.CharField(verbose_name='action file link', max_length=255, blank=True)

    def __unicode__(self):
        s = u"%s" % self.action_type
        if self.method:
            s += u" | %s" % self.method
        if self.method:
            s += u" | %s" % (self.actiondescription[:25])
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."actions'
        verbose_name = 'action'


class Affiliations(models.Model):
    affiliationid = models.AutoField(primary_key=True)
    personid = models.ForeignKey('People', verbose_name='person', db_column='personid')
    organizationid = models.ForeignKey('Organizations', verbose_name='organization',
                                       db_column='organizationid',
                                       blank=True, null=True)
    isprimaryorganizationcontact = models.NullBooleanField(
        verbose_name='primary organization contact? ')
    affiliationstartdate = models.DateField(verbose_name="When affiliation began ")
    affiliationenddate = models.DateField(verbose_name="When affiliation ended", blank=True,
                                          null=True)
    primaryphone = models.CharField(verbose_name="primary phone", max_length=50, blank=True)
    primaryemail = models.CharField(verbose_name="primary email", max_length=255)
    primaryaddress = models.CharField(verbose_name="primary address", max_length=255, blank=True)
    personlink = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        s = u"%s" % self.personid
        if self.organizationid:
            s += u" | %s" % self.organizationid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."affiliations'
        verbose_name = 'affiliation (relate people and organizations)'
        verbose_name_plural = 'affiliation (relate people and organizations)'
        ordering = ['-primaryemail']


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

    def __unicode__(self):
        s = u" %s" % self.annotationtext
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."annotations'


class Authorlists(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', verbose_name='citation', db_column='citationid')
    personid = models.ForeignKey('People', verbose_name='person', db_column='personid', blank=True,
                                 null=True)
    authororder = models.IntegerField(verbose_name='author order', blank=True, null=True)

    def __unicode__(self):
        s = u"{0} - {1}".format(self.personid, self.authororder)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."authorlists'
        verbose_name = 'author list'
        verbose_name_plural = 'author list'

    def csvheader(self):
        s = 'Author ' + str(self.authororder) + ','
        return s

    def csvoutput(self):
        s = '"' + str(self.personid.personlastname) + ', ' + str(
            self.personid.personfirstname) + ', ' + str(
            self.personid.personmiddlename) + '",'
        return s

    def endnoteexport(self):
        # if self.authororder ==1:
        # s = 'FAU - '+ str(self.personid.personlastname)+","+ str(self.personid.personfirstname) +
        # ', '+str(self.personid.personmiddlename) +'\n'
        # else:
        s = 'AU  - ' + str(self.personid.personlastname) + "," + str(
            self.personid.personfirstname) + ', ' + str(
            self.personid.personmiddlename) + '\r\n'
        return s


class Calibrationactions(models.Model):
    actionid = models.OneToOneField(Actions, db_column='actionid', primary_key=True)
    calibrationcheckvalue = models.FloatField(blank=True, null=True)
    instrumentoutputvariableid = models.ForeignKey('Instrumentoutputvariables',
                                                   db_column='instrumentoutputvariableid')
    calibrationequation = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."calibrationactions'


class Calibrationreferenceequipment(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Calibrationactions, db_column='actionid')
    equipmentid = models.ForeignKey('Equipment', db_column='equipmentid')

    class Meta:
        managed = False
        db_table = r'odm2"."calibrationreferenceequipment'


class Calibrationstandards(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Calibrationactions, db_column='actionid')
    referencematerialid = models.ForeignKey('Referencematerials', db_column='referencematerialid')

    class Meta:
        managed = False
        db_table = r'odm2"."calibrationstandards'


class Categoricalresults(models.Model):
    resultid = models.OneToOneField('Results', db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.IntegerField(blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.IntegerField(blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.IntegerField(blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid',
                                           blank=True, null=True)
    qualitycodecv = models.ForeignKey('CvQualitycode', db_column='qualitycodecv')

    class Meta:
        managed = False
        db_table = r'odm2"."categoricalresults'


class Categoricalresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Categoricalresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."categoricalresultvalueannotations'


class Categoricalresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Categoricalresults, db_column='resultid')
    datavalue = models.CharField(max_length=255)
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()

    class Meta:
        managed = False
        db_table = r'odm2"."categoricalresultvalues'


class Citationextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', db_column='citationid')
    propertyid = models.ForeignKey('Extensionproperties', db_column='propertyid')
    propertyvalue = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        s = u"%s - %s - %s" % (self.citationid, self.propertyid, self.propertyvalue)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."citationextensionpropertyvalues'
        verbose_name = 'citation extension property'
        verbose_name_plural = 'citation extension properties'

    def csvheader(self):
        s = '"' + str(self.propertyid) + '",'
        return s

    def csvoutput(self):
        s = '"' + str(self.propertyvalue) + '",'
        return s
        # def endnoteheader(self):
        # s ='"'+ str(self.propertyid)+'"\t'
        # return s

    def pubType(self):
        type = None
        if str(self.propertyvalue).__len__() > 0:
            if str(
                    self.propertyid) == 'Citation Category - Paper, Book, Talk, Poster, ' \
                                        'Dissertation, Thesis, Undergrad Thesis, Report':
                if str(self.propertyvalue) == 'Paper':
                    type = "Paper"
                if str(self.propertyvalue) == 'Book':
                    type = "Book"
                if str(self.propertyvalue) == 'Talk':
                    type = "Conference"
                if str(self.propertyvalue) == 'Poster':
                    type = "Poster"
                if str(self.propertyvalue) == 'Dissertation' or str(
                        self.propertyvalue) == 'Thesis' or str(self.propertyvalue) == \
                        'Undergrad Thesis':
                    type = "Thesis"
                if str(self.propertyvalue) == 'Report':
                    type = "Report"
        return type

    def endnoteexport(self):
        s = ''
        if str(self.propertyvalue).__len__() > 0:
            if str(
                    self.propertyid) == 'Citation Category - Paper, Book, Talk, Poster, ' \
                                        'Dissertation, Thesis, Undergrad Thesis, Report':
                s += 'TY  - '
                if str(self.propertyvalue) == 'Paper':
                    s += 'JOUR' + '\r\n'
                if str(self.propertyvalue) == 'Book':
                    s += 'BOOK' + '\r\n'
                if str(self.propertyvalue) == 'Talk':
                    s += 'CONF' + '\r\n'
                if str(self.propertyvalue) == 'Poster':
                    s += 'ABST' + '\r\n'
                if str(self.propertyvalue) == 'Dissertation' or str(
                        self.propertyvalue) == 'Thesis' or str(self.propertyvalue) == \
                        'Undergrad Thesis':
                    s += 'THES' + '\r\n'
                if str(self.propertyvalue) == 'Report':
                    s += 'RPRT' + '\r\n'
            s += 'N1  - ' + str(self.propertyid) + ': ' + str(self.propertyvalue) + '\r\n'
        else:
            s = ''
        return s


class Citationexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey('Citations', db_column='citationid')
    externalidentifiersystemid = models.ForeignKey('Externalidentifiersystems',
                                                   db_column='externalidentifiersystemid')
    # externalidentifiersystemid
    citationexternalidentifier = models.CharField(max_length=255,
                                                  db_column="citationexternalidentifier")
    citationexternalidentifieruri = models.CharField(max_length=255, blank=True,
                                                     db_column="citationexternalidentifieruri")

    def __unicode__(self):
        s = u"{0} - {1}".format(self.externalidentifiersystemid, self.citationexternalidentifier)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."citationexternalidentifiers'
        verbose_name = 'citationexternalidentifier'


class Citations(models.Model):
    citationid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publicationyear = models.IntegerField(verbose_name='year')
    citationlink = models.CharField(max_length=255, blank=True, verbose_name='Citation Link', )

    def __unicode__(self):
        s = u"%s" % self.title
        if self.publisher:
            s += u"- %s," % self.publisher
        if self.publicationyear:
            s += u", %s," % self.publicationyear
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."citations'
        ordering = ['title']
        verbose_name = 'citation'

    @staticmethod
    def csvheader():
        s = 'citationid,title,publisher,year,citationlink,'
        return s

    def csvoutput(self):
        s = str(self.citationid)
        s += ',"{0}"'.format(self.title)
        s += ',"{0}"'.format(self.publisher)
        s += ', {0}'.format(self.publicationyear)
        s += ', {0},'.format(self.citationlink)
        return s

    @staticmethod
    def endnoteexportheader():
        s = 'TI\tPB\tPY\tcitationlink\t'
        return s

    def endnoteexport(self):
        propertyvalues = Citationextensionpropertyvalues.objects.filter(citationid=self.citationid)
        pubType = None
        for propertyvalue in propertyvalues:
            if propertyvalue.pubType():
                pubType = propertyvalue.pubType()
        if not pubType:  # "Conference""Poster""Thesis""Report"
            pubType = "Unknown"
        s = 'TI  - {0}\r\n'.format(self.title)
        if pubType == "Paper":
            s += 'JO  - {0}\r\n'.format(self.publisher)
        else:
            s += 'PB  - {0}\r\n'.format(self.publisher)
        s += 'PY  - {0}\r\n'.format(self.publicationyear)
        s += 'DI  - {0}\r\n'.format(self.citationlink)
        return s


class CvActiontype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_actiontype'
        ordering = ['term', 'name']


class CvAggregationstatistic(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_aggregationstatistic'
        ordering = ['term', 'name']


class CvAnnotationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_annotationtype'
        ordering = ['term', 'name']


class CvCensorcode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_censorcode'
        ordering = ['term', 'name']


class CvDataqualitytype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_dataqualitytype'
        ordering = ['term', 'name']


class CvDatasettypecv(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_datasettype'
        ordering = ['term', 'name']


class CvDirectivetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_directivetype'
        ordering = ['term', 'name']


class CvElevationdatum(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_elevationdatum'
        verbose_name = 'elevation datum'
        ordering = ['term', 'name']


class CvEquipmenttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_equipmenttype'
        ordering = ['term', 'name']


class CvMethodtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_methodtype'
        ordering = ['term', 'name']


class CvOrganizationtype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_organizationtype'
        ordering = ['term', 'name']


class CvPropertydatatype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_propertydatatype'
        ordering = ['term', 'name']


class CvQualitycode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_qualitycode'
        ordering = ['term', 'name']


class CvReferencematerialmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_referencematerialmedium'
        ordering = ['term', 'name']


class CvRelationshiptype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_relationshiptype'
        ordering = ['term', 'name']


class CvResulttype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_resulttype'
        ordering = ['term', 'name']


class CvMedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_medium'
        ordering = ['term', 'name']


class CvSamplingfeaturegeotype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_samplingfeaturegeotype'
        verbose_name = 'sampling feature geo type'
        ordering = ['term', 'name']


class CvSamplingfeaturetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_samplingfeaturetype'
        verbose_name = 'sampling feature type'
        ordering = ['term', 'name']


class CvSitetype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_sitetype'
        ordering = ['term', 'name']


class CvSpatialoffsettype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_spatialoffsettype'
        ordering = ['term', 'name']


class CvSpeciation(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_speciation'
        ordering = ['term', 'name']


class CvSpecimenmedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_medium'
        ordering = ['term', 'name']


class CvSpecimentype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_specimentype'
        ordering = ['term', 'name']


class CvStatus(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_status'
        ordering = ['term', 'name']


class CvTaxonomicclassifiertype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_taxonomicclassifiertype'
        ordering = ['term', 'name']
        verbose_name = "taxonomic classifier"


class CvUnitstype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_unitstype'
        ordering = ['term', 'name']


class CvVariablename(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        managed = False
        db_table = r'odm2"."cv_variablename'
        ordering = ['term', 'name']


class CvVariabletype(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourcevocabularyuri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2"."cv_variabletype'
        ordering = ['term', 'name']


class Dataloggerfilecolumns(models.Model):
    dataloggerfilecolumnid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', verbose_name="result", db_column='resultid', blank=True,
                                 null=True)
    dataloggerfileid = models.ForeignKey('Dataloggerfiles', verbose_name="data logger file",
                                         db_column='dataloggerfileid')
    instrumentoutputvariableid = models.ForeignKey('Instrumentoutputvariables',
                                                   verbose_name="instrument output variable",
                                                   db_column='instrumentoutputvariableid')
    columnlabel = models.CharField(verbose_name="column label", max_length=50)
    columndescription = models.CharField(verbose_name="column description",
                                         help_text="To disble ingestion of a column type skip, " +
                                                "or to specify a column as the date time enter datetime" +
                                                " if the datetime is an excel format numeric datetime" +
                                                " enter exceldatetime",
                                         max_length=5000,
                                         blank=True)
    measurementequation = models.CharField(verbose_name="measurement equation", max_length=255,
                                           blank=True)
    scaninterval = models.FloatField(verbose_name="scan interval (time)", blank=True, null=True)
    scanintervalunitsid = models.ForeignKey('Units', verbose_name="scan interval units",
                                            related_name='relatedScanIntervalUnitsid',
                                            db_column='scanintervalunitsid',
                                            blank=True, null=True)
    recordinginterval = models.FloatField(verbose_name="recording interval", blank=True, null=True)
    recordingintervalunitsid = models.ForeignKey('Units', verbose_name="recording interval units",
                                                 related_name='relatedRecordingintervalunitsid',
                                                 db_column='recordingintervalunitsid', blank=True,
                                                 null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               verbose_name="aggregation statistic",
                                               db_column='aggregationstatisticcv', blank=True,
                                               null=True)

    def __unicode__(self):
        # s = u"%s" % (self.dataloggerfileid)
        s = u"Label: %s," % self.columnlabel
        # s += u" Description: %s," % (self.columndescription)
        s += u" Result: %s" % self.resultid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."dataloggerfilecolumns'
        verbose_name = 'data logger file column'


class Dataloggerfiles(models.Model):
    dataloggerfileid = models.AutoField(primary_key=True)
    programid = models.ForeignKey('Dataloggerprogramfiles',  verbose_name="Data logger program", db_column='programid')
    dataloggerfilename = models.CharField(max_length=255, verbose_name="Data logger file name")
    dataloggerfiledescription = models.CharField(max_length=5000, blank=True, verbose_name="Data logger file description")
    # dataloggerfilelink = models.CharField(max_length=255, blank=True)
    dataloggerfilelink = models.FileField(upload_to='dataloggerfiles', verbose_name="Data logger file")  # upload_to='.'
    
    def dataloggerfilelinkname(self):
        return self.dataloggerfilelink.name
    def __unicode__(self):
        s = u"%s" % self.dataloggerfilename
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."dataloggerfiles'
        verbose_name = 'data logger file'


class ProcessDataloggerfile(models.Model):
    processdataloggerfileid = models.AutoField(primary_key=True)
    dataloggerfileid = models.ForeignKey('dataloggerfiles',
                                         help_text="CAUTION dataloggerfilecolumns must be setup" +
                                                   ", the date and time stamp is expected to " +
                                                   "be the first column, " +
                                                   " column names must match " +
                                                   "the column name in associated " +
                                                   "dataloggerfilecolumns.",
                                         verbose_name='data logger file',
                                         db_column='dataloggerfileid')
    processingCode = models.CharField(max_length=255, verbose_name='processing code',
                                      help_text="to setup an FTP file download set the processing" +
                                      "code as 'x hours between download' where x is how many hours to " +
                                      "wait between downloading copies of the file from the FTP site. " +
                                      "A datalogger file setup for FTP download must have only 1 " +
                                      "process data logger file record.", default="0")
    databeginson = models.IntegerField(verbose_name="Data begins on this row number", default=2)
    columnheaderson = models.IntegerField(
        verbose_name="Column headers matching column labels from data logger columns on row")
    date_processed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        s = u"%s" % self.dataloggerfileid
        s += u"- Processed on %s" % self.date_processed
        return s

    class Meta:
        managed = False
        db_table = r'odm2extra"."processdataloggerfile'
        verbose_name = 'process data logger file'

    def save(self, *args, **kwargs):
        # ProcessDataLoggerFile(self.dataloggerfileid.dataloggerfilelink,self.dataloggerfileid,
        # self.databeginson, self.columnheaderson, False)
        linkname = str(self.dataloggerfileid.dataloggerfilelinkname())
        fileid = self.dataloggerfileid.dataloggerfileid
        ftpfile = self.dataloggerfileid.dataloggerfiledescription
        ftpparse = urlparse(ftpfile)
        if len(ftpparse.netloc) > 0:
            ftpfrequencyhours = re.findall(r'^\D*(\d+)', self.processingCode)[0]
            management.call_command('update_preprocess_process_datalogger_file', linkname, str(fileid)
                                    , str(self.databeginson), str(self.columnheaderson),
                                    str(ftpfrequencyhours), False)
        else:
            management.call_command('ProcessDataLoggerFile', linkname ,str(fileid)
                                    , str(self.databeginson), str(self.columnheaderson),
                                    False, False, False)
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
    programdescription = models.CharField(max_length=5000, blank=True)
    programversion = models.CharField(max_length=50, blank=True)
    # programfilelink = models.CharField(max_length=255, blank=True)
    programfilelink = models.FileField(
        upload_to='dataloggerprogramfiles')

    # + '/' + programname.__str__() settings.settings.MEDIA_ROOT upload_to='/upfiles/'

    def __unicode__(self):
        s = u"%s" % self.programname
        s += u"- Version %s" % self.programversion
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."dataloggerprogramfiles'
        verbose_name = 'data logger program file'


class Dataquality(models.Model):
    dataqualityid = models.AutoField(primary_key=True)
    dataqualitytypecv = models.ForeignKey(CvDataqualitytype, db_column='dataqualitytypecv',
                                          verbose_name="data quality type")
    dataqualitycode = models.CharField(max_length=255, verbose_name="data quality code",
                                       help_text="for an alarm test include the word alarm." +
                                       " for a hard bounds check include the word bound (if a value" +
                                       " falls below a lower limit, or exceeds a lower limit the " +
                                       "value will be set to NaN (not a number). ")
    dataqualityvalue = models.FloatField(blank=True, null=True, verbose_name="data quality value")
    dataqualityvalueunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='dataqualityvalueunitsid',
                                                verbose_name="data quality value units", blank=True,
                                                null=True)
    dataqualitydescription = models.CharField(max_length=5000, blank=True,
                                              verbose_name="data quality description")
    dataqualitylink = models.CharField(max_length=255, blank=True, verbose_name="data quality link")

    def __unicode__(self):
        return u"%s - %s - %s" % (
            self.dataqualitycode, self.dataqualityvalue, self.dataqualityvalueunitsid)

    class Meta:
        managed = False
        db_table = r'odm2"."dataquality'
        verbose_name = 'data quality'
        verbose_name_plural = 'data quality'


class Datasetcitations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey('Datasets', verbose_name='dataset', db_column='datasetid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, verbose_name='relationship type',
                                           db_column='relationshiptypecv')
    citationid = models.ForeignKey(Citations, db_column='citationid', verbose_name='citation')

    class Meta:
        managed = False
        db_table = r'odm2"."datasetcitations'
        verbose_name = 'dataset citation'


class Datasets(models.Model):
    datasetid = models.AutoField(primary_key=True)
    datasetuuid = UUIDField(default=uuid.uuid4, editable=False)
    datasettypecv = models.ForeignKey(CvDatasettypecv, verbose_name="dataset type",
                                      db_column='datasettypecv')
    datasetcode = models.CharField(verbose_name="dataset code", max_length=50)
    datasettitle = models.CharField(verbose_name="dataset title", max_length=255)
    datasetabstract = models.CharField(verbose_name="dataset abstract", max_length=5000)

    def __unicode__(self):
        s = u"%s" % self.datasetcode
        if self.datasettitle:
            s += u"- %s" % self.datasettitle
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."datasets'
        verbose_name = 'dataset'


class Datasetsresults(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, verbose_name="dataset", db_column='datasetid')
    resultid = models.ForeignKey('Results', verbose_name="add the dataset to the result",
                                 db_column='resultid')

    def __unicode__(self):
        s = u"%s" % self.datasetid
        if self.resultid:
            s += u"- %s" % self.resultid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."datasetsresults'
        verbose_name = 'dataset result'


class Derivationequations(models.Model):
    derivationequationid = models.AutoField(primary_key=True)
    derivationequation = models.CharField(max_length=255, verbose_name='derivation equation')

    def __unicode__(self):
        s = u"%s" % self.derivationequation
        return s
    class Meta:
        managed = False
        db_table = r'odm2"."derivationequations'
        verbose_name='derivation equation'

class Directives(models.Model):
    directiveid = models.AutoField(primary_key=True)
    directivetypecv = models.ForeignKey(CvDirectivetype, db_column='directivetypecv')
    directivedescription = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = r'odm2"."directives'


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
    equipmentdescription = models.CharField(max_length=5000, blank=True)
    equipmentdocumentationlink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."equipment'


class Equipmentannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."equipmentannotations'


class Equipmentmodels(models.Model):
    equipmentmodelid = models.AutoField(primary_key=True)
    modelmanufacturerid = models.ForeignKey('Organizations', verbose_name="model manufacturer",
                                            db_column='modelmanufacturerid')
    modelpartnumber = models.CharField(max_length=50, blank=True, verbose_name="model part number")
    modelname = models.CharField(max_length=255, verbose_name="model name")
    modeldescription = models.CharField(max_length=5000, blank=True, null=True,
                                        verbose_name="model description")
    isinstrument = models.BooleanField(verbose_name="Is this an instrument?")
    modelspecificationsfilelink = models.CharField(max_length=255,
                                                   verbose_name="link to manual for equipment",
                                                   blank=True)
    modellink = models.CharField(max_length=255, verbose_name="link to website for model",
                                 blank=True)

    def __unicode__(self):
        s = u"%s" % self.modelname
        if self.modelpartnumber:
            s += u"- %s" % self.modelpartnumber
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."equipmentmodels'
        verbose_name = "equipment model"


class Equipmentused(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid')
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')

    class Meta:
        managed = False
        db_table = r'odm2"."equipmentused'


class Extensionproperties(models.Model):
    propertyid = models.AutoField(primary_key=True)
    propertyname = models.CharField(max_length=255, verbose_name="property name")
    propertydescription = models.CharField(max_length=5000, blank=True,
                                           verbose_name="property description")
    propertydatatypecv = models.ForeignKey(CvPropertydatatype, db_column='propertydatatypecv',
                                           verbose_name="property data type")
    propertyunitsid = models.ForeignKey('Units', db_column='propertyunitsid', blank=True, null=True,
                                        verbose_name="units for property")

    def __unicode__(self):
        return u"%s - %s" % (self.propertyname, self.propertydescription)

    class Meta:
        managed = False
        db_table = r'odm2"."extensionproperties'
        verbose_name = 'extension property'
        verbose_name_plural = 'extension properties'


class Externalidentifiersystems(models.Model):
    externalidentifiersystemid = models.AutoField(primary_key=True)
    externalidentifiersystemname = models.CharField(max_length=255)
    identifiersystemorganizationid = models.ForeignKey('Organizations',
                                                       db_column='identifiersystemorganizationid')
    externalidentifiersystemdescription = models.CharField(max_length=5000, blank=True)
    externalidentifiersystemurl = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s" % self.externalidentifiersystemname

    class Meta:
        managed = False
        db_table = r'odm2"."externalidentifiersystems'


class Featureactions(models.Model):
    featureactionid = models.AutoField(primary_key=True, verbose_name="sampling feature action")
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    action = models.ForeignKey(Actions, db_column='actionid')

    def __unicode__(self):
        return u"%s- %s - %s" % (self.featureactionid, self.samplingfeatureid, self.action)

    #     nameexists = FeatureactionsNames.objects.filter(featureactionid=self.featureactionid)
    #     if nameexists.__len__() >0:
    #         return u"%s" % nameexists[0]
    #     else:
    #         s = u"%s- %s - %s" % (self.featureactionid, self.samplingfeatureid, self.action)
    #         fan = FeatureactionsNames.objects.create(featureactionid=self,name=s)
    #         return "%s" % (fan)
    # def save(self, *args, **kwargs):
    #     nameexists = FeatureactionsNames.objects.filter(featureactionid=self.featureactionid)
    #     if nameexists.__len__() >0:
    #         s = u"%s- %s - %s" % (self.featureactionid, self.samplingfeatureid, self.action)
    #         nameexists.update(name = s)
    #     else:
    #         s = u"%s- %s - %s" % (self.featureactionid, self.samplingfeatureid, self.action)
    #         fan = FeatureactionsNames.objects.create(featureactionid=self, name=s)
    #     super(Featureactions, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = r'odm2"."featureactions'
        verbose_name = 'action at sampling feature'
        verbose_name_plural = 'action at sampling feature'


# this class just stores the unicode representation of a featureaction for faster lookup
class FeatureactionsNames(models.Model):
    featureactionNamesid = models.AutoField(primary_key=True)
    featureactionid = models.ForeignKey('Featureactions', db_column='featureactionid')
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False
        db_table = r'odm2extra"."featureactionsNames'
        verbose_name = 'feature action names'


class Instrumentoutputvariables(models.Model):
    instrumentoutputvariableid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey(Equipmentmodels, verbose_name="equipment model",
                                db_column='modelid')
    variableid = models.ForeignKey('Variables', verbose_name="variable", db_column='variableid')
    instrumentmethodid = models.ForeignKey('Methods', verbose_name="instrument method",
                                           db_column='instrumentmethodid')
    instrumentresolution = models.CharField(max_length=255, verbose_name="instrument resolution",
                                            blank=True)
    instrumentaccuracy = models.CharField(max_length=255, verbose_name="instrument accuracy",
                                          blank=True)
    instrumentrawoutputunitsid = models.ForeignKey('Units', related_name='+',
                                                   verbose_name="instrument raw output unit",
                                                   db_column='instrumentrawoutputunitsid')

    def __unicode__(self):
        s = u"%s " % self.modelid
        s += u"- %s" % self.variableid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."instrumentoutputvariables'
        verbose_name = "instrument output variable"


class Maintenanceactions(models.Model):
    actionid = models.OneToOneField(Actions, db_column='actionid', primary_key=True)
    isfactoryservice = models.BooleanField()
    maintenancecode = models.CharField(max_length=50, blank=True)
    maintenancereason = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."maintenanceactions'


class Measurementresults(models.Model):
    resultid = models.OneToOneField('Results', verbose_name="Result Series", db_column='resultid',
                                    primary_key=True)
    xlocation = models.FloatField(verbose_name="x location", blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', verbose_name="x location units",
                                         related_name='relatedXlocationUnits',
                                         db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, verbose_name="y location", null=True)
    ylocationunitsid = models.ForeignKey('Units', verbose_name="y location units",
                                         related_name='relatedYlocationUnits',
                                         db_column='ylocationunitsid', blank=True, null=True)
    zlocation = models.FloatField(blank=True, verbose_name="z location", null=True)
    zlocationunitsid = models.ForeignKey('Units', verbose_name="z location units",
                                         related_name='relatedZlocationUnits',
                                         db_column='zlocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', verbose_name="spatial reference",
                                           db_column='spatialreferenceid', blank=True, null=True)
    censorcodecv = models.ForeignKey(CvCensorcode, verbose_name="censor code",
                                     db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, verbose_name="quality code",
                                      db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               verbose_name="aggregation statistic",
                                               db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField(verbose_name="time aggregation interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units',
                                                       verbose_name="time aggregation " +
                                                                    "interval unit",
                                                       related_name='+',
                                                       db_column='timeaggregationintervalunitsid')

    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u", %s" % self.qualitycodecv
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."measurementresults'
        ordering = ['censorcodecv', 'resultid']
        verbose_name = 'measurement result'


class Measurementresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Measurementresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."measurementresultvalueannotations'


class Measurementresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Measurementresults, verbose_name='Result Series',
                                 db_column='resultid')
    datavalue = models.FloatField(verbose_name='data value')
    valuedatetime = models.DateTimeField(verbose_name='value date time')
    valuedatetimeutcoffset = models.IntegerField(verbose_name='value date time UTC offset',
                                                 default=4)

    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        s += 'time aggregation interval,'
        s += 'time aggregation unit,'
        s += 'citation,'

        return s

    def csvoutput(self):
        s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)
        s += ', {0}'.format(self.resultid.timeaggregationinterval)
        s += ', {0},'.format(self.resultid.timeaggregationintervalunitsid)
        s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s

    def csvheaderShort(self):
        s = '\" {0} -unit-{1}-processing level-{2}\",annotation,'.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level)
        return s

    def csvoutputShort(self):
        s = '{0}'.format(self.datavalue)
        mrvannotation = Measurementresultvalueannotations.objects.filter(valueid=self.valueid)
        annotations = Annotations.objects.filter(annotationid__in=mrvannotation)
        s += ',\"'
        for anno in annotations:
            s += '{0} '.format(anno)
        s += '\"'
        s += ','
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."measurementresultvalues'
        verbose_name = 'measurement result value'


class MeasurementresultvalueFile(models.Model):
    valueFileid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Measurementresults,
                                 help_text="CAUTION saving a measurement " +
                                           "result value file will attempt to " +
                                           "load values into the database.", verbose_name='result',
                                 db_column='resultid')
    valueFile = models.FileField(upload_to='resultvalues', verbose_name="value file ")

    def __unicode__(self):
        s = u"%s" % self.resultid
        return s

    class Meta:
        managed = False
        db_table = r'odm2extra"."Measurementresultvaluefile'
        verbose_name = 'measurement result value file'

    def save(self, *args, **kwargs):
        handle_uploaded_file(self.valueFile.file, self.resultid)
        super(MeasurementresultvalueFile, self).save(*args, **kwargs)


class Methodannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."methodannotations'


class Methodcitations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid', verbose_name='method')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv',
                                           verbose_name='relationship type')
    citationid = models.ForeignKey(Citations, db_column='citationid', verbose_name='citation')

    def __unicode__(self):
        s = u"%s " % self.methodid
        s += u"-, %s" % self.citationid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."methodcitations'
        verbose_name = 'method citation'


class Methodextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = r'odm2"."methodextensionpropertyvalues'


class Methodexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    methodid = models.ForeignKey('Methods', db_column='methodid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    methodexternalidentifier = models.CharField(max_length=255)
    methodexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."methodexternalidentifiers'


class Methods(models.Model):
    methodid = models.AutoField(primary_key=True)
    methodtypecv = models.ForeignKey(CvMethodtype, verbose_name='method type',
                                     help_text='A vocabulary for describing types of Methods '
                                               'associated with creating observations. '
                                               'MethodTypes correspond with ActionTypes in ODM2. '
                                               'An Action must be performed using an '
                                               'appropriate MethodType - e.g., a specimen '
                                               'collection Action should be associated with a '
                                               'specimen collection method. details for '
                                               'individual values '
                                               'here: http://vocabulary.odm2.org/methodtype/',
                                     db_column='methodtypecv')
    methodcode = models.CharField(verbose_name='method code', max_length=50)
    methodname = models.CharField(verbose_name='method name', max_length=255)
    methoddescription = models.CharField(verbose_name='method description', max_length=5000,
                                         blank=True)
    methodlink = models.CharField(verbose_name='web link for method', max_length=255, blank=True)
    organizationid = models.ForeignKey('Organizations', verbose_name='organization',
                                       db_column='organizationid',
                                       blank=True, null=True)

    def __unicode__(self):
        s = u"%s " % self.methodcode
        if self.methodtypecv:
            s += u", %s" % self.methodtypecv
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."methods'
        verbose_name = 'method'
        ordering = ["methodname"]


class Modelaffiliations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey('Models', db_column='modelid')
    affiliationid = models.ForeignKey(Affiliations, db_column='affiliationid')
    isprimary = models.BooleanField()
    roledescription = models.CharField(max_length=5000, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."modelaffiliations'


class Models(models.Model):
    modelid = models.AutoField(primary_key=True)
    modelcode = models.CharField(max_length=50)
    modelname = models.CharField(max_length=255)
    modeldescription = models.CharField(max_length=5000, blank=True)
    version = models.CharField(max_length=255, blank=True)
    modellink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."models'


class Organizations(models.Model):
    organizationid = models.AutoField(primary_key=True)
    organizationtypecv = models.ForeignKey(CvOrganizationtype, verbose_name="organization type",
                                           db_column='organizationtypecv')
    organizationcode = models.CharField(verbose_name="organization code", max_length=50)
    organizationname = models.CharField(verbose_name="organization name", max_length=255)
    organizationdescription = models.CharField(verbose_name="organization description",
                                               max_length=5000, blank=True)
    organizationlink = models.CharField(verbose_name="organization web link", max_length=255,
                                        blank=True)
    parentorganizationid = models.ForeignKey('self', verbose_name="parent organization",
                                             db_column='parentorganizationid', blank=True,
                                             null=True, default=1)

    def __unicode__(self):
        s = u"%s" % self.organizationcode
        if self.organizationname:
            s += u", %s" % self.organizationname
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."organizations'
        verbose_name = 'organization'


class People(models.Model):
    personid = models.AutoField(primary_key=True)
    personfirstname = models.CharField(max_length=255, verbose_name="first name")
    personmiddlename = models.CharField(max_length=255, verbose_name="middle name", blank=True)
    personlastname = models.CharField(max_length=255, verbose_name="last name")

    def __unicode__(self):
        s = u"%s" % self.personlastname
        if self.personfirstname:
            s += u", %s" % self.personfirstname
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."people'
        verbose_name = 'people'
        verbose_name_plural = 'people'
        ordering = ["personlastname"]


class Personexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    personid = models.ForeignKey(People, db_column='personid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    personexternalidentifier = models.CharField(max_length=255)
    personexternalidentifieruri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        s = u"%s - %s - %s - %s" % (
            self.personid, self.externalidentifiersystemid, self.personexternalidentifier,
            self.personexternalidentifieruri)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."personexternalidentifiers'
        verbose_name_plural = 'ORCID (Person Unique Identifier)'


class Pointcoverageresults(models.Model):
    resultid = models.OneToOneField('Results', db_column='resultid', primary_key=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid',
                                           blank=True, null=True)
    intendedxspacing = models.FloatField(blank=True, null=True)
    intendedxspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedxspacingunitsid',
                                                blank=True, null=True)
    intendedyspacing = models.FloatField(blank=True, null=True)
    intendedyspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedyspacingunitsid',
                                                blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.IntegerField()

    class Meta:
        managed = False
        db_table = r'odm2"."pointcoverageresults'


class Pointcoverageresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Pointcoverageresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."pointcoverageresultvalueannotations'


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
        db_table = r'odm2"."pointcoverageresultvalues'


class Processinglevels(models.Model):
    processinglevelid = models.AutoField(primary_key=True)
    processinglevelcode = models.CharField(verbose_name='processing level code', max_length=50)
    definition = models.CharField(max_length=5000, blank=True)
    explanation = models.CharField(max_length=5000, blank=True)

    def __unicode__(self):
        s = u"%s " % self.processinglevelcode
        if self.definition:
            s += u", %s" % self.definition
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."processinglevels'
        verbose_name = 'processing level'


class Profileresults(models.Model):
    resultid = models.OneToOneField('Results', verbose_name='result', db_column='resultid',
                                    primary_key=True)
    xlocation = models.FloatField(blank=True, verbose_name='x location', null=True)
    xlocationunitsid = models.ForeignKey('Units', verbose_name='x location units', related_name='+',
                                         db_column='xlocationunitsid', blank=True, null=True)
    ylocation = models.FloatField(blank=True, verbose_name='y location', null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', verbose_name='y location units',
                                         db_column='ylocationunitsid', blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', verbose_name='spatial reference',
                                           db_column='spatialreferenceid', blank=True, null=True)
    intendedzspacing = models.FloatField(blank=True, verbose_name='intended depth', null=True)
    intendedzspacingunitsid = models.ForeignKey('Units', verbose_name='intended depth units',
                                                related_name='+',
                                                db_column='intendedzspacingunitsid', blank=True,
                                                null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True,
                                            verbose_name='intended time spacing')
    intendedtimespacingunitsid = models.ForeignKey('Units',
                                                   verbose_name='intended time spacing unit',
                                                   related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               verbose_name='aggregation statistic',
                                               db_column='aggregationstatisticcv')

    def __unicode__(self):
        s = u"%s" % self.resultid
        if self.xlocation:
            s += u"- %s" % self.xlocation
        if self.xlocationunitsid:
            s += u", %s" % self.xlocationunitsid
        if self.ylocation:
            s += u"- %s" % self.ylocation
        if self.ylocationunitsid:
            s += u", %s" % self.ylocationunitsid
        if self.intendedzspacing:
            s += u"- %s" % self.intendedzspacing
        if self.intendedzspacingunitsid:
            s += u", %s" % self.intendedzspacingunitsid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."profileresults'
        verbose_name = 'profile result'


class Profileresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Profileresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."profileresultvalueannotations'


class Profileresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Profileresults, db_column='resultid')
    datavalue = models.FloatField(verbose_name='data value')
    valuedatetime = models.DateTimeField(verbose_name='value date and time', blank=True, null=True)
    valuedatetimeutcoffset = models.IntegerField(verbose_name='value date and time UTC offset',
                                                 blank=True, null=True)
    zlocation = models.FloatField(verbose_name='z location', blank=True, null=True)
    zaggregationinterval = models.FloatField(verbose_name='z aggregation interval', blank=True,
                                             null=True)
    zlocationunitsid = models.ForeignKey('Units', verbose_name='z location unit', related_name='+',
                                         db_column='zlocationunitsid', blank=True, null=True)
    censorcodecv = models.ForeignKey(CvCensorcode, verbose_name='censor code',
                                     db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, verbose_name='quality code',
                                      db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField(verbose_name='time aggregation interval',
                                                blank=True, null=True)
    timeaggregationintervalunitsid = models.ForeignKey('Units',
                                                       verbose_name='time aggregation ' +
                                                                    'interval unit',
                                                       related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       blank=True, null=True)

    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u", %s" % self.datavalue
        s += u", %s" % self.zlocation
        # s += u", %s" % (self.zaggregationinterval)
        s += u", %s" % self.zlocationunitsid
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        # s += 'Date and Time,'
        s += 'depth,'
        # s += '\" {0}{1}\",'.format(self.resultid.resultid.variableid
        # .variablecode,self.resultid.resultid.unitsid.unitsname)
        s += 'sampling feature/location,'
        s += 'sampling feature uri,'
        s += 'method,'
        s += 'citation'
        # s = buildCitation(s,self)
        return s

    def cite(self):
        s = buildCitation('', self)
        return s

    def csvheaderShort(self):
        # s='databaseid,'
        s = ',\" {0} -unit-{1}-processing level-{2}\"'.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level)
        # s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        return s

    def csvoutput(self):
        s = '{0}'.format(self.resultid.resultid.resultid)  # .samplingfeatureid.samplingfeatureid
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}-{1} {2} '.format((self.zlocation - self.zaggregationinterval), self.zlocation,
                                     self.zlocationunitsid)
        # s += ', {0}'.format(self.zaggregationinterval)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        s += ',\" {0}\"'.format(
            self.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)
        try:
            sfei = Samplingfeatureexternalidentifiers.objects.filter(
                samplingfeatureid=self.resultid.resultid.featureactionid.samplingfeatureid).get()
            s += ', {0}'.format(sfei.samplingfeatureexternalidentifieruri)
        except Samplingfeatureexternalidentifiers.DoesNotExist:
            s += ','
        s += ',\" {0}\"'.format(
            self.resultid.resultid.featureactionid.action.method.methoddescription)
        s = buildCitation(s, self)
        s += ','
        return s

    def csvoutputShort(self):
        # s = '{0}'.format(self.resultid.resultid.featureactionid.
        # samplingfeatureid.samplingfeatureid)
        s = '{0}'.format(self.datavalue)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        s += ','
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."profileresultvalues'
        verbose_name = 'profile result value'


class Referencematerialexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    referencematerialid = models.ForeignKey('Referencematerials', db_column='referencematerialid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    referencematerialexternalidentifier = models.CharField(max_length=255)
    referencematerialexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."referencematerialexternalidentifiers'


class Referencematerials(models.Model):
    referencematerialid = models.AutoField(primary_key=True)
    referencematerialmediumcv = models.ForeignKey(CvReferencematerialmedium,
                                                  db_column='referencematerialmediumcv')
    referencematerialorganizationid = models.ForeignKey(Organizations,
                                                        db_column='referencematerialorganizationid')
    referencematerialcode = models.CharField(max_length=50)
    referencemateriallotcode = models.CharField(max_length=255, blank=True)
    referencematerialpurchasedate = models.DateTimeField(blank=True, null=True)
    referencematerialexpirationdate = models.DateTimeField(blank=True, null=True)
    referencematerialcertificatelink = models.CharField(max_length=255, blank=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid',
                                          blank=True, null=True)

    class Meta:
        managed = False
        db_table = r'odm2"."referencematerials'


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
        db_table = r'odm2"."referencematerialvalues'


class Relatedactions(models.Model):
    relationid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, verbose_name='action', db_column='actionid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, verbose_name='relationship type',
                                           db_column='relationshiptypecv')
    relatedactionid = models.ForeignKey(Actions, verbose_name='related action',
                                        related_name='RelatedActions',
                                        db_column='relatedactionid')

    def __unicode__(self):
        s = u"%s" % self.actionid
        if self.relationshiptypecv:
            s += u", %s" % self.relationshiptypecv
        if self.relatedactionid:
            s += u", %s" % self.relatedactionid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."relatedactions'
        verbose_name = 'related action (associates one action with another)'
        verbose_name_plural = 'related action (associates one action with another)'


class Relatedannotations(models.Model):
    relationid = models.AutoField(primary_key=True)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedannotationid = models.ForeignKey(Annotations, related_name='RelatedAnnotations',
                                            db_column='relatedannotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."relatedannotations'


class Relatedcitations(models.Model):
    relationid = models.AutoField(primary_key=True)
    citationid = models.ForeignKey(Citations, db_column='citationid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedcitationid = models.ForeignKey(Citations, related_name='RelatedCitations',
                                          db_column='relatedcitationid')

    class Meta:
        managed = False
        db_table = r'odm2"."relatedcitations'


class Relateddatasets(models.Model):
    relationid = models.AutoField(primary_key=True)
    datasetid = models.ForeignKey(Datasets, db_column='datasetid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relateddatasetid = models.ForeignKey(Datasets, related_name='relatedDataset',
                                         db_column='relateddatasetid')
    versioncode = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."relateddatasets'


class Relatedequipment(models.Model):
    relationid = models.AutoField(primary_key=True)
    equipmentid = models.ForeignKey(Equipment, db_column='equipmentid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedequipmentid = models.ForeignKey(Equipment, related_name='RelatedEquipment',
                                           db_column='relatedequipmentid')
    relationshipstartdatetime = models.DateTimeField()
    relationshipstartdatetimeutcoffset = models.IntegerField()
    relationshipenddatetime = models.DateTimeField(blank=True, null=True)
    relationshipenddatetimeutcoffset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = r'odm2"."relatedequipment'


class Relatedfeatures(models.Model):
    relationid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', verbose_name="first feature",
                                          db_column='samplingfeatureid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, verbose_name="relationship type",
                                           db_column='relationshiptypecv')
    relatedfeatureid = models.ForeignKey('Samplingfeatures', verbose_name="second feature",
                                         related_name='RelatedFeatures',
                                         db_column='relatedfeatureid')
    spatialoffsetid = models.ForeignKey('Spatialoffsets', verbose_name="spatial offset",
                                        db_column='spatialoffsetid',
                                        blank=True, null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (
            self.samplingfeatureid, self.relationshiptypecv, self.relatedfeatureid)

    class Meta:
        managed = False
        db_table = r'odm2"."relatedfeatures'
        verbose_name = 'relate two feature'


class Relatedmodels(models.Model):
    relatedid = models.AutoField(primary_key=True)
    modelid = models.ForeignKey(Models, db_column='modelid')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv')
    relatedmodelid = models.IntegerField()

    class Meta:
        managed = False
        db_table = r'odm2"."relatedmodels'


class Relatedresults(models.Model):
    relationid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid', verbose_name='data result')
    relationshiptypecv = models.ForeignKey(CvRelationshiptype, db_column='relationshiptypecv',
                                           verbose_name='relationship type')
    relatedresultid = models.ForeignKey('Results', related_name='RelatedResult',
                                        db_column='relatedresultid',
                                        verbose_name='related data result')
    versioncode = models.CharField(max_length=50, blank=True, verbose_name='version code')
    relatedresultsequencenumber = models.IntegerField(blank=True, null=True,
                                                      verbose_name='related result sequence number')

    def __unicode__(self):
        return u"%s - %s - %s" % (
            self.resultid, self.relationshiptypecv, self.relatedresultid)
    class Meta:
        managed = False
        db_table = r'odm2"."relatedresults'
        verbose_name = 'related result'


class Resultannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')
    begindatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = r'odm2"."resultannotations'


class Resultderivationequations(models.Model):
    resultid = models.OneToOneField('Results', db_column='resultid',
                                    verbose_name='data result', primary_key=True)
    derivationequationid = models.ForeignKey(Derivationequations, db_column='derivationequationid')

    def __unicode__(self):
        return u"%s - %s" % (self.resultid, self.derivationequationid)

    class Meta:
        managed = False
        db_table = r'odm2"."resultderivationequations'
        verbose_name='result derivation equation'


class Resultextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey('Results', db_column='resultid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s - %s: value %s" % (self.resultid, self.propertyid,self.propertyvalue)
    class Meta:
        managed = False
        db_table = r'odm2"."resultextensionpropertyvalues'


class Resultnormalizationvalues(models.Model):
    resultid = models.OneToOneField('Results', db_column='resultid', primary_key=True)
    normalizedbyreferencematerialvalueid = models.ForeignKey(
        Referencematerialvalues,
        db_column='normalizedbyreferencematerialvalueid'
    )

    class Meta:
        managed = False
        db_table = r'odm2"."resultnormalizationvalues'


class Results(models.Model):
    resultid = models.AutoField(primary_key=True, verbose_name="data result")
    resultuuid = UUIDField(default=uuid.uuid4, editable=False)
    featureactionid = models.ForeignKey(Featureactions, related_name="feature_actions",
                                        verbose_name="sampling feature action",
                                        db_column='featureactionid')
    result_type = models.ForeignKey(CvResulttype, verbose_name='result type',
                                    db_column='resulttypecv')
    variableid = models.ForeignKey('Variables', verbose_name='variable', db_column='variableid')
    unitsid = models.ForeignKey('Units', verbose_name='units', related_name='+',
                                db_column='unitsid')
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers',
                                              verbose_name='taxonomic classifier',
                                              db_column='taxonomicclassifierid', blank=True,
                                              null=True)
    processing_level = models.ForeignKey(Processinglevels, db_column='processinglevelid')
    resultdatetime = models.DateTimeField(verbose_name='Start result date time', blank=True,
                                          null=True)
    resultdatetimeutcoffset = models.BigIntegerField(
        verbose_name='Start result date time UTC offset', default=4,
        null=True)
    # validdatetime>> Date and time for which the result is valid (e.g., for a forecast result).
    # Should probably be expressed as a duration
    validdatetime = models.DateTimeField(
        verbose_name='valid date time- Date and time for which the result is valid',
        blank=True, null=True)
    validdatetimeutcoffset = models.BigIntegerField(verbose_name='valid date time UTC offset',
                                                    default=4, null=True)
    statuscv = models.ForeignKey(CvStatus, verbose_name='status', db_column='statuscv', blank=True,
                                 null=True)
    sampledmediumcv = models.ForeignKey(CvMedium, verbose_name='sampled medium',
                                        db_column='sampledmediumcv',
                                        blank=True, null=True)
    valuecount = models.IntegerField(verbose_name='number of recorded values')

    # def __unicode__(self):
    #    return u'%s - %s' % (self.resultid, self.feature_action)
    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        s += 'time aggregation interval,'
        s += 'time aggregation unit,'
        #s += 'citation,'

        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variableid.variablecode,
            self.unitsid.unitsname,
            self.processing_level.processinglevelcode)
        return s

    def csvheaderShort(self):
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variableid.variablecode,
            self.unitsid.unitsabbreviation,
            self.processing_level.processinglevelcode)
        return s
    def __unicode__(self):
        return u"%s - %s - ID: %s" % (self.variableid, self.featureactionid, self.resultid)

    class Meta:
        managed = False
        db_table = r'odm2"."results'
        verbose_name = 'data result'
        ordering = ["variableid"]


class Resultsdataquality(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Results, db_column='resultid', verbose_name='result')
    dataqualityid = models.ForeignKey(Dataquality, db_column='dataqualityid',
                                      verbose_name='data quality')

    def __unicode__(self):
        return u"%s - %s" % (self.resultid, self.dataqualityid)

    class Meta:
        managed = False
        db_table = r'odm2"."resultsdataquality'
        verbose_name = 'results data quality'
        verbose_name_plural = 'results data quality'


class Samplingfeatureannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    def __unicode__(self):
        s = u"%s" % self.samplingfeatureid
        if self.annotationid:
            s += u"- %s" % self.annotationid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."samplingfeatureannotations'


class Samplingfeatureextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    def __unicode__(self):
        s = u"%s" % self.samplingfeatureid
        if self.propertyvalue:
            s += u"- %s - %s%s" % (self.propertyid.propertyname, self.propertyvalue, self.propertyid.propertyunitsid.unitsabbreviation)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."samplingfeatureextensionpropertyvalues'


class Samplingfeatureexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    samplingfeatureexternalidentifier = models.CharField(max_length=255)
    samplingfeatureexternalidentifieruri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        s = u"%s - %s - %s - %s" % (
            self.samplingfeatureid, self.externalidentifiersystemid,
            self.samplingfeatureexternalidentifier,
            self.samplingfeatureexternalidentifieruri)
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."samplingfeatureexternalidentifiers'


class Samplingfeatures(models.Model):
    samplingfeatureid = models.AutoField(primary_key=True)
    samplingfeatureuuid = UUIDField(default=uuid.uuid4, editable=False)
    sampling_feature_type = models.ForeignKey(CvSamplingfeaturetype,
                                              db_column='samplingfeaturetypecv')
    samplingfeaturecode = models.CharField(verbose_name='sampling feature or location code', max_length=50)
    samplingfeaturename = models.CharField(verbose_name='sampling feature or location name', max_length=255,
                                           blank=True, null=True)
    samplingfeaturedescription = models.CharField(verbose_name='sampling feature or location description',
                                                  max_length=5000,
                                                  blank=True)
    sampling_feature_geo_type = models.ForeignKey(CvSamplingfeaturegeotype,
                                                  db_column='samplingfeaturegeotypecv',
                                                  default="Point", null=True)
    featuregeometry = models.TextField(verbose_name='feature geometry', blank=True,
                                       null=True)  # GeometryField This field type is a guess.
    elevation_m = models.FloatField(verbose_name='elevation', blank=True, null=True)
    elevation_datum = models.ForeignKey(CvElevationdatum, db_column='elevationdatumcv', blank=True,
                                        null=True)

    objects = gis_models.GeoManager()

    def featuregeometrywkt(self):
        return GEOSGeometry(self.featuregeometry)

    def __unicode__(self):
        s = u"%s - %s- %s" % (
            self.samplingfeaturecode, self.samplingfeatureid, self.sampling_feature_type)
        if self.samplingfeaturename:
            s += u" - %s" % self.samplingfeaturename
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."samplingfeatures'
        ordering = ('sampling_feature_type', 'samplingfeaturename',)
        verbose_name = 'sampling feature (location)'


class Sectionresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         blank=True, null=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid',
                                           blank=True, null=True)
    intendedxspacing = models.FloatField(blank=True, null=True)
    intendedxspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedxspacingunitsid',
                                                blank=True, null=True)
    intendedzspacing = models.FloatField(blank=True, null=True)
    intendedzspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedzspacingunitsid',
                                                blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = r'odm2"."sectionresults'


class Sectionresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Sectionresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."sectionresultvalueannotations'


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
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = r'odm2"."sectionresultvalues'


class Simulations(models.Model):
    simulationid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid')
    simulationname = models.CharField(max_length=255)
    simulationdescription = models.CharField(max_length=5000, blank=True)
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
        db_table = r'odm2"."simulations'


class Sites(models.Model):
    samplingfeatureid = models.OneToOneField(Samplingfeatures, db_column='samplingfeatureid',
                                             primary_key=True, verbose_name='sampling feature')
    sitetypecv = models.ForeignKey(CvSitetype, db_column='sitetypecv')
    latitude = models.FloatField()
    longitude = models.FloatField()
    spatialreferenceid = models.ForeignKey('Spatialreferences', verbose_name='spatial reference id',
                                           db_column='spatialreferenceid')

    class Meta:
        managed = False
        verbose_name = 'Site'
        db_table = r'odm2"."sites'

    def __unicode__(self):
        s = u"%s" % self.samplingfeatureid
        s += u"- %s" % self.sitetypecv
        return s

class Spatialoffsets(models.Model):
    spatialoffsetid = models.AutoField(primary_key=True)
    spatialoffsettypecv = models.ForeignKey(CvSpatialoffsettype, db_column='spatialoffsettypecv')
    offset1value = models.FloatField()
    offset1unitid = models.ForeignKey('Units', related_name='+', db_column='offset1unitid')
    offset2value = models.FloatField(blank=True, null=True)
    offset2unitid = models.ForeignKey('Units', related_name='+', db_column='offset2unitid',
                                      blank=True, null=True)
    offset3value = models.FloatField(blank=True, null=True)
    offset3unitid = models.ForeignKey('Units', related_name='+', db_column='offset3unitid',
                                      blank=True, null=True)

    class Meta:
        managed = False
        db_table = r'odm2"."spatialoffsets'


class Spatialreferenceexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    spatialreferenceexternalidentifier = models.CharField(max_length=255)
    spatialreferenceexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."spatialreferenceexternalidentifiers'


class Spatialreferences(models.Model):
    spatialreferenceid = models.AutoField(primary_key=True, verbose_name='spatial reference id')
    srscode = models.CharField(max_length=50, blank=True, verbose_name='spatial reference code')
    srsname = models.CharField(max_length=255, verbose_name='spatial reference name')
    srsdescription = models.CharField(max_length=5000, blank=True,
                                      verbose_name='spatial reference description')
    srslink = models.CharField(max_length=255, blank=True,verbose_name='spatial reference link')

    class Meta:
        managed = False
        verbose_name = 'Spatial reference'
        db_table = r'odm2"."spatialreferences'

    def __unicode__(self):
        if self.srscode:
            s = u"%s" % self.srscode
        s += u"- %s" % self.srsname
        return s

class Specimenbatchpostions(models.Model):
    featureactionid = models.OneToOneField(Featureactions, db_column='featureactionid',
                                           primary_key=True)
    batchpositionnumber = models.IntegerField()
    batchpositionlabel = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."specimenbatchpostions'


class Specimens(models.Model):
    samplingfeatureid = models.OneToOneField(Samplingfeatures, db_column='samplingfeatureid',
                                             primary_key=True)
    specimentypecv = models.ForeignKey(CvSpecimentype, db_column='specimentypecv')
    specimenmediumcv = models.ForeignKey(CvSpecimenmedium, db_column='specimenmediumcv')
    isfieldspecimen = models.BooleanField()

    def __unicode__(self):
        return u'{spectypecv} - {specmedcv}'.format(spectypecv=self.specimentypecv,
                                                    specmedcv=self.specimenmediumcv)

    class Meta:
        managed = False
        verbose_name = 'Specimen'
        db_table = r'odm2"."specimens'


class Specimentaxonomicclassifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey(Specimens, db_column='samplingfeatureid')
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers',
                                              db_column='taxonomicclassifierid')
    citationid = models.ForeignKey(Citations, db_column='citationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = r'odm2"."specimentaxonomicclassifiers'


class Spectraresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                         blank=True, null=True)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True)
    intendedwavelengthspacing = models.FloatField(blank=True, null=True)
    intendedwavelengthspacingunitsid = models.ForeignKey(
        'Units',
        related_name='+',
        db_column='intendedwavelengthspacingunitsid',
        blank=True,
        null=True
    )
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = r'odm2"."spectraresults'


class Spectraresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Spectraresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."spectraresultvalueannotations'


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
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = r'odm2"."spectraresultvalues'


class Taxonomicclassifierexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers',
                                              db_column='taxonomicclassifierid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    taxonomicclassifierexternalidentifier = models.CharField(max_length=255)
    taxonomicclassifierexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."taxonomicclassifierexternalidentifiers'

        # I needed to add a sequence and set it as the default for the primary
        #  key to make the Taxonomic Classifiers class work
        # this is the SQL

        # CREATE SEQUENCE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
        #   INCREMENT 1
        #   MINVALUE 2
        #   MAXVALUE 9223372036854775807
        #   START 3
        #   CACHE 1;
        # ALTER TABLE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
        #   OWNER TO postgres;

        # ALTER TABLE odm2.taxonomicclassifiers
        #  ALTER COLUMN taxonomicclassifierid SET DEFAULT nextval
        # ('odm2.taxonomicclassifiers_taxonomicclassifiersid_seq'::regclass);


class Taxonomicclassifiers(models.Model):
    taxonomicclassifierid = models.AutoField(primary_key=True)
    taxonomic_classifier_type = models.ForeignKey(CvTaxonomicclassifiertype,
                                                  db_column='taxonomicclassifiertypecv',
                                                  help_text="A vocabulary for describing "
                                                            "types of taxonomies from which "
                                                            "descriptive terms used "
                                                            "in an ODM2 database have been drawn. "
                                                            "Taxonomic classifiers provide "
                                                            "a way to classify"
                                                            " Results and Specimens "
                                                            "according to terms from a formal "
                                                            "taxonomy.. Check "
                                                            "http://vocabulary.odm2.org/"
                                                            "taxonomicclassifiertype/  "
                                                            "for more info")
    taxonomicclassifiername = models.CharField(verbose_name='taxonomic classifier name',
                                               max_length=255)
    taxonomicclassifiercommonname = models.CharField(
        verbose_name='taxonomic classifier common name', max_length=255,
        blank=True)
    taxonomicclassifierdescription = models.CharField(
        verbose_name='taxonomic classifier description', max_length=5000,
        blank=True)
    parent_taxonomic_classifier = models.ForeignKey('self', db_column='parenttaxonomicclassifierid',
                                                    blank=True,
                                                    null=True)

    def __unicode__(self):
        s = u"%s" % self.taxonomicclassifiername
        if self.taxonomicclassifiercommonname:
            s += u"- %s" % self.taxonomicclassifiercommonname
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."taxonomicclassifiers'
        verbose_name = 'taxonomic classifier'


class Timeseriesresults(models.Model):
    resultid = models.OneToOneField(Results, verbose_name="Result Series", db_column='resultid',
                                    primary_key=True)
    xlocation = models.FloatField(blank=True, null=True, verbose_name="x location")
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                         blank=True, null=True, verbose_name="x location units")
    ylocation = models.FloatField(blank=True, null=True, verbose_name="y location")
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         verbose_name="y location units", blank=True, null=True)
    zlocation = models.FloatField(blank=True, null=True, verbose_name="z location")
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         verbose_name="z location units", blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           verbose_name="spatial reference",
                                           blank=True, null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True, verbose_name="Intended time spacing",
                                            help_text="time between measurements")
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   help_text="Units of time between measurements. This defines the time"
                                                             " series 1 hour, or 15 minutes for example.",
                                                   verbose_name="Time Units",
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')

    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u", %s" % self.intendedtimespacing
        s += u", %s" % self.intendedtimespacingunitsid
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."timeseriesresults'
        ordering = ['resultid']
        verbose_name = 'time series result'


class Timeseriesresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Timeseriesresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."timeseriesresultvalueannotations'


class Timeseriesresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Timeseriesresults, db_column='resultid')
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       verbose_name="Time Units",
                                                       db_column='timeaggregationintervalunitsid')

    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        s += 'citation,'

        return s

    def csvoutput(self):
        s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s


    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level.processinglevelcode)
        return s

    def csvheaderShort(self):
        # s = 'method,'
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level.processinglevelcode)
        s += 'quality code,'
        s += 'annotation,'
        return s

    def csvoutputShort(self):
        #s = '\" {0}\",'.format(
        #    self.resultid.resultid.featureactionid.action.method.methodcode)
        s = '{0},'.format(self.datavalue)
        s += '{0}'.format(self.qualitycodecv)
        trvannotation = Timeseriesresultvalueannotations.objects.filter(valueid=self.valueid)
        annotations = Annotations.objects.filter(annotationid__in=trvannotation)
        s += ',\"'
        for anno in annotations:
            s += '{0} '.format(anno)
        s += '\"'
        s += ','
        return s

    class Meta:
        managed = False
        db_table = r'odm2"."timeseriesresultvalues'
        verbose_name = 'time series result value'


class Timeseriesresultvaluesext(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Timeseriesresults, db_column='resultid',
                                 on_delete=models.DO_NOTHING)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.DO_NOTHING)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.DO_NOTHING)
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       verbose_name="Time Units",
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.DO_NOTHING)
    samplingfeaturename = models.CharField(verbose_name='sampling feature name',
                                           max_length=255, blank=True, null=True)
    sampling_feature_type = models.ForeignKey(CvSamplingfeaturetype,
                                              db_column='samplingfeaturetypecv',
                                              on_delete=models.DO_NOTHING)
    processinglevelcode = models.CharField(verbose_name='processing level code', max_length=50)
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    aggregationstatisticname = models.CharField(primary_key=True, max_length=255)
    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        #s += 'citation,'

        return s
    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'location- {0}'.format(self.samplingfeaturename)
        return s
    def csvheaderShort(self):
        s = 'method,'
        s += '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'quality code,'
        return s
    def csvoutput(self):
        s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.samplingfeaturename)
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        #s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s



    def csvoutputShort(self):
        s = '\" {0}\",'.format(
            self.resultid.resultid.featureactionid.action.method.methodcode)
        s += '{0},'.format(self.datavalue)
        s += '{0},'.format(self.qualitycodecv)
        return s

    class Meta:
        managed = False
        db_table = r'odm2extra"."timeseriesresultvaluesext'
        verbose_name = 'time series result value'


class Timeseriesresultvaluesextwannotations(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.IntegerField()
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.CharField(max_length=255)
    qualitycodecv = models.CharField(max_length=255)
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.IntegerField()
    samplingfeaturename = models.CharField(verbose_name='sampling feature name',
                                           max_length=255, blank=True, null=True)
    samplingfeaturetypecv = models.CharField(max_length=255)
    processinglevelcode = models.CharField(verbose_name='processing level code', max_length=50)
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    aggregationstatisticname = models.CharField(primary_key=True, max_length=255)
    annotationtext = models.CharField(max_length=500)
    def __unicode__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        # s = 'databaseid,'
        # s+='Value,'
        s = 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        s += 'citation,'
        return s

    def csvoutput(self):
        # s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s = '{0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.samplingfeaturename)
        s += ','
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'location- {0}'.format(self.samplingfeaturename)
        return s

    def csvheaderShort(self):
        # s = 'method,'
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'quality code,'
        s += 'quality annotation,'
        return s

    def csvoutputShort(self):
        # result = Results.objects.get(resultid=self.resultid)
        # s = '\" {0}\",'.format(
        #     result.featureactionid.action.method.methodcode)
        s = '{0},'.format(self.datavalue)
        s += '{0},'.format(self.qualitycodecv)
        if self.annotationtext:
            s += '\"{0} \",'.format(self.annotationtext)
        else:
             s += ','
        return s

    class Meta:
        managed = False
        db_table = r'odm2extra"."timeseriesresultvaluesextwannotations'
        verbose_name = 'time series result value'

class Trajectoryresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True)
    intendedtrajectoryspacing = models.FloatField(blank=True, null=True)
    intendedtrajectoryspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                         db_column='intendedtrajec'
                                                                   'toryspacingunitsid',
                                                         blank=True,
                                                         null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = r'odm2"."trajectoryresults'


class Trajectoryresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Trajectoryresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."trajectoryresultvalueannotations'


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
    trajectorydistanceunitsid = models.ForeignKey('Units', related_name='+',
                                                  db_column='trajectorydistanceunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = r'odm2"."trajectoryresultvalues'


class Transectresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         blank=True, null=True)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True)
    intendedtransectspacing = models.FloatField(blank=True, null=True)
    intendedtransectspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='intendedtransectspacingunitsid',
                                                       blank=True,
                                                       null=True)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')

    class Meta:
        managed = False
        db_table = r'odm2"."transectresults'


class Transectresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Transectresultvalues', db_column='valueid')
    annotationid = models.ForeignKey(Annotations, db_column='annotationid')

    class Meta:
        managed = False
        db_table = r'odm2"."transectresultvalueannotations'


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
    transectdistanceunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='transectdistanceunitsid')
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv')
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv')
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv')
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid')

    class Meta:
        managed = False
        db_table = r'odm2"."transectresultvalues'


class Units(models.Model):
    unitsid = models.AutoField(primary_key=True)
    unit_type = models.ForeignKey(CvUnitstype,
                                  help_text="A vocabulary for describing the type of the Unit "
                                            "or the more general quantity that the Unit "
                                            "represents. View unit type details here "
                                            "http://vocabulary.odm2.org/unitstype/",
                                  db_column='unitstypecv')
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    unitsname = models.CharField(verbose_name='unit name', max_length=255)
    unitslink = models.CharField(verbose_name='reference for the unit (web link)',
                                 max_length=255,
                                 blank=True)

    def __unicode__(self):
        s = u"%s" % self.unitsabbreviation
        # if self.unit_type:
        #    s = u"- %s" % (self.unit_type)
        if self.unitsname:
            s += u"- %s" % self.unitsname
        return s

    class Meta:
        managed = False
        ordering = ('unitsabbreviation', 'unitsname',)
        db_table = r'odm2"."units'
        verbose_name = 'unit'


class Variableextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid')
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid')
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = r'odm2"."variableextensionpropertyvalues'


class Variableexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid')
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid')
    variableexternalidentifier = models.CharField(max_length=255)
    variableexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = r'odm2"."variableexternalidentifiers'


class Variables(models.Model):
    variableid = models.AutoField(primary_key=True)
    variable_type = models.ForeignKey(CvVariabletype,
                                      help_text="view variable types here "
                                                "http://vocabulary.odm2.org/variabletype/ ",
                                      db_column='variabletypecv')
    # variabletypecv = models.ModelChoiceField(CvVariabletype, db_column='variabletypecv')
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    variable_name = models.ForeignKey(CvVariablename,
                                      help_text="view variable names here "
                                                "http://vocabulary.odm2.org/variablename/",
                                      db_column='variablenamecv')
    variabledefinition = models.CharField(verbose_name='variable definition', max_length=500,
                                          blank=True)
    # variabledefinition.name = 'variable_definition'
    speciation = models.ForeignKey(CvSpeciation, db_column='speciationcv', blank=True, null=True)
    nodatavalue = models.FloatField(verbose_name='no data value')

    def __unicode__(self):
        s = "%s" % self.variablecode
        if self.variabledefinition:
            s += " - %s" % self.variabledefinition[:20]
        return s

    class Meta:
        managed = False
        ordering = ('variablecode', 'variable_name',)
        db_table = r'odm2"."variables'
        verbose_name = 'variable'
