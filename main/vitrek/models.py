import json

from django.db import models
from django.utils import timezone

# Create your models here.


class CurrentMeasure(models.Model):
    measure_point = models.FloatField(default=0)
    current_type = models.CharField(max_length=64, default='AC_50_Hz')
    measures = models.JSONField(default=dict(data=[]))

    @classmethod
    def set_measure_point(cls, measure_point, current_type):
        m = cls.objects.all()[0]
        m.current_type = current_type
        m.measure_point = measure_point
        m.save()

    @classmethod
    def add_measure(cls, data):
        m = cls.objects.all()[0]
        m.measures['data'].append(data)
        m.save()

    @classmethod
    def drop_measures(cls):
        m = cls.objects.all()[0]
        m.measures['data'] = []
        m.save()


class Customer(models.Model):
    name = models.CharField(max_length=1024)
    type = models.CharField(max_length=256, default='')
    number = models.CharField(max_length=64, default='')

    @classmethod
    def add_customer(cls, name, dev_type, dev_number):
        customer = cls.objects.all()
        if len(customer) == 0:
            customer = cls(name=name, type=dev_type, number=dev_number)
            customer.save()
        else:
            customer[0].name = name
            customer[0].type = dev_type
            customer[0].number = dev_number
            customer[0].save()

    @classmethod
    def delete_customer(cls):
        cls.objects.all().delete()


    @classmethod
    def get_customer(cls):
        customer = cls.objects.all()
        if len(customer) == 0:
            customer = cls(name='', type='', number='')
            customer.save()
            return customer
        return customer[0]

    def __str__(self):
        return f"{self.name}"


class MeasurePoint(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    measure_point = models.FloatField(default=0)
    current_type = models.CharField(max_length=64)
    date = models.DateTimeField(default=timezone.now)
    measures = models.JSONField(default=dict(data=[]))

    @classmethod
    def add_new_measure(cls):
        measures = CurrentMeasure.objects.get(pk=1)
        measure = cls(customer=Customer.objects.all()[0],
                      measure_point=measures.measure_point,
                      current_type=measures.current_type,
                      date=timezone.now(),
                      measures=measures.measures)
        measure.save()

    @classmethod
    def clear_data(cls):
        measures = MeasurePoint.objects.all().delete()

    @classmethod
    def get_measures_data(cls):
        return cls.objects.all()

    def __str__(self):
        return "point: %s kV; " % (self.measure_point)


class MeasuresSetting(models.Model):
    vitrek_IP = models.GenericIPAddressField(default='0.0.0.0')
    vitrek_Port = models.PositiveIntegerField(default='10733')
    measures_delay_seconds = models.FloatField(default=0.1)
    measures_count = models.IntegerField(default=10)
    protocol_folder = models.CharField(max_length=1024, default='')
    emr = models.IntegerField(default=3)
    divider = models.IntegerField(default=1000)

    @classmethod
    def get_emr(cls):
        return cls.objects.all()[0].emr

    @classmethod
    def get_divider(cls):
        return cls.objects.all()[0].divider

    @classmethod
    def get_file_path(cls):
        return cls.objects.all()[0].protocol_folder

    def __str__(self):
        return f"{self.vitrek_IP}: {self.vitrek_Port}. {self.measures_count} measures"

