"""
Django settings for odm2testsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from templatesAndSettings.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR_APP = os.path.join(os.path.dirname(__file__), '..')
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'templates')
# TEMPLATE_PATH2 = os.path.join(TEMPLATE_DIR, 'templates/odm2testapp')
# print(TEMPLATE_PATH)
TEMPLATE_DIRS = [TEMPLATE_PATH, ]  # TEMPLATE_PATH2,

# TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

# TEMPLATE_DEBUG = TEMPLATE_DEBUG
ADMINS = ADMINS
ALLOWED_HOSTS = []
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_PORT = EMAIL_PORT
EMAIL_FROM_ADDRESS = EMAIL_FROM_ADDRESS
RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY

MEDIA_ROOT = MEDIA_ROOT
MEDIA_URL = MEDIA_URL

# Application definition
CUSTOM_TEMPLATE_PATH = CUSTOM_TEMPLATE_PATH
# ADMIN_SHORTCUTS_PATH=admin_shortcuts_path
URL_PATH = URL_PATH
STATIC_ROOT = STATIC_ROOT
MAP_CONFIG = MAP_CONFIG
DATA_DISCLAIMER = DATA_DISCLAIMER
# https://github.com/mishbahr/django-modeladmin-reorder
# {'app': 'auth', 'models': ('auth.User', 'auth.Group')},
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
    '{}'.format(APP_NAME),
    'import_export',
    'admin_shortcuts',
    'daterange_filter',
    'captcha',
    # 'dal',
    # 'dal_select2',
    'ajax_select',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'admin_reorder',

)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader',
)
# find icon images here https://github.com/alesdotio/
# django-admin-shortcuts/blob/master/admin_shortcuts/
# templatetags/admin_shortcuts_tags.py#L134
ADMIN_SHORTCUTS = ADMIN_SHORTCUTS
ADMIN_SHORTCUTS_SETTINGS = {
    'hide_app_list': False,
    'open_new_window': False,
}

# https://github.com/crucialfelix/django-ajax-selects
AJAX_LOOKUP_CHANNELS = AJAX_LOOKUP_CHANNELS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware', didn't work in production
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'admin_reorder.middleware.ModelAdminReorder',
)

ROOT_URLCONF = 'templatesAndSettings.urls'

WSGI_APPLICATION = 'templatesAndSettings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = DATABASES
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = STATIC_URL
