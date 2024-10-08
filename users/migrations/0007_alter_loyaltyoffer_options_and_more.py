# Generated by Django 4.2 on 2024-09-13 09:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.validations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_benefit_offer_alter_loyalty_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loyaltyoffer',
            options={'verbose_name': '(m2m) Персональное предложение', 'verbose_name_plural': '(m2m) Персональные предложения'},
        ),
        migrations.RenameField(
            model_name='offer',
            old_name='about_offer',
            new_name='about',
        ),
        migrations.AddField(
            model_name='benefit',
            name='about',
            field=models.CharField(default='', max_length=300, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benefit',
            name='bonuses_to_add',
            field=models.PositiveIntegerField(default=0, help_text='Количество бонус для автоматического начисления после выбора выгоды', validators=[django.core.validators.MaxValueValidator(30000)], verbose_name='Начислить бонусов'),
        ),
        migrations.AddField(
            model_name='benefit',
            name='feedback_text',
            field=models.TextField(default='', help_text='Данный текст будет всплывать после выбора выгоды.\nКак пример если выбрали 10к денежными средствами, текст должен оповестить пользователя, что с ним свяжутся.\nЕсли выгода начислит бонусы: Вам начислены бонусы!', verbose_name='Всплывающий текст после выбора'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benefit',
            name='send_email_to_staff',
            field=models.BooleanField(default=False, help_text='Включите эту опцию если выбранную выгоду должен выдать лично сотрудник', verbose_name='Нужно оповестить сотрудников'),
        ),
        migrations.AddField(
            model_name='benefit',
            name='title',
            field=models.CharField(default='', max_length=150, verbose_name='Заголовок или сокращенная информация'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='balance',
            field=models.IntegerField(blank=True, default=0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='balance_history',
            field=models.TextField(blank=True, default='', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя', verbose_name='(Тех)Статистика бонусного счета'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='benefits_history',
            field=models.TextField(blank=True, help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя, и получение бонусов за приглашение нового пользователя.', verbose_name='(Тех)История выбора выгод счета'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='bonus_from_reference',
            field=models.IntegerField(blank=True, default=0, help_text='Автоматически начисляется если другой пользователь зарегистрировался и прошел опросник.На уровне кода блокируется максимальным значением в 5000', validators=[django.core.validators.MaxValueValidator(5000), django.core.validators.MinValueValidator(0)], verbose_name='(Тех)Бонус полученный с приглашения на регистрацию'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='card_number',
            field=models.CharField(blank=True, default=None, help_text='(Не обязательное поле. Номер карты создается автоматически.)\nФормат: FS5Kl. Только заглавные латинские буквы и цифры.', max_length=19, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер карты должен быть указан в формате: 0000 0000 0000 0000', regex='\\d{4}\\s\\d{4}\\s\\d{4}\\s\\d{4}$')], verbose_name='Номер карты лояльности'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='code',
            field=models.CharField(blank=True, default=None, help_text='(Не обязательное поле. Номер карты создается автоматически.)\nФормат: 0000 0000 0000 0000. Только цифры и пробелы.', max_length=150, null=True, unique=True, validators=[users.validations.code_validation], verbose_name='Код программы лояльности'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='new_befit',
            field=models.BooleanField(blank=True, default=False, help_text='Если по коду пользователя была произведена покупка, автоматически оповещает пользователя и дает сделать выбор выгоды в личном кабинете', verbose_name='(Тех)Настройка появление выбора выгоды'),
        ),
        migrations.AlterField(
            model_name='loyaltyoffer',
            name='loyalty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loyalty', verbose_name='Лояльность'),
        ),
        migrations.AlterField(
            model_name='loyaltyoffer',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.offer', verbose_name='Предложение'),
        ),
    ]
