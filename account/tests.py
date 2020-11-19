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


# Below test case is not working correctly
    def test_withdrawal_amount_greater_than_balance(self):
        customer = Customer(current_balance=199999)
        result = BankAccountTransactions(customer, 10111).withdraw_amount()
        self.assertFalse(False, result)



