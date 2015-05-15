from django.contrib import admin

from .models import Samplingfeatures
from .forms import SamplingfeaturesAdmin
from .models import Affiliations
from .models import People
from .models import Actionby
from .models import Organizations
from .forms import OrganizationsAdmin
from .models import Featureactions
from .models import Actions
from .models import Results
from .forms import ResultsAdmin
from .models import Relatedactions
from .forms import RelatedactionsAdmin
from .models import Methods
from .models import Variables
from .forms import VariablesAdmin
from .models import Units
from .models import Taxonomicclassifiers
from .forms import TaxonomicclassifiersAdmin
from .models import Datasets
from .models import Datasetsresults
from .models import Processinglevels

admin.site.register(Samplingfeatures,SamplingfeaturesAdmin)
admin.site.register(Affiliations)
admin.site.register(People)
admin.site.register(Actionby)
admin.site.register(Organizations,OrganizationsAdmin)
admin.site.register(Featureactions)
admin.site.register(Actions)
admin.site.register(Results,ResultsAdmin)
admin.site.register(Relatedactions,RelatedactionsAdmin)
admin.site.register(Variables, VariablesAdmin)
admin.site.register(Units)
admin.site.register(Taxonomicclassifiers,TaxonomicclassifiersAdmin)
admin.site.register(Datasets)
admin.site.register(Datasetsresults)
admin.site.register(Processinglevels)