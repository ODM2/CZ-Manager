from django.contrib import admin

from .models import Samplingfeatures
from .forms import SamplingfeaturesAdmin
from .models import Affiliations
from .forms import AffiliationsAdmin
from .models import People
from .models import Actionby
from .models import Organizations
from .forms import OrganizationsAdmin
from .models import Featureactions
from .forms import FeatureactionsAdmin
from .models import Actions
from .models import Results
from .forms import ResultsAdmin
from .models import Relatedactions
from .forms import RelatedactionsAdmin
from .models import Methods
from .forms import MethodsAdmin
from .models import Variables
from .forms import VariablesAdmin
from .models import Units
from .models import Taxonomicclassifiers
from .forms import TaxonomicclassifiersAdmin
from .models import Datasets
from .forms import DatasetsAdmin
from .forms import ActionsAdmin
from .forms import ActionByAdmin
from .models import Datasetsresults
from .models import Processinglevels

admin.site.register(Samplingfeatures,SamplingfeaturesAdmin)
admin.site.register(Affiliations,AffiliationsAdmin)
admin.site.register(People)
admin.site.register(Methods,MethodsAdmin)
admin.site.register(Actionby, ActionByAdmin)
admin.site.register(Organizations,OrganizationsAdmin)
admin.site.register(Featureactions,FeatureactionsAdmin)
admin.site.register(Actions,ActionsAdmin)
admin.site.register(Results,ResultsAdmin)
admin.site.register(Relatedactions,RelatedactionsAdmin)
admin.site.register(Variables, VariablesAdmin)
admin.site.register(Units)
admin.site.register(Taxonomicclassifiers,TaxonomicclassifiersAdmin)
admin.site.register(Datasets,DatasetsAdmin)
admin.site.register(Datasetsresults)
admin.site.register(Processinglevels)