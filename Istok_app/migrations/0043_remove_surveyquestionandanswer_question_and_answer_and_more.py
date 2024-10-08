# Generated by Django 4.2 on 2024-09-17 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0042_rename_survey_was_changed_survey_questions_was_changed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyquestionandanswer',
            name='question_and_answer',
        ),
        migrations.RemoveField(
            model_name='surveyquestionandanswer',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='question_and_answers',
        ),
        migrations.AddField(
            model_name='questionandanswer',
            name='survey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Istok_app.survey', verbose_name='Опросник'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(unique=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='dependable',
            field=models.BooleanField(default=True, help_text='Статус становится положительным в случае если опросник заполняли больше минимального времени заполнения. При аналитике ненадежные будут вычеркиваться из выборки', verbose_name='Опросник надежен'),
        ),
        migrations.AddConstraint(
            model_name='questionandanswer',
            constraint=models.UniqueConstraint(fields=('survey', 'question'), name='survey_question'),
        ),
        migrations.DeleteModel(
            name='SurveyQuestionAndAnswer',
        ),
    ]
