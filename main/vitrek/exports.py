import openpyxl

from .models import MeasurePoint, Customer, MeasuresSetting
from datetime import date
import os


class ExportData:
    template_filename = 'vitrek/protocol_template.xlsm'
    ps_name = 'Протокол'  # protocol title sheet name
    ds_sheet_name = 'Измерения'  # measures data sheet name

    dev_type_addr = 'C4'
    dev_num_addr = 'C6'

    start_column = 2
    point_row = 2
    date_row = 7
    curr_type_row = 6
    meas_start_row = 13

    @classmethod
    def export_data(cls):
        customer = Customer.get_customer()
        points = MeasurePoint.get_measures_data()

        wb = openpyxl.open(cls.template_filename)
        ws = wb[cls.ps_name]
        ws[cls.dev_type_addr] = customer.type
        ws[cls.dev_num_addr] = customer.number

        ws = wb[cls.ds_sheet_name]

        for col, point in enumerate(points, start=cls.start_column):
            ws.cell(cls.point_row, col).value = point.measure_point
            ws.cell(cls.curr_type_row, col).value = point.current_type  # change selection AC, DC, AC_0,1

             # insert measures
            for row, data in enumerate(point.measures['data'], start=cls.meas_start_row):
                ws.cell(row, col).value = data['ACV']
        f_name = cls.gen_file_name()
        f_path = MeasuresSetting.get_file_path()
        path = MeasuresSetting.get_file_path()
        wb.save(os.path.join(path, f_name))

    @classmethod
    def gen_file_name(cls):
        customer = Customer.get_customer()
        return f'{customer.name} {customer.type} №{customer.number}.xlsm'


