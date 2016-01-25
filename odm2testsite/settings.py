"""
Keep this file untracked
"""

# SECURITY WARNING: keep the secret key used in production secret!
secret_key = 'x'


media_root = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/odm2testapp/upfiles/'
media_url = '/odm2testapp/upfiles/'
# Application definition
custom_template_path = '/admin/odm2testapp/'
admin_shortcuts_path = '/admin/'
static_root = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/static'
debug = True
template_debug = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
ODM2_configs = {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'x',
        'USER': 'x',
        'PASSWORD': 'x',
        'HOST': 'x', #micro server  '52.20.81.11'
        'PORT': 'x',
     'OPTIONS': {
      'options': '-c search_path=odm2,odm2extra'
    }

}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

static_url = '/static/'
from odm2testsite.base import *