from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as login_, logout as logout_
from django.views import View
from .models import Customer, Supplier

from accounts.forms import CustomerRegister, LoginForm, SupplierRegister


def logout(request):
    logout_(request)
    return redirect("/")


# def index(request):
#     return render(request, "index.html")


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
