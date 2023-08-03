import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import Profile
from blog.models import Category, Tag
import os


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='category_products')
    tags = models.ManyToManyField(Tag,
                                  blank=True,
                                  verbose_name='Тэги',
                                  related_name='tags_products')
    title = models.CharField('Название', max_length=128, db_index=True)
    preview_about = models.TextField('Превью', max_length=512)
    about = models.TextField('О товаре', db_index=True)
    features = models.TextField('Характеристики', db_index=True)
    old_price = models.DecimalField('Старая цена', max_digits=16, decimal_places=2, null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=16, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField('Количество на складе')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.price} руб'

    def get_percent_discount(self):
        if self.old_price and self.price:
            discount = 100 - ( self.price * 100 / self.old_price )
            return int(discount)
        else:
            return ''

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


def get_path_productimage(instance, filename):
    """
    Сохраняет фото товара в products/id_товара/filename
    """
    folder = os.path.join('products', str(instance.product.id))
    return os.path.join(folder, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Товар',
                                related_name='image')
    image = models.ImageField('Фото',
                              upload_to=get_path_productimage,
                              default='avatars/no_pic.png',
                              blank=True,
                              null=True)
    created_at = models.DateField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['-created_at']


class Discount(models.Model):
    code = models.CharField('Купон', max_length=64, unique=True)
    discount_percentage = models.PositiveIntegerField('Размер скидки %',
                                                      validators=[
                                                          MinValueValidator(0),
                                                          MaxValueValidator(100)
                                                      ])
    start_date = models.DateField('Дата начала акции')
    end_date = models.DateField('Дата окончания акции')
    active = models.BooleanField('Активен?', default=False)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'Купон {self.code} -{self.discount_percentage}%'


class Question(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Товар',
                                related_name='questions')
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              verbose_name='Пользователь')
    approved = models.BooleanField('Опубликовано', default=False)
    published = models.DateTimeField('Дата публикации', auto_now_add=True)
    content = models.TextField('Вопрос', max_length=512)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-published']

    def __str__(self):
        return f'{self.owner} {self.content}'


class Wishlist(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='wish')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        ordering = ['-created_at']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='Владелец')
    data = models.JSONField('Данные', default=dict)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


