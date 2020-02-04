from django.contrib import admin

# Register your models here.
from .models import RiderDriver, Order, Ride

admin.site.register(RiderDriver)
admin.site.register(Order)
admin.site.register(Ride)