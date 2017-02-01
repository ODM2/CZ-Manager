import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import odm2admin.modelHelpers as modelHelpers
from odm2admin.models import Actions, Units, Variables

__author__ = 'leonmi'

# Carbon Percent.
samplingfeaturedescription = "Stone M.M. et al. site, see http://dx.doi.org/10.1016/j.soilbio.2014.10.019",  # noqa
fname = 'EnzBiomass.csv'
variableFileIndex = 12
variableDBID = 22
variableUnitID = 21
actionID = 27
# zspacing = 20
# zinterval = 20
# modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False, samplingfeaturedescription)  # noqa

# NitrogenPercent.
fname = 'EnzBiomass.csv'
variableFileIndex = 13
variableDBID = 59
variableUnitID = 21
actionID = 27
# zspacing = 20
# zinterval = 20
# modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False, samplingfeaturedescription)  # noqa


# Phosphorus, mg/kg.
fname = 'EnzBiomass.csv'
variableFileIndex = 14
# variable= modelHelpers.searchModelColumnFor(" P ", Variables, 'variablecode')  # 74  # noqa
variableDBID = 74
print(variableDBID)
unit = modelHelpers.searchModelColumnFor(" milligrams per kilogram ", Units, 'unitsname')  # 36 'unitsabbreviation'  # noqa
variableUnitID = unit.unitsid
print(variableUnitID)
actionID = 27
act = Actions.objects.filter(actionid=actionID).get()
print(act)
# zspacing = 20
# zinterval = 20
# modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False, samplingfeaturedescription)  # noqa


# Phosphorus, mg/kg.
fname = 'EnzBiomass.csv'
variableFileIndex = 15
variable = modelHelpers.searchModelColumnFor(" sodium bicarbonate extractable phosphorus ", Variables, 'variablecode')  # 74  # noqa
variableDBID = variable.variableid
print(variableDBID)
unit = modelHelpers.searchModelColumnFor(" milligrams per kilogram ", Units, 'unitsname')  # 36 'unitsabbreviation'  # noqa
variableUnitID = unit.unitsid
print(variableUnitID)
actionID = 27
act = Actions.objects.filter(actionid=actionID).get()
# print(act)
# zspacing = 20
# zinterval = 20
# modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False, samplingfeaturedescription)  # noqa

# NaOH extractable Phosphorus.
fname = 'EnzBiomass.csv'
variableFileIndex = 16
variable = modelHelpers.searchModelColumnFor(" NaOH extractable Phosphorus ", Variables, 'variablecode')  # 74  # noqa
variableDBID = variable.variableid
print(variableDBID)
unit = modelHelpers.searchModelColumnFor(" milligrams per kilogram ", Units, 'unitsname')  # 36 'unitsabbreviation'  # noqa
variableUnitID = unit.unitsid
print(variableUnitID)
actionID = 27
act = Actions.objects.filter(actionid=actionID).get()
# print(act)
# zspacing = 20
# zinterval = 20
# modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False, samplingfeaturedescription)  # noqa


fname = 'EnzBiomass.csv'
variableFileIndex = 17
variable = modelHelpers.searchModelColumnFor(" pH, Soil ", Variables, 'variablecode')  # 74  # noqa
variableDBID = variable.variableid
print(variableDBID)
unit = Units.objects.get(unitsid=7)
# modelHelpers.searchModelColumnFor(" pH ", Units, 'unitsname')  # 36 'unitsabbreviation'  # noqa
variableUnitID = unit.unitsid
print(variableUnitID)
actionID = 27
act = Actions.objects.filter(actionid=actionID).get()
print(act)
# zspacing = 20
# zinterval = 20
modelHelpers.importValues(fname, variableFileIndex, variableDBID, variableUnitID, actionID, False,)  # noqa
