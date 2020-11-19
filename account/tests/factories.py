import factory
from account.models import User
from rest_framework.authtoken.models import Token
from faker import Factory

faker = Factory.create()

"""
Fixtures for account.models required for test cases with database interactions
"""


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('email', 'first_name', 'last_name', 'user_type')

    email = faker.email()
    first_name = faker.name()
    last_name = faker.name()
    user_type = 'customer'


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'account.Account'
        django_get_or_create = ('account_number', 'account_type', 'current_balance', 'account_id', 'user')

    account_number = '12222211111'
    account_type = 'saving'
    account_id = '212121'
    current_balance = 0
    user = factory.SubFactory(UserFactory)


class TokenFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Token
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
