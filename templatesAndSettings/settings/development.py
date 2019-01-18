"""
Development settings and globals.
"""

from .base import *

""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = True
""" END DEBUG CONFIGURATION """

""" EXTRA VARIABLES CONFIGURATION -"""
EXPORTDB = False #  if set to true this will use Camel case table names for SQLite
UTC_OFFSET = -4
#Needed for Hydroshare integration
PYTHON_EXEC='/home/bitnami/miniconda3/envs/odm2adminenv/bin/python'
""" EXTRA VARIABLES CONFIGURATION """

""" TRAVIS CONFIGURATION """
TRAVIS_ENVIRONMENT = False
if 'TRAVIS' in os.environ:
    TRAVIS_ENVIRONMENT = True
""" END TRAVIS CONFIGURATION """

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
if TRAVIS_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test',  # Must match travis.yml setting
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:

    DATABASES = {
        'export': {  # export
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'ODM2SQliteBlank.db',
        },
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

        },
        'published': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'db_name_published',
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

""" SENSOR DASHBOARD CONFIGURATION """

SENSOR_DASHBOARD = {
    "time_series_days": 30,
    "featureactionids": [1699, 1784,1782,1701],
}
""" END SENSOR DASHBOARD CONFIGURATION"""

""" MAP CONFIGURATION """
MAP_CONFIG = {
    "lat": 0,
    "lon": 0,
    "zoom": 2,
    "cluster_feature_types": ['Profile','Specimen','Excavation','Field area'],
    "time_series_months": 1,
    "display_titles": True,
    "MapBox": {
      "access_token": 'mapbox accessToken'
    },
    "result_value_processing_levels_to_display": [1, 2, 3],
    "feature_types": ['Site','Profile','Specimen','Excavation','Field area',
                  'Weather station','Observation well','Stream gage','Transect']
}
""" END MAP CONFIGURATION """


""" DATA DISCLAIMER CONFIGURATION """
DATA_DISCLAIMER = {
    "text" : "Add a link discribing where your data come from",
    "linktext" : "The name of my site",
    "link" : "http://mysiteswegpage.page/",
}
""" END DATA DISCLAIMER CONFIGURATION """
