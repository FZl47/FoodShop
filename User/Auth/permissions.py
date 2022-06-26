from rest_framework.permissions import BasePermission
from .exceptions import NeedLogin



class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        raise NeedLogin()

