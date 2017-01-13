"""
Keep this file untracked
"""
import os
from base import *
import yaml

# ========================================================================
# ACTUAL SETTINGS ========================================================

SETTINGS_FILE = 'settings.yaml'

with open(os.path.join(BASE_DIR, SETTINGS_FILE), 'r') as src:
    configs = yaml.load(src)

VERBOSE_NAME = configs['Name']
SITE_HEADER = configs['Site Header']
SITE_TITLE = configs['Site Title']

MAP_CONFIG = configs['Map Config']
DATA_DISCLAIMER = configs['Data Disclaimer']

SECRET_KEY = configs['Secret Key']
ROOT = configs['Root']

DATABASES['default']['NAME'] = configs['Database config']['name']
DATABASES['default']['USER'] = configs['Database config']['user']
DATABASES['default']['PASSWORD'] = configs['Database config']['password']
DATABASES['default']['HOST'] = configs['Database config']['host']
DATABASES['default']['PORT'] = configs['Database config']['port']

ADMINS = configs['Administrator']
APP_NAME = configs['App']

EMAIL_HOST = configs['Email Host']
EMAIL_HOST_USER = configs['User']
EMAIL_HOST_PASSWORD = configs['Password']
EMAIL_FROM_ADDRESS = configs['Email From Address']
RECAPTCHA_PUBLIC_KEY = configs['Recaptcha Public Key']
RECAPTCHA_PRIVATE_KEY = configs['Recaptcha Private Key']
EMAIL_USE_TLS = configs['Use TLS']
EMAIL_PORT = configs['Email PORT']

# TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

DEBUG = configs['Debug']
ALLOWED_HOSTS = configs['Allowed Hosts']

MEDIA_ROOT = configs['Media Root']
MEDIA_URL = configs['Media URL']
CUSTOM_TEMPLATE_PATH = configs['Custom Template Path']
URL_PATH = configs['URL Path']
STATIC_ROOT = configs['Static Root']

# =======================================================
