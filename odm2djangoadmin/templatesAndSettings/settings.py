"""
Keep this file untracked
"""

# SECURITY WARNING: keep the secret key used in production secret!
secret_key = 'random_secret_key_like_so_7472873649836'


media_root = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/ODM2CZOData/upfiles/'
media_url = '/odm2testapp/upfiles/'
# Application definition
custom_template_path = '/admin/ODM2CZOData/'
#admin_shortcuts_path = '/admin/'
url_path = 'admin/'
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
from templatesAndSettings.base import *