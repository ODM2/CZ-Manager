"""
Django settings for odm2testsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR =os.path.dirname(__file__)
TEMPLATE_DIR_APP = os.path.join(os.path.dirname(__file__), '..')
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'templates')
#TEMPLATE_PATH2 = os.path.join(TEMPLATE_DIR, 'templates/odm2testapp')
print(TEMPLATE_PATH)
TEMPLATE_DIRS = [TEMPLATE_PATH,] #TEMPLATE_PATH2,

#TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0c6x-v91u8z$kiq-)s6t1=a%lx!u946aa9wp2*_46#d1y4c-%m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/odm2testapp/upfiles/'
MEDIA_URL = '/odm2testapp/upfiles/'
# Application definition
STATIC_ROOT = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/static'

#https://github.com/mishbahr/django-modeladmin-reorder
#{'app': 'auth', 'models': ('auth.User', 'auth.Group')},
# ADMIN_REORDER = ('odm2testsite',
#                  {'app':'Odm2Testapp',
#                   'auth':'staff',
#                   'models':("People", "Organizations","Affiliations", "Variables","Units",
#                       "Taxonomicclassifiers","Methods","Actions","Relatedactions","Actionby","Samplingfeatures",
#                       "Featureactions","Datatsets","Results","Datasetsresults","Processinglevels","Measurementresults",
#                       "Measurementresultvalues","MeasurementresultvalueFile", "Dataloggerfiles",
#                       "Dataloggerprogramfiles")},
# )
INSTALLED_APPS = (
    'djangocms_admin_style',
    'odm2testapp',
    'chartit',
    'highcharts',
    'jquery',
    'admin_shortcuts',
    'daterange_filter',
    'django.contrib.admin',
    #'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'admin_reorder',
    'ajax_select',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader',
)
#find icon images here https://github.com/alesdotio/django-admin-shortcuts/blob/master/admin_shortcuts/templatetags/admin_shortcuts_tags.py#L134
ADMIN_SHORTCUTS = [
    {

        'shortcuts': [
            {
                'url': '/admin/',
                'app_name': 'odm2testapp',
                'title': 'Home',
                'class':'home',
            },
            {
                'url_name': 'admin:odm2testapp_results_changelist',
                'app_name': 'odm2testapp',
                'title': 'Results',
                'class':'archive',
            },
            {
                'url': '/admin/AddSensor.html',
                'app_name': 'odm2testapp',
                'title': 'Add Sensor Data',
                'class':'tool',
            },
        ]
    },
]
ADMIN_SHORTCUTS_SETTINGS = {
    'hide_app_list': False,
    'open_new_window': False,
}


#https://github.com/crucialfelix/django-ajax-selects
AJAX_LOOKUP_CHANNELS = {
    #  simple: search Person.objects.filter(name__icontains=q)
    'cv_variable_name': ('odm2testapp.lookups',  'CvVariableNameLookup'),
    'cv_variable_type': ('odm2testapp.lookups',  'CvVariableTypeLookup'),
    'cv_unit_type': ('odm2testapp.lookups',  'CvUnitTypeLookup'),
    # define a custom lookup channel
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'admin_reorder.middleware.ModelAdminReorder',
)

ROOT_URLCONF = 'odm2testsite.urls'

WSGI_APPLICATION = 'odm2testsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'x',
        'USER': 'x',
        'PASSWORD': 'x',
        'HOST': 'x', #micro server  '52.20.81.11'
        'PORT': 'x',
     'OPTIONS': {
      'options': '-c search_path=odm2'
    }
	}
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
