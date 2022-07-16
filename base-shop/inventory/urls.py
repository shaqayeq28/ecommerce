from django.urls import path

from .views import ProductList, ProductDetail, add_comment

urlpatterns = [
    path('shop/', ProductList.as_view(), name="shop"),
    path('product-details/<int:pk>', ProductDetail.as_view(), name="detail"),
    path("add-comment/<int:product_pk>", add_comment, name="add-comment"),

]
