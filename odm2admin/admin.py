from django.contrib import admin

from .forms import ActionByAdmin
from .forms import ActionsAdmin
from .forms import AffiliationsAdmin
from .forms import AuthorlistsAdmin
from .forms import CitationextensionpropertyvaluesAdmin
from .forms import CitationsAdmin
from .forms import DataloggerfilecolumnsAdmin
from .forms import DataloggerfilesAdmin
from .forms import DataloggerprogramfilesAdmin
from .forms import DataqualityAdmin
from .forms import DatasetcitationsAdmin
from .forms import DatasetsAdmin
from .forms import DatasetsresultsAdmin
from .forms import DerivationequationsAdmin
from .forms import EquipmentmodelsAdmin
from .forms import ExtensionpropertiesAdmin
from .forms import ExternalidentifiersystemAdmin
from .forms import FeatureactionsAdmin
from .forms import InstrumentoutputvariablesAdmin
from .forms import MeasurementresultsAdmin
from .forms import MeasurementresultvaluesAdmin
from .forms import MeasurementresultvalueFileAdmin
from .forms import MethodcitationsAdmin
from .forms import MethodsAdmin
from .forms import OrganizationsAdmin
from .forms import PeopleAdmin
from .forms import ProfileresultsAdmin
from .forms import ProfileresultsvaluesAdmin
from .forms import ProcessingLevelsAdmin
from .forms import ProcessDataloggerfileAdmin
from .forms import RelatedactionsAdmin
from .forms import RelatedfeaturesAdmin
from .forms import RelatedresultsAdmin
from .forms import ResultsAdmin
from .forms import ResultsdataqualityAdmin
from .forms import ResultderivationequationsAdmin
from .forms import SamplingfeatureexternalidentifiersAdmin
from .forms import SamplingfeaturesAdmin
from .forms import SitesAdmin
from .forms import SpatialreferencesAdmin
from .forms import TaxonomicclassifiersAdmin
from .forms import TimeseriesresultsAdmin
from .forms import TimeseriesresultvaluesAdmin
from .forms import UnitsAdmin
from .forms import VariablesAdmin
from .models import Actionby
from .models import Actions
from .models import Affiliations
from .models import Authorlists
from .models import Citationextensionpropertyvalues
from .models import Citations
from .models import Dataloggerfilecolumns
from .models import Dataloggerfiles
from .models import Dataloggerprogramfiles
from .models import Dataquality
from .models import Datasetcitations
from .models import Datasets
from .models import Datasetsresults
from .models import Derivationequations
from .models import Equipmentmodels
from .models import Extensionproperties
from .models import Externalidentifiersystems
from .models import Featureactions
from .models import Instrumentoutputvariables
from .models import Measurementresults
from .models import MeasurementresultvalueFile
from .models import Measurementresultvalues
from .models import Methodcitations
from .models import Methods
from .models import Organizations
from .models import People
from .models import Personexternalidentifiers
from .models import ProcessDataloggerfile
from .models import Processinglevels
from .models import Profileresults
from .models import Profileresultvalues
from .models import Relatedactions
from .models import Relatedfeatures
from .models import Relatedresults
from .models import Results
from .models import Resultsdataquality
from .models import Resultderivationequations
from .models import Samplingfeatureexternalidentifiers
from .models import Samplingfeatures
from .models import Sites
from .models import Spatialreferences
from .models import Taxonomicclassifiers
from .models import Timeseriesresults
from .models import Timeseriesresultvalues
from .models import Units
from .models import Variables

admin.site.register(Dataquality, DataqualityAdmin)
admin.site.register(Resultsdataquality, ResultsdataqualityAdmin)
admin.site.register(Datasetcitations, DatasetcitationsAdmin)
admin.site.register(Derivationequations, DerivationequationsAdmin)
admin.site.register(Citations, CitationsAdmin)
admin.site.register(Authorlists, AuthorlistsAdmin)
admin.site.register(Methodcitations, MethodcitationsAdmin)
admin.site.register(Extensionproperties, ExtensionpropertiesAdmin)
admin.site.register(Citationextensionpropertyvalues, CitationextensionpropertyvaluesAdmin)

admin.site.register(Profileresults, ProfileresultsAdmin)
admin.site.register(Profileresultvalues, ProfileresultsvaluesAdmin)
admin.site.register(Equipmentmodels, EquipmentmodelsAdmin)
admin.site.register(Instrumentoutputvariables, InstrumentoutputvariablesAdmin)
admin.site.register(Dataloggerfilecolumns, DataloggerfilecolumnsAdmin)
admin.site.register(Dataloggerprogramfiles, DataloggerprogramfilesAdmin)
admin.site.register(Dataloggerfiles, DataloggerfilesAdmin)
admin.site.register(Samplingfeatures, SamplingfeaturesAdmin)
admin.site.register(Samplingfeatureexternalidentifiers, SamplingfeatureexternalidentifiersAdmin)
admin.site.register(Sites, SitesAdmin)
admin.site.register(Spatialreferences,SpatialreferencesAdmin)
admin.site.register(Affiliations, AffiliationsAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Personexternalidentifiers)
admin.site.register(Methods, MethodsAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Actionby, ActionByAdmin)
admin.site.register(Organizations, OrganizationsAdmin)
admin.site.register(Featureactions, FeatureactionsAdmin)
admin.site.register(Actions, ActionsAdmin)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Relatedactions, RelatedactionsAdmin)
admin.site.register(Relatedresults, RelatedresultsAdmin)
admin.site.register(Resultderivationequations, ResultderivationequationsAdmin)
admin.site.register(Variables, VariablesAdmin)
admin.site.register(ProcessDataloggerfile, ProcessDataloggerfileAdmin)
admin.site.register(Externalidentifiersystems, ExternalidentifiersystemAdmin)

admin.site.register(Taxonomicclassifiers, TaxonomicclassifiersAdmin)
admin.site.register(Datasets, DatasetsAdmin)
admin.site.register(Datasetsresults, DatasetsresultsAdmin)
admin.site.register(Processinglevels, ProcessingLevelsAdmin)
admin.site.register(Relatedfeatures, RelatedfeaturesAdmin)
admin.site.register(Timeseriesresults, TimeseriesresultsAdmin)
admin.site.register(Timeseriesresultvalues, TimeseriesresultvaluesAdmin)
admin.site.register(Measurementresults, MeasurementresultsAdmin)
admin.site.register(Measurementresultvalues, MeasurementresultvaluesAdmin)
admin.site.register(MeasurementresultvalueFile, MeasurementresultvalueFileAdmin)
admin.site.index_template = "admin/my_index.html"
