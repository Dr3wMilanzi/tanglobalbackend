from rest_framework import permissions

class IsCompany(permissions.BasePermission):
    """
    Custom permission to only allow company users to perform certain actions.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_company