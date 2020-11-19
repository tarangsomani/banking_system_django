from account.models import User, Account
from decimal import Decimal


class BankAccountTransactions():
    def __init__(self, account, amount):
        try:
            self.amount = Decimal(amount)
            if self.amount <= 10:
                raise ValueError('Negative/Zero Values not allowed')
            if self.amount > 99999999.99:
                raise ValueError('Max Value exceeded')
        except:
            raise ValueError('Bad input for amount')

        self.account = account
        if not isinstance(account, Account):
            raise ValueError('')

    def deposit_amount(self):

        account = self.account
        amount = self.amount
        new_balance = account.current_balance + amount
        if new_balance > 99999999.99:
            raise ValueError('Max Value exceeded')

        account.current_balance += amount
        account.save()
        return True

    def withdraw_amount(self):
        # Add a check for min amount while withdrawal
        account = self.account
        amount = self.amount

        current_balance = account.current_balance

        if current_balance >= amount:
            account.current_balance -= amount
            account.save()
            return True
        return False

