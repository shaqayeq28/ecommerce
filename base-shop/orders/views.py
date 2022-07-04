from django.shortcuts import render

from accounts.models import Customer
from orders.models import Order, OrderItem


def cart(request):
    context = dict()
    return render(request, 'orders/cart.html', context)