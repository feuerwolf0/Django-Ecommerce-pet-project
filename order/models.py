from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from shop.models import Product
from users.models import Address, Profile


class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Владелец')
    full_name = models.CharField('ФИО', max_length=256)
    phone_number = models.CharField('Номер телефона', max_length=32)
    address = models.CharField('Адрес', max_length=512)
    total_price = models.DecimalField('Полная стоимость', decimal_places=2, max_digits=32)
    end_price = models.DecimalField('Конечная стоимость', decimal_places=2, max_digits=32)
    discount_percent = models.PositiveIntegerField('Скидка %',
                                                   validators=[
                                                       MinValueValidator(0),
                                                       MaxValueValidator(100)
                                                   ],
                                                   blank=True,
                                                   null=True)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    paid = models.BooleanField('Оплачено', default=False)
    unique_id = models.CharField('Номер заказа', max_length=16, unique=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_discount_count(self):
        if self.discount_percent:
            return self.total_price - self.end_price
        else:
            return None


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name='Заказ',
                              related_name='order_items')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Товар')
    unit_price = models.DecimalField('Цена за единицу', max_digits=32, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def get_total_price(self):
        if self.quantity > 1:
            return self.quantity * self.unit_price
        else:
            return self.unit_price




