# Generated by Django 3.0.3 on 2020-05-21 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edusd_app', '0003_auto_20200520_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotion',
            name='speech_recording',
            field=models.FileField(upload_to='edusd/'),
        ),
    ]
