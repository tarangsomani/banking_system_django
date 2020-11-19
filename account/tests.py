from django.test import TestCase
from account.api.utils import BankAccountTransactions
from account.models import Customer
from faker import Faker


class TestBankAccountTransactions(TestCase):

    def test_bad_input_for_amount(self):
        with self.assertRaises(ValueError):
            bank = BankAccountTransactions('customer', Faker().word())

    def test_invalid_customer_instance(self):
        with self.assertRaises(ValueError):
            bank = BankAccountTransactions('customer', Faker().pyint())

    def test_withdrawal_amount_greater_than_balance(self):
        pass



