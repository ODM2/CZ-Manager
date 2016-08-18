from django.apps import AppConfig
from templatesAndSettings.settings import app_config

class ODM2AdminConfig(AppConfig):
    name = '{}'.format(app_config['app_name'])
    verbose_name = '{}'.format(app_config['verbose_name'])
