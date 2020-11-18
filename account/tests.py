from django.test import TestCase
from account.utils import BankAccountTransactions
from account.models import Customer


class TestBankAccountTransactions(TestCase):

    def test_bad_input_for_amount(self):

        with self.assertRaises(ValueError):
            bank = BankAccountTransactions('customer', 'abc')

