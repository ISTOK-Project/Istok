# Generated by Django 4.2 on 2024-08-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0021_application_alter_furnitureimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='python_date_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Для теста перевода формата времени из js в python'),
        ),
        migrations.AlterField(
            model_name='application',
            name='text',
            field=models.TextField(verbose_name='Дополнительная информация'),
        ),
    ]
