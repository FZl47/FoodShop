from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from Config import task
from Config import redis_py
from Config import tools
from Public.response import Response
from Public import response_exceptions

_loop = task.Loop()


def get_user_by_email(email):
    User = get_user_model()
    try:
        return User.objects.get(email=email)
    except:
        return None

class ResetPasswordGetCode(APIView):
    """
        Get fields = [email]
    """

    def resetCode(self,email):
        code = tools.RandomString(5)
        email = f"Email_Reset_{email}"
        # After 5 minutes code will delete
        redis_py.set_value_expire(email,code,299)
        return code

    def _send_email_target(self,email):
        code = self.resetCode(email)
        subject = 'Food Shop - Reset Password'
        template_html = get_template('email_template.html')
        context = {'code': code}
        content_html = template_html.render(context)
        _email = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
        _email.attach_alternative(content_html, "text/html")
        _email.send()

    def post(self, request):

        # Response info
        status_code = None
        error_response = ''
        message_response = ''

        data = request.data
        email = data.get('email')
        if email:
            user = get_user_by_email(email)
            if user:
                # Checking the code has been sended or not
                code_is_sended = False if redis_py.get_value(f"Email_Reset_{email}") == None else True
                if not code_is_sended:
                    # Add task to loop for run in background
                    t = task.Task(self._send_email_target,args=(email,))
                    _loop.add(t)
                    _loop.start_thread()
                    status_code = 200
                    message_response = 'کد بازیابی به ایمیل شما ارسال شد'
                    data_response = {
                        'email':email
                    }
                else:
                    status_code = 226
                    message_response = 'کد بازیابی به ایمیل شما ارسال شده است'
                    data_response = {
                        'email': email
                    }
            else:
                return response_exceptions.UserNotFoundWithEmail()
        else:
            return response_exceptions.EmailFieldIsEmpty()

        return Response(status_code,data_response,message=message_response,error=error_response)


class ResetPasswordValidateCode(APIView):
    """
            Get fields = [email, code]
    """

    def post(self,request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''

        data = request.data
        email = data.get('email')
        code_get = data.get('code')

        if email and code_get:
            user = get_user_by_email(email)
            if user:
                code_sened = redis_py.get_value(f"Email_Reset_{email}")
                if (code_sened) and (code_sened == code_get):
                    # Set 5 minutes for access to submit new password
                    redis_py.set_value_expire(f"Email_Reset_{email}_Code_{code_get}",'True',299)
                    redis_py.remove_key(f"Email_Reset_{email}")
                    status_code = 200
                    data_response = {
                        'email': email,
                        'code':code_get
                    }
                else:
                    return response_exceptions.InvalidCode()
            else:
                return response_exceptions.UserNotFoundWithEmail()
        else:
            return response_exceptions.InvalidEmailOrCode()
        return Response(status_code, data_response, message=message_response, error=error_response)

class ResetPasswordSetPassword(APIView):
    """
        Get fields = [email, code, password, password2]
    """

    def post(self,request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''
        data_response = {}

        data = request.data
        email = data.get('email')
        code_get = data.get('code')
        password_1 = data.get('password')
        password_2 = data.get('password2')

        if email and code_get and password_1 and password_1:
            user = get_user_by_email(email)
            if user:
                access_to_set_password = True if redis_py.get_value(f"Email_Reset_{email}_Code_{code_get}") != None else False
                if access_to_set_password:
                    if password_1 == password_2:
                        user.set_password(password_1)
                        user.save()
                        status_code = 200
                        message_response = 'رمز جدید شما با موفقیت ساخته شد'
                        redis_py.remove_key(f"Email_Reset_{email}_Code_{code_get}")
                    else:
                        return response_exceptions.PasswordsNotMatch()
                else:
                    return response_exceptions.ForbiddenAction()
            else:
                return response_exceptions.UserNotFoundWithEmail()
        else:
            return response_exceptions.FieldsIsEmpty()
        return Response(status_code, data_response, message=message_response, error=error_response)