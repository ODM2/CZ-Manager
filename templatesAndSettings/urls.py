# from ajax_select import urls as ajax_select_urls
from ajax_select import views as ajax_select_views
from django.core.management import settings
from django.urls import include, re_path
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
# from ODM2CZOData import views # How can I use config file for this??
from django.urls import reverse
import importlib

views = importlib.import_module("{}.views".format(settings.APP_NAME))

admin.autodiscover()
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
app_name="odm2admin"
# admin_site.admin_view()
urlpatterns = [re_path(r'^' + '', admin.site.urls),
               #ajax_select_views.ajax_lookup, name='ajax_lookup'
               #below line needed instead of import ajax select urls as they haven't been fixed for django 2.0
               re_path(r'^lookups/(?P<channel>[-\w]+)$',ajax_select_views.ajax_lookup,name='ajax_lookup'),
               # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
               # url(r'^oauthview$', views.oauth_view, name='oauth_view'),
               # re_path('', include('social_django.urls', namespace='social')),
               # url(r'^login/$', auth_views.login, name='login'),
               # url(r'^logout/$', auth_views.logout, name='logout'),
               re_path(r'^oauth/', include('social_django.urls', namespace='social')),
               re_path(r'^$', lambda r: HttpResponseRedirect('{}/'.format(settings.APP_NAME))),
               re_path(r'^' + 'AddSensor', views.AddSensor, name="AddSensor"),
               re_path(r'^' + 'chartIndex', views.chartIndex,
                   name="chartIndex"),
               re_path(r'^' + 'AddProfile', views.AddProfile,
                   name="AddProfile"),
               re_path(r'^' + 'RecordAction', views.RecordAction,
                   name="RecordAction"),
               re_path(r'^' + 'ManageCitations', views.ManageCitations,
                   name="ManageCitations"),
               re_path(r'^' + 'chart', views.TimeSeriesGraphing,
                   name="TimeSeriesGraphing"),
               re_path(r'^' + 'mapdata', views.web_map, name="WebMap"),
               #  url(r'^' + ^login/$', login, {'template_name': 'login.html'}),
               re_path(r'^' + 'graph/$', views.TimeSeriesGraphing),
               re_path(r'^' + 'graph/featureaction=(?P<feature_action>(\d+))/$',
                   views.TimeSeriesGraphing, name="TimeSeriesGraphing"),
               # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+)
               # (?P<feature_action>(\d+))
               re_path(r'^' + 'emaildata/$', views.email_data_from_graph),
               re_path(r'^' + 'export_to_hydroshare/$', views.export_to_hydroshare),
               re_path(r'^' + 'addannotation/$', views.add_annotation),
               re_path(r'^' + 'addoffset/$', views.add_offset),
               re_path(r'^' + 'addshiftvals/$', views.add_shiftvalues),
               re_path(r'^' + 'addL1timeseries/$', views.addL1timeseries),
               re_path(r'^' + 'processdlfile/$', views.procDataLoggerFile),
               re_path(r'^' + 'preprocessdlfile/$', views.preProcDataLoggerFile),
               re_path(r'^' + 'sensordashboard/featureaction=(?P<feature_action>(\d+))/', views.sensor_dashboard),
               re_path(r'^' + 'sensordashboard/samplingfeature=(?P<sampling_feature>(\d+))/', views.sensor_dashboard),
               re_path(r'^' + 'sensordashboard/$', views.sensor_dashboard),

               re_path(r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                          'resultidu=\[(?P<resultidu>\d+(, \d+)*\])/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/featureaction=(?P<feature_action>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(r'^' + 'graph/samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.TimeSeriesGraphing, name="TimeSeriesGraphing"),
               # (?:featureaction-(?P<featureaction>\d+)/)?$  (?P<variable_a>(\d+)
               # (?P<feature_action>(\d+))
               re_path(r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

               re_path(r'^' + 'mappopup/featureaction=(?P<feature_action>(\d+))/$',
                   views.mappopuploader,
                   name="mappopuploader"),
               re_path(
                   r'^' + 'mappopup/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.mappopuploader, name="mappopuploader"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                          'resultidu=(?P<resultidu>(\d+))/'
                          'dischargeresult=(?P<dischargeresult>(\d+))/'
                          'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                          'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/'
                          'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                          'resultidu=(?P<resultidu>(\d+))/'
                          'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}\s+\d+:\d+))/'
                          'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}\s+\d+:\d+))/'
                          'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/samplingfeature=(?P<samplingfeature>(\d+))/'
                          'resultidu=(?P<resultidu>(\d+))/'
                          'dischargeresult=(?P<dischargeresult>(\d+))/'
                          'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}\s+\d+:\d+))/'
                          'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}\s+\d+:\d+))/'
                          'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/$',
                   views.TimeSeriesGraphingShort,
                   name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),
               re_path(
                   r'^' + 'graphfa/dataset=(?P<dataset>(\d+))/'
                                     'resultidu=(?P<resultidu>(\d+))/'
                                     'startdate=(?P<startdate>(\d{4}-\d{2}-\d{2}))/'
                                     'enddate=(?P<enddate>(\d{4}-\d{2}-\d{2}))/$',
                   views.TimeSeriesGraphingShort, name="TimeSeriesGraphingShort"),

               re_path(
                   r'^' + 'profilegraph/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/$',
                   views.graph_data, name="graph_data"),
               re_path(
                   r'^' + 'profilegraph/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),
               re_path(
                   r'^' + 'profilegraph/'
                                     'selectedrelatedfeature='
                                     '(?P<selectedrelatedfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),
               re_path(
                   r'^' + 'profilegraph/'
                                     'selectedrelatedfeature='
                                     '(?P<selectedrelatedfeature>(\d+))/'
                                     'samplingfeature=(?P<samplingfeature>(\d+))/'
                                     'popup=(?P<popup>(([a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z])))/$',
                   views.graph_data, name="graph_data"),

               # /(?P<startdate>(\d+))/(?P<enddate>(\d+))
               re_path(r'^' + 'chartVariableAndFeature.html', views.graph_data,
                   name="graph_data"),
               re_path(r'^' + 'soilsscatterplot.html', views.scatter_plot,
                   name="scatter_plot"),
               re_path(r'^' + 'publications.html', views.publications,
                   name="publications"),
               re_path(r'^' + 'features/type=(?P<sf_type>([\w\s]+,?)+)&'
                                              'datasets=(?P<ds_ids>([a-zA-Z]+)?(([0-9]+,?)+)?)', cache_page(settings.CACHE_TTL)(views.get_features)),
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
