from rest_framework import serializers
from account.models import User, Account, Transactions
import uuid
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    account_type = serializers.ChoiceField(choices=Account.ACCOUNT_TYPE)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'account_type')

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        account_type = validated_data.pop('account_type')
        instance = User.objects.create(**validated_data, password=password, user_type=User.CUSTOMER,
                                       username=validated_data.get('email'))

        """
        - Generating the related Account for user.
        - Account Number is a random string here but in actual application it would be based on some logic and also there
          would be a criteria for its uniqueness as random string may cause collisions
        - Account ID would be used in API calls to avoid using Account Number or Primary Keys (to avoid API Leakage)
        """

        Account.objects.create(user=instance, account_number=get_random_string(length=16, allowed_chars='1234567890'),
                               account_id=uuid.uuid4(), account_type=account_type)
        return instance


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('account_number', 'account_type', 'current_balance', 'account_id')


class TransactionSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.CharField(required=False)

    class Meta:
        model = Transactions
        fields = ('transaction_type', 'amount', 'transaction_id')
