from django.shortcuts import render
from .models import CakeSize, CakeForm, CakeTopping, CakeBerry, CakeDecor


def index(request):
    cake_elements = {
        'sizes': CakeSize.objects.all(),
        'forms': CakeForm.objects.all(),
        'toppings': CakeTopping.objects.all(),
        'berries': CakeBerry.objects.all(),
        'decors': CakeDecor.objects.all()
    }
    return render(request, template_name='index.html', context={
        'cake_elements': cake_elements
    })


def view_lk_order(request):
    return render(request, 'lk-order.html')


def view_lk(request):
    return render(request, 'lk.html')
