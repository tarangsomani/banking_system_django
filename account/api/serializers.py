from rest_framework import serializers
from account.models import User, Customer, Transactions
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    account_type = serializers.ChoiceField(choices=Customer.ACCOUNT_TYPE)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'account_type')

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        account_type = validated_data.pop('account_type')
        instance = User.objects.create(**validated_data, password=password, user_type=User.CUSTOMER,
                                       username=validated_data.get('email'))
        Customer.objects.create(user=instance, account_number=get_random_string(length=16, allowed_chars='1234567890'),
                                customer_id=uuid.uuid4(), account_type=account_type)
        return instance


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('account_number', 'account_type', 'current_balance')


class TransactionSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.CharField(required=False)

    class Meta:
        model = Transactions
        fields = ('transaction_type', 'amount', 'transaction_id')
