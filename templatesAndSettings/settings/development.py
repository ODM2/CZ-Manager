"""
Development settings and globals.
"""


from .base import *

# oauth name =odm2adminlczotest
# oauth client id =HkKIdftCyywZs7IipyED7hwAPAGRVVmAuf2SkGFh
#oauth client secert = 4Dt2LpEyB5tAyZ27u3iE9eo0F1Q7uGoXyjnq5qrrCxpPDxJDWMJVULdyPoKQ7KeJXCHaN416CZta7NhElnlKWkVLXbYl4LjkC2RONF3L8hN3IpaIPCqA2oa6qdViQGZm
PYTHON_PATH = ''
EXPORTDB =False
UTC_OFFSET = 0

""" DEBUG CONFIGURATION """
# Disable debugging by default.
DEBUG = True
""" END DEBUG CONFIGURATION """

""" ALLOWED HOSTS CONFIGURATION """
ALLOWED_HOSTS = ['odm2admin.cuahsi.org', 'dev-odm2admin.cuahsi.org', '127.0.0.1','bitnami-miguel.cuahsi.org']
""" END ALLOWED HOSTS CONFIGURATION """
# from https://console.cloud.google.com/apis/credentials?project=centering-cable-182714
#ODM2 Admin key and secret
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='939572189050-iuo3536bfhhjn876tj1ti60829glt7l8.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ='uNnjcTe9ajvr6OyKyTHgZwUB'
SOCIAL_AUTH_HYDROSHARE_KEY ='o7bwd2SBOhk82KpLq8kJSMDbANh5rEt0JideQrFk'
SOCIAL_AUTH_HYDROSHARE_SECRET ='G9OPLzpLauZDgs4tfnYiwInc3OwW7AxaubYH0PM3Tpb6KYahMQPyHvZXSgmUR5mT0yRxAzz9P7vJsSmTUQqyh6D4pLJQmXUxyD0w8mD1chqEH4Fwdj8dR2WkpCdI3TGY'

SOCIAL_AUTH_HYDROSHARE_UP_KEY = 'QKSeACnlgEWCz3vG2Rv1VJFrzNFRv7Syn6eHMLle'
SOCIAL_AUTH_HYDROSHARE_UP_SECRET = 'Wb7QBF5vPHyz7pQk8xvdAkE9OCaM02GhtKuJowBnj0e56apoiMi0chVdfRoi3nsaihcIbyMzHphVfWLEVZ1sSuoM8pkiR26UsGHzug1S4ZrnRJD7VdiLnQ6p78xUlwkl'

""" EMAIL CONFIGURATION """
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'do-not-reply-LuquilloCZO'
EMAIL_HOST_PASSWORD = '7jmftUpata'
EMAIL_FROM_ADDRESS = 'do-not-reply-ODM2-Admin@cuahsi.org'
RECAPTCHA_PUBLIC_KEY = '6LdYnQ8UAAAAAI38kvlrKy4kF28VMYWnGO4dDjPA'
RECAPTCHA_PRIVATE_KEY = '6LdYnQ8UAAAAAIAfLHzvj9MEnW2PKt1WDnInyafn'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
""" EMAIL CONFIGURATION """
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
TRAVIS_ENVIRONMENT=False
FIXTURE_DIR = '/home/miguelcleon/webapps/odm2admin2/templatesAndSettings/fixtures/'


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
                  'NAME': 'C:/Users/leonmi/Google Drive/ODM2AdminLT2/ODM2SQliteBlank.db',
              },
    'default': {
                   'ENGINE': 'django.contrib.gis.db.backends.postgis', #django.contrib.gis.db.backends.postgis
                   'OPTIONS': {
                        'options': '-c search_path=odm2,admin,odm2extra,public'
                    },
                   'NAME': 'ODM2DryCreek',  # ODM2LCZO ODM2CJCZO  ODM2DryCreek ODM2MSU ODM2LCZO ODM2LCZOPublished DryCreekTest CJCZOTest DryCreekTest # texas odm2two
                   'USER': 'azureadmin',  # local azureadmin
                   'PASSWORD': 'cuahsi196',  # MSU msu196 cuahsi196 local 7jmftUpata
                   'HOST': '13.82.236.30',  # MSU 52.168.167.57   dev  40.85.180.138 prod 13.82.236.30 # texas 18.216.144.246
                   'PORT': '5432', # 5432

               },
    # 'default': {
    #                'ENGINE': 'sql_server.pyodbc', #django.contrib.gis.db.backends.postgis
    #                'NAME': 'ODM2',  # ODM2LCZO ODM2CJCZO  ODM2DryCreek ODM2MSU ODM2LCZO ODM2LCZOPublished
    #                'USER': 'SA',  # local
    #                'PASSWORD': '7jmftUpata',  # MSU msu196 cuahsi196 local 7jmftUpata
    #                'HOST': '127.0.0.1',  # MSU 52.168.167.57   dev  40.85.180.138 prod 13.82.236.30
    #                'PORT': '', # 5432
    #            },
    'published': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'odm2two',  # ODM2CJCZO  ODM2DryCreek ODM2MSU ODM2LCZOPublished ODM2LCZO
        'USER': 'azureadmin',
        'PASSWORD': 'cuahsi196',  # MSU msu196
        'HOST': '18.216.144.246',  # MSU 52.168.167.57   dev 0.85.180.138  prod 13.82.236.30 texas
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=odm2,admin,odm2extra,public'
        }
    }
     }
""" END DATABASE CONFIGURATION """
""" SENSOR DASHBOARD CONFIGURATION """

SENSOR_DASHBOARD = {
    "time_series_days": 10,
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
      "access_token": 'pk.eyJ1IjoibWlndWVsY2xlb24iLCJhIjoiY2o5dTkyOWVlM3pxZTMzbGc2OWswdzA1MyJ9.K4gp1ZRvOi-36nDsKqTLvw'
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
MEDIA_ROOT = '/home/miguelcleon/webapps/odm2admin2/odm2admin/upfiles/'