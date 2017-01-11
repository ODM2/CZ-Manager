from django.apps import AppConfig
from django.core.management import settings


class ODM2AdminConfig(AppConfig):
    name = '{}'.format(settings.APP_NAME)
    verbose_name = '{}'.format(settings.VERBOSE_NAME)
