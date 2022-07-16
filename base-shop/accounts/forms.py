from django.core.validators import RegexValidator
from django.forms import PasswordInput
from django import forms
from django.core import validators

from .models import User


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


class ProfileForm(forms.Form):
    phone = forms.CharField(
        label='تلفن همراه',
        validators=[RegexValidator(r'^09\d{9}$')],
        required=True,
        max_length=11
    )

    first_name = forms.CharField(
        label='نام',
        max_length=255
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=255
    )

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    job = forms.CharField(label='شغل', max_length=255)


class AddressForm(forms.Form):

    province = forms.CharField(
        label='استان',

    )
    city = forms.CharField(
        label='شهر',
    )
    address = forms.CharField(

        label='آدرس',
    )


class RestPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if user:
            self.cleaned_data["user"] = user
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError("user not found")


class ForgetPassForm(forms.Form):
    password = forms.CharField(max_length=16, widget=PasswordInput(
        attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید', 'type': 'password', 'required': '',
               'class': 'e-field-inner'}), label=' رمزعبور')
    re_password = forms.CharField(widget=PasswordInput(
        attrs={'placeholder': 'لطفا کلمه عبور خود را تکرار نمایید', 'type': 'password', 'required': '',
               'class': 'e-field-inner'}), label='تکرار رمزعبور')
    fields = ['password', "re_password"]
    widgets = {
        'password': PasswordInput(
            attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید', 'type': 'password', 'required': '',
                   'class': 'e-field-inner', "id": "password"}),
    }
    labels = {
        'password': ('رمزعبور'),
        're_password': 'تکرار رمزعبور',
    }
    validators = {
    }

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')
        return password


class ResetPasswordProfile(forms.Form):

    password1 = forms.CharField(max_length=100)

    password2 = forms.CharField(max_length=100)

    def clean_re_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')
        return password1
