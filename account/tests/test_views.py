from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from django.urls import reverse
from faker import Factory
from .factories import UserFactory, AccountFactory, TokenFactory
import random
import json
from decimal import Decimal

factory = APIRequestFactory()
client = APIClient()
faker = Factory.create()


class TestTransactionAPIs(TestCase):

    def setUp(self) -> None:
        self.account = AccountFactory()
        self.token = TokenFactory()

    # Test Case - CustomerDepositMoneyView
    def test_deposit_amount_view(self):
        """
        Performing action on CustomerDepositMoneyView - 2 times
        """
        client.force_authenticate(user=self.account.user, token=self.token)
        url = reverse('customer_deposit')
        amount_1 = random.randint(10, 50000)
        amount_2 = random.randint(10, 50000)

        request_1 = client.post(url, {'amount': amount_1}, format='json')
        self.account.refresh_from_db()

        request_2 = client.post(url, {'amount': amount_2}, format='json')
        self.account.refresh_from_db()

        self.assertEqual(amount_1 + amount_2, self.account.current_balance)

    # Test Case - CustomerDepositMoneyView with negative amount
    def test_deposit_amount_view_with_negative_amount(self):
        client.force_authenticate(user=self.account.user, token=self.token)
        url = reverse('customer_deposit')

        request = client.post(url, {'amount': -500}, format='json')
        self.assertEqual(400, request.status_code)

    # Test Case - CustomerWithdrawMoneyView
    def test_withdraw_amount_view(self):
        """
        Setting up initial balance to 100000
        And then withdrawing amount
        """
        self.account.current_balance = 100000
        self.account.save()

        amount = random.randint(10, 100000)
        client.force_authenticate(user=self.account.user, token=self.token)
        url = reverse('customer_withdraw')
        request = client.post(url, {'amount': amount}, format='json')
        self.account.refresh_from_db()
        self.assertEqual(100000-amount, self.account.current_balance)

    # Test Case - CustomerWithdrawMoneyView with negative amount
    def test_withdraw_amount_view_with_negative_amount(self):
        """
        Setting up initial balance to 100000
        And then withdrawing amount
        """
        self.account.current_balance = 100000
        self.account.save()

        client.force_authenticate(user=self.account.user, token=self.token)
        url = reverse('customer_withdraw')
        request = client.post(url, {'amount': -100}, format='json')
        self.assertEqual(400, request.status_code)

    # Test Case - CustomerWithdrawMoneyView with invalid amount (string, etc.)
    def test_withdraw_amount_view_with_bad_input_for_amount(self):
        pass

    # Test Case - Deposit and Withdraw amount simultaneously and check integrity
    def test_deposit_and_withdrawal_views_simultaneously(self):
        deposit_amount_url = reverse('customer_deposit')
        withdraw_amount_url = reverse('customer_withdraw')
        client.force_authenticate(user=self.account.user, token=self.token)
        request_1 = client.post(deposit_amount_url, {'amount': 500}, format='json')
        self.account.refresh_from_db()

        request_2 = client.post(deposit_amount_url, {'amount': 1000}, format='json')
        self.account.refresh_from_db()

        request_3 = client.post(withdraw_amount_url, {'amount': 400}, format='json')
        self.account.refresh_from_db()

        self.assertEqual(1100, self.account.current_balance)

    # Test Case for CustomerAccountDetailsView
    def test_account_details_view(self):
        account_details_url = reverse('customer_account_details')
        account = self.account
        client.force_authenticate(user=account.user, token=self.token)
        request = client.get(account_details_url)
        self.assertEqual(200, request.status_code)

