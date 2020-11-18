from account.models import Customer


def deposit_amount(customer, amount):
    try:
        customer.current_balance += int(amount)
        customer.save()
        return True
    except ValueError:
        raise ValueError


def withdraw_amount(customer, amount):
    # Add a check for min amount while withdrawal

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
