# Generated by Django 4.2 on 2024-09-12 21:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.validations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_loyaltest_alter_loyalty_card_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название предложения')),
                ('about_offer', models.CharField(max_length=300, verbose_name='Описание предложения')),
                ('offer_to_all', models.BooleanField(default=False, help_text='Если настройка включена, данное предложение будет у всех лояльных пользователей', verbose_name='Доступ всем лояльным')),
            ],
            options={
                'verbose_name': 'Предложение лояльному пользователю',
                'verbose_name_plural': 'Предложения пользователям',
            },
        ),
        migrations.AlterModelOptions(
            name='loyalty',
            options={'verbose_name': 'Лояльность', 'verbose_name_plural': 'Лояльность '},
        ),
        migrations.RemoveField(
            model_name='loyalty',
            name='bonus',
        ),
        migrations.AddField(
            model_name='loyalty',
            name='balance_history',
            field=models.TextField(default='', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя', verbose_name='(Тех)Статистика бонусного счета'),
        ),
        migrations.AddField(
            model_name='loyalty',
            name='benefits_history',
            field=models.TextField(default='', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя', verbose_name='(Тех)Статистика выбора выгод счета'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loyalty',
            name='bonus_from_reference',
            field=models.IntegerField(default=0, help_text='Автоматически начисляется если другой пользователь зарегистрировался и прошел опросник.На уровне кода блокируется максимальным значением в 5000', validators=[django.core.validators.MaxValueValidator(5000), django.core.validators.MinValueValidator(0)], verbose_name='(Тех)Бонус полученный с приглашения на регистрацию'),
        ),
        migrations.AddField(
            model_name='loyalty',
            name='new_befit',
            field=models.BooleanField(blank=True, default=False, help_text='Если по коду пользователя была произведена покупка, автоматически оповещает пользователя и дает сделать выбор выгоды в личном кабинете', verbose_name='Настройка появление выбора выгоды'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='card_number',
            field=models.CharField(blank=True, default=None, help_text='Формат: FS5Kl. Только заглавные латинские буквы и цифры\n(Не обязательное поле. Номер карты создается автоматически.)', max_length=19, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер карты должен быть указан в формате: 0000 0000 0000 0000', regex='\\d{4}\\s\\d{4}\\s\\d{4}\\s\\d{4}$')], verbose_name='Номер карты лояльности'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='code',
            field=models.CharField(blank=True, default=None, help_text='Формат: 0000 0000 0000 0000. Только цифры и пробелы.\n(Не обязательное поле. Номер карты создается автоматически.)', max_length=150, null=True, unique=True, validators=[users.validations.code_validation], verbose_name='Код программы лояльности'),
        ),
        migrations.CreateModel(
            name='LoyaltyOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loyalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loyalty')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.offer')),
            ],
            options={
                'verbose_name': 'm2m Loyalty-Offer',
                'verbose_name_plural': 'm2m Loyalty-Offers',
            },
        ),
        migrations.AddField(
            model_name='loyalty',
            name='offers',
            field=models.ManyToManyField(help_text='Можно добавить индивидуальное предложение', related_name='offers', through='users.LoyaltyOffer', to='users.offer', verbose_name='Персональные предложения'),
        ),
        migrations.AddConstraint(
            model_name='loyaltyoffer',
            constraint=models.UniqueConstraint(fields=('loyalty', 'offer'), name='loyalty_offer'),
        ),
    ]
