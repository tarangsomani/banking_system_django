from django.test import TestCase
from account.api.utils import BankAccountTransactions
from account.models import Customer
from faker import Faker
from .tests.factories.account import CustomerFactory


class TestBankAccountTransactions(TestCase):

    # setup class
    def setUp(self) -> None:
        self.customer = CustomerFactory()

    # Test Case where amount cannot be a string
    def test_bad_input_for_amount(self):
        with self.assertRaises(ValueError):
            BankAccountTransactions('customer', Faker().word())

    # Test Case where we used invalid Customer Instance
    def test_invalid_customer_instance(self):
        with self.assertRaises(ValueError):
            BankAccountTransactions('customer', Faker().pyint())

    # Test Case during withdrawal - Amount > Balance
    def test_withdrawal_amount_greater_than_balance(self):
        self.customer.current_balance = 100000
        self.customer.save()
        self.assertFalse(BankAccountTransactions(self.customer, 999999).withdraw_amount())

    # Test Case - Amount cannot be negative
    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            BankAccountTransactions(customer, -1)

    # Test Case - Amount cannot be zero
    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            BankAccountTransactions(customer, 0)

    # Test Case - Amount should be greater than minimum amount required for a transaction (min. required amount is 10 here)
    def test_min_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            BankAccountTransactions(customer, 10)

    # Test Case - Amount cannot exceed 99999999
    def test_max_amount(self):
        with self.assertRaises(ValueError):
            customer = Customer()
            BankAccountTransactions(customer, 100000000)

    # Test Case - Balance cannot exceed 99999999
    def test_max_account_balance_exceeded(self):
        with self.assertRaises(ValueError):
            deposit_1 = BankAccountTransactions(self.customer, 99999999).deposit_amount()
            deposit_2 = BankAccountTransactions(self.customer, 99999).deposit_amount()



