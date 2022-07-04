from django.urls import path

from orders.views import cart


urlpatterns = [
    path('cart/', cart, name="cart"),
    # path('checkout/<int:pk>', ProductDetail.as_view(), name="checkout"),
]

