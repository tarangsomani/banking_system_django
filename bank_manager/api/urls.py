from django.urls import path
from .views import GetTransactionHistoryView


urlpatterns = [
    path('transactions', GetTransactionHistoryView.as_view(), name='login'),


]