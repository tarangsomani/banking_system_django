from django.test import TestCase
from account.api.utils import BankAccountTransactions
from account.models import Account
from faker import Faker
from .factories import AccountFactory


class TestBankAccountTransactions(TestCase):

    # setup class
    def setUp(self) -> None:
        self.account = AccountFactory()

    # Test Case where amount cannot be a string
    def test_bad_input_for_amount(self):
        with self.assertRaises(ValueError):
            BankAccountTransactions('account', Faker().word())

    # Test Case where we used invalid Customer Instance
    def test_invalid_customer_instance(self):
        with self.assertRaises(ValueError):
            BankAccountTransactions('account', Faker().pyint())

    # Test Case during withdrawal - Amount > Balance
    def test_withdrawal_amount_greater_than_balance(self):
        self.account.current_balance = 100000
        self.account.save()
        self.assertFalse(BankAccountTransactions(self.account, 999999).withdraw_amount())

    # Test Case - Amount cannot be negative
    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            account = Account()
            BankAccountTransactions(account, -1)

    # Test Case - Amount cannot be zero
    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            account = Account()
            BankAccountTransactions(account, 0)

    # Test Case - Amount should be greater than minimum amount required for a transaction (min. required amount is 10 here)
    def test_min_amount(self):
        with self.assertRaises(ValueError):
            account = Account()
            BankAccountTransactions(account, 10)

    # Test Case - Amount cannot exceed 99999999
    def test_max_amount(self):
        with self.assertRaises(ValueError):
            account = Account()
            BankAccountTransactions(account, 100000000)

    # Test Case - Balance cannot exceed 99999999
    def test_max_account_balance_exceeded(self):
        with self.assertRaises(ValueError):
            deposit_1 = BankAccountTransactions(self.account, 99999999).deposit_amount()
            deposit_2 = BankAccountTransactions(self.account, 99999).deposit_amount()



