from django.test import TestCase
from account.api.utils import BankAccountTransactions
from account.models import Customer
from faker import Faker


class TestBankAccountTransactions(TestCase):

    # Test Case where amount cannot be a string
    def test_bad_input_for_amount(self):
        with self.assertRaises(ValueError):
            bank = BankAccountTransactions('customer', Faker().word())

    # Test Case where we used invalid Customer Instance
    def test_invalid_customer_instance(self):
        with self.assertRaises(ValueError):
            bank = BankAccountTransactions('customer', Faker().pyint())

    def test_withdrawal_amount_greater_than_balance(self):
        pass

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            bank = BankAccountTransactions(customer, -1)

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            bank = BankAccountTransactions(customer, 0)

    def test_min_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            bank = BankAccountTransactions(customer, 10)

    def test_max_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            bank = BankAccountTransactions(customer, 100000000)

    def test_max_account_balance_exceeded(self):
        pass


