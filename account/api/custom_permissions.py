from rest_framework.permissions import BasePermission
from account.models import User


class IsManager(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.MANAGER)


class IsCustomer(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.CUSTOMER)