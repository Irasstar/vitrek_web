import json

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .libs.Vitrek4700driver import Vitrek4700, TCPConnector
from .models import MeasuresSetting, CurrentMeasure, Customer, MeasurePoint
import time



def measures(request):
    data = []

    # customer = Customer.objects.get(pk=1) or None
    # customer_form = CustomerForm(instance=customer or None)
    #
    # device = Device.objects.get(pk=1) or None
    # device_form = DeviceForm(instance=device or None)
    customer = Customer.get_customer()

    context = {
        'customer': customer.name or '',
        'type': customer.type or '',
        'number': customer.number or '',
        'header': ['ACV', 'FREQ', 'DCV', 'PK-PK', 'CRF'],
        'data': []
    }

    return render(request, 'vitrek/measures.html', context)


def exports(request):
    customer = Customer.get_customer()
    measures = MeasurePoint.get_measures_data()
    context = {
        'customer': customer,
        'measures': measures,
        'header': ['ACV', 'FREQ', 'DCV', 'PK-PK', 'CRF'],
    }
    return render(request, 'vitrek/data_export.html', context)





# Create your views here.
