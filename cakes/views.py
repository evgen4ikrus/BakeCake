from django.shortcuts import render, redirect
from yookassa import Payment, Configuration

import uuid
from .models import Customer, Order

from django.shortcuts import render
from yookassa import Configuration, Payment

from .models import CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping


def index(request):
    phone = request.GET.get('PHONE')
    if phone:
        email = request.GET.get('EMAIL')
        address = request.GET.get('ADDRESS')
        order_date = request.GET.get('DATE')
        order_time = request.GET.get('TIME')
        comment = request.GET.get('DELIVCOMMENTS')
        customer_name = request.GET.get('NAME')
        cake_levels = request.GET.get('LEVELS')
        cake_form = request.GET.get('FORM')
        cake_topping = request.GET.get('TOPPING')
        cake_berries = request.GET.get('BERRIES')
        cake_decor = request.GET.get('DECOR')
        cake_words = request.GET.get('WORDS')
        cake_name = request.GET.get('COMMENTS')
        payment_url = make_payment(1,1,1000)
        return redirect(payment_url)

    cake_elements = {
        'sizes': CakeSize.objects.all(),
        'forms': CakeForm.objects.all(),
        'toppings': CakeTopping.objects.all(),
        'berries': CakeBerry.objects.all(),
        'decors': CakeDecor.objects.all()
    }
    cake_elements_json = {
        'size_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['sizes']},
        'size_costs': {0: 0} | {item.id: item.price for item in cake_elements['sizes']},
        'form_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['forms']},
        'form_costs': {0: 0} | {item.id: item.price for item in cake_elements['forms']},
        'topping_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['toppings']},
        'topping_costs': {0: 0} | {item.id: item.price for item in cake_elements['toppings']},
        'berry_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['berries']},
        'berry_costs': {0: 0} | {item.id: item.price for item in cake_elements['berries']},
        'decor_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['decors']},
        'decor_costs': {0: 0} | {item.id: item.price for item in cake_elements['decors']},
    }
    return render(
        request,
        template_name='index.html',
        context={
            'cake_elements': cake_elements,
            'cake_elements_json': cake_elements_json,
        }
    )


def view_lk_order(request):
    return render(request, 'lk-order.html')


def view_lk(request):
    return render(request, 'lk.html')


def make_payment(client_id, order_id, amount, description="CakeBaker order"):
    #will fix after debug function and complete writting of views, don't beat me for a while :)
    from environs import Env
    env = Env()
    env.read_env()
    Configuration.account_id = env('YOOMONEY_SHOPID')
    Configuration.secret_key = env('YOOMONEY_KEY')
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
            },
        "payment_method_data": {
            "type": "bank_card"
            },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/"
            },
        "description": description,
        "metadata": {
            "client_id": client_id,
            "order_id": order_id
            }
        }, idempotence_key)
    return payment.confirmation.confirmation_url
