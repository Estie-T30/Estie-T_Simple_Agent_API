from rest_framework import permissions
from .models import Appointment

class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permissions to only allow owners of a house to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
       
        return obj.owner == request.user
    
class IsTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tenant

class IsAppointmentOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner(tenant) of an appointment to access it
    """

    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user
    
class IsAdminOrAgent(permissions.BasePermission):
    """
    Allows access only to admin users or agents.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_agent)
        )