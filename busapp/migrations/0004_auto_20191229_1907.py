# Generated by Django 2.2.1 on 2019-12-29 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline3app', '0003_flightdetail_bus_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightdetail',
            name='bus_route',
            field=models.CharField(max_length=1000),
        ),
    ]
