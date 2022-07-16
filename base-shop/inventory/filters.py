import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    CHOICES = (('جدید', 'جدید '), ('قدیمی', 'قدیمی'))
    ordering = django_filters.ChoiceFilter(label='ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        product_price = django_filters.NumberFilter()
        model = Product

        fields = {
            'product_price': ['lt', 'gt'],
            'category': ['exact'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'added_date' if value == 'جدید' else '-added_date'
        return queryset.order_by(expression)
