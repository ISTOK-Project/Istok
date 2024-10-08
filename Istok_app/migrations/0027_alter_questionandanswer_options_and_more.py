# Generated by Django 4.2 on 2024-09-04 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Istok_app', '0026_alter_option_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionandanswer',
            options={'verbose_name': '(Тех)Ответ к опроснику', 'verbose_name_plural': '(Тех)Ответы к опроснику'},
        ),
        migrations.RenameField(
            model_name='survey',
            old_name='answer',
            new_name='question_and_answer',
        ),
        migrations.AlterField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
