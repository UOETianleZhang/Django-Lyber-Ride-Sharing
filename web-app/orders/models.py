from django.contrib.auth.models import User
import datetime
from django.db import models
from django.forms import Form, ModelForm, DateTimeInput, ChoiceField, CharField, IntegerField, DateTimeField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RiderDriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver', null=True)
    # user = models.CharField(max_length=120)
    driverName = models.CharField(max_length=120)
    plateNumber = models.TextField(blank=True, null=True)
    # id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    VEHICLE_CHOICE = [("Hatchback", "Hatchback"), ("Sedan", "Sedan"), ("MPV", "MPV"), ("SUV", "SUV"),
               ("Crossover", "Crossover"), ("Coupe", "Coupe"), ("Convertible", "Convertible")]
    PASSENGER_N_CHOICE = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    vehicle_type = models.CharField(
        max_length=100,
        choices=VEHICLE_CHOICE,
        default="Hatchback"
    )
    max_passenger_num = models.IntegerField(choices=PASSENGER_N_CHOICE)
    special_info = models.IntegerField(choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                                                   (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')], default=0)
    is_driving = models.BooleanField()


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
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=User.objects.create())
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
    status = models.CharField(
        max_length=100,
        choices=[("open", "open"), ("confirmed", "confirmed"), ("completed", "completed")],
        default="open"
    )
    max_passenger_num = models.IntegerField(default=6)
    owner_passenger_num = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    total_cur_passenger_num = models.IntegerField()
    special_request = models.IntegerField(choices=[(0, "no special request"), (1, 'special request 1'), (2, 'special request 2'),
                                                   (3, 'special request 3'), (4, 'special request 4'), (5, 'special request 5')])
    can_share = models.BooleanField(choices = [(True, 'Yes'), (False, 'No')])

    def was_published_recently(self):
        return self.start_time >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "start_point: " + self.starting_point + ", destination: " + self.destination + ", start time: " + str(self.start_time) + ", finish time: " + str(self.finish_time) + "\n"


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(RiderDriver, on_delete=models.CASCADE, null=True)
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, null=True)
    can_share = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)
    total_cur_passenger_num = models.IntegerField()


class RiderSharer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ManyToManyField(Order, null=True)
    sharer_passenger_num = models.IntegerField()


