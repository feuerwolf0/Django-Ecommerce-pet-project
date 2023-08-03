from django.db import models
from django.contrib.auth.models import User
import os

from users.models import Profile


class Category(models.Model):
    name = models.CharField('Категория', max_length=32)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Тэг', max_length=32)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']

    def __str__(self):
        return self.name


def get_upload_image_path(instance, filename):
    """
    Возвращает путь вида id_продукта/file.etc
    """
    return os.path.join(str(instance.id), filename)


class Post(models.Model):
    owner = models.ForeignKey(Profile,
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE,
                              verbose_name='Пользователь')
    title = models.CharField('Заголовок', max_length=128)
    content = models.TextField('Текст', max_length=5000)
    published = models.DateTimeField('Дата публикации',
                                     auto_now_add=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 related_name='post_category')
    tags = models.ManyToManyField(Tag,
                                  related_name='posts',
                                  verbose_name='Тэги',
                                  blank=True)
    image = models.ImageField('Изображение',
                              upload_to=get_upload_image_path,
                              blank=True,
                              null=True)
    likes = models.ManyToManyField(Profile,
                                   related_name='post_likes',
                                   verbose_name='Лайк',
                                   blank=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']

    def __str__(self):
        return f'{self.owner.user.username} {self.title}'

    def num_of_likes(self):
        if self.likes.count() == 0:
            return ''
        else:
            return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='comments')
    content = models.TextField('Текст', max_length=512)
    owner = models.ForeignKey(Profile,
                              verbose_name='Автор',
                              on_delete=models.CASCADE)
    published = models.DateTimeField('Дата создания', auto_now_add=True)
    approved = models.BooleanField('Опубликован', default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-published']

    def __str__(self):
        return f'{self.owner} {self.content}'

