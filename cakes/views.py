import uuid

from django.shortcuts import redirect, render
from yookassa import Configuration, Payment

from .models import (CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping,
                     Customer, Order)
from django.contrib.auth.models import User


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
        customer = Customer.objects.filter(phone_number=phone)
        if not customer:
            username, tail = email.split('@')
            user = User.objects.create(username=username, email=email, password='12345cake', first_name=customer_name)
            customer = Customer.objects.create(user=user, phone_number=phone, address=address)
        cake_berries_obj=CakeBerry.objects.get(id=cake_berries)
        cake_decor_obj = CakeDecor.objects.get(id=cake_decor)
        cake_form_obj = CakeForm.objects.get(id=cake_form)
        cake_levels_obj = CakeSize.objects.get(id=cake_levels)
        cake_topping_obj = CakeTopping.objects.get(id=cake_topping)
        total_cost = cake_berries_obj.price + cake_decor_obj.price + cake_form_obj.price + cake_levels_obj.price + cake_topping_obj.price
        order = Order.objects.create(
            customer=customer,
            cake_size=cake_levels_obj,
            cake_form=cake_form_obj,
            cake_topping=cake_topping_obj,
            cake_berry=cake_berries_obj,
            cake_decor=cake_decor_obj,
            cake_caption=cake_words,
            order_comment=cake_name,
            delivery_time=order_date,
            delivery_comment=f'{order_time} {comment}',
            total_cost = total_cost
            )
        payment_url = make_payment(customer.id, order.id, total_cost)
        return redirect(payment_url)
    return render(request, 'index.html')


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
