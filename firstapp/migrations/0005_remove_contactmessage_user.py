# Generated by Django 5.0.6 on 2024-07-12 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='user',
        ),
    ]