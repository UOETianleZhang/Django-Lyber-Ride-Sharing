from django import forms
from django.contrib.auth.models import User
from .models import RiderDriver


class RiderDriverForm(forms.Form):
    driver_name = forms.CharField()
    plate_number = forms.CharField()
    vehicle_type = forms.ChoiceField(choices=RiderDriver.VEHICLE_CHOICE)
    max_passenger_num = forms.ChoiceField(choices=RiderDriver.PASSENGER_N_CHOICE)
    special_info = forms.ChoiceField(
        choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                 (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')], required=True)
