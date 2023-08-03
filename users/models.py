from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь',
                                related_name='profile')
    first_name = models.CharField('Имя',
                                  max_length=32,
                                  blank=True,
                                  null=True
                                  )
    last_name = models.CharField('Фамилия',
                                 max_length=32,
                                 blank=True,
                                 null=True
                                 )
    surname = models.CharField('Отчество',
                               max_length=32,
                               blank=True,
                               null=True)
    email = models.EmailField('Email',
                              max_length=128,
                              blank=True,
                              null=True)
    created_at = models.DateTimeField('Дата создания',
                                      auto_now_add=True)
    avatar = models.ImageField('Аватар',
                               upload_to='avatars/',
                               null=True,
                               blank=True,
                               default='avatars/default.png')
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Муж'), (GENDER_FEMALE, 'Жен')]
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='Пол', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['created_at']

    def __str__(self):
        """
        Формирует строку вида: (id) ФИО никнейм
        """
        fname = ['('+ str(self.user.id) +')',str(self.last_name), str(self.first_name), str(self.surname), str(self.user.username)]
        return ' '.join([name for name in fname if name != 'None'])

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.surname}'


class Address(models.Model):
    name = models.CharField('Название адреса', max_length=128)
    user = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='address')
    full_name = models.CharField('ФИО получателя', max_length=256)
    phone_number = models.CharField('Номер телефона', max_length=20)
    address_line = models.CharField('Адрес', max_length=512)
    city = models.CharField('Город', max_length=128)
    postal_code = models.CharField('Почтовый код', max_length=20)
    region = models.CharField('Регион', max_length=256, blank=True, null=True)
    country = models.CharField('Страна', max_length=128)
    is_main = models.BooleanField('Основной адрес', default=False)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f'{self.id} {self.full_name} {self.country} {self.city} {self.is_main}'

    def get_full_address(self):
        if self.region:
            return f'{self.country}, {self.region}, {self.city}, {self.address_line}, {self.postal_code}'
        else:
            return f'{self.country}, {self.city}, {self.address_line}, {self.postal_code}'



