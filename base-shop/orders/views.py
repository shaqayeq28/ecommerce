import uuid

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from idpay.api import IDPayAPI


from accounts.models import Address
from inventory.models import Product
from .forms import CheckOutForm
from .models import Order, OrderItem, Payment, Factor


@login_required(login_url='login')
def show_cart(request):
    order_items = request.order.order_items.all()
    shipping = 0
    if order_items:
        shipping = 30000

    context = {
        'order_items': order_items,
        'shipping': shipping,
    }
    return render(request, 'orders/cart.html', context)


@login_required(login_url='login')
def add_cart(request, product_id):
    p = Product.objects.get(id=product_id)
    try:
        if request.order.order_items.filter(product__id=product_id).exists():
            order_items = request.order.order_items.get(product__id=product_id)
            if order_items.quantity < order_items.product.available_quantity:
                order_items.quantity += 1
                order_items.save()
                messages.success(request, "Added successfully!")
            else:
                messages.warning(request, 'More Item is not available')
        else:
            if p.available_quantity >= 1:
                OrderItem.objects.create(order=request.order, product_id=product_id, quantity=1)
                messages.success(request, "Added successfully!")
            messages.warning(request, 'Item is not available')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('cart')


def product_remove(self, product):
    product = str(product.id)
    if product in self.order:
        self.order[product]['quantity'] -= 1
        if self.order[product]['quantity'] == 0:
            del self.order[product]
        self.save()


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(
        customer=request.user,
        paid=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(product__id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                order__customer=request.user,
                order__paid=False,
            )[0]
            order_item.delete()
            messages.info(request, "OrderItem remove from your cart")
            return redirect("shop")
        else:
            messages.info(request, "This Item is not in your cart")
            return redirect("cart", product__id=product_id)
    else:
        messages.info(request, "You do not have an Order")
        return redirect("cart", product__id=product_id)


@login_required(login_url='login')
def reduce_quantity_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(
        customer=request.user,
        paid=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(product__id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                order__customer=request.user,
                order__paid=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("cart")
        else:
            messages.info(request, "This Item is not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an Order")
        return redirect("cart")


@login_required(login_url='login')
def increase_quantity_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(
        customer=request.user,
        paid=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(product__id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                order__customer=request.user,
                order__paid=False,
            )[0]
            if order_item.quantity >= 1 and order_item.quantity < order_item.product.available_quantity:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Item quantity was updated")
            messages.warning(request, 'More Item is not available')
            return redirect("cart")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an Order")


class CheckOut(View):

    def get(self, request):
        order_items = request.order.order_items.all()
        shipping_address_qs = Address.objects.filter(
            customer=self.request.user
        )
        initial_data = {}
        for ele in shipping_address_qs:
            initial_data['city'] = ele.city
            initial_data['province'] = ele.province
            initial_data['address'] = ele.address_shipment

        form = CheckOutForm(initial=initial_data)
        context = {
            'form': form,
            'order_items': order_items,
        }
        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        try:
            order_obj = Order.objects.get(customer=self.request.user, paid=False)
            a = Address.objects.get(customer=self.request.user)
            form = CheckOutForm(request.POST)
            if form.is_valid():
                shipment_choice = form.cleaned_data['shipment_choice']
                payment_option = form.cleaned_data['payment_option']
                final_sum_price = request.order.cart_summation
                if payment_option == 'C':
                    if shipment_choice == 'R':
                        final_sum_price += 10000
                    else:
                        final_sum_price += 50000
                    order_obj.paid = True
                    order_obj.save()
                    Payment.objects.create(address=a, customer=order_obj.customer,
                                           shipment_type=shipment_choice, order=order_obj,
                                           final_price=final_sum_price,
                                           status=True, payment_info={"checked_out": "cash"})
                    cart_item = order_obj.order_items.all()
                    for ele in cart_item:
                        products_in_cart = ele.product
                        products_in_cart.available_quantity -= ele.quantity
                        products_in_cart.save()
                    messages.info(request, "SuccessFul!")
                    return redirect('shop')

                if payment_option == 'S':
                    return redirect('payment_start', payment_option='IdPay')
                else:
                    messages.info(request, "Not SuccessFul!")
                    return redirect('show_checkout')
        except ObjectDoesNotExist:

            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

############################################################################


def payment_init():

    api_key = config('IDPAY_API_KEY', default='b4617826-ac94-4421-9714-149e8fafb132', cast=str)
    base_url = config('BASE_URL', default='http://localhost:8000/', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)


def payment_start(request):
    if request.method == 'POST':
        order_id = uuid.uuid1()
        amount = request.order.cart_summation
        payer = {
            'name': 'masoud',
            'phone': '09118873087',
            'mail': 'mail@mail.com',
            'desc': 'description',
        }
        record = Factor(order_id=order_id, amount=int(amount))
        record.save()
        idpay_payment = payment_init()
        result = idpay_payment.payment(str(order_id), amount, 'order/checkout/', payer)  ####

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"

    return render(request, 'orders/error.html', {'txt': txt})


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':
        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')

        if Factor.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:
            idpay_payment = payment_init()
            payment = Factor.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()

            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:
                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()

                    return render(request, 'orders/error.html', {'txt': result['message']})

                else:
                    txt = result['message']
            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)
        else:
            txt = "Order Not Found"
    else:
        txt = "Bad Request"

    return render(request, 'orders/error.html', {'txt': txt})


def payment_check(request, pk):
    payment = Factor.objects.get(pk=pk)
    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:
        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()

    return render(request, 'orders/error.html', {'txt': result['message']})
