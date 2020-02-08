from django import forms
from .models import RiderDriver, Order, Ride
import datetime
from django.forms import Form, ModelForm, DateTimeInput, ChoiceField, CharField, IntegerField, DateTimeField
from django.utils.translation import gettext_lazy as _


class RiderDriverForm(forms.Form):
    driver_name = forms.CharField()
    plate_number = forms.CharField()
    vehicle_type = forms.ChoiceField(choices=RiderDriver.VEHICLE_CHOICE)
    max_passenger_num = forms.ChoiceField(choices=RiderDriver.PASSENGER_N_CHOICE)
    special_info = forms.ChoiceField(
        choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                 (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')], required=True)


class ShareSearchForm(Form):
    start_time = DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local', 'value': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}))
    destination = CharField()
    num_passengers = IntegerField()
    special_request = ChoiceField(choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                                                   (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')])


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['can_share']


class RideForm(ModelForm):
    status = ChoiceField(choices=[("open", "open"), ("confirmed", "confirmed"), ("completed", "completed")],
                         disabled=True, required=False, initial='open')
    start_time = DateTimeField(input_formats=["%Y-%m-%dT%H:%M"], widget=DateTimeInput(attrs={'type': 'datetime-local', 'value': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}))
    finish_time = DateTimeField(input_formats=["%Y-%m-%dT%H:%M"], widget=DateTimeInput(attrs={'type': 'datetime-local', 'value': (datetime.datetime.now()+datetime.timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M")}))

    class Meta:
        model = Ride
        fields = '__all__'
        exclude = ('max_passenger_num', 'total_cur_passenger_num')
        labels = {
            'finish_time': _('Finish Time'),
        }
        help_texts = {
            'finish_time': _('Some useful help text.'),
        }
        error_messages = {
            'finish_time': {
                'max_length': _("This writer's name is too long."),
            },
        }
        initial = {
            'status': 'open',
        }
