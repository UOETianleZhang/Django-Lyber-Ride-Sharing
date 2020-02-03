from django import forms
from django.contrib.auth.models import User
from .models import RiderDriver

class RiderDriverForm(forms.Form):
	driver_name = forms.CharField()
	plate_number = forms.CharField()
	vehicle_type = forms.ChoiceField(choices=RiderDriver.VEHICLE_CHOICE)
	max_passenger_num = forms.ChoiceField(choices=RiderDriver.PASSENGER_N_CHOICE)
	special_info = forms.CharField(required=False, widget=forms.Textarea)