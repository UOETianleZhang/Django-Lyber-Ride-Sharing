import datetime

from django.db import models
from django.forms import ModelForm, Textarea, Select, DateTimeInput
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Ride(models.Model):
    starting_point = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_time = models.DateTimeField('Start Time')
    finish_time = models.DateTimeField('Finish Time')
    vehicle_type = models.CharField(
        max_length=100,
        choices=[("Hatchback", "Hatchback"), ("Sedan", "Sedan"), ("MPV", "MPV"), ("SUV", "SUV"),
                 ("Crossover", "Crossover"), ("Coupe", "Coupe"), ("Convertible", "Convertible")],
        default="Hatchback"
    )
    status = models.CharField(max_length=100, choices=[("open", "open"), ("confirmed", "confirmed"), ("completed", "completed")])
    max_passenger_num = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    cur_passenger_num = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    special_request = models.IntegerField(choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                                                   (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')])

    def was_published_recently(self):
        return self.start_time >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return "start_point: " + self.starting_point + ", destination: " + self.destination + ", start time: " + str(self.start_time) + ", finish time: " + str(self.finish_time) + "\n"



class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = '__all__'
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
        # widgets = {
        #     # 'vehicle_type': Textarea(attrs={'readonly': True}),
        #     'vehicle_type' : Select(attrs={'disabled':True}),
        #     'start_time': DateTimeInput(),
        #     'finish_time': DateTimeInput()
        # }

