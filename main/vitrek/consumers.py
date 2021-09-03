import json

from channels.generic.websocket import JsonWebsocketConsumer
from .models import MeasuresSetting, CurrentMeasure, Customer, MeasurePoint
from .libs.Vitrek4700driver import Vitrek4700, TCPConnector
import time
from .exports import ExportData


class MeasuresConsumer(JsonWebsocketConsumer):

    def receive_json(self, content, **kwargs):
        print(content)
        if content.get('command') == 'start_measures':
            self.start_measures(content)
        elif content.get('command') == 'clear_table':
            self.clear_table()
        elif content.get('command') == 'save_data':
            self.save_data(content)
        elif content.get('command') == 'new_device':
            self.new_device()
        elif content.get('command') == 'save_customer':
            self.save_customer(content)
        elif content.get('command') == 'generate_report':
            self.generate_report()

    def start_measures(self, content):
        settings = MeasuresSetting.objects.get(pk=1)  # change to class method
        vitrek = Vitrek4700(TCPConnector(ip=settings.vitrek_IP, port=settings.vitrek_Port))
        vitrek.connector.connect()
        divider = MeasuresSetting.get_divider()
        emr = MeasuresSetting.get_emr()
        CurrentMeasure.set_measure_point(measure_point=content["measure_point"], current_type=content["current_type"])
        for i in range(settings.measures_count):
            data = vitrek.get_measures()
            data['ACV'] = round(data['ACV'] / divider, ndigits=emr)
            data['DCV'] = round(data['DCV'] / divider, ndigits=emr)
            data['PKPK'] = round(data['PKPK'] / divider, ndigits=emr)
            CurrentMeasure.add_measure(data)
            self.send_json(data)
            time.sleep(settings.measures_delay_seconds)

        vitrek.connector.disconnect()

    def clear_table(self):
        CurrentMeasure.drop_measures()

    def save_customer(self, content):
        Customer.add_customer(name=content['customer_name'],
                              dev_type=content['device_type'],
                              dev_number=content['device_number'],
                              )

    def save_data(self, content):
        new_measure = MeasurePoint.add_new_measure()

    def new_device(self):
        Customer.delete_customer()

    def generate_report(self):
        ExportData.export_data()
    # def write_measures(self, data):
