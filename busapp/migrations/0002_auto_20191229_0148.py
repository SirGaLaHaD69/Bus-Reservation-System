# Generated by Django 2.2.1 on 2019-12-28 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline3app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightdetail',
            name='price',
            field=models.FloatField(),
        ),
    ]