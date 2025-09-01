from django.db import models
from django.contrib.auth.models import User

class Ip(models.Model):
    ip = models.CharField(max_length=100)
    def __str__(self):
        return self.ip


class Main_info(models.Model):
    Our_mission = models.TextField(verbose_name='Наша миссия')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    number_phone_1 = models.BigIntegerField(verbose_name='Номер телефона 1')
    number_phone_2 = models.BigIntegerField(verbose_name='Номер телефона 2')
    email = models.CharField(max_length=200, verbose_name='Электронная почта')
    id_group = models.BigIntegerField(verbose_name='id Group')

    class Meta:
        verbose_name = 'Основную информацию'
        verbose_name_plural = 'Основная информация'

    def __str__(self):
        return self.address


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    discount = models.BooleanField(verbose_name='Товар по скидке')
    discount_price = models.IntegerField(verbose_name='Цена по скидке', null=True, blank=True)
    img = models.ImageField(upload_to='product_img/', verbose_name='Фото')
    short_description = models.TextField(verbose_name='Краткое описание', null=True, blank=True)
    full_description = models.TextField(verbose_name='Описание', null=True, blank=True)
    available = models.BooleanField(verbose_name='Наличие')
    width = models.IntegerField(verbose_name='Ширина в см.', null=True, blank=True)
    height = models.IntegerField(verbose_name='Высота в см.', null=True, blank=True)
    quality_checking = models.BooleanField(verbose_name='Проверка качества')
    guarantee = models.CharField(max_length=200, verbose_name='Гарантия', null=True, blank=True)
    views = models.IntegerField(verbose_name='Просмотры',  null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название статьи')
    short_description = models.TextField(verbose_name='Краткое описание', null=True, blank=True)
    img = models.ImageField(upload_to='product_img/', verbose_name='Главное фото')
    text_1 = models.TextField(verbose_name='Текст 1', null=True, blank=True)
    text_2 = models.TextField(verbose_name='Текст 2', null=True, blank=True)
    img_1 = models.ImageField(upload_to='product_img/', verbose_name='Фото к статье', null=True, blank=True)
    img_2 = models.ImageField(upload_to='product_img/', verbose_name='Фото к статье', null=True, blank=True)
    text_3 = models.TextField(verbose_name='Текст 3', null=True, blank=True)

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    email = models.CharField(max_length=200, verbose_name='Почта')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    text = models.TextField(verbose_name="Отзыв")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    stars = models.IntegerField(verbose_name="Рейтинг")
    is_public = models.BooleanField(verbose_name='Публиковать')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Guest_Review(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    tel_number = models.CharField(max_length=200, verbose_name='Телефон')
    email = models.CharField(max_length=200, verbose_name='Почта')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    text = models.TextField(verbose_name="Отзыв")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    is_public = models.BooleanField(verbose_name='Публиковать')

    class Meta:
        verbose_name = 'гостевой Отзыв'
        verbose_name_plural = 'гостевые Отзывы'

    def __str__(self):
        return self.text