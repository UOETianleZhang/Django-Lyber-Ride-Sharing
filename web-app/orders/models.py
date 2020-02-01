from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class RiderUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Vehicle(object):
    plateNumber = None

    def __init__(self):
        None

class RiderDriver(models.Model):
    driverName = models.CharField(max_length=120)
    vehicleInfo = Vehicle()


