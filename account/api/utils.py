from account.models import Customer


class BankAccountTransactions():
    def __init__(self, customer, amount):
        try:
            self.amount = int(amount)
        except:
            raise ValueError('Bad input for amount')
        self.customer = customer

    @classmethod
    def deposit_amount(cls):
        customer = cls.customer
        amount = cls.amount
        try:
            customer.current_balance += int(amount)
            customer.save()
            return True
        except ValueError:
            raise ValueError

    @classmethod
    def withdraw_amount(cls):
        # Add a check for min amount while withdrawal
        customer = cls.customer
        amount = cls.amount

        current_balance = customer.current_balance
        try:
            amount = int(amount)
        except ValueError:
            raise ValueError

        if current_balance >= amount:
            customer.current_balance -= amount
            customer.save()
            return True
        return False
