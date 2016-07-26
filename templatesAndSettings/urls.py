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
    #(r'^ajax_select/', include('ajax_select.urls')),
     url(r'^' + URL_PATH +'AddSensor.html', views.AddSensor, name="AddSensor"),
    url(r'^' + URL_PATH +'chartIndex.html', views.chartIndex, name="chartIndex"),
    url(r'^' + URL_PATH +'AddProfile.html', views.AddProfile, name="AddProfile"),
    url(r'^' + URL_PATH +'RecordAction.html', views.RecordAction, name="RecordAction"),
    url(r'^' + URL_PATH +'ManageCitations.html', views.ManageCitations, name="ManageCitations"),
    url(r'^' + URL_PATH +'chart.html', views.TimeSeriesGraphing, name="TimeSeriesGraphing"),
    url(r'^' + URL_PATH + 'mapdata.html', views.web_map, name="WebMap"),
    url(r'^' + URL_PATH +'graph/$', views.TimeSeriesGraphing),
    url(r'^' + URL_PATH +'graph/featureaction=(?P<feature_action>(\d+))/$', views.TimeSeriesGraphing, name="TimeSeriesGraphing"), # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+) (?P<feature_action>(\d+))
    url(r'^' + URL_PATH +'graphfa/featureaction=(?P<feature_action>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/featureaction=(?P<feature_action>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/featureaction=(?P<feature_action>(\d+))/resultidu=(?P<resultidu>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/featureaction=(?P<feature_action>(\d+))/resultidu=(?P<resultidu>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graph/samplingfeature=(?P<samplingfeature>(\d+))/$', views.TimeSeriesGraphing, name="TimeSeriesGraphing"), # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+) (?P<feature_action>(\d+))
    url(r'^' + URL_PATH +'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/resultidu=(?P<resultidu>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/resultidu=(?P<resultidu>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),


    url(r'^' + URL_PATH +'graphfa/dataset=(?P<dataset>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/dataset=(?P<dataset>(\d+))/resultidu=(?P<resultidu>(\d+))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/dataset=(?P<dataset>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
    url(r'^' + URL_PATH +'graphfa/dataset=(?P<dataset>(\d+))/resultidu=(?P<resultidu>(\d+))/startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$', views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

    #/(?P<startdate>(\d+))/(?P<enddate>(\d+))
    url(r'^' + URL_PATH +'chartVariableAndFeature.html', views.graph_data, name="graph_data"),
     url(r'^' + URL_PATH +'soilsscatterplot.html', views.scatter_plot, name="scatter_plot"),
    url(r'^' + URL_PATH +'publications.html', views.publications, name="publications"),
    url(r'^' + URL_PATH +'pubview/citationid=(?P<citationid>(\d+))/$', views.add_pub, name="add_pub"),
    url(r'^' + URL_PATH +'pubview', views.add_pub),
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