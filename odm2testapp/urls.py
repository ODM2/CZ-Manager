from django.conf.urls import patterns,include, url
from django.contrib import admin
from odm2testapp import views
from django.conf import settings

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
		#url(r'^add_variable/', views.add_variable, name='add_variable'),
		url(r'^admin/', include(admin.site.urls)))
if settings.DEBUG:
     # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
    (r'^upfiles/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))
