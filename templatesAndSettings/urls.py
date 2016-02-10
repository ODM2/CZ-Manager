from django.conf.urls import patterns, include, url
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from ODM2CZOData import views
from templatesAndSettings.settings import MEDIA_ROOT
from templatesAndSettings.settings import MEDIA_URL
from templatesAndSettings.settings import URL_PATH
from django.views.generic import View
admin.autodiscover()
admin.site.site_header = 'ODM2 Admin'

#admin_site.admin_view()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project_17.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^' + URL_PATH +'', include(admin.site.urls)),
    (r'^' + URL_PATH +'lookups/', include(ajax_select_urls)),
     url(r'^' + URL_PATH +'AddSensor.html', views.AddSensor, name="AddSensor"),
    url(r'^' + URL_PATH +'chartIndex.html', views.chartIndex, name="chartIndex"),
    url(r'^' + URL_PATH +'AddProfile.html', views.AddProfile, name="AddProfile"),
    url(r'^' + URL_PATH +'RecordAction.html', views.RecordAction, name="RecordAction"),
   url(r'^' + URL_PATH +'ManageCitations.html', views.ManageCitations, name="ManageCitations"),
    url(r'^' + URL_PATH +'chart.html', views.temp_pivot_chart_view, name="temp_pivot_chart_view"),
    url(r'^' + URL_PATH +'chartVariableAndFeature.html', views.graph_data, name="graph_data"),

    #for uploaded files like dataloggerfiles
    #url(r'^' + MEDIA_URL +'(?P<path>.*)$', 'django.views.static.serve', {
    #        'document_root': MEDIA_ROOT,
    #    }),
    url(r'^' + URL_PATH +'upfiles/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT,
        }),
    #url(r'^admin/DataloggerfilecolumnsDisplay.html', views.dataloggercolumnView, name="dataloggercolumnView"),

    #url(r'^contas_pagar/pagamento/(?P<id_parcela>\d+)/$',
                             #'contas_pagar.views.retorna_pagamentos_parcela'),

)