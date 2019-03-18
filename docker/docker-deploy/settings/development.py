"""
Development settings and globals.
"""

from .base import *

""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = True
""" END DEBUG CONFIGURATION """

""" EXPORTDB FLAG CONFIGURATION - if set to true this will use Camel case table names for SQLite"""
EXPORTDB = False
""" EXPORTDB FLAG CONFIGURATION """

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
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'OPTIONS': {
            'options': '-c search_path=admin,odm2,odm2extra,public'
        }
    }
}
""" END DATABASE CONFIGURATION """


""" MAP CONFIGURATION """
MAP_CONFIG = {
    "lat": 0,
    "lon": 0,
    "zoom": 2,
    "cluster_sites": False,
    "time_series_months": 3,
    "MapBox": {
      "access_token": 'mapboxAccessToken'
    },
    "result_value_processing_levels_to_display": [1, 2, 3],
    "feature_types": ['Excavation', 'Field area', 'Weather station', 
    'Ecological land classification', 'Observation well', 'Site','Stream gage','Transect', 'Profile','Specimen']
}
""" END MAP CONFIGURATION """


""" DATA DISCLAIMER CONFIGURATION """
DATA_DISCLAIMER = {
    "text" : "Add a link discribing where your data come from",
    "linktext" : "The name of my site",
    "link" : "http://mysiteswegpage.page/"

}
""" END DATA DISCLAIMER CONFIGURATION """
