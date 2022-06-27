from rest_framework.exceptions import APIException
from rest_framework import status
from Public.response import ResponseDict

class NeedLogin(APIException):
    """
        Must login
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = ResponseDict(status_code,'User is not authenticated','به حساب خود وارد شوید')


class TokenExpiredOrInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = ResponseDict(status_code,'Token expired or invalid','توکن وارد شده منقضی شده یا نامعتبر است')