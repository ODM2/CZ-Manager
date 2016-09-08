"""
Keep this file untracked
"""

# Custom App settings
# This has to match the name of the folder that the app is saved.
app_name = "ODM2CZOData"
verbose_name = "ODM2CZOData"
site_title = "ODM2 Admin"
site_header = "ODM2 Admin"
map_config = {
    "lat": 0,
    "lon": 0,
    "zoom": 2
}

data_disclaimer = {
    "text": "Add a link discribing where your data come from ",
    "linktext": "The name of my site",
    "link": "http://mysiteswegpage.page/",
}

# SECURITY WARNING: keep the secret key used in production secret!
secret_key = 'random_secret_key_like_so_7472873649836'
_root = 'C:/Users/leonmi/Google Drive/ODM2Djangoadmin'

media_root = '{}'.format(_root)
media_url = '/odm2testapp/upfiles/'

# Application definition
custom_template_path = '/admin/{}/'.format(app_name)
url_path = 'admin/'
static_root = '{}/static'.format(_root)
debug = True
template_debug = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
ODM2_configs = {

    'ENGINE': 'django.contrib.gis.db.backends.postgis',  # 'django.db.backends.postgresql_psycopg2'  # noqa
    'NAME': 'name',
    'USER': 'postgres',
    'PASSWORD': 'password',
    'HOST': 'localhost',
    'PORT': '5432',
    'OPTIONS': {
        'options': '-c search_path=admin,odm2,odm2extra'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
static_url = '/static/'

admins = [{
    "name": "first last",
    "email": "email@example.com"
}]

# FIXME: Do not import *
# from templatesAndSettings.base import *
