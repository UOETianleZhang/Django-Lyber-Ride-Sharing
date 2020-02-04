# Generated by Django 2.2.5 on 2020-02-04 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200204_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='order',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ride',
        ),
        migrations.RemoveField(
            model_name='riderdriver',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ridersharer',
            name='order',
        ),
        migrations.RemoveField(
            model_name='ridersharer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Ride',
        ),
        migrations.DeleteModel(
            name='RiderDriver',
        ),
        migrations.DeleteModel(
            name='RiderSharer',
        ),
    ]
