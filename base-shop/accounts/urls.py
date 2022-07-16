from django.urls import path

from .views import logout, Login, SignUpCustomer, SignUpSupplier, \
    ProfileFormShow, AddressFormShow, ForgetPassword, \
    WaitingForVerify, PasswordReset, \
    ResetPasswordProfileFormShow, OrderHistoryShow, OrderDetailHistoryShow

urlpatterns = [
    # path('', index, name="index"),
    path('login/', Login.as_view(), name="login"),   # vase form django
    path('logout/', logout, name="logout"),
    path('signup-customer/', SignUpCustomer.as_view(), name="signup_customer"),
    path('signup-supplier/', SignUpSupplier.as_view(), name="signup_supplier"),
    path('profile/', ProfileFormShow.as_view(), name="profile"),
    path('address/', AddressFormShow.as_view(), name="address"),
    path('forget_password/', ForgetPassword.as_view(), name="forget_password"),
    path('verify/', WaitingForVerify.as_view(), name='verify'),
    path('passwordreset/', PasswordReset.as_view(), name='passwordresest'),
    path('reset_password_profile/', ResetPasswordProfileFormShow.as_view(), name='reset_password_profile'),
    path('history/', OrderHistoryShow.as_view(), name="history"),
    path('detail-history/<int:order_id>', OrderDetailHistoryShow.as_view(), name="detail-history"),
]
