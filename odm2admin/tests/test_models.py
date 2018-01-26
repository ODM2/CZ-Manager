from django.test import TestCase
from ..models import Variables, CvVariabletype, CvVariablename
from django.utils import timezone



class VariablesTest(TestCase):
    def create_variable(self, variablecode='test',variabledefinition='test', nodatavalue=-6999):
        var_type = CvVariabletype(term="test", name="test", definition="this is just a test")
        var_name = CvVariablename(term="test", name="test", definition="this is just a test")
        test_var = Variables(variable_type=var_type,variablecode=variablecode,variable_name=var_name,
                             variabledefinition=variabledefinition, nodatavalue=nodatavalue)
        return test_var

    def test_variables_creation(self):
        var = self.create_variable()
        var_unicode_rep = "%s" % var.variablecode
        if self.variabledefinition:
            var_unicode_rep += " - %s" % var.variabledefinition[:20]
        self.assertTrue(isinstance(var, Variables))
        self.assertEqual(var.__str__(), var_unicode_rep)