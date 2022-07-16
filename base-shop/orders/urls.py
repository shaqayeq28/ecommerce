from django.urls import path

from orders.views import show_cart, add_cart, remove_from_cart,\
    reduce_quantity_item, increase_quantity_item, CheckOut,\
    payment_start, payment_return, payment_check

urlpatterns = [
    path('cart/', show_cart, name="cart"),
    path('add/<int:product_id>/', add_cart, name="add"),
    path('remove/<int:product_id>/', remove_from_cart, name="remove"),
    path('reduce/<int:product_id>/', reduce_quantity_item, name="reduce"),
    path('increase/<int:product_id>/', increase_quantity_item, name="increase"),
    path('show-cart/', show_cart, name='show_cart'),
    path('add-cart/<int:product_id>', add_cart, name='add_cart'),

    path('show_checkout/', CheckOut.as_view(), name='show_checkout'),

    path('payment', payment_start, name='payment_start'),
    path('orders/factor/', payment_return, name='payment_return'),
    path('payment/check/<pk>', payment_check, name='payment_check'),

]
