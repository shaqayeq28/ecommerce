from allauth.socialaccount.models import SocialAccount
from django.db import models
from django.db.models import Sum

from inventory.models import Product
from accounts.models import Customer, Address


class Order(models.Model):
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    social_user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, null=True)
    date_of_order = models.DateField(auto_now_add=True)

    @property
    def order_items_cardinality(self):
        qty_s = self.order_items.all().aggregate(qty_sum=Sum('quantity'))['qty_sum']
        print(qty_s)

        return qty_s

    @property
    def cart_summation(self):
        cart_items = self.order_items.select_related('product')
        sum_prices = 0
        for item in cart_items:
            sum_prices += (item.product.price_after_discount() * item.quantity)
        return int(sum_prices)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def product_sum_price(self):
        return int(self.product.price_after_discount() * self.quantity)


class Payment(models.Model):
    SHIPMENT_TYPE_CHOICES = (
        ('R', 'Regular'),
        ('P', 'Pishtaz'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    payment_info = models.JSONField(default=dict)
    shipment_type = models.CharField(
        max_length=100, default='regular', choices=SHIPMENT_TYPE_CHOICES)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, default='', related_name='address_set')
    final_price = models.PositiveIntegerField(default=0)


class Factor(models.Model):
    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.TextField(default='-')
    card_number = models.TextField(default="****")
    idpay_track_id = models.IntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + "  |  " + self.order_id + "  |  " + str(self.status)
