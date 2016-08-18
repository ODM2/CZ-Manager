"""
Keep this file untracked
"""

# SECURITY WARNING: keep the secret key used in production secret!
import json
json_data = open('./templatesAndSettings/config.json')
configurations = json.load(json_data)
json_data.close()


app_config = configurations['app_configuration']
db_config = configurations['database_configuration']

secret_key = '{}'.format(app_config['secret_key'])


media_root = '{0}/{1}/upfiles/'.format(app_config['*_root'],app_config['app_name'])
media_url = '/odm2testapp/upfiles/'
# Application definition
custom_template_path = '/admin/{}/'.format(app_config['app_name'])
#admin_shortcuts_path = '/admin/'
url_path = 'admin/'
static_root = '{}/static'.format(app_config['*_root'])
debug = True
template_debug = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
ODM2_configs = {

        'ENGINE': 'django.contrib.gis.db.backends.postgis', #'django.db.backends.postgresql_psycopg2',
        'NAME': '{}'.format(db_config['name']),
        'USER': '{}'.format(db_config['user']),
        'PASSWORD': '{}'.format(db_config['password']),
        'HOST': '{}'.format(db_config['host']),
        'PORT': '{}'.format(db_config['port']),
     'OPTIONS': {
      'options': '-c search_path=admin,odm2,odm2extra'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

static_url = '/static/'
from templatesAndSettings.base import *