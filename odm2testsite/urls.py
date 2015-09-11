from django.conf.urls import patterns, include, url
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from odm2testapp import views
from odm2testsite.settings import MEDIA_ROOT

admin.autodiscover()
admin.site.site_header = 'ODM2 Admin'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project_17.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/AddSensor.html', views.AddSensor, name="AddSensor"),
    url(r'^admin/RecordAction.html', views.RecordAction, name="RecordAction"),
    #for uploaded files like dataloggerfiles
    url(r'^odm2testapp/upfiles/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT,
        }),
    url(r'^admin/chart.html', views.temp_pivot_chart_view, name="temp_pivot_chart_view"),
    #url(r'^admin/DataloggerfilecolumnsDisplay.html', views.dataloggercolumnView, name="dataloggercolumnView"),
    #url(r'^admin/odm2testapp/dataloggerfiles/\d+/', views.dataloggercolumnView, name="dataloggercolumnView"),
    #url(r'^contas_pagar/pagamento/(?P<id_parcela>\d+)/$',
                             #'contas_pagar.views.retorna_pagamentos_parcela'),

)