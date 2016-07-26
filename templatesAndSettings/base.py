"""
Django settings for odm2testsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from templatesAndSettings.settings import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR =os.path.dirname(__file__)
TEMPLATE_DIR_APP = os.path.join(os.path.dirname(__file__), '..')
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'templates')
#TEMPLATE_PATH2 = os.path.join(TEMPLATE_DIR, 'templates/odm2testapp')
#print(TEMPLATE_PATH)
TEMPLATE_DIRS = [TEMPLATE_PATH,] #TEMPLATE_PATH2,

#TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug

TEMPLATE_DEBUG = template_debug

ALLOWED_HOSTS = []

MEDIA_ROOT = media_root
MEDIA_URL = media_url
# Application definition
CUSTOM_TEMPLATE_PATH = custom_template_path
#ADMIN_SHORTCUTS_PATH=admin_shortcuts_path
URL_PATH = url_path
STATIC_ROOT = static_root
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
    'jquery',
    'djangocms_admin_style',
    'ODM2CZOData',
    'import_export',
    'admin_shortcuts',
    'daterange_filter',
    'ajax_select',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'admin_reorder',

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
                'url': CUSTOM_TEMPLATE_PATH,
                'app_name': 'ODM2CZOData',
                'title': 'Home',
                'class':'home',
            },
            {
                'url_name': 'admin:ODM2CZOData_measurementresultvalues_changelist',
                'app_name': 'ODM2CZOData',
                'title': 'Results',
                'class':'archive',
            },
            {
                'url': '/'+URL_PATH+ 'AddSensor.html',
                'app_name': 'ODM2CZOData',
                'title': 'Add Sensor Data',
                'class':'tool',
            },
            {
                'url': '/'+URL_PATH+'AddProfile.html',
                'app_name': 'ODM2CZOData',
                'title': 'Add Soil Profile Data',
                'class':'flag',
            },
            {
                'url': '/'+URL_PATH+ 'RecordAction.html',
                'app_name': 'ODM2CZOData',
                'title': 'Record an Action',
                'class':'notepad',
            },
             {
                'url': '/'+URL_PATH+ 'ManageCitations.html',
                'app_name': 'ODM2CZOData',
                'title': 'Manage Citations',
                'class':'pencil',
            },
            {
                'url': '/'+URL_PATH+ 'chartIndex.html',
                'app_name': 'ODM2CZOData',
                'title': 'Graph My Data',
                'class':'monitor',
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
    'cv_variable_name': ('ODM2CZOData.lookups',  'CvVariableNameLookup'),
    'cv_variable_type': ('ODM2CZOData.lookups',  'CvVariableTypeLookup'),
    'cv_unit_type': ('ODM2CZOData.lookups',  'CvUnitTypeLookup'),
    'cv_speciation': ('ODM2CZOData.lookups',  'CvVariableSpeciationLookup'),
    'featureaction_lookup': ('ODM2CZOData.lookups',  'FeatureactionsLookup'),
    'result_lookup': ('ODM2CZOData.lookups',  'ResultsLookup'),
    'profileresult_lookup': ('ODM2CZOData.lookups', 'ProfileResultsLookup'),
    'measurementresult_lookup': ('ODM2CZOData.lookups', 'MeasurementResultsLookup')
    # define a custom lookup channel
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware', didn't work in production
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'admin_reorder.middleware.ModelAdminReorder',
)

ROOT_URLCONF = 'templatesAndSettings.urls'

WSGI_APPLICATION = 'templatesAndSettings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':  ODM2_configs['ENGINE'],
        'NAME': ODM2_configs['NAME'],
        'USER': ODM2_configs['USER'],
        'PASSWORD': ODM2_configs['PASSWORD'],
        'HOST': ODM2_configs['HOST'],
        'PORT': ODM2_configs['PORT'],
     'OPTIONS': ODM2_configs['OPTIONS'],

}}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = static_url
