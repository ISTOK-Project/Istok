# Generated by Django 4.2 on 2024-09-27 09:02

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.validations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Заголовок или сокращенная информация')),
                ('about', models.CharField(max_length=300, verbose_name='Описание')),
                ('feedback_text', models.TextField(help_text='Данный текст будет всплывать после выбора выгоды.\nКак пример если выбрали 10к денежными средствами, текст должен оповестить пользователя, что с ним свяжутся.\nЕсли выгода начислит бонусы: Вам начислены бонусы!', verbose_name='Всплывающий текст после выбора')),
                ('bonuses_to_add', models.PositiveIntegerField(default=0, help_text='Количество бонус для автоматического начисления после выбора выгоды. Ограничение 30000', validators=[django.core.validators.MaxValueValidator(30000)], verbose_name='Автоматически начислить бонусов')),
                ('send_email_to_staff', models.BooleanField(default=False, help_text='Включите эту опцию если выбранную выгоду должен выдать лично сотрудник', verbose_name='Нужно оповестить сотрудников')),
            ],
            options={
                'verbose_name': 'Выгода',
                'verbose_name_plural': 'Выгода',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название предложения')),
                ('about', models.CharField(max_length=300, verbose_name='Описание предложения')),
                ('offer_to_all', models.BooleanField(default=False, help_text='Если настройка включена, данное предложение будет у всех лояльных пользователей', verbose_name='Доступ всем лояльным')),
            ],
            options={
                'verbose_name': 'Предложение лояльному пользователю',
                'verbose_name_plural': 'Предложения пользователям',
            },
        ),
        migrations.CreateModel(
            name='Loyalty',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('balance', models.IntegerField(blank=True, default=0, verbose_name='Баланс')),
                ('balance_history', models.TextField(blank=True, default='Регистрация в системе лояльности 2024-09-27', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя', verbose_name='(Тех)Статистика бонусного счета')),
                ('benefits_history', models.TextField(blank=True, default='Регистрация в системе лояльности 2024-09-27', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя, и получение бонусов за приглашение нового пользователя.', verbose_name='(Тех)История выбора выгод счета')),
                ('code', models.CharField(blank=True, default=None, help_text='(Не обязательное поле. Номер карты создается автоматически.)\nФормат: FS5Kl. Только заглавные латинские буквы и цифры.', max_length=150, null=True, unique=True, validators=[users.validations.code_validation], verbose_name='Код программы лояльности')),
                ('card_number', models.CharField(blank=True, default=None, help_text='(Не обязательное поле. Номер карты создается автоматически.)\nФормат: 0000 0000 0000 0000. Только цифры и пробелы.', max_length=19, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер карты должен быть указан в формате: 0000 0000 0000 0000', regex='\\d{4}\\s\\d{4}\\s\\d{4}\\s\\d{4}$')], verbose_name='Номер карты лояльности')),
                ('friends_loyalty_used', models.BooleanField(blank=True, default=False, help_text='Чужим кодом можно воспользоваться лишь раз.', verbose_name='(Тех)Использован код друга')),
                ('bonus_from_reference', models.PositiveIntegerField(blank=True, default=0, help_text='Автоматически начисляется если другой пользователь зарегистрировался и прошел опросник.При достижении 5000 рублей, оповещает пользователя и сотрудника о возможности обменять бонусы на деньги.', verbose_name='(Тех)Бонусы полученные с приглашения на регистрацию')),
            ],
            options={
                'verbose_name': 'Лояльность',
                'verbose_name_plural': 'Лояльность ',
            },
        ),
        migrations.CreateModel(
            name='LoyaltyOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.offer', verbose_name='Предложение')),
                ('loyalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loyalty', verbose_name='Лояльность')),
            ],
            options={
                'verbose_name': '(m2m) Персональное предложение',
                'verbose_name_plural': '(m2m) Персональные предложения',
            },
        ),
        migrations.CreateModel(
            name='LoyaltyBenefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Оповещение отправлено', 'Послано автоматическое оповещение на почту сотрудников'), ('Принято в работу', 'Сотрудник оповещен, выдача выгоды в процессе'), ('Завершен', 'Выгода выдана'), ('Отклонена', 'Отклонена')], default='Оповещение отправлено', help_text='Три статуса процесса выдачи награды. Если выбрали начисление бонусов автоматически "Завершен"', max_length=150, verbose_name='Статус выдачи выбранной выгоды')),
                ('benefit', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.benefit', verbose_name='Выбранная выгода')),
                ('loyalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loyalty', verbose_name='Лояльность')),
            ],
            options={
                'verbose_name': '(m2m) Выбранная выгода',
                'verbose_name_plural': '(m2m) Выбранная выгода',
            },
        ),
        migrations.AddField(
            model_name='loyalty',
            name='benefits',
            field=models.ManyToManyField(related_name='benefits', through='users.LoyaltyBenefit', to='users.benefit', verbose_name='Выбранная выгода'),
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
