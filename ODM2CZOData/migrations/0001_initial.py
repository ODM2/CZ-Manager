# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actionannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'actionannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actionby',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('isactionlead', models.BooleanField()),
                ('roledescription', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'actionby',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actiondirectives',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'actiondirectives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actionextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'actionextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('actionid', models.IntegerField(serialize=False, primary_key=True)),
                ('begindatetime', models.DateTimeField()),
                ('begindatetimeutcoffset', models.IntegerField()),
                ('enddatetime', models.DateTimeField(null=True, blank=True)),
                ('enddatetimeutcoffset', models.IntegerField(null=True, blank=True)),
                ('actiondescription', models.CharField(blank=True, max_length=500)),
                ('actionfilelink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'actions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('affiliationid', models.IntegerField(serialize=False, primary_key=True)),
                ('isprimaryorganizationcontact', models.NullBooleanField()),
                ('affiliationstartdate', models.DateField()),
                ('affiliationenddate', models.DateField(null=True, blank=True)),
                ('primaryphone', models.CharField(blank=True, max_length=50)),
                ('primaryemail', models.CharField(max_length=255)),
                ('primaryaddress', models.CharField(blank=True, max_length=255)),
                ('personlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'affiliations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Annotations',
            fields=[
                ('annotationid', models.IntegerField(serialize=False, primary_key=True)),
                ('annotationcode', models.CharField(blank=True, max_length=50)),
                ('annotationtext', models.CharField(max_length=500)),
                ('annotationdatetime', models.DateTimeField(null=True, blank=True)),
                ('annotationutcoffset', models.IntegerField(null=True, blank=True)),
                ('annotationlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'annotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Authorlists',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('authororder', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'authorlists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Calibrationactions',
            fields=[
                ('actionid',
                 models.ForeignKey(db_column='actionid', to='odm2testapp.Actions', serialize=False,
                                   primary_key=True)),
                ('calibrationcheckvalue', models.FloatField(null=True, blank=True)),
                ('calibrationequation', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'calibrationactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Calibrationreferenceequipment',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'calibrationreferenceequipment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Calibrationstandards',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'calibrationstandards',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoricalresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'categoricalresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoricalresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.CharField(max_length=255)),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'categoricalresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Citationextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'citationextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Citationexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('citationexternalidentifer', models.CharField(max_length=255)),
                ('citationexternalidentiferuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'citationexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Citations',
            fields=[
                ('citationid', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
                ('publicationyear', models.IntegerField()),
                ('citationlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'citations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvActiontype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_actiontype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvAggregationstatistic',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_aggregationstatistic',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvAnnotationtype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_annotationtype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvCensorcode',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_censorcode',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvDataqualitytype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_dataqualitytype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvDatasettypecv',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_datasettypecv',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvDirectivetype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_directivetype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvElevationdatum',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_elevationdatum',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvEquipmenttype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_equipmenttype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvMethodtype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_methodtype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvOrganizationtype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_organizationtype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvPropertydatatype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_propertydatatype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvQualitycode',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_qualitycode',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvReferencematerialmedium',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_referencematerialmedium',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvRelationshiptype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_relationshiptype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvResulttype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_resulttype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSampledmedium',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_sampledmedium',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSamplingfeaturegeotype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_samplingfeaturegeotype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSamplingfeaturetype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_samplingfeaturetype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSitetype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_sitetype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSpatialoffsettype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_spatialoffsettype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSpeciation',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_speciation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSpecimenmedium',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_specimenmedium',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvSpecimentype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_specimentype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvStatus',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_status',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvTaxonomicclassifiertype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_taxonomicclassifiertype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvUnitstype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_unitstype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvVariablename',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_variablename',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CvVariabletype',
            fields=[
                ('term', models.CharField(max_length=255)),
                ('name', models.CharField(primary_key=True, serialize=False, max_length=255)),
                ('definition', models.CharField(blank=True, max_length=1000)),
                ('category', models.CharField(blank=True, max_length=255)),
                ('sourcevocabularyuri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'cv_variabletype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataloggerfilecolumns',
            fields=[
                ('dataloggerfilecolumnid', models.IntegerField(serialize=False, primary_key=True)),
                ('columnlabel', models.CharField(max_length=50)),
                ('columndescription', models.CharField(blank=True, max_length=500)),
                ('measurementequation', models.CharField(blank=True, max_length=255)),
                ('scaninterval', models.FloatField(null=True, blank=True)),
                ('recordinginterval', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'dataloggerfilecolumns',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataloggerfiles',
            fields=[
                ('dataloggerfileid', models.IntegerField(serialize=False, primary_key=True)),
                ('dataloggerfilename', models.CharField(max_length=255)),
                ('dataloggerfiledescription', models.CharField(blank=True, max_length=500)),
                ('dataloggerfilelink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'dataloggerfiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataloggerprogramfiles',
            fields=[
                ('programid', models.IntegerField(serialize=False, primary_key=True)),
                ('programname', models.CharField(max_length=255)),
                ('programdescription', models.CharField(blank=True, max_length=500)),
                ('programversion', models.CharField(blank=True, max_length=50)),
                ('programfilelink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'dataloggerprogramfiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataquality',
            fields=[
                ('dataqualityid', models.IntegerField(serialize=False, primary_key=True)),
                ('dataqualitycode', models.CharField(max_length=255)),
                ('dataqualityvalue', models.FloatField(null=True, blank=True)),
                ('dataqualitydescription', models.CharField(blank=True, max_length=500)),
                ('dataqualitylink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'dataquality',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datasetcitations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'datasetcitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datasets',
            fields=[
                ('datasetid', models.IntegerField(serialize=False, primary_key=True)),
                ('datasetuuid', models.TextField()),
                ('datasetcode', models.CharField(max_length=50)),
                ('datasettitle', models.CharField(max_length=255)),
                ('datasetabstract', models.CharField(max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'datasets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datasetsresults',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'datasetsresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Derivationequations',
            fields=[
                ('derivationequationid', models.IntegerField(serialize=False, primary_key=True)),
                ('derivationequation', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'derivationequations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Directives',
            fields=[
                ('directiveid', models.IntegerField(serialize=False, primary_key=True)),
                ('directivedescription', models.CharField(max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'directives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('equipmentid', models.IntegerField(serialize=False, primary_key=True)),
                ('equipmentcode', models.CharField(max_length=50)),
                ('equipmentname', models.CharField(max_length=255)),
                ('equipmentserialnumber', models.CharField(max_length=50)),
                ('equipmentpurchasedate', models.DateTimeField()),
                ('equipmentpurchaseordernumber', models.CharField(blank=True, max_length=50)),
                ('equipmentdescription', models.CharField(blank=True, max_length=500)),
                ('equipmentdocumentationlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'equipment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipmentannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'equipmentannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipmentmodels',
            fields=[
                ('equipmentmodelid', models.IntegerField(serialize=False, primary_key=True)),
                ('modelpartnumber', models.CharField(blank=True, max_length=50)),
                ('modelname', models.CharField(max_length=255)),
                ('modeldescription', models.CharField(blank=True, max_length=500)),
                ('isinstrument', models.BooleanField()),
                ('modelspecificationsfilelink', models.CharField(blank=True, max_length=255)),
                ('modellink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'equipmentmodels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipmentused',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'equipmentused',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extensionproperties',
            fields=[
                ('propertyid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyname', models.CharField(max_length=255)),
                ('propertydescription', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'extensionproperties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Externalidentifiersystems',
            fields=[
                ('externalidentifiersystemid',
                 models.IntegerField(serialize=False, primary_key=True)),
                ('externalidentifiersystemname', models.CharField(max_length=255)),
                ('externalidentifiersystemdescription',
                 models.CharField(blank=True, max_length=500)),
                ('externalidentifiersystemurl', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'externalidentifiersystems',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Featureactions',
            fields=[
                ('featureactionid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'featureactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instrumentoutputvariables',
            fields=[
                ('instrumentoutputvariableid',
                 models.IntegerField(serialize=False, primary_key=True)),
                ('instrumentresolution', models.CharField(blank=True, max_length=255)),
                ('instrumentaccuracy', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'instrumentoutputvariables',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maintenanceactions',
            fields=[
                ('actionid',
                 models.ForeignKey(db_column='actionid', to='odm2testapp.Actions', serialize=False,
                                   primary_key=True)),
                ('isfactoryservice', models.BooleanField()),
                ('maintenancecode', models.CharField(blank=True, max_length=50)),
                ('maintenancereason', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'maintenanceactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurementresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'measurementresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurementresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'measurementresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Methodannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'methodannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Methodcitations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'methodcitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Methodextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'methodextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Methodexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('methodexternalidentifier', models.CharField(max_length=255)),
                ('methodexternalidentifieruri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'methodexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Methods',
            fields=[
                ('methodid', models.IntegerField(serialize=False, primary_key=True)),
                ('methodcode', models.CharField(max_length=50)),
                ('methodname', models.CharField(max_length=255)),
                ('methoddescription', models.CharField(blank=True, max_length=500)),
                ('methodlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'methods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modelaffiliations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('isprimary', models.BooleanField()),
                ('roledescription', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'modelaffiliations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Models',
            fields=[
                ('modelid', models.IntegerField(serialize=False, primary_key=True)),
                ('modelcode', models.CharField(max_length=50)),
                ('modelname', models.CharField(max_length=255)),
                ('modeldescription', models.CharField(blank=True, max_length=500)),
                ('version', models.CharField(blank=True, max_length=255)),
                ('modellink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'models',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('organizationid', models.IntegerField(serialize=False, primary_key=True)),
                ('organizationcode', models.CharField(max_length=50)),
                ('organizationname', models.CharField(max_length=255)),
                ('organizationdescription', models.CharField(blank=True, max_length=500)),
                ('organizationlink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'organizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('personid', models.IntegerField(serialize=False, primary_key=True)),
                ('personfirstname', models.CharField(max_length=255)),
                ('personmiddlename', models.CharField(blank=True, max_length=255)),
                ('personlastname', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'people',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('personexternalidentifier', models.CharField(max_length=255)),
                ('personexternalidentifieruri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'personexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pointcoverageresultvalueannotations',
            fields=[
                ('bridgeid', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'pointcoverageresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pointcoverageresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.BigIntegerField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
                ('xlocation', models.FloatField()),
                ('ylocation', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'pointcoverageresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Processinglevels',
            fields=[
                ('processinglevelid', models.IntegerField(serialize=False, primary_key=True)),
                ('processinglevelcode', models.CharField(max_length=50)),
                ('definition', models.CharField(blank=True, max_length=500)),
                ('explanation', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'processinglevels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profileresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'profileresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profileresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
                ('zlocation', models.FloatField()),
                ('zaggregationinterval', models.FloatField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'profileresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Referencematerialexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('referencematerialexternalidentifier', models.CharField(max_length=255)),
                ('referencematerialexternalidentifieruri',
                 models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'referencematerialexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Referencematerials',
            fields=[
                ('referencematerialid', models.IntegerField(serialize=False, primary_key=True)),
                ('referencematerialcode', models.CharField(max_length=50)),
                ('referencemateriallotcode', models.CharField(blank=True, max_length=255)),
                ('referencematerialpurchasedate', models.DateTimeField(null=True, blank=True)),
                ('referencematerialexpirationdate', models.DateTimeField(null=True, blank=True)),
                ('referencematerialcertificatelink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'referencematerials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Referencematerialvalues',
            fields=[
                ('referencematerialvalueid',
                 models.IntegerField(serialize=False, primary_key=True)),
                ('referencematerialvalue', models.FloatField()),
                ('referencematerialaccuracy', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'referencematerialvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedactions',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedannotations',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedcitations',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedcitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relateddatasets',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
                ('versioncode', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'managed': False,
                'db_table': 'relateddatasets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedequipment',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
                ('relationshipstartdatetime', models.DateTimeField()),
                ('relationshipstartdatetimeutcoffset', models.IntegerField()),
                ('relationshipenddatetime', models.DateTimeField(null=True, blank=True)),
                ('relationshipenddatetimeutcoffset', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedequipment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedfeatures',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedfeatures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedmodels',
            fields=[
                ('relatedid', models.IntegerField(serialize=False, primary_key=True)),
                ('relatedmodelid', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'relatedmodels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relatedresults',
            fields=[
                ('relationid', models.IntegerField(serialize=False, primary_key=True)),
                ('versioncode', models.CharField(blank=True, max_length=50)),
                ('relatedresultsequencenumber', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'relatedresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('begindatetime', models.DateTimeField()),
                ('enddatetime', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'resultannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'resultextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('resultid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('resultuuid', models.TextField()),
                ('resultdatetime', models.DateTimeField(null=True, blank=True)),
                ('resultdatetimeutcoffset', models.BigIntegerField(null=True, blank=True)),
                ('validdatetime', models.DateTimeField(null=True, blank=True)),
                ('validdatetimeutcoffset', models.BigIntegerField(null=True, blank=True)),
                ('valuecount', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'results',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultnormalizationvalues',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'resultnormalizationvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultderivationequations',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'resultderivationequations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profileresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('xlocation', models.FloatField(null=True, blank=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('intendedzspacing', models.FloatField(null=True, blank=True)),
                ('intendedtimespacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'profileresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pointcoverageresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('intendedxspacing', models.FloatField(null=True, blank=True)),
                ('intendedyspacing', models.FloatField(null=True, blank=True)),
                ('timeaggregationinterval', models.FloatField()),
                ('timeaggregationintervalunitsid', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'pointcoverageresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurementresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('xlocation', models.FloatField(null=True, blank=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'measurementresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoricalresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('xlocation', models.FloatField(null=True, blank=True)),
                ('xlocationunitsid', models.IntegerField(null=True, blank=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('ylocationunitsid', models.IntegerField(null=True, blank=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('zlocationunitsid', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'categoricalresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultsdataquality',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'resultsdataquality',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Samplingfeatureannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'samplingfeatureannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Samplingfeatureextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'samplingfeatureextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Samplingfeatureexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('samplingfeatureexternalidentifier', models.CharField(max_length=255)),
                ('samplingfeatureexternalidentifieruri',
                 models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'samplingfeatureexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Samplingfeatures',
            fields=[
                ('samplingfeatureid', models.IntegerField(serialize=False, primary_key=True)),
                ('samplingfeatureuuid', models.TextField()),
                ('samplingfeaturecode', models.CharField(max_length=50)),
                ('samplingfeaturename', models.CharField(blank=True, max_length=255)),
                ('samplingfeaturedescription', models.CharField(blank=True, max_length=500)),
                ('featuregeometry', models.TextField(blank=True)),
                ('elevation_m', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'samplingfeatures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sectionresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('intendedxspacing', models.FloatField(null=True, blank=True)),
                ('intendedzspacing', models.FloatField(null=True, blank=True)),
                ('intendedtimespacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'sectionresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sectionresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'sectionresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sectionresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.BigIntegerField()),
                ('valuedatetimeutcoffset', models.BigIntegerField()),
                ('xlocation', models.FloatField()),
                ('xaggregationinterval', models.FloatField()),
                ('zlocation', models.BigIntegerField()),
                ('zaggregationinterval', models.FloatField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'sectionresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Simulations',
            fields=[
                ('simulationid', models.IntegerField(serialize=False, primary_key=True)),
                ('simulationname', models.CharField(max_length=255)),
                ('simulationdescription', models.CharField(blank=True, max_length=500)),
                ('simulationstartdatetime', models.DateTimeField()),
                ('simulationstartdatetimeutcoffset', models.IntegerField()),
                ('simulationenddatetime', models.DateTimeField()),
                ('simulationenddatetimeutcoffset', models.IntegerField()),
                ('timestepvalue', models.FloatField()),
                ('timestepunitsid', models.IntegerField()),
                ('inputdatasetid', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'simulations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('samplingfeatureid',
                 models.ForeignKey(db_column='samplingfeatureid', to='odm2testapp.Samplingfeatures',
                                   serialize=False,
                                   primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'sites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spatialoffsets',
            fields=[
                ('spatialoffsetid', models.IntegerField(serialize=False, primary_key=True)),
                ('offset1value', models.FloatField()),
                ('offset2value', models.FloatField(null=True, blank=True)),
                ('offset3value', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'spatialoffsets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spatialreferenceexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('spatialreferenceexternalidentifier', models.CharField(max_length=255)),
                ('spatialreferenceexternalidentifieruri',
                 models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'spatialreferenceexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spatialreferences',
            fields=[
                ('spatialreferenceid', models.IntegerField(serialize=False, primary_key=True)),
                ('srscode', models.CharField(blank=True, max_length=50)),
                ('srsname', models.CharField(max_length=255)),
                ('srsdescription', models.CharField(blank=True, max_length=500)),
                ('srslink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'spatialreferences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Specimenbatchpostions',
            fields=[
                ('featureactionid',
                 models.ForeignKey(db_column='featureactionid', to='odm2testapp.Featureactions',
                                   serialize=False,
                                   primary_key=True)),
                ('batchpositionnumber', models.IntegerField()),
                ('batchpositionlabel', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'specimenbatchpostions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Specimens',
            fields=[
                ('samplingfeatureid',
                 models.ForeignKey(db_column='samplingfeatureid', to='odm2testapp.Samplingfeatures',
                                   serialize=False,
                                   primary_key=True)),
                ('isfieldspecimen', models.BooleanField()),
            ],
            options={
                'managed': False,
                'db_table': 'specimens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Specimentaxonomicclassifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'specimentaxonomicclassifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spectraresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('xlocation', models.FloatField(null=True, blank=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('intendedwavelengthspacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'spectraresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spectraresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'spectraresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spectraresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
                ('excitationwavelength', models.FloatField()),
                ('emissionwavelength', models.FloatField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'spectraresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taxonomicclassifierexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('taxonomicclassifierexternalidentifier', models.CharField(max_length=255)),
                ('taxonomicclassifierexternalidentifieruri',
                 models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'taxonomicclassifierexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taxonomicclassifiers',
            fields=[
                ('taxonomicclassifierid', models.IntegerField(serialize=False, primary_key=True)),
                ('taxonomicclassifiername', models.CharField(max_length=255)),
                ('taxonomicclassifiercommonname', models.CharField(blank=True, max_length=255)),
                ('taxonomicclassifierdescription', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'taxonomicclassifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timeseriesresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('xlocation', models.FloatField(null=True, blank=True)),
                ('ylocation', models.FloatField(null=True, blank=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('intendedtimespacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'timeseriesresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timeseriesresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'timeseriesresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timeseriesresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'timeseriesresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trajectoryresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('intendedtrajectoryspacing', models.FloatField(null=True, blank=True)),
                ('intendedtimespacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'trajectoryresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trajectoryresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'trajectoryresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trajectoryresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.IntegerField()),
                ('xlocation', models.FloatField()),
                ('ylocation', models.FloatField()),
                ('zlocation', models.FloatField()),
                ('trajectorydistance', models.FloatField()),
                ('trajectorydistanceaggregationinterval', models.FloatField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'trajectoryresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transectresults',
            fields=[
                ('resultid',
                 models.ForeignKey(db_column='resultid', to='odm2testapp.Results', serialize=False,
                                   primary_key=True)),
                ('zlocation', models.FloatField(null=True, blank=True)),
                ('intendedtransectspacing', models.FloatField(null=True, blank=True)),
                ('intendedtimespacing', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'transectresults',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transectresultvalueannotations',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'transectresultvalueannotations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transectresultvalues',
            fields=[
                ('valueid', models.BigIntegerField(serialize=False, primary_key=True)),
                ('datavalue', models.FloatField()),
                ('valuedatetime', models.DateTimeField()),
                ('valuedatetimeutcoffset', models.DateTimeField()),
                ('xlocation', models.FloatField()),
                ('ylocation', models.FloatField()),
                ('transectdistance', models.FloatField()),
                ('transectdistanceaggregationinterval', models.FloatField()),
                ('timeaggregationinterval', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'transectresultvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('unitsid', models.IntegerField(serialize=False, primary_key=True)),
                ('unitsabbreviation', models.CharField(max_length=50)),
                ('unitsname', models.CharField(max_length=255)),
                ('unitslink', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'units',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variableextensionpropertyvalues',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('propertyvalue', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'variableextensionpropertyvalues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variableexternalidentifiers',
            fields=[
                ('bridgeid', models.IntegerField(serialize=False, primary_key=True)),
                ('variableexternalidentifer', models.CharField(max_length=255)),
                ('variableexternalidentifieruri', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'variableexternalidentifiers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('variableid', models.IntegerField(serialize=False, primary_key=True)),
                ('variablecode', models.CharField(max_length=50)),
                ('variabledefinition', models.CharField(blank=True, max_length=500)),
                ('nodatavalue', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'variables',
            },
            bases=(models.Model,),
        ),
    ]
