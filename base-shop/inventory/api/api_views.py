from rest_framework.generics import ListAPIView, RetrieveAPIView

from inventory.api.serializers import ProductListSerializer, ProductDetailSerializer
from inventory.models import Product


class ProductListView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


