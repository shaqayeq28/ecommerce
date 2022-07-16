from django import forms

from orders.models import Payment


PAYMENT_CHOICES = (
    ('I', 'IdPay'),
    ('C', 'Cash')
)


class CheckOutForm(forms.Form):

    province = forms.CharField(
        label='استان',
        disabled=True,
        required=False
    )
    city = forms.CharField(
        label='شهر',
        disabled=True,
        required=False
    )
    address = forms.CharField(
        label='آدرس',
        disabled=True,
        required=False
    )

    shipment_choice = forms.ChoiceField(choices=Payment.SHIPMENT_TYPE_CHOICES, label='نحوه ارسال', required=True,
                                        widget=forms.Select)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

