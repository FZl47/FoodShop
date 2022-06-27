from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from Public.response import Response


class ResetPassword(APIView):
    def post(self, request):
        # Must Complete ...

        # Response info
        status_code = None
        error_response = ''
        message_response = ''

        data = request.data
        email = data.get('email')
        if email:
            subject = 'Welcome Fazel'
            message = f'Hi , thank you for registering in Food Shop.'
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                status_code = 200
            except:
                status_code = 500
                error_response = 'There is a problem sending the email'
                message_response = 'مشکلی در ارسال ایمیل وجود دارد لطفا بعدا مجددا امتحان کنید'
        else:
            status_code = 204
            error_response = 'Email is empty'
            message_response = 'لطفا ایمیل را به درستی وارد نمایید'

        return Response(status_code,error_response,message_response)
