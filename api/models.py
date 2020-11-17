from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Define a model manager for User model with no username set
class UserManager(BaseUserManager):
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
        extra_fields.setdefault('role', 'manager')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Custom User Class
class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        MANAGER = 'manager', 'Менеджер'

    username = None
    full_name = models.CharField('ФИО', max_length=100)
    role = models.CharField('Роль пользователя', max_length=10, choices=RoleChoices.choices,
                            default=RoleChoices.CLIENT)
    mailing_address = models.CharField('Адрес доставки', max_length=100)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name


class Product(models.Model):
    vendor_code = models.CharField('артикул', max_length=100, unique=True)
    name = models.CharField('наименование', max_length=64)
    retail_price = models.PositiveSmallIntegerField('Розничная цена')
    purchase_price = models.PositiveSmallIntegerField('Цена закупки', blank=True, default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.OneToOneField(User, models.CASCADE,
                                related_name='order')
    products = models.ManyToManyField(Product, verbose_name='Товары в корзине', through='ProductsInOrder')
    price = models.PositiveIntegerField('Сумма заказа', default=0)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return 'Корзина' + self.user.email

    def clean_price(self):
        self.price = 0
        for product in self.productsinorder_set.all():
            self.price += product.sum

    def generate_html(self):
        html = self.user.email + '<br/>' + str(self.pk) + '<br/>' + self.user.mailing_address
        return html


# intermediary model for adding quantity and sum to each item in order
class ProductsInOrder(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, 'товар')
    order = models.ForeignKey(Order, models.CASCADE, 'корзина')
    quantity = models.PositiveSmallIntegerField('количество товара', default=1)
    sum = models.PositiveIntegerField('Сумма по строке', default=0)

    def clean_product_sum(self):
        return self.product.retail_price * self.quantity
