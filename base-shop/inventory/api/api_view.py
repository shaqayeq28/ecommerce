from rest_framework.generics import ListAPIView, RetrieveAPIView

from inventory.models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer



