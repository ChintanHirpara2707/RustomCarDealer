# Generated by Django 5.0.6 on 2024-07-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_alter_car_car_model_alter_car_car_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
