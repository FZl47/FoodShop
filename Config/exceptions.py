from rest_framework.exceptions import APIException
from rest_framework import status
from Config.response import ResponseDict



class NeedLogin(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = ResponseDict(status_code,message='به حساب خود وارد شوید',error='User is not authenticated')

class TokenExpiredOrInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = ResponseDict(status_code,message='توکن وارد شده منقضی شده یا نامعتبر است',error='Token expired or invalid')

class UserNotFoundWithEmail(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code,message='کاربری با این ایمیل یافت نشد',error='User not found with this email')

class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code, message='کاربری با این مشخصات یافت نشد', error='User not found')

class UserAlreadyExsists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = ResponseDict(status_code, message='کاربری با این نام کاربری وجود دارد', error='User is exsists')

class EmailFieldIsEmpty(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='لطفا ایمیل را وارد نمایید',error='Email is empty')

class InvalidCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='کد وارد شده نامعتبر است',error='Invalid Code')

class InvalidEmailOrCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='ایمیل یا کد وارد شده نامعتبر است',error='Invalid Email or Code')

class FieldsIsEmpty(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='لطفا فیلد هارا وارد نمایید',error='Fields is Empty')

class FieldsIsWrong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='لطفا فیلد هارا به درستی وارد نمایید',error='Please enter the fields correctly')

class FormatIsWrong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='لطفا فرمت فیلد هارا به درستی وارد نمایید',error='Please enter the format fields correctly')

class ForbiddenAction(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = ResponseDict(status_code,message='شما دسترسی برای انجام عملیات را ندارید',error='You do not have access to perform operations')

class PasswordsNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='رمز های وارد شده با یکدیگر مغایرت دارند',error='Passwords not match')

class Problem(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ResponseDict(status_code,message='اوه ، مشکلی پیش امده است ...',error='Ohh , There is a Problem')

class ProblemAddToCart(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ResponseDict(status_code,message='مشکلی در اضافه کردن محصول به سبد خرید وجود دارد',error='Cant add to cart')

class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code,message='چیزی یافت نشد',error='Not found')

class OrderNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code,message='سبد خریدی یافت نشد',error='Order not found')

class OrderDetailNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code,message='محصول در سبد خرید یافت نشد',error='Order Detail not found')

class MealNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ResponseDict(status_code,message='غذایی یافت نشد',error='Not found meal')