# Generated by Django 5.0.6 on 2024-07-10 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_model',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(max_length=20),
        ),
    ]
