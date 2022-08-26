from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            admin = request.user.admin
            return True
        
        except ObjectDoesNotExist:
            return False

