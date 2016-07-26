"""
Keep this file untracked
"""

# SECURITY WARNING: keep the secret key used in production secret!
secret_key = 'random_secret_key_like_so_7472873649836'


media_root = '/Users/lsetiawan/Desktop/shared_ubuntu/APL/ODM2/ODM2-Admin/ODM2CZOData/upfiles/'
media_url = '/odm2testapp/upfiles/'
# Application definition
custom_template_path = '/admin/ODM2CZOData/'
#admin_shortcuts_path = '/admin/'
url_path = 'admin/'
static_root = '/Users/lsetiawan/Desktop/shared_ubuntu/APL/ODM2/ODM2-Admin/static'#'C:/Users/leonmi/Google Drive/ODM2Djangoadmin/static'
debug = True
template_debug = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
ODM2_configs = {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'odm2',
        'USER': 'lsetiawan',
        'PASSWORD': '',
        'HOST': 'localhost', #micro server  '52.20.81.11'
        'PORT': '5432',
     'OPTIONS': {
      'options': '-c search_path=admin,odm2,odm2extra'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

static_url = '/static/'
from templatesAndSettings.base import *