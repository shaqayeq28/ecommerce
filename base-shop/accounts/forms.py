from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import User, Customer, Supplier
from django import forms
from django.core import validators


class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')


class CustomerRegister(forms.Form):

    phone = forms.CharField(
        label='تلفن همراه',
        validators=[RegexValidator(r'^09\d{9}$')],
        required=True,
        max_length=11
    )

    email = forms.CharField(
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password = forms.CharField(widget=forms.PasswordInput,
                               label='کلمه ی عبور'
    )

    re_password = forms.CharField(widget=forms.PasswordInput,
                                  label='تکرار کلمه ی عبور'
    )

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(password)
        print(re_password)

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')
        return email


class SupplierRegister(forms.Form):

    phone = forms.CharField(
        label='تلفن همراه',
        validators=[RegexValidator(r'^09\d{9}$')],
        required=True,
        max_length=11
    )

    email = forms.CharField(
        label='ایمیل',
        validators=[validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')]
    )

    password = forms.CharField(widget=forms.PasswordInput,
                               label='کلمه ی عبور'
    )

    re_password = forms.CharField(widget=forms.PasswordInput,
                                  label='تکرار کلمه ی عبور'
    )

    company_name = forms.CharField(
        label='نام شرکت'
    )

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(password)
        print(re_password)

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')
        return email
