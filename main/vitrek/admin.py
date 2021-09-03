from django.contrib import admin
from .models import Customer, MeasurePoint, MeasuresSetting, CurrentMeasure

# Register your models here.


admin.site.register(MeasurePoint)
admin.site.register(Customer)
admin.site.register(MeasuresSetting)
admin.site.register(CurrentMeasure)
