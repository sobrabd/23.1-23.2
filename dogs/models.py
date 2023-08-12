from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Порода')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'порода'
        verbose_name_plural = 'породы'


class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='Кличка')
    # category = models.CharField(max_length=100, verbose_name='Порода')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Порода')

    phot = models.ImageField(upload_to='dogs/', null=True, blank=True, verbose_name='Фото')
    birth_day = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='владелец')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'собака'
        verbose_name_plural = 'собаки'


class Parent(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='Кличка')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Порода')
    birth_day = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'предок'
        verbose_name_plural = 'предки'
