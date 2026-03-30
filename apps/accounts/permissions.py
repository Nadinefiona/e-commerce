from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class IsVendor(BasePermission):
    message = "Only vendors can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.VENDOR


class IsCustomer(BasePermission):
    message = "Only customers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.CUSTOMER


class IsAdminUser(BasePermission):
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == User.Role.ADMIN or request.user.is_staff)
