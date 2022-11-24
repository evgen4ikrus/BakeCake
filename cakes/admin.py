from django.contrib import admin

from .models import (CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping,
                     Customer, Order)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Покупатели'


class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'cake_type',
        'customer',
        'order_comment',
        'delivery_time',
        'delivery_comment',
        'total_cost'
    ]
    list_filter = [
        'status',
    ]
    search_fields = [
        'customer',
    ]


@admin.register(CakeBerry)
class CakeBerryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price'
    ]


@admin.register(CakeDecor)
class CakeDecorAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price'
    ]


@admin.register(CakeForm)
class CakeFormAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price'
    ]


@admin.register(CakeSize)
class CakeSizeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price'
    ]


@admin.register(CakeTopping)
class CakeToppingAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price'
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)