import datetime
import json
import uuid

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from environs import Env
from yookassa import Configuration, Payment

from .models import (CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping,
                     Customer, Order, Promocod)

from django.db.utils import IntegrityError


env = Env()
env.read_env()


def index(request):
    reg = request.GET.get('REG')
    if reg:
        try:
            customer = Customer.objects.get(phone_number=reg)
            if customer:
                login(request, customer.user)
        except:
            pass
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
        raw_promocod = request.GET.get('PROMOCOD')
        customer = Customer.objects.filter(phone_number=phone)
        if customer:
            customer = customer[0]
        if not customer:
            username, tail = email.split('@')
            try:
                user = User.objects.create(username=username, email=email, password='12345cake', first_name=customer_name)
                customer = Customer.objects.create(user=user, phone_number=phone, address=address)
            except IntegrityError:
                return render(request, 'error.html')
        cake_form_obj = CakeForm.objects.get(id=cake_form)
        cake_levels_obj = CakeSize.objects.get(id=cake_levels)
        cake_topping_obj = CakeTopping.objects.get(id=cake_topping)        
        total_cost = cake_form_obj.price + cake_levels_obj.price + cake_topping_obj.price
        cake_berries_obj = None
        cake_decor_obj = None
        if cake_berries:
            cake_berries_obj = CakeBerry.objects.get(id=cake_berries)
            total_cost += cake_berries_obj.price
        if cake_decor:
            cake_decor_obj = CakeDecor.objects.get(id=cake_decor)
            total_cost += cake_decor_obj.price
        if cake_words:
            total_cost = total_cost + 500
        if order_date:
            order_date_dtobj = datetime.datetime.strptime(order_date, '%Y-%m-%d')
            min_date = datetime.datetime.now() + datetime.timedelta(days=1)
            if order_date_dtobj < min_date:
                total_cost = total_cost * 1.2
        if raw_promocod:
            checked_promocode = Promocod.objects.filter(promocod=raw_promocod)
            if checked_promocode:
                total_cost = total_cost - total_cost * checked_promocode[0].discount / 100
            else:
                error_text = 'Не действительный промокод'
                return render(
                    request,
                    template_name='error.html',
                    context={
                        'page_error': error_text
                    }
                    )
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
            total_cost=total_cost
            )
        payment_url = make_payment(customer.id, order.id, total_cost)
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
    customer_data = {
        'name': '',
        'phone_number': '',
        'email': '',
    }
    user = request.user
    if user.username:
        customer_data['name'] = user.username
        customer_data['email'] = user.email
        try:
            customer = Customer.objects.get(user=user)
            customer_data['name'] = user.first_name
            customer_data['address'] = customer.address
            customer_data['phone_number'] = str(customer.phone_number)
        except ObjectDoesNotExist:
            pass
    customer_json = json.dumps(customer_data)
    return render(
        request,
        template_name='index.html',
        context={
            'cake_elements': cake_elements,
            'cake_elements_json': cake_elements_json,
            'customer_json': customer_json
        }
    )


def view_lk(request):
    reg = request.GET.get('reg')
    if reg:
        try:
            customer = Customer.objects.get(phone_number=reg)
            if customer:
                login(request, customer.user)
        except ObjectDoesNotExist:
            pass
    if request.method == 'POST':
        phone = request.POST.get('PHONE')
        name = request.POST.get('NAME')
        email = request.POST.get('EMAIL')
        user = request.user
        customer = Customer.objects.get(user=request.user)
        user.first_name = name
        user.email = email
        customer.phone_number = phone
        customer.save()
        user.save()

    customer_data = {
        'name': '',
        'phone_number': '',
        'email': '',
    }
    user = request.user
    if user.username:
        customer_data['name'] = user.username
        customer_data['email'] = user.email
        try:
            customer = Customer.objects.get(user=user)
            orders = Order.objects.filter(customer=customer)
            customer_data['name'] = user.first_name
            customer_data['phone_number'] = str(customer.phone_number),
            customer_json = json.dumps(customer_data)
            return render(request, 'lk.html', context={'orders': orders, 'customer_json': customer_json})
        except ObjectDoesNotExist:
            pass
    customer_json = json.dumps(customer_data)
    return render(request, 'lk.html', context={'customer_json': customer_json})


def make_payment(client_id, order_id, amount, description="CakeBaker order"):
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
            "return_url": env('RETURN_URL')
            },
        "description": description,
        "metadata": {
            "client_id": client_id,
            "order_id": order_id
            }
        }, idempotence_key)
    return payment.confirmation.confirmation_url
