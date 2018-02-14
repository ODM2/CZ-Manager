"""
Common settings and globals.
"""

import random
import os

""" NAMES CONFIGURATION """
APP_NAME = "odm2admin" # This has to match the name of the folder that the app is saved
VERBOSE_NAME = "ODM2 Admin"

SITE_HEADER = "ODM2 Admin"
SITE_TITLE = "ODM2 Admin"
""" END NAMES CONFIGURATION """


""" PATH CONFIGURATION """
# Absolute filesystem path to this Django project directory.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Absolute path where project is located
ROOT = os.path.dirname(BASE_DIR)# '/Volumes/Landung_2TB/Work/ODM2-Admin/'

# SECRET_KEY.
SECRET_KEY = 'myRanDom_Secret_Key'
# Application definition
BASE_URL = '' # Enter the base url in your APACHE SETTINGS. e.g. 'ODM2ADMIN/'

CUSTOM_TEMPLATE_PATH = '/{}{}/'.format(BASE_URL, APP_NAME)
""" END PATH CONFIGURATION """


""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = True
""" END DEBUG CONFIGURATION """


""" TEMPLATE CONFIGURATION """
TEMPLATE_DIR = os.path.join(ROOT)
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'templatesAndSettings/templates')

# List of callables that know how to import templates from various sources.
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [TEMPLATE_PATH, ],
    'APP_DIRS': True,
    'OPTIONS': {
        # 'loaders': [(
        #             'django.template.loaders.filesystem.Loader',
        #             'django.template.loaders.app_directories.Loader',
        #             'apptemplates.Loader',
        #             ), ],
        'debug': DEBUG,
        'context_processors': [
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'social_django.context_processors.backends',
            'social_django.context_processors.login_redirect',
        ],
    },
}]
""" END TEMPLATE CONFIGURATION """

""" MANAGER CONFIGURATION """
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = [
    {"name": "first last",
     "email": "email@example.com"}
]
""" END MANAGER CONFIGURATION """


""" GENERAL CONFIGURATION """
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Time zone support is disabled by default.
# To enable it, set USE_TZ = True
USE_TZ = True
""" END GENERAL CONFIGURATION """


""" MEDIA CONFIGURATION """
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '{}/{}/upfiles/'.format(BASE_DIR, APP_NAME)
#  URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/{}/{}/media/'.format(os.path.basename(BASE_DIR), APP_NAME)
""" END MEDIA CONFIGURATION """
# Absolute filesystem path to the directory that will hold database export and import files
FIXTURE_DIR = '{}/{}/fixtures/'.format(BASE_DIR, APP_NAME)

""" STATIC FILE CONFIGURATION """
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '{}/{}/static'.format(BASE_DIR, APP_NAME)
# URL prefix for static files.
STATIC_URL = '/static/'
""" END STATIC FILE CONFIGURATION """
""" END PATH CONFIGURATION """

""" MIDDLEWARE CONFIGURATION """
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware', didn't work in production
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'admin_reorder.middleware.ModelAdminReorder',
)
""" END MIDDLEWARE CONFIGURATION """

""" OAUTH SETTINGS """
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    #'odm2admin.hydroshare_backend.HydroShareOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
# Oauth CORS_ORIGIN_ALLOW_ALL = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)
""" END OAUTH SETTINGS """

""" URL AND WSGI CONFIGURATION """
ROOT_URLCONF = 'templatesAndSettings.urls'

WSGI_APPLICATION = 'templatesAndSettings.wsgi.application'
""" END URL CONFIGURATION"""

""" APP CONFIGURATION """
INSTALLED_APPS = (
    'jquery',
    'djangocms_admin_style',
    '{}'.format(APP_NAME),
    'import_export',
    'social_django',
    'admin_shortcuts',
    'daterange_filter',
    'captcha',
    'fixture_magic',
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
""" END APP CONFIGURATION """


""" ADMIN SHORTCUTS CONFIGURATION """
ADMIN_SHORTCUTS = [
    {

        'shortcuts': [
            {
                'url': CUSTOM_TEMPLATE_PATH,
                'app_name': '{}'.format(APP_NAME),
                'title': '{}'.format(VERBOSE_NAME),
                'class': 'config',
            },
            {
                'url': '/' + 'AddSensor',
                'app_name': '{}'.format(APP_NAME),
                'title': 'Add Sensor Data',
                'class': 'tool',
            },
            {
                'url': '/' + 'AddProfile',
                'app_name': '{}'.format(APP_NAME),
                'title': 'Add Soil Profile Data',
                'class': 'flag',
            },
            {
                'url': '/' + 'RecordAction',
                'app_name': '{}'.format(APP_NAME),
                'title': 'Record an Action',
                'class': 'notepad',
            },
            {
                'url': '/' + 'ManageCitations',
                'app_name': '{}'.format(APP_NAME),
                'title': 'Manage Citations',
                'class': 'pencil',
            },
            {
                'url': '/' + 'chartIndex',
                'app_name': '{}'.format(APP_NAME),
                'title': 'Graph My Data',
                'class': 'monitor',
            },
        ]
    },
]
ADMIN_SHORTCUTS_SETTINGS = {
    'hide_app_list': False,
    'open_new_window': False,
}
""" END ADMIN SHORTCUTS CONFIGURATION """



""" SAMPLING FEATURE TYPE LEGEND MAPPING """
LEGEND_MAP = {
        'Excavation': dict(feature_type="Excavation", icon="fa-spoon", color="darkred",
                           style_class="awesome-marker-icon-darkred"),
        'Field area': dict(feature_type="Field area", icon="fa-map-o", color="darkblue",
                           style_class="awesome-marker-icon-darkblue"),
        'Weather station': dict(feature_type="Weather station", icon="fa-cloud", color="darkblue",
                                style_class="awesome-marker-icon-darkblue"),
        'Ecological land classification': dict(feature_type="Ecological land classification",
                                               icon="fa-bar-chart", color="darkpurple",
                                               style_class="awesome-marker-icon-darkpurple"),
        'Observation well': dict(feature_type="Observation well", icon="fa-eye", color="orange",
                                 style_class="awesome-marker-icon-orange"),
        'Site': dict(feature_type="Site", icon="fa-dot-circle-o", color="green",
                     style_class="awesome-marker-icon-green"),
        'Stream gage': dict(feature_type="Stream gage", icon="fa-tint", color="blue",
                            style_class="awesome-marker-icon-blue"),
        'Transect': dict(feature_type="Transect", icon="fa-area-chart", color="cadetblue",
                         style_class="awesome-marker-icon-cadetblue"),
        'Profile': dict(feature_type="Profile", icon="fa-database", color="purple",
             style_class="awesome-marker-icon-purple"),
        'Specimen': dict(feature_type="Specimen", icon="fa-flask", color="cadetblue",
                         style_class="awesome-marker-icon-cadetblue")
    }
""" END SAMPLING FEATURE TYPE LEGEND MAPPING """

""" REDIS CACHING CONFIGURATION """
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "odm2admin"
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15
""" END REDIS CACHING CONFIGURATION"""