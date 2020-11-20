from django.urls import path
from .views import LoginAPIView, CustomerSignUpAPIView, CustomerDepositMoneyView, CustomerWithdrawMoneyView, \
    CustomerAccountDetailsView


urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('signup', CustomerSignUpAPIView.as_view(), name='customer_signup'),
    path('customer/deposit', CustomerDepositMoneyView.as_view(), name='customer_deposit'),
    path('customer/withdraw', CustomerWithdrawMoneyView.as_view(), name='customer_withdraw'),
    path('customer/account_details', CustomerAccountDetailsView.as_view(), name='customer_account_details'),

]
