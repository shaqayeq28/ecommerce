from .models import Order
from django.utils.deprecation import MiddlewareMixin
from accounts.models import Customer


class OrderMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        assert hasattr(request, 'user'), 'shalgham'
        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.filter(id=request.user.id).first()
            order, status = Order.objects.get_or_create(customer=customer, paid=False)
            request.order = order

    def process_response(self, request, response):
        print(response)
        return response

    def process_exception(self, request, exception):
        return None