# Generated by Django 3.0.3 on 2020-05-08 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speech_recording', models.BinaryField()),
                ('speech_text', models.BinaryField()),
                ('speech_emotions', models.TextField()),
            ],
        ),
    ]