from djqscsv import render_to_csv_response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.custom_permissions import IsManager
from rest_framework import generics
from rest_framework import status
from utils.restful_response import send_response
from utils.responses import *
from account.models import Account, Transactions
from .utils import CSV_FIELDS_MAP
import ast


class GetTransactionHistoryView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsManager)

    def list(self, request, *args, **kwargs):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            account_id = ast.literal_eval(request.GET.get('account_id'))
            accounts = Account.objects.filter(account_id__in=account_id)
            transactions = Transactions.objects.filter(created_on__range=[start_date, end_date], account__in=accounts).\
                select_related('account', 'account__user').\
                values('account__account_number', 'account__user__first_name', 'transaction_type', 'amount', 'transaction_id')

            return render_to_csv_response(transactions, field_header_map=CSV_FIELDS_MAP)

        except:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                                 ui_message='Bad Data.', status=status.HTTP_400_BAD_REQUEST)
