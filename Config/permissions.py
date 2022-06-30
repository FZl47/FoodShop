from rest_framework.permissions import BasePermission
from Config import exceptions



class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        raise exceptions.NeedLogin()

