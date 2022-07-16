from django.contrib import admin

from orders.models import Order, OrderItem, Payment, Factor

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Factor)
