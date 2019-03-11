"""
Development settings and globals.
"""

from .base import *

""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = True
EXPORTDB =False
USE_TZ = False
""" END DEBUG CONFIGURATION """

""" ALLOWED HOSTS CONFIGURATION """
ALLOWED_HOSTS = ['127.0.0.1',]
""" END ALLOWED HOSTS CONFIGURATION """

""" HYDROSHARE API CONFIGURATION """
PYTHON_EXEC='/home/bitnami/miniconda3/envs/odm2adminenv/bin/python'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='xxx.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ='xxx'
SOCIAL_AUTH_HYDROSHARE_KEY ='xxx'
SOCIAL_AUTH_HYDROSHARE_SECRET ='xxx'

SOCIAL_AUTH_HYDROSHARE_UP_KEY = 'xxx'
SOCIAL_AUTH_HYDROSHARE_UP_SECRET = 'xxx'

""" END HYDROSHARE API CONFIGURATION """

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
    "link" : "http://mysiteswegpage.page/"

}
""" END DATA DISCLAIMER CONFIGURATION """

""" DATABASE CONFIGURATION """
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3','NAME':'',}, 'export': {'ENGINE': 'django.db.backends.sqlite3','NAME':'',}}

""" END DATABASE CONFIGURATION """
