# Generated by Django 4.2 on 2024-09-17 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0035_websitesettings_survey_dependable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitesettings',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
