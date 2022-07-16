from django.urls import path

from inventory.api.api_view import ProductListView, ProductDetailView


urlpatterns = [
    path('product-list/', ProductListView.as_view(), name="product-list"),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name="product-detail"),
]
