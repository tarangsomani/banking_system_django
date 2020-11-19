from account.models import User, Customer


class BankAccountTransactions():
    def __init__(self, customer, amount):
        try:
            self.amount = int(amount)
        except:
            raise ValueError('Bad input for amount')

        self.customer = customer
        if not isinstance(customer, Customer):
            raise ValueError('')

    def deposit_amount(self):
        customer = self.customer
        amount = self.amount
        customer.current_balance += amount
        customer.save()
        return True

    def withdraw_amount(self):
        # Add a check for min amount while withdrawal
        customer = self.customer
        amount = self.amount
        print(customer.current_balance, amount)

        current_balance = customer.current_balance

        if current_balance >= amount:
            customer.current_balance -= amount
            customer.save()
            return True
        return False

