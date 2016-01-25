from ajax_select import LookupChannel
from .models import CvVariablename
from .models import CvVariabletype
from .models import CvUnitstype
from .models import CvSpeciation
from django.utils.html import escape

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