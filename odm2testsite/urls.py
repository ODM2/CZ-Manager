from django.conf.urls import patterns, include, url
from django.contrib import admin
from rango import views 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project_17.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	 url(r'^odm2testapp/', include('odm2testapp.urls')),
)