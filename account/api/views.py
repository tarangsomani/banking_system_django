from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from utils.restful_response import send_response
from utils.responses import *
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer, UserDetailSerializer, TransactionSerializer
from account.models import User, Customer, Transactions
from .custom_permissions import IsManager, IsCustomer
from .utils import BankAccountTransactions
import uuid


class CustomerSignUpAPIView(generics.CreateAPIView):

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user_exists = User.objects.filter(email=email).first()
        if user_exists:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                                 ui_message='User already exists', status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            token = Token.objects.create(user=instance)
            data = dict()
            data['token'] = token.key
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',
                                 data=data, status=status.HTTP_200_OK)

        return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        request_data = request.data
        password = request_data.pop('password')

        try:
            user = self.queryset.get(**request_data)
            auth_token = Token.objects.get(user=user).key

            if not check_password(password, user.password) or (user.user_type != request.data.get('user_type')):
                return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                                     ui_message='Wrong username or password', status=status.HTTP_401_UNAUTHORIZED)

        except:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                                 ui_message='Wrong username or password', status=status.HTTP_401_UNAUTHORIZED)

        user.is_active = True
        user.save()
        data = self.get_serializer(instance=user).data
        data['token'] = auth_token
        return send_response(response_code=RESPONSE_CODES['SUCCESS'],
                             developer_message='Request was successful.', data=data, status=status.HTTP_200_OK)


class CustomerDepositMoneyView(generics.CreateAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)

    def create(self, request, *args, **kwargs):
        customer = request.user.user.customer
        amount = request.data.get('amount')

        # Creating a Transaction History
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            deposit_amount = BankAccountTransactions(customer, amount).deposit_amount()
            instance = serializer.save(customer=customer, transaction_id=uuid.uuid4(), transaction_type=Transactions.CREDIT)
            return send_response(response_code=RESPONSE_CODES['SUCCESS'],
                                 developer_message='Request was successful.', data=serializer.data,
                                 status=status.HTTP_200_OK)

        return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Bad Data.', status=status.HTTP_400_BAD_REQUEST)


class CustomerWithdrawMoneyView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)

    def create(self, request, *args, **kwargs):
        customer = request.user.user.customer
        amount = request.data.get('amount')
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            withdraw_amount = BankAccountTransactions(customer, amount).withdraw_amount()
            if withdraw_amount:
                instance = serializer.save(customer=customer, transaction_id=uuid.uuid4(), transaction_type=Transactions.DEBIT)
                return send_response(response_code=RESPONSE_CODES['SUCCESS'],
                                     developer_message='Request was successful.', data=serializer.data)
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                                 ui_message='Insufficient Balance', status=status.HTTP_200_OK)

        return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Bad Data.', status=status.HTTP_400_BAD_REQUEST)

