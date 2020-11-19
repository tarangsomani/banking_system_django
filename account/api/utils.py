from account.models import User, Customer
from decimal import Decimal


class BankAccountTransactions():
    def __init__(self, customer, amount):
        try:
            self.amount = Decimal(amount)
            if self.amount <= 10:
                raise ValueError('Negative/Zero Values not allowed')
            if self.amount > 99999999.99:
                raise ValueError('Max Value exceeded')
        except:
            raise ValueError('Bad input for amount')

        self.customer = customer
        if not isinstance(customer, Customer):
            raise ValueError('')

    def deposit_amount(self):

        customer = self.customer
        amount = self.amount
        new_balance = customer.current_balance + amount
        if new_balance > 99999999.99:
            raise ValueError('Max Value exceeded')

        customer.current_balance += amount
        customer.save()
        return True

    def withdraw_amount(self):
        # Add a check for min amount while withdrawal
        customer = self.customer
        amount = self.amount

        current_balance = customer.current_balance

        if current_balance >= amount:
            customer.current_balance -= amount
            customer.save()
            return True
        return False

