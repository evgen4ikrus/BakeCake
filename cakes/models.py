from django.contrib import admin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    name = models.CharField('Имя', max_length=100, blank=True)
    phone_number = PhoneNumberField('Телефон', max_length=20)
    email = models.EmailField('Почта', max_length=100, blank=True)
    address = models.CharField('Адрес', max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = '       Клиенты'


class CakeSize(models.Model):
    title = models.CharField('Количество уровней', max_length=1)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Размер торта'
        verbose_name_plural = '     Размеры тортов'


class CakeForm(models.Model):
    title = models.CharField('Форма торта', max_length=20)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Форма торта'
        verbose_name_plural = '    Формы тортов'


class CakeTopping(models.Model):
    title = models.CharField('Топпинг', max_length=20)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = '   Топпинги'


class CakeBerry(models.Model):
    title = models.CharField('Ягода', max_length=20)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = '  Ягоды'


class CakeDecor(models.Model):
    title = models.CharField('Декор', max_length=20)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = ' Декоры'


class Order(models.Model):
    NEW_STATUS, PAID_STATUS, COMPLETE_STATUS = range(3)
    status = models.IntegerField(
        'Статус',
        choices=[
            (NEW_STATUS, 'Новый'),
            (PAID_STATUS, 'Оплачен'),
            (COMPLETE_STATUS, 'Завершён'),
        ],
        default=NEW_STATUS,
        db_index=True
    )
    customer = models.ForeignKey(
        Customer,
        related_name='orders',
        verbose_name='Клиент',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )
    cake_size = models.ForeignKey(
        CakeSize,
        related_name='orders',
        verbose_name='Количество уровней',
        on_delete=models.SET_NULL,
        null=True
    )
    cake_form = models.ForeignKey(
        CakeForm,
        related_name='orders',
        verbose_name='Форма торта',
        on_delete=models.SET_NULL,
        null=True
    )
    cake_topping = models.ForeignKey(
        CakeTopping,
        related_name='orders',
        verbose_name='Топпинг',
        on_delete=models.SET_NULL,
        null=True
    )
    cake_berry = models.ForeignKey(
        CakeBerry,
        related_name='orders',
        verbose_name='Ягоды',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cake_decor = models.ForeignKey(
        CakeDecor,
        related_name='orders',
        verbose_name='Декор',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cake_caption = models.CharField('Надпись', max_length=200, blank=True)
    order_comment = models.TextField('Комментарий к заказу', blank=True)
    delivery_time = models.DateTimeField('Дата и время доставки', null=True, blank=True)
    delivery_comment = models.TextField('Комментарий для курьера', blank=True)
    total_cost = models.IntegerField('Стоимость заказа', null=True, blank=True)

    @admin.display(description='Торт')
    def cake_type(self):
        cake_type = f'{self.cake_size.title} • {self.cake_form.title} • {self.cake_topping.title}'
        if self.cake_berry:
            cake_type += f' • {self.cake_berry.title}'
        if self.cake_decor:
            cake_type += f' • {self.cake_decor.title}'
        if self.cake_caption:
            cake_type += ' • Надпись'
        return cake_type

    def __str__(self):
        return self.cake_type()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = '      Заказы'
