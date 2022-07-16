import six

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as login_, logout as logout_, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .tasks import email_sender
from .models import Customer, Supplier, Address
from accounts.forms import CustomerRegister, LoginForm,\
    SupplierRegister, ProfileForm, AddressForm, RestPasswordForm, \
    ForgetPassForm, ResetPasswordProfile

User = get_user_model()


def logout(request):
    logout_(request)
    return redirect("/")


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, password=password, email=email)
            print('salam')
            if user:
                print(user)
                login_(request, user)
                return redirect('/')
            else:
                return redirect('login')


class SignUpCustomer(View):

    def get(self, request):
        form = CustomerRegister()
        context = {
            'form': form
        }
        return render(request, 'accounts/signup_customer.html', context)

    def post(self, request):
        form = CustomerRegister(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            user = Customer.objects.create_user(email=email, password=password,
                                                phone=phone)

            return redirect('login')

        context = {
            'form': form
        }
        return render(request, 'accounts/signup_customer.html', context)


class SignUpSupplier(View):

    def get(self, request):
        form = SupplierRegister()
        context = {
            'form': form
        }
        return render(request, 'accounts/signup_supplier.html', context)

    def post(self, request):
        form = SupplierRegister(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            company_name = form.cleaned_data['company_name']
            phone = form.cleaned_data['phone']
            user = Supplier.objects.create_user(email=email,
                                                password=password, company_name=company_name,
                                                phone=phone)
            return redirect('login')

        context = {
            'form': form
        }
        return render(request, 'accounts/signup_supplier.html', context)


class ProfileFormShow(LoginRequiredMixin, View):

    def get(self, request):
        user = Customer.objects.get(user_ptr=request.user.id)
        initial_data = {}
        initial_data['first_name'] = user.first_name
        initial_data['last_name'] = user.last_name
        initial_data['job'] = user.job
        initial_data['phone'] = user.phone
        initial_data['date_of_birth'] = user.date_of_birth

        form = ProfileForm(initial=initial_data)
        context = {
            'form': form
        }

        return render(request, 'accounts/my-account.html', context)

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            job = form.cleaned_data['job']
            phone = form.cleaned_data['phone']
            date_of_birth = form.cleaned_data['date_of_birth']

            Customer.objects.update(first_name=first_name,
                                    last_name=last_name, job=job,
                                    phone=phone, date_of_birth=date_of_birth)
            return redirect('profile')


class AddressFormShow(LoginRequiredMixin, View):

    def get(self, request):
        user = Customer.objects.get(user_ptr=request.user.id)
        shipping_address_qs = Address.objects.filter(
            customer=user
        )
        initial_data = {}
        for ele in shipping_address_qs:
            initial_data['city'] = ele.city
            initial_data['province'] = ele.province
            initial_data['address'] = ele.address_shipment

        form = AddressForm(initial=initial_data)
        context = {
            'form_address': form
        }
        return render(request, 'accounts/address.html', context)

    def post(self, request):
        user = Customer.objects.get(user_ptr=request.user.id)
        form = AddressForm(request.POST)
        if form.is_valid():
            province = form.cleaned_data['province']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            shipping_address_qs = Address.objects.filter(
                customer=user
            )
            if shipping_address_qs:
                Address.objects.update(province=province,
                                       city=city,
                                       address_shipment=address,
                                       customer=user)
            else:
                Address.objects.create(province=province,
                                       city=city,
                                       address_shipment=address,
                                       customer=user)
            return redirect('address')


class ResetPasswordProfileFormShow(LoginRequiredMixin, View):

    def get(self, request):
        form = ResetPasswordProfile()
        context = {
            'form': form
        }
        return render(request, 'accounts/reset_password_profile.html', context=context)

    def post(self, request):
        user = Customer.objects.get(user_ptr=request.user.id)
        form = ResetPasswordProfile(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            return redirect('reset_password_profile')


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def email_message_generator(request, user, template):
    current_site = get_current_site(request)
    message = render_to_string(f'{template}', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    return message


class ForgetPassword(View):

    def get(self, request):
        form = RestPasswordForm()
        return render(request, "accounts/forget_password.html", {"form": form})

    def post(self, request):
        form = RestPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            mail_subject = 'reset your password'
            to_email = form.cleaned_data.get("email")
            message = email_message_generator(request, user, "accounts/reset_password_email.html",)
            email_sender.delay(message, to_email, mail_subject)
            return redirect("verify")
        else:
            render(request, "accounts/forget_password.html", {"form": form})


class WaitingForVerify(View):

    def get(self, request):
        return render(request, "accounts/verify.html", {})


def token_validator(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print('tk_ui',uid)
        user = User.objects.get(pk=uid)
        print('token_validator', user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return user
    if user is not None and account_activation_token.check_token(user, token):
        return user


class PasswordReset(View):

    def get(self, request):
        uidb64 = request.GET.get("uidb64", "")
        print('uuu is', uidb64)
        token = request.GET.get("token", "")
        print('token khali is', token)
        user = token_validator(uidb64, token)
        print('user token is', user)
        if user:
            print('test')
            form = ForgetPassForm()
            return render(request, "accounts/reset_password.html", {"form": form, "user": user})

    def post(self, request):
        email = request.POST.get("user")
        print('emailesh',email)
        user = User.objects.get(email=email)
        print('post2',user)
        form = ForgetPassForm(request.POST)
        if form.is_valid():
            password = request.POST.get("password")
            user.set_password(password)
            user.save()
            return redirect("home")
        else:
            render(request, "accounts/reset_password.html", {"form": form})


class OrderHistoryShow(LoginRequiredMixin, View):

    def get(self, request):
        customer = Customer.objects.get(user_ptr=request.user.id)
        qs = customer.payment_set.all()
        context = {
            'payment_qs': qs
        }
        return render(request, 'accounts/history.html', context)


class OrderDetailHistoryShow(LoginRequiredMixin, View):

    def get(self, request, order_id):
        customer = Customer.objects.get(user_ptr=request.user.id)
        obj_payment = customer.payment_set.filter(order=order_id).first()
        obj_order = obj_payment.order
        qs_order_items = obj_order.order_items.all()
        context = {
            'order_items': qs_order_items,
            'payment': obj_payment
        }
        return render(request, 'accounts/detailhistory.html', context)