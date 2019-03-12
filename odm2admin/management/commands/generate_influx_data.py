from datetime import datetime

from django.core.management import BaseCommand

# from dataloader.helpers import InfluxHelper
# from odm2admin.models import SiteSensor


from datetime import datetime

import pandas as pd
import numpy as np
import os

from django.conf import settings
from django.db.models import F

from influxdb import DataFrameClient
from influxdb.exceptions import InfluxDBClientError

from odm2admin.models import Timeseriesresultvalues
from odm2admin.models import Timeseriesresults
from odm2admin.models import Results
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings")

class InfluxHelper(object):
    class MissingConnectionException(Exception):
        """Client is not defined or connected"""
        pass

    def __init__(self, *args, **kwargs):
        self.client = None
        self.batch_size = 10000
        self.connection_info = settings.INFLUX_CONNECTION

    def connect_to_dataframe_client(self):
        self.client = DataFrameClient(
            host=self.connection_info['host'],
            port=self.connection_info['port'],
            username=self.connection_info['username'],
            password=self.connection_info['password'],
            database=self.connection_info['database']
        )

    def recreate_database(self):
        read_user = self.connection_info['read_username']
        database_name = self.connection_info['database']

        if not self.client:
            raise InfluxHelper.MissingConnectionException('InfluxDB client is not connected.')

        self.client.drop_database(database_name)
        self.client.create_database(database_name)
        self.client.grant_privilege('read', database_name, read_user)

    def write_all_sensor_values(self, sensor):
        self.write_sensor_values(sensor, datetime.min)

    def get_series_last_value(self, identifier):
        query_string = 'select last(DataValue), time from {identifier}'.format(identifier=identifier)
        result = self.client.query(query_string, database=self.connection_info['database'])
        if result and len(result) == 1:
            dataframe = result[identifier]  # type: pd.DataFrame
            return dataframe.first_valid_index().to_pydatetime()

    def write_sensor_values(self, sensor, starting_datetime):
        values = Timeseriesresultvalues.objects.filter(valuedatetime__gt=starting_datetime, resultid=sensor.resultid)\
            .annotate(DateTime=F('valuedatetime'))\
            .annotate(UTCOffset=F('valuedatetimeutcoffset'))\
            .annotate(DataValue=F('datavalue'))
        values_dataframe = self.prepare_data_values(values)
        if values_dataframe.empty:
            return 0

        result = self.add_dataframe_to_database(values_dataframe, sensor.influx_identifier)
        del values_dataframe
        return result

    def prepare_data_values(self, values_queryset):
        dataframe = pd.DataFrame.from_records(values_queryset.values('DateTime', 'UTCOffset', 'DataValue'))
        if dataframe.empty:
            return dataframe

        dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])
        dataframe.set_index(['DateTime'], inplace=True)
        dataframe['DataValue'] = pd.to_numeric(dataframe['DataValue'], errors='coerce').astype(np.float64)
        dataframe['UTCOffset'] = pd.to_numeric(dataframe['UTCOffset'], errors='coerce').astype(np.float64)
        dataframe.dropna(how='any', inplace=True)
        return dataframe

    def add_dataframe_to_database(self, dataframe, identifier):
        try:
            write_success = self.client.write_points(dataframe, identifier, time_precision='s', batch_size=self.batch_size)
            return len(dataframe) if write_success else 0
        except InfluxDBClientError as e:
            print('Error while writing to database {}: {}'.format(identifier, e.message))
            return 0

class Command(BaseCommand):
    help = 'Copy data values over to the InfluxDB instance.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            help='Drop the influx database before filling up data.',
        )

    def handle(self, *args, **options):
        recreate_database = True # options.get('clean')
        dfc = DataFrameClient(host='bitnami-miguel.cuahsi.org',port=18086,
                              database='lczotest', username='miguelcleon', password='Upata7jmft')
        print('list db')
        print(dfc.get_list_database())
        helper = InfluxHelper()
        helper.client = dfc
        helper.connect_to_dataframe_client()
        # QS conductivity
        sensors = Timeseriesresults.objects.all()  # filter(resultid=18580)

        if recreate_database:
            helper.recreate_database()

        for sensor in sensors:
            print('- writing data to sensor {}'.format(sensor.resultid))
            last_value = helper.get_series_last_value(sensor.resultid.resultuuid)
            starting_point = last_value and last_value.replace(tzinfo=None) or datetime.min
            result = helper.write_sensor_values(sensor, starting_point)
            print('-- {} points written.'.format(result))