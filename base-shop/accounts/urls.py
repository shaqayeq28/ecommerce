from django.urls import path

from .views import logout, Login, SignUpCustomer, SignUpSupplier


urlpatterns = [
    # path('', index, name="index"),
    path('login/', Login.as_view(), name="login"),   # vase form django
    path('logout/', logout, name="logout"),
    path('signup-customer/', SignUpCustomer.as_view(), name="signup_customer"),
    path('signup-supplier/', SignUpSupplier.as_view(), name="signup_supplier"),
]
