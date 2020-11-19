from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from django.urls import reverse
from faker import Factory
from .factories.account import UserFactory, CustomerFactory, TokenFactory
import random

factory = APIRequestFactory()
client = APIClient()
faker = Factory.create()


class TestDepositAndWithdrawalAPIs(TestCase):

    def setUp(self) -> None:
        self.customer = CustomerFactory()
        self.token = TokenFactory()

    # Test Case - CustomerDepositMoneyView
    def test_deposit_amount_api(self):
        """
        Performing action on CustomerDepositMoneyView - 2 times
        """
        client.force_authenticate(user=self.customer.user, token=self.token)
        url = reverse('customer_deposit')
        amount_1 = random.randint(10, 50000)
        amount_2 = random.randint(10, 50000)

        request_1 = client.post(url, {'amount': amount_1}, format='json')
        self.customer.refresh_from_db()

        request_2 = client.post(url, {'amount': amount_2}, format='json')
        self.customer.refresh_from_db()

        self.assertEqual(amount_1 + amount_2, self.customer.current_balance)

    # Test Case - CustomerWithdrawMoneyView
    def test_withdraw_amount_api(self):
        """
        Setting up initial balance to 100000
        And then withdrawing amount
        """
        self.customer.current_balance = 100000
        self.customer.save()

        amount = random.randint(10, 100000)
        client.force_authenticate(user=self.customer.user, token=self.token)
        url = reverse('customer_withdraw')
        request = client.post(url, {'amount': amount}, format='json')
        self.customer.refresh_from_db()
        self.assertEqual(100000-amount, self.customer.current_balance)

    # Test Case - Deposit and Withdraw amount simultaneously and check integrity
    def test_deposit_and_withdrawal_api_simultaneously(self):
        deposit_amount_url = reverse('customer_deposit')
        withdraw_amount_url = reverse('customer_withdraw')
        client.force_authenticate(user=self.customer.user, token=self.token)
        request_1 = client.post(deposit_amount_url, {'amount': 500}, format='json')
        self.customer.refresh_from_db()

        request_2 = client.post(deposit_amount_url, {'amount': 1000}, format='json')
        self.customer.refresh_from_db()

        request_3 = client.post(withdraw_amount_url, {'amount': 400}, format='json')
        self.customer.refresh_from_db()

        self.assertEqual(1100, self.customer.current_balance)
