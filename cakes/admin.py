from django.contrib import admin
from .models import Customer, Order, CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone_number',
        'email',
        'address'
    ]
    search_fields = [
        'name',
        'phone_number',
        'email',
        'address'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
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
