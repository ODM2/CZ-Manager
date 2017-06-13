"""
Production settings and globals.
"""

from base import *

""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = False
""" END DEBUG CONFIGURATION """

""" ALLOWED HOSTS CONFIGURATION """
ALLOWED_HOSTS = ['127.0.0.1',]
""" END ALLOWED HOSTS CONFIGURATION """


""" EMAIL CONFIGURATION """
EMAIL_HOST = 'smtp.host'
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_FROM_ADDRESS = 'do-not-reply-ODM2-Admin@cuahsi.org'
RECAPTCHA_PUBLIC_KEY = 'googlerecaptchakey'
RECAPTCHA_PRIVATE_KEY = 'googlerecaptchaprivatekey'
EMAIL_USE_TLS = True
EMAIL_PORT = 123
""" EMAIL CONFIGURATION """


""" DATABASE CONFIGURATION """
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'db_name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public,admin,odm2,odm2extra'
        }
    }
}
""" END DATABASE CONFIGURATION """


""" MAP CONFIGURATION """
MAP_CONFIG = {
    "lat": 0,
    "lon": 0,
    "zoom": 11,
    "cluster_sites": False,
    "time_series_months": 3,
    "MapBox": {
      "access_token": 'mapbox accessToken'
    },
    "result_value_processing_levels_to_display": [1, 2, 3],
    "feature_types": ['Site', 'Profile']
}
""" END MAP CONFIGURATION """


""" DATA DISCLAIMER CONFIGURATION """
DATA_DISCLAIMER = {
    "text" : "Add a link discribing where your data come from",
    "linktext" : "The name of my site",
    "link" : "http://mysiteswegpage.page/"

}
""" END DATA DISCLAIMER CONFIGURATION """

""" PATH CONFIGURATION """
# SECRET_KEY.
SECRET_KEY = 'myRanDom_Secret_Key'
# Application definition
CUSTOM_TEMPLATE_PATH = '/admin/{}/'.format(APP_NAME)
BASE_URL= 'admin/'
URL_PATH = 'admin/'
""" END PATH CONFIGURATION """

""" MEDIA CONFIGURATION """
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '{}/{}/upfiles/'.format(BASE_DIR, APP_NAME)
# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/{}/{}/media/'.format(os.path.basename(BASE_DIR), APP_NAME)
""" END MEDIA CONFIGURATION """


""" STATIC FILE CONFIGURATION """
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '{}/{}/static'.format(BASE_DIR, APP_NAME)
# URL prefix for static files.
STATIC_URL = '/static/'
""" END STATIC FILE CONFIGURATION """

