from django.db import models
from django.conf import settings
from django.forms import ModelForm
from inventory.models import Product
from accounts.models import Customer, Address


class Order(models.Model):

    paid = models.BooleanField(default=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_of_order = models.DateField(auto_now_add=True)
    total_cost = models.FloatField()


class OrderItem(models.Model):
    CART_STATUS_FIELD = (
        ('Not purchased', 'Not purchased'),
        ('purchased', 'purchased'),
        ('in progress', 'in progress')
    )
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart_status_field = models.CharField(default='Not purchased', max_length=255, choices=CART_STATUS_FIELD)


class Payment(models.Model):

    SHIPMENT_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('pishtaz', 'Pishtaz'),
        ('tipax', 'Tipax'),
    )

    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    payment_info = models.JSONField(default=dict)
    shipment_type = models.CharField(
        max_length=100, default='regular', choices=SHIPMENT_TYPE_CHOICES)
    address = models.OneToOneField(Address, on_delete=models.RESTRICT, default='', related_name='address_set')

