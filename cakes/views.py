import uuid

from django.shortcuts import render
from yookassa import Configuration, Payment

from .models import CakeBerry, CakeDecor, CakeForm, CakeSize, CakeTopping


def index(request):
    cake_elements = {
        'sizes': CakeSize.objects.all(),
        'forms': CakeForm.objects.all(),
        'toppings': CakeTopping.objects.all(),
        'berries': CakeBerry.objects.all(),
        'decors': CakeDecor.objects.all()
    }
    return render(request, template_name='index.html',
                  context={'cake_elements': cake_elements})


def view_lk_order(request):
    return render(request, 'lk-order.html')


def view_lk(request):
    return render(request, 'lk.html')


def make_payment(client_id, order_id, amount, description="CakeBaker order"):
    Configuration.account_id = '960972'
    Configuration.secret_key = 'test_8PDhbolVyRcVvZsmU0vy-jo4YRr53QiJv2CvwNYtQ3o'
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


if __name__ == '__main__':
    print(make_payment('1', '1', '100'))
