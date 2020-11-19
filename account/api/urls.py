from django.urls import path
from .views import LoginAPIView, CustomerSignUpAPIView, CustomerDepositMoneyView


urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('signup', CustomerSignUpAPIView.as_view(), name='customer_signup'),
    path('customer/deposit', CustomerDepositMoneyView.as_view(), name='customer_signup'),

]
