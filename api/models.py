from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    full_name = models.CharField('ФИО', max_length=100)
    mailing_address = models.CharField('Адрес доставки', max_length=100)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Role(models.Model):
    class RoleChoices(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        MANAGER = 'manager', 'Менеджер'

    role = models.CharField('Роль пользователя', max_length=32, choices=RoleChoices.choices,
                            default=RoleChoices.CLIENT)


class Product(models.Model):
    vendor_code = models.CharField('артикул', max_length=100, unique=True)
    name = models.CharField('наименование', max_length=64)
    retail_price = models.PositiveSmallIntegerField('Розничная цена')
    purchase_price = models.PositiveSmallIntegerField('Цена закупки')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    user = models.OneToOneField(User, models.CASCADE,
                                related_name='order')
    products = models.ManyToManyField(Product, 'Товары в корзине')

