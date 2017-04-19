from ajax_select import urls as ajax_select_urls
from django.core.management import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.conf.urls.static import static

# from ODM2CZOData import views # How can I use config file for this??
import importlib

views = importlib.import_module("{}.views".format(settings.APP_NAME))

admin.autodiscover()
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE

# admin_site.admin_view()
urlpatterns = [url(r'^' + '', include(admin.site.urls)),
               url(r'^' + 'lookups/', include(ajax_select_urls)),
               url(r'^$', lambda r: HttpResponseRedirect('{}/'.format(settings.APP_NAME))),
               url(r'^' + 'AddSensor', views.AddSensor, name="AddSensor"),
               url(r'^' + 'chartIndex', views.chartIndex,
                   name="chartIndex"),
               url(r'^' + 'AddProfile', views.AddProfile,
                   name="AddProfile"),
               url(r'^' + 'RecordAction', views.RecordAction,
                   name="RecordAction"),
               url(r'^' + 'ManageCitations', views.ManageCitations,
                   name="ManageCitations"),
               url(r'^' + 'chart', views.TimeSeriesGraphing,
                   name="TimeSeriesGraphing"),
               url(r'^' + 'mapdata', views.web_map, name="WebMap"),
               #  url(r'^' + ^login/$', login, {'template_name': 'login.html'}),
               url(r'^' + 'graph/$', views.TimeSeriesGraphing),
               url(r'^' + 'graph/featureaction=(?P<feature_action>(\d+))/$',
                   views.TimeSeriesGraphing, name="TimeSeriesGraphing"),
               # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+)
               # (?P<feature_action>(\d+))
               url(r'^' + 'emaildata/$', views.email_data_from_graph),
               url(r'^' + 'addannotation/$', views.add_annotation),
               url(r'^' + 'addL1timeseries/$', views.addL1timeseries),
               url(r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(r'^' + 'graph/samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.TimeSeriesGraphing, name="TimeSeriesGraphing"),
               # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+)
               # (?P<feature_action>(\d+))
               url(r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

               url(r'^' + 'mappopup/featureaction=(?P<feature_action>(\d+))/$',
                   views.mappopuploader,
                   name="mappopuploader"),
               url(
                   r'^' + 'mappopup/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.mappopuploader, name="mappopuploader"),

               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

               url(r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/$',
                   views.TimeSeriesGraphingShort,
                   name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               url(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

               url(
                   r'^' + 'profilegraph/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.graph_data, name="graph_data"),
               url(
                   r'^' + 'profilegraph/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),
               url(
                   r'^' + 'profilegraph/'
                                     'selectedrelatedfeature='
                                     '(?P<selectedrelatedfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),
               url(
                   r'^' + 'profilegraph/'
                                     'selectedrelatedfeature='
                                     '(?P<selectedrelatedfeature>(\d+))/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),

               # /(?P<startdate>(\d+))/(?P<enddate>(\d+))
               url(r'^' + 'chartVariableAndFeature.html', views.graph_data,
                   name="graph_data"),
               url(r'^' + 'soilsscatterplot.html', views.scatter_plot,
                   name="scatter_plot"),
               url(r'^' + 'publications.html', views.publications,
                   name="publications"),
               url(r'^' + 'features/type=(?P<sf_type>([\w\s]+,?)+)&'
                                              'datasets=(?P<ds_ids>([a-zA-Z]+)?(([0-9]+,?)+)?)', views.get_features),
               # url(r'^' + 'pubview/citationid=(?P<citationid>(\d+))/$',
               # views.add_pub,
               #    name="add_pub"),
               # url(r'^' + 'pubview', views.add_pub),
               # for uploaded files like dataloggerfiles
               # url(r'^' + MEDIA_URL +'(?P<path>.*)$', 'django.views.static.serve', {
               #        'document_root': MEDIA_ROOT,
               #    }),
               # url(r'^' + 'upfiles/(?P<path>.*)$', 'django.views.static.serve',
               #    {'document_root': MEDIA_ROOT}),
               # url(r'^admin/DataloggerfilecolumnsDisplay.html',
               # views.dataloggercolumnView,
               # name="dataloggercolumnView"),

               # url(r'^contas_pagar/pagamento/(?P<id_parcela>\d+)/$',
               # 'contas_pagar.views.retorna_pagamentos_parcela')
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
