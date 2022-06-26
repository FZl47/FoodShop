from rest_framework.exceptions import APIException
from rest_framework import status


class NeedLogin(APIException):
    """
        Must login
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = {
        'status_code':'401',
        'error': 'User is not authenticated',
        'message':  'به حساب خود وارد شوید'
    }


class TokenExpiredOrInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = {
        'status_code': '401',
        'error': 'Token expired or invalid',
        'message': 'توکن وارد شده منقضی شده یا نامعتبر است'
    }