from django.apps import AppConfig

from templatesAndSettings.settings import app_name, verbose_name


class ODM2AdminConfig(AppConfig):
    name = '{}'.format(app_name)
    verbose_name = '{}'.format(verbose_name)
