# Generated by Django 2.2.5 on 2020-02-04 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_ride_canshare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='canShare',
            new_name='can_share',
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='canShare',
            new_name='can_share',
        ),
    ]
