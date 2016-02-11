from ajax_select import LookupChannel
from .models import CvVariablename
from .models import CvVariabletype
from .models import CvUnitstype
from .models import CvSpeciation
from .models import Featureactions
from .models import Results
from .models import Profileresults
from .models import Measurementresults
from .models import FeatureactionsNames
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.db.models import Q

#need profileresults and measurementresults lookups


class MeasurementResultsLookup(LookupChannel):
    model = Measurementresults
    def get_query(self,q,request):
        qset = None
        for part in q.split():
            if not qset:
               qset =  Measurementresults.objects.filter(Q(resultid__resultid__icontains=part)\
                                       | Q(resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                       | Q(resultid__featureactionid__action__method__methodname__icontains=part)\
                                       | Q(resultid__variableid__variablecode__icontains=part)\
                                       | Q(resultid__variableid__variable_name__name__icontains=part))

            else:
                 qset = qset &  Measurementresults.objects.filter(Q(resultid__resultid__icontains=part)\
                                        | Q(resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                        | Q(resultid__featureactionid__action__method__methodname__icontains=part)\
                                        | Q(resultid__variableid__variablecode__icontains=part)\
                                        | Q(resultid__variableid__variable_name__name__icontains=part))
        return qset
    def get_result(self,obj):
        return "%s" % (obj.resultid)

    def format_match(self,obj):
        return "%s" % (obj.resultid)

    def format_item_display(self,obj):
        return "%s" % (obj.resultid)#,

    def get_objects(self, ids):
        obj = Measurementresults.objects.filter(resultid__in=ids)
        return obj

class ProfileResultsLookup(LookupChannel):
    model = Profileresults
    def get_query(self,q,request):
        qset = None
        for part in q.split():
            if not qset:
               qset =  Profileresults.objects.filter(Q(resultid__resultid__icontains=part)\
                                       | Q(resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                       | Q(resultid__featureactionid__action__method__methodname__icontains=part)\
                                       | Q(resultid__variableid__variablecode__icontains=part)\
                                       | Q(resultid__variableid__variable_name__name__icontains=part))

            else:
                 qset = qset &  Profileresults.objects.filter(Q(resultid__resultid__icontains=part)\
                                        | Q(resultid__featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                        | Q(resultid__featureactionid__action__method__methodname__icontains=part)\
                                        | Q(resultid__variableid__variablecode__icontains=part)\
                                        | Q(resultid__variableid__variable_name__name__icontains=part))
        return qset
    def get_result(self,obj):
        return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)

    def format_match(self,obj):
         return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)

    def format_item_display(self,obj):
         return "%s- %s %s" % (obj.resultid, obj.intendedzspacing, obj.intendedzspacingunitsid)#,

    def get_objects(self, ids):
        obj = Profileresults.objects.filter(resultid__in=ids)
        return obj

class ResultsLookup(LookupChannel):
    model = Results

    def get_query(self,q,request):
        qset = None
        for part in q.split():
            if not qset:
               qset =  Results.objects.filter(Q(resultid__icontains=part)\
                                       | Q(featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                       | Q(featureactionid__action__method__methodname__icontains=part)\
                                       | Q(variableid__variabledefinition__icontains=part)\
                                       | Q(variableid__variablecode__icontains=part))

            else:
                qset = qset &  Results.objects.filter(Q(resultid__icontains=part)\
                                       | Q(featureactionid__samplingfeatureid__samplingfeaturename__icontains=part)\
                                       | Q(featureactionid__action__method__methodname__icontains=part)\
                                       | Q(variableid__variabledefinition__icontains=part)\
                                       | Q(variableid__variablecode__icontains=part))
                #raise ValidationError(qset)
        return qset
    def get_result(self,obj):
       return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name,obj.variableid.variablecode, obj.featureactionid.samplingfeatureid.samplingfeaturename,obj.featureactionid.action.method.methodname)

    def format_match(self,obj):
        #return self.format_item_display(obj)
        return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name,obj.variableid.variablecode, obj.featureactionid.samplingfeatureid.samplingfeaturename,obj.featureactionid.action.method.methodname)

    def format_item_display(self,obj):
        return "%s- %s - %s - %s - %s" % (obj.resultid, obj.variableid.variable_name.name,obj.variableid.variablecode, obj.featureactionid.samplingfeatureid.samplingfeaturename,obj.featureactionid.action.method.methodname)

    def get_objects(self, ids):
        obj = Results.objects.filter(resultid__in=ids)
        return obj


class FeatureactionsLookup(LookupChannel):
    model = Featureactions

    def get_query(self,q,request):
        qset = None
        for part in q.split():
            if not qset:
                qset = Featureactions.objects.filter(Q(samplingfeatureid__samplingfeaturename__icontains=part)\
                | Q(action__method__methoddescription__icontains=part)\
                | Q(action__method__methodname__icontains=part)).order_by('samplingfeatureid__samplingfeaturename')
            else:
                qset = qset &   Featureactions.objects.filter(Q(samplingfeatureid__samplingfeaturename__icontains=part)\
                | Q(action__method__methoddescription__icontains=part)\
                | Q(action__method__methodname__icontains=part)).order_by('samplingfeatureid__samplingfeaturename')
        return qset #
        #return Featureactions.objects.filter(name__icontains=q)#.order_by('name')
    def get_result(self,obj):
        #return obj.featureactionid
        return "%s- %s - %s" % (obj.featureactionid, obj.samplingfeatureid.samplingfeaturename,obj.action.method.methodname) #Featureactions.objects.filter(featureactionid__in=obj.featureactionid) #

    def format_match(self,obj):
        return self.format_item_display(obj)
        #return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self,obj):
        #return u"<span class='tag'>%s</span>" % obj.name
        return "%s- %s - %s" % (obj.featureactionid,obj.samplingfeatureid.samplingfeaturename,obj.action.method.methodname)

    def get_objects(self, ids):
        obj = Featureactions.objects.filter(featureactionid__in=ids)
        return obj

class CvVariableNameLookup(LookupChannel):
    model = CvVariablename

    def get_query(self,q,request):
        return CvVariablename.objects.filter(name__icontains=q).order_by('name') #

    def get_result(self,obj):
        return obj.name

    def format_match(self,obj):
        return self.format_item_display(obj)
        #return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self,obj):
        #return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank'> reference link </a>" % \
               (escape(obj.name),escape(obj.sourcevocabularyuri))
    #onClick="window.open('http://www.yahoo.com', '_blank')


class CvVariableSpeciationLookup(LookupChannel):
    model = CvSpeciation

    def get_query(self,q,request):
        return CvSpeciation.objects.filter(name__icontains=q).order_by('name') #

    def get_result(self,obj):
        return obj.name

    def format_match(self,obj):
        return self.format_item_display(obj)
        #return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self,obj):
        #return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank'> reference link </a>" % \
               (escape(obj.name),escape(obj.sourcevocabularyuri))
    #onClick="window.open('http://www.yahoo.com', '_blank')



class CvVariableTypeLookup(LookupChannel):
    model = CvVariabletype

    def get_query(self,q,request):
        return CvVariabletype.objects.filter(name__icontains=q).order_by('name') #

    def get_result(self,obj):
        return obj.name

    def format_match(self,obj):
        return self.format_item_display(obj)
        #return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self,obj):
        #return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank'> reference link </a>" % \
               (escape(obj.name),escape(obj.sourcevocabularyuri))
    #onClick="window.open('http://www.yahoo.com', '_blank')


class CvUnitTypeLookup(LookupChannel):
    model = CvUnitstype

    def get_query(self,q,request):
        return CvUnitstype.objects.filter(name__icontains=q).order_by('name') #

    def get_result(self,obj):
        return obj.name

    def format_match(self,obj):
        return self.format_item_display(obj)
        #return u"<a href= %s> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))

    def format_item_display(self,obj):
        #return "<a href= %s target='_blank'> %s </a>" % (escape(obj.sourcevocabularyuri), escape(obj.name))
        return u"%s  <a href= %s target='_blank'> reference link </a>" % \
               (escape(obj.name),escape(obj.sourcevocabularyuri))
    #onClick="window.open('http://www.yahoo.com', '_blank')