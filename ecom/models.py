from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Countrys(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Citys(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Streets(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=40)
    country = models.ForeignKey(Countrys, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(Citys, on_delete=models.CASCADE, null=True)
    street = models.ForeignKey(Streets, on_delete=models.CASCADE, null=True)
    phone = models.IntegerField()
    index = models.IntegerField()

    def __str__(self):
        return self.name

class Supply(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True,null=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.date) + str(" ") + str(self.provider)

class Categorys(models.Model):
    fullname = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

class Products(models.Model):
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, null=True)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)

    def __str__(self):
        return self.name

from django.utils.translation import gettext_lazy as _

class Users(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name='Имя')
    surname = models.CharField(max_length=40, verbose_name='Фамилия')
    phone = models.IntegerField(verbose_name='Телефон')

    country = models.ForeignKey(Countrys, on_delete=models.SET_NULL, null=True, verbose_name='Страна')
    city = models.ForeignKey(Citys, on_delete=models.SET_NULL, null=True, verbose_name='Город')
    street = models.ForeignKey(Streets, on_delete=models.SET_NULL, null=True, verbose_name='Улица')

    index = models.IntegerField(verbose_name='Индекс')
    house = models.IntegerField(verbose_name='Дом')
    liter = models.CharField(max_length=10, verbose_name='Литер')
    apartment = models.IntegerField(verbose_name='Квартира')
    password = models.CharField(max_length=20, verbose_name='Пароль')

    def __str__(self):
        return self.name


class Couriers(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    pass_id = models.IntegerField()

    def __str__(self):
        return self.name

class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, on_delete=models.CASCADE)
    delivery_price = models.IntegerField()
    order_price = models.IntegerField()

    def __str__(self):
        return self.user

def in_three_days():
    return timezone.now() + timedelta(days=3)

class Deliverys(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    courier = models.ForeignKey(Couriers, on_delete=models.CASCADE)
    date_begin = models.DateTimeField(auto_now_add=True)
    data_done = models.DateTimeField(default=in_three_days)

    def __str__(self):
        return self.order or ' '
