from birthday import BirthdayField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import random
from . import validations
import string
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime


# from Istok_app.models import Orders


class Profile(models.Model):

    surname = models.CharField(max_length=30, unique=False, verbose_name='Отчество', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User джанго модели', primary_key=True)
    birth_date = BirthdayField(null=True, verbose_name='Дата рождения')
    mailing = models.BooleanField(default=False, verbose_name='Согласие на рассылку', blank=True)
    personal_data_processing = models.BooleanField(default=False, blank=True,
        verbose_name='Согласие на обработку персональных данных')

    def __str__(self):
        return f'{self.user.username} Profile'


# todo вероятна уязвимость при редактировании полей опроса модели, путем изменения post ее могут привязать
# к другому пользователю, если редактирование модели будет происходит в одной въюшке.
# Возможно стоит выделить опросник в отдельную модель


# BONUS_CHOICE = [
#     ('Скидка 10%', 'Скидка 10%\nДополнительная скидка при оплате техники или сантехники'),
#     ('Скидка на столешницы SLOTEX', 'Скидка на столешницы SLOTEX\n'
#           'Столешница Slotex - это влагостойкая ДСП, облицованная декоративным покрытием Slotex.'),
#     ('4', '10 000 рублей\nДенежными средствами (не на бонусный счёт)'),
#     ('5', '15 000 рублей\nНа бонусный счёт (1 бонус = 1 рубль)'),
#     ('6', '20 000 рублей\nМебель стоимость до 20 000 рублей в подарок')
# ]


class Offer(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название предложения')
    about = models.CharField(max_length=300, verbose_name='Описание предложения')

    offer_to_all = models.BooleanField(default=False, verbose_name='Доступ всем лояльным',
        help_text='Если настройка включена, данное предложение будет у всех лояльных пользователей')

    def __str__(self):
        if self.offer_to_all:
            text = f'(не выбирать)Предложение и так есть у всех!({self.pk}){self.title[:15]}'
        else:
            text = f'({self.pk}){self.title[:15]}'
        return text

    class Meta:
        verbose_name = "Предложение лояльному пользователю"
        verbose_name_plural = "Предложения пользователям"


# m2m
class LoyaltyOffer(models.Model):
    loyalty = models.ForeignKey('Loyalty', on_delete=models.CASCADE, verbose_name='Лояльность')
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, verbose_name='Предложение')

    def __str__(self):
        return f'({self.pk})|Loyalty({self.loyalty.pk})|Offer({self.offer.pk})'

    class Meta:
        # Для уникальности м2м
        constraints = [
            models.UniqueConstraint(fields=['loyalty', 'offer'], name='loyalty_offer'),
        ]
        verbose_name = "(m2m) Персональное предложение"
        verbose_name_plural = "(m2m) Персональные предложения"


class Loyalty(models.Model):
    CARD_REGEX = RegexValidator(
        regex=r'\d{4}\s\d{4}\s\d{4}\s\d{4}$',
        message="Номер карты должен быть указан в формате: "
                "0000 0000 0000 0000")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', primary_key=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    balance = models.IntegerField(default=0, verbose_name='Баланс', blank=True)
    balance_history = models.TextField(verbose_name='(Тех)Статистика бонусного счета', blank=True,
        help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя',
        default=f'Регистрация в системе лояльности {datetime.now().date()}')

    offers = models.ManyToManyField('Offer', through='LoyaltyOffer',
        related_name='offers', verbose_name='Персональные предложения',
        help_text='Можно добавить индивидуальное предложение')
    benefits = models.ManyToManyField('Benefit', through='LoyaltyBenefit',
        related_name='benefits', verbose_name='Выбранная выгода')

    benefits_history = models.TextField(verbose_name='(Тех)История выбора выгод счета', blank=True,
        help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя, '
                  'и получение бонусов за приглашение нового пользователя.',
        default=f'Регистрация в системе лояльности {datetime.now().date()}')

    code = models.CharField(max_length=150, verbose_name='Код программы лояльности', unique=True,
        null=True, blank=True, default=None, validators=[validations.code_validation],
        help_text='(Не обязательное поле. Номер карты создается автоматически.)\n'
                  'Формат: FS5Kl. Только заглавные латинские буквы и цифры.')

    card_number = models.CharField(max_length=19, verbose_name='Номер карты лояльности', unique=True,
        null=True, blank=True, default=None, validators=[CARD_REGEX],
        help_text='(Не обязательное поле. Номер карты создается автоматически.)\n'
                  'Формат: 0000 0000 0000 0000. Только цифры и пробелы.')

    friends_loyalty_used = models.BooleanField(default=False, blank=True,
        verbose_name='(Тех)Использован код друга', help_text='Чужим кодом можно воспользоваться лишь раз.')

    bonus_from_reference = models.PositiveIntegerField(default=0,
        verbose_name='(Тех)Бонусы полученные с приглашения на регистрацию', blank=True,
        help_text='Автоматически начисляется если другой пользователь зарегистрировался и прошел опросник.'
                  'При достижении 5000 рублей, оповещает пользователя и сотрудника о '
                  'возможности обменять бонусы на деньги.')

    def __str__(self):
        return f'{self.user.last_name.capitalize()} {self.user.first_name.capitalize()}({self.user.pk})|' \
               f'Код лояльности - {self.code}'

    class Meta:
        verbose_name = "Лояльность"
        verbose_name_plural = "Лояльность "

    def benefit_to_choose(self):
        m2m = self.loyaltybenefit_set.all().filter(benefit=None).first()
        if m2m:
            dct = {'id': m2m.pk, 'loyalty': m2m.loyalty_id, 'benefit': m2m.benefit_id}
        else:
            dct = None
        return dct

    #todo данную функцию запускать из сигнала регистрации
    def increase_bonus_from_reference(self, user=None):
        self.bonus_from_reference += 100
        self.balance += 100
        self.save()
        diff = 5000 - self.bonus_from_reference
        if diff > 0:
            remain = diff // 100
            text_to_user = f'Дата:{datetime.now().date().strftime("%d-%m-%Y")}\n' \
                           f'Вашей пригласительной ссылкой для регистрации воспользовались.' \
                           f'Вы получаете 100 бонусов(рублей).\n' \
                           f'Если пригласите еще {remain} пользователей, сможете снять 5000 рублей наличными\n\n'
            self.benefits_history = text_to_user + self.benefits_history
            self.save()

        if diff == 0:
            text_to_user = f'Дата:{datetime.now().date().strftime("%d-%m-%Y")}\n' \
                           f'Вы пригласили 50 человек на регистрацию!!\n' \
                           f'Большое спасибо Вам за рекламу нашего сайта! ' \
                           f'Вы имеете право снять 5000 рублями с бонусного счета\n' \
                           f'С вами в ближайшее время свяжутся для перевода денег.'
            self.benefits_history = text_to_user + self.benefits_history
            text = f'+ 100 бонусов за приглашение на регистрацию. Баланс:{self.balance}\n'
            self.balance_history = text + self.benefits_history
            self.save()
            text_to_staff = f'Пользователь {self.show_user_name()}(код лояльности {self.code}), ' \
                            f'пригласил 50 пользователей для ' \
                            f'регистрации и опроса. Он имеет имеет право снять 5000 рублей с бонусного счета.\n' \
                            f'Не забудьте после выдачи награды списать 5000 бонусов с его счета.\n\n'
            # todo f'Данные пользователя:'
            print(text_to_staff)
            # todo send_mail_staff
            # todo send_email_user
        if diff < 0:
            text_to_user = f'Дата:{datetime.now().date().strftime("%d-%m-%Y")}\n' \
                           f'Вашей пригласительной ссылкой для регистрации воспользовались.' \
                           f'Вы получаете 100 бонусов(рублей).\n\n'
            self.benefits_history = text_to_user + self.benefits_history
            self.save()

    def new_benefits_count(self):
        return self.loyaltybenefit_set.all().filter(benefit=None).count()

    def show_user_name(self):
        return f'{self.user.last_name} {self.user.first_name}'

    def show_all_offers(self):
        text = ''
        user_offers_set = list(self.offers.all())
        offers = list(Offer.objects.filter(offer_to_all=True)) + user_offers_set
        for offer in offers:
            text = text + f' {offer.title} |'
        return text

    def increase_balance(self, number_of_bonuses: int) -> None:
        if number_of_bonuses > 0:
            self.balance += number_of_bonuses
            self.save()

    def save(self, *args, **kwargs):
        super(Loyalty, self).save(*args, **kwargs)
        if self.code is None:
            self.code = self.create_code()
            self.save()
        if self.card_number is None:
            self.card_number = self.create_card_number()
            self.save()

    @staticmethod
    def create_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if Loyalty.objects.filter(code=code).exists():
                continue
            return code

    def create_card_number(self):
        while True:
            digits = self.random_4_digits()
            card_number = f"{digits} {digits} {digits} {digits}"
            if Loyalty.objects.filter(card_number=card_number).exists():
                continue
            return card_number

    @staticmethod
    def random_4_digits():
        return ''.join(random.choices(string.digits, k=4))


class Benefit(models.Model):

    title = models.CharField(max_length=150, verbose_name='Заголовок или сокращенная информация', unique=True)
    about = models.CharField(max_length=300, verbose_name='Описание')
    feedback_text = models.TextField(verbose_name='Всплывающий текст после выбора',
        help_text='Данный текст будет всплывать после выбора выгоды.\n'
                  'Как пример если выбрали 10к денежными средствами, '
                  'текст должен оповестить пользователя, что с ним свяжутся.\n'
                  'Если выгода начислит бонусы: Вам начислены бонусы!')
    bonuses_to_add = models.PositiveIntegerField(verbose_name='Автоматически начислить бонусов', default=0,
        validators=[MaxValueValidator(30000)], help_text='Количество бонус для автоматического '
                                                         'начисления после выбора выгоды. Ограничение 30000')
    send_email_to_staff = models.BooleanField(default=False, verbose_name='Нужно оповестить сотрудников',
        help_text='Включите эту опцию если выбранную выгоду должен выдать лично сотрудник')

    def __str__(self):
        return f'({self.pk}){self.title}'

    class Meta:
        verbose_name = "Выгода"
        verbose_name_plural = "Выгода"


class LoyaltyBenefit(models.Model):
    STATUS = [
        ('Оповещение отправлено', 'Послано автоматическое оповещение на почту сотрудников'),
        ('Принято в работу', 'Сотрудник оповещен, выдача выгоды в процессе'),
        ('Завершен', 'Выгода выдана'),
        ('Отклонена', 'Отклонена')
    ]

    loyalty = models.ForeignKey('Loyalty', on_delete=models.CASCADE, verbose_name='Лояльность')
    benefit = models.ForeignKey('Benefit', on_delete=models.CASCADE, verbose_name='Выбранная выгода',
        null=True, default=None)

    status = models.CharField(max_length=150, choices=STATUS, verbose_name='Статус выдачи выбранной выгоды',
        default='Оповещение отправлено',
        help_text='Три статуса процесса выдачи награды. Если выбрали начисление бонусов автоматически "Завершен"')

    def __str__(self):
        return f'{self.loyalty.code}-{self.benefit}({self.status})'

    class Meta:
        verbose_name = "(m2m) Выбранная выгода"
        verbose_name_plural = "(m2m) Выбранная выгода"

# # m2m
# class LoyaltyBenefit(models.Model):
#     # furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
#     # project_image = models.ForeignKey(ProjectImage, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f''
#
#     # class Meta:
#     #     # Для уникальности м2м
#     #     constraints = [
#     #         models.UniqueConstraint(fields=['furniture', 'project_image'], name='furniture_project_image'),
#     #     ]
#     #     verbose_name = "Изображение для мебели"
#     #     verbose_name_plural = "Изображения для мебели"


# для быстрого подключения в консоли
# from django.contrib.auth.models import User
# from users.models import Loyalty, Profile
# from Istok_app.models import Orders
# u = User.objects.all().first()
