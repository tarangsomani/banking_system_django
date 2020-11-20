from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from utils.restful_response import send_response
from utils.responses import *
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer, UserDetailSerializer, TransactionSerializer, AccountSerializer
from account.models import User, Account, Transactions
from utils.custom_permissions import IsManager, IsCustomer
from .utils import BankAccountTransactions
from utils.sendgrid_integration import SendGridService
import uuid
from django.db import transaction
from .constant import CREDIT_AMOUNT_EMAIL_BODY, DEBIT_AMOUNT_EMAIL_BODY


class CustomerSignUpAPIView(generics.CreateAPIView):
    """
    Not allowing Users (Managers) to sign up using this as there would be some other functionality for Manager Account.
    """

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                                 developer_message='Request failed.', ui_message='User already exists')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            token = Token.objects.create(user=instance)
            data = dict()
            data['token'] = token.key
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',
                                 data=data, status=status.HTTP_200_OK)

        return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                             developer_message='Request failed.', ui_message='Invalid data', error=serializer.errors)


class LoginAPIView(generics.UpdateAPIView):

    """
    Same Login View for Customers and Managers. But in actual application it would be different views
    based on the requirement.
    """
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        request_data = request.data
        password = request_data.pop('password')

        try:
            user = self.queryset.get(**request_data)
            auth_token = Token.objects.get(user=user).key

            if not check_password(password, user.password) or (user.user_type != request.data.get('user_type')):
                return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_401_UNAUTHORIZED,
                                     developer_message='Request failed.', ui_message='Wrong username or password')

        except:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_401_UNAUTHORIZED,
                                 developer_message='Request failed.', ui_message='Wrong username or password')

        user.is_active = True
        user.save()
        data = self.get_serializer(instance=user).data
        data['token'] = auth_token
        return send_response(response_code=RESPONSE_CODES['SUCCESS'], status=status.HTTP_200_OK,
                             developer_message='Request was successful.', data=data)


class CustomerDepositMoneyView(generics.CreateAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)

    # Atomic Transaction
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user.user
        # Acquiring the lock on the related account to avoid concurrency
        account = Account.objects.select_for_update().get(user=user)
        amount = request.data.get('amount')

        # Creating a Transaction History
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                deposit_amount = BankAccountTransactions(account, amount).deposit_amount()
            except:
                return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                                     developer_message='Request failed.',
                                     ui_message='Max Value for Account Balance Exceeded!')
            instance = serializer.save(account=account, transaction_id=uuid.uuid4(), transaction_type=Transactions.CREDIT)

            # Sending Transaction Email using Sendgrid
            send_mail = SendGridService().send_mail(receiver=user.email, subject="CREDIT",
                                                    content=CREDIT_AMOUNT_EMAIL_BODY % (amount, account.current_balance))
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], status=status.HTTP_200_OK,
                                 developer_message='Request was successful.', data=serializer.data)

        return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                             developer_message='Request failed.', ui_message='Bad Data.')


class CustomerWithdrawMoneyView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user.user
        # Acquiring the lock on the related account to avoid concurrency
        account = Account.objects.select_for_update().get(user=user)
        amount = request.data.get('amount')
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                withdraw_amount = BankAccountTransactions(account, amount).withdraw_amount()
            except:
                return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                                     developer_message='Request failed.',
                                     ui_message='Negative Amount not allowed')
            if withdraw_amount:
                instance = serializer.save(account=account, transaction_id=uuid.uuid4(), transaction_type=Transactions.DEBIT)
                # Sending Transaction Email using Sendgrid
                send_mail = SendGridService().send_mail(receiver=user.email, subject="DEBIT",
                                                        content=DEBIT_AMOUNT_EMAIL_BODY %
                                                        (amount, account.current_balance))
                return send_response(response_code=RESPONSE_CODES['SUCCESS'], status=status.HTTP_200_OK,
                                     developer_message='Request was successful.', data=serializer.data)

            return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_200_OK,
                                 developer_message='Request failed.', ui_message='Insufficient Balance')

        return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                             developer_message='Request failed.', ui_message='Bad Data.')


class CustomerAccountDetailsView(generics.RetrieveAPIView):

    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsCustomer)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.user.user
            instance = Account.objects.get(user=user)
        except:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], status=status.HTTP_400_BAD_REQUEST,
                                 developer_message='Request failed.',
                                 ui_message='The user_id you\'re trying to access does not exist')

        serializer = self.get_serializer(instance)
        return send_response(response_code=RESPONSE_CODES['SUCCESS'], status=status.HTTP_200_OK,
                             developer_message='Request was successful.', data=serializer.data)

