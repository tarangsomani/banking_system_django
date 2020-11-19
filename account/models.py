from django.db import models
from django.db import IntegrityError
from utils.models import TimeStampedModel
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser, TimeStampedModel):

    """
    Assumption: - 2 Types of Users
                - 10 Digit Mobile Number (India) [should be mandatory if required to send SMS, etc.
                -
    """

    MANAGER = 'manager'
    CUSTOMER = 'customer'

    USER_TYPE = (
        (MANAGER, 'manager'),
        (CUSTOMER, 'customer')
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default=CUSTOMER)
    mobile = models.CharField(max_length=10, null=True)
    branch_name = models.CharField(max_length=255, null=True)


class Customer(TimeStampedModel):
    SAVING = 'saving'
    CURRENT = 'current'

    ACCOUNT_TYPE = (
        (SAVING, 'saving'),
        (CURRENT, 'current')
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer')
    customer_id = models.CharField(unique=True, max_length=20)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE, default=SAVING)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transactions(TimeStampedModel):
    CREDIT = 'credit'
    DEBIT = 'debit'

    TRANSACTION_TYPE = (
        (CREDIT, 'credit'),
        (DEBIT, 'debit')
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_id = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Transactions, self).save(*args, **kwargs)
        else:
            raise IntegrityError('This model instance cannot be updated')
