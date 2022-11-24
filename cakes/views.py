from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def view_lk_order(request):
    return render(request, 'lk-order.html')


def view_lk(request):
    return render(request, 'lk.html')
