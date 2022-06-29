from .response import Response


def UserNotFoundWithEmail():
    return Response(404,message='کاربری با این ایمیل یافت نشد',error='User not found with this email')

def UserNotFound():
    return Response(404, message='کاربری با این مشخصات یافت نشد', error='User not found')

def UserAlreadyExsists():
    return Response(409, message='کاربری با این نام کاربری وجود دارد', error='User is exsists')

def EmailFieldIsEmpty():
    return Response(400,message='لطفا ایمیل را وارد نمایید',error='Email is empty')

def InvalidCode():
    return Response(400,message='کد وارد شده نامعتبر است',error='Invalid Code')

def InvalidEmailOrCode():
    return Response(400,message='ایمیل یا کد وارد شده نامعتبر است',error='Invalid Email or Code')

def FieldsIsEmpty():
    return Response(400,message='لطفا فیلد هارا وارد نمایید',error='Fields is Empty')

def ForbiddenAction():
    return Response(403,message='شما دسترسی برای انجام عملیات را ندارید',error='You do not have access to perform operations')

def PasswordsNotMatch():
    return Response(400,message='رمز های وارد شده با یکدیگر مغایرت دارند',error='Passwords not match')