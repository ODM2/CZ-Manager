from ajax_select import LookupChannel

# ========= Import all Controlled Vocabulary Module =========#
from .models import CvActiontype
from .models import CvElevationdatum
from .models import CvMethodtype
from .models import CvSamplingfeaturetype
from .models import CvSamplingfeaturegeotype
from .models import CvSpeciation
from .models import CvTaxonomicclassifiertype
from .models import CvUnitstype
from .models import CvVariablename
from .models import CvVariabletype
############################################################
from .models import Featureactions
from .models import Results
from .models import Profileresults
from .models import Measurementresults
from .models import Timeseriesresults
from django.utils.html import escape
from django.db.models import Q


class TimeseriesResultsLookup(LookupChannel):
    model = Timeseriesresults

    def get_query(self, q, request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Timeseriesresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                        | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                        | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                        | Q(resultid__variableid__variablecode__icontains=part) \
                                                        | Q(resultid__variableid__variable_name__name__icontains=part))

            else:
                qset = qset & Timeseriesresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                               | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                               | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                               | Q(resultid__variableid__variablecode__icontains=part) \
                                                               | Q(
                    resultid__variableid__variable_name__name__icontains=part))
        return qset

    def get_result(self, obj):
        return "%s" % (obj.resultid)

    def format_match(self, obj):
        return "%s" % (obj.resultid)

    def format_item_display(self, obj):
        return "%s" % (obj.resultid)  # ,

    def get_objects(self, ids):
        obj = Timeseriesresults.objects.filter(resultid__in=ids)
        return obj


class MeasurementResultsLookup(LookupChannel):
    model = Measurementresults

    def get_query(self, q, request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Measurementresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                         | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                         | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                         | Q(resultid__variableid__variablecode__icontains=part) \
                                                         | Q(resultid__variableid__variable_name__name__icontains=part))

            else:
                qset = qset & Measurementresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                                | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                                | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                                | Q(resultid__variableid__variablecode__icontains=part) \
                                                                | Q(
                    resultid__variableid__variable_name__name__icontains=part))
        return qset

    def get_result(self, obj):
        return "%s" % (obj.resultid)

    def format_match(self, obj):
        return "%s" % (obj.resultid)

    def format_item_display(self, obj):
        return "%s" % (obj.resultid)  # ,

    def get_objects(self, ids):
        obj = Measurementresults.objects.filter(resultid__in=ids)
        return obj


class ProfileResultsLookup(LookupChannel):
    model = Profileresults

    def get_query(self, q, request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Profileresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                     | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                     | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                     | Q(resultid__variableid__variablecode__icontains=part) \
                                                     | Q(resultid__variableid__variable_name__name__icontains=part))

            else:
                qset = qset & Profileresults.objects.filter(Q(resultid__resultid__icontains=part) \
                                                            | Q(
                    resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                            | Q(
                    resultid__featureactionid__action__method__methodname__icontains=part) \
                                                            | Q(resultid__variableid__variablecode__icontains=part) \
                                                            | Q(
                    resultid__variableid__variable_name__name__icontains=part))
        return qset

    def get_result(self, obj):
        return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)

    def format_match(self, obj):
        return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)

    def format_item_display(self, obj):
        return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)  # ,

    def get_objects(self, ids):
        obj = Profileresults.objects.filter(resultid__in=ids)
        return obj


class ResultsLookup(LookupChannel):
    model = Results

    def get_query(self, q, request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Results.objects.filter(Q(resultid__icontains=part) \
                                              | Q(
                    featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                              | Q(featureactionid__action__method__methodname__icontains=part) \
                                              | Q(variableid__variabledefinition__icontains=part) \
                                              | Q(variableid__variablecode__icontains=part))

            else:
                qset = qset & Results.objects.filter(Q(resultid__icontains=part) \
                                                     | Q(
                    featureactionid__samplingfeatureid__samplingfeaturename__icontains=part) \
                                                     | Q(featureactionid__action__method__methodname__icontains=part) \
                                                     | Q(variableid__variabledefinition__icontains=part) \
                                                     | Q(variableid__variablecode__icontains=part))
                # raise ValidationError(qset)
        return qset

    def get_result(self, obj):
        return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name, obj.variableid.variablecode,
                                          obj.featureactionid.samplingfeatureid.samplingfeaturename,
                                          obj.featureactionid.action.method.methodname)

    def format_match(self, obj):
        # return self.format_item_display(obj)
        return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name, obj.variableid.variablecode,
                                          obj.featureactionid.samplingfeatureid.samplingfeaturename,
                                          obj.featureactionid.action.method.methodname)

    def format_item_display(self, obj):
        return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name, obj.variableid.variablecode,
                                          obj.featureactionid.samplingfeatureid.samplingfeaturename,
                                          obj.featureactionid.action.method.methodname)

    def get_objects(self, ids):
        obj = Results.objects.filter(resultid__in=ids)
        return obj


class FeatureactionsLookup(LookupChannel):
    model = Featureactions

    def get_query(self, q, request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Featureactions.objects.filter(Q(samplingfeatureid__samplingfeaturename__icontains=part) \
                                                     | Q(action__method__methoddescription__icontains=part) \
                                                     | Q(action__method__methodname__icontains=part)).order_by(
                    'samplingfeatureid__samplingfeaturename')
            else:
                qset = qset & Featureactions.objects.filter(Q(samplingfeatureid__samplingfeaturename__icontains=part) \
                                                            | Q(action__method__methoddescription__icontains=part) \
                                                            | Q(action__method__methodname__icontains=part)).order_by(
                    'samplingfeatureid__samplingfeaturename')
        return qset  #
        # return Featureactions.objects.filter(name__icontains=q)#.order_by('name')

    def get_result(self, obj):
        # return obj.featureactionid
        return "%s- %s - %s" % (obj.featureactionid, obj.samplingfeatureid.samplingfeaturename,
                                obj.action.method.methodname)  # Featureactions.objects.filter(featureactionid__in=obj.featureactionid) #

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return u"<span class='tag'>%s</span>" % obj.name
        return "%s- %s - %s" % (
            obj.featureactionid, obj.samplingfeatureid.samplingfeaturename, obj.action.method.methodname)

    def get_objects(self, ids):
        obj = Featureactions.objects.filter(featureactionid__in=ids)
        return obj


class CvVariableNameLookup(LookupChannel):
    model = CvVariablename

    def get_query(self, q, request):
        return CvVariablename.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvVariableSpeciationLookup(LookupChannel):
    model = CvSpeciation

    def get_query(self, q, request):
        return CvSpeciation.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvVariableTypeLookup(LookupChannel):
    model = CvVariabletype

    def get_query(self, q, request):
        return CvVariabletype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvUnitTypeLookup(LookupChannel):
    model = CvUnitstype

    def get_query(self, q, request):
        return CvUnitstype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvTaxonomicClassifierTypeLookup(LookupChannel):
    model = CvTaxonomicclassifiertype

    def get_query(self, q, request):
        return CvTaxonomicclassifiertype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvMethodTypeLookup(LookupChannel):
    model = CvMethodtype

    def get_query(self, q, request):
        return CvMethodtype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvActionTypeLookup(LookupChannel):
    model = CvActiontype

    def get_query(self, q, request):
        return CvActiontype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvSamplingFeatureTypeLookup(LookupChannel):
    model = CvSamplingfeaturetype

    def get_query(self, q, request):
        return CvSamplingfeaturetype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvSamplingFeatureGeoTypeLookup(LookupChannel):
    model = CvSamplingfeaturegeotype

    def get_query(self, q, request):
        return CvSamplingfeaturegeotype.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')


class CvElevationDatumLookup(LookupChannel):
    model = CvElevationdatum

    def get_query(self, q, request):
        return CvElevationdatum.objects.filter(name__icontains=q).order_by('name')  #

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)
        # return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self, obj):
        # return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank' style='color:blue;'> reference link </a>" % \
               (escape(obj.name), escape(obj.sourcevocabularyuri))
        # onClick="window.open('http://www.yahoo.com', '_blank')
