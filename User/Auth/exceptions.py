from rest_framework.exceptions import APIException
from rest_framework import status
from Public.response import ResponseDict

class NeedLogin(APIException):
    """
        Must login
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = ResponseDict(status_code,message='به حساب خود وارد شوید',error='User is not authenticated')


class TokenExpiredOrInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = ResponseDict(status_code,message='توکن وارد شده منقضی شده یا نامعتبر است',error='Token expired or invalid')