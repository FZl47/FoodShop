from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Config.permissions import IsAuthenticated
from Config import task
from Config import redis_py
from Config import tools
from Config.response import Response
from Config import exceptions
from Food import serializers as FoodSerializers
from .models import OrderDetail, Address
from . import serializers

_loop = task.Loop()


def get_user_by_email(email):
    User = get_user_model()
    try:
        return User.objects.get(email=email)
    except:
        return None


def get_user_by_email_password(email, password):
    try:
        User = get_user_model()
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
        return None
    except:
        return None


def create_tokens_jwt(user):
    refresh_token = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh_token),
        'access_token': str(refresh_token.access_token)
    }


class GetAccessToken(APIView):
    """
          Get fields = [refresh]
          Auth = False
    """

    def post(self, request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''
        data_response = {}

        data = request.data
        refresh = data.get('refresh')
        if refresh:
            try:
                access = RefreshToken(refresh).access_token
                if access:
                    status_code = 200
                    data_response['access'] = str(access)
            except:
                raise exceptions.TokenExpiredOrInvalid
        else:
            raise exceptions.TokenExpiredOrInvalid
        return Response(status_code, data_response, message=message_response, error=error_response)


class LoginUser(APIView):
    """
        Get fields = [email, password]
        Auth = False
    """

    def post(self, request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''
        data_response = {}

        data = request.data
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = get_user_by_email_password(email, password)
            if user:
                data_response = create_tokens_jwt(user)
                status_code = 200
                message_response = 'WelCome'
            else:
                raise exceptions.UserNotFound
        else:
            raise exceptions.FieldsIsEmpty

        return Response(status_code, data_response, message=message_response, error=error_response)


class RegisterUser(APIView):
    """
            Get fields = [email, password, password2]
            Auth = False
    """

    def post(self, request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''
        data_response = {}

        data = request.data
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        if email and password and password2:
            if password == password2:
                user = get_user_by_email(email)
                if not user:
                    user = get_user_model().objects.create(email=email)
                    user.set_password(password)
                    data_response = create_tokens_jwt(user)
                    status_code = 200
                    message_response = 'Your account created successfuly'
                else:
                    raise exceptions.UserAlreadyExsists
            else:
                raise exceptions.PasswordsNotMatch
        else:
            raise exceptions.FieldsIsEmpty

        return Response(status_code, data_response, message=message_response, error=error_response)


class ResetPasswordGetCode(APIView):
    """
        Get fields = [email]
        Auth = False
    """

    def resetCode(self, email):
        code = tools.RandomString(5)
        email = f"Email_Reset_{email}"
        # After 5 minutes code will delete
        redis_py.set_value_expire(email, code, 299)
        return code

    def _send_email_target(self, email):
        code = self.resetCode(email)
        subject = 'Pizzle - Reset Password'
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
        data_response = {}

        data = request.data
        email = data.get('email')
        if email:
            user = get_user_by_email(email)
            if user:
                # Checking the code has been sended or not
                code_is_sended = False if redis_py.get_value(f"Email_Reset_{email}") == None else True
                if not code_is_sended:
                    # Add task to loop for run in background
                    t = task.Task(self._send_email_target, args=(email,))
                    _loop.add(t)
                    _loop.start_thread()
                    status_code = 200
                    message_response = 'The recovery code has been sent to your email'
                    data_response = {
                        'email': email
                    }
                else:
                    status_code = 226
                    message_response = 'The recovery code has been sended to your email'
                    data_response = {
                        'email': email
                    }
            else:
                raise exceptions.UserNotFoundWithEmail
        else:
            raise exceptions.EmailFieldIsEmpty
        return Response(status_code, data_response, message=message_response, error=error_response)


class ResetPasswordValidateCode(APIView):
    """
            Get fields = [email, code]
            Auth = False
    """

    def post(self, request):
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
                    redis_py.set_value_expire(f"Email_Reset_{email}_Code_{code_get}", 'True', 299)
                    redis_py.remove_key(f"Email_Reset_{email}")
                    status_code = 200
                    data_response = {
                        'email': email,
                        'code': code_get
                    }
                else:
                    raise exceptions.InvalidCode
            else:
                raise exceptions.UserNotFoundWithEmail
        else:
            raise exceptions.InvalidEmailOrCode
        return Response(status_code, data_response, message=message_response, error=error_response)


class ResetPasswordSetPassword(APIView):
    """
        Get fields = [email, code, password, password2]
        Auth = False
    """

    def post(self, request):
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
                access_to_set_password = True if redis_py.get_value(
                    f"Email_Reset_{email}_Code_{code_get}") != None else False
                if access_to_set_password:
                    if password_1 == password_2:
                        user.set_password(password_1)
                        user.save()
                        status_code = 200
                        message_response = 'Your new password has been created successfully'
                        redis_py.remove_key(f"Email_Reset_{email}_Code_{code_get}")
                    else:
                        raise exceptions.PasswordsNotMatch
                else:
                    raise exceptions.ForbiddenAction
            else:
                raise exceptions.UserNotFoundWithEmail
        else:
            raise exceptions.FieldsIsEmpty
        return Response(status_code, data_response, message=message_response, error=error_response)


class AddToCart(APIView):
    """
        Get fields = [
        slug,
        count=optional : Default 1
        ]
        Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Response info
        status_code = None
        error_response = ''
        message_response = ''
        data_response = {}

        data = request.data
        slug = data.get('slug') or ''
        count = data.get('count') or 1
        added_to_cart = request.user.add_to_cart(slug, count)
        if added_to_cart:
            status_code = 200
            message_response = 'Added to cart successfuly'
        else:
            raise exceptions.ProblemAddToCart()
        return Response(status_code, data_response, message_response, error_response)


class GetCart(APIView):
    """
        Get fields = []
        Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}
        user = request.user
        order = user.get_order_active()
        if order:
            order = serializers.OrderSerializer(order)
            user_data = serializers.UserSerializer(user).data
            data_response = {
                'user': user_data,
                'order': order
            }
        else:
            raise exceptions.OrderNotFound
        return Response(200, data_response)


class GetUser(APIView):
    """
            Get fields = []
            Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}
        user = request.user
        if user.is_authenticated:
            data_response = {
                'user': serializers.UserBasicSerializer(user).data
            }
            return Response(200, data_response)
        raise exceptions.UserNotFound()


class DeleteOrderDetail(APIView):
    """
          Get fields = [
                id : id is orderdetail id,
          ]
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}
        data = request.data
        orderdetail_id = data.get('id')
        user = request.user
        order = user.get_order_active()
        try:
            orderdetail = OrderDetail.objects.get(id=orderdetail_id, order=order)
            orderdetail.delete()
            data_response = {
                'order': serializers.OrderBasicSerializer(order),
            }
        except:
            raise exceptions.OrderDetailNotFound
        return Response(200, data_response)


class DeleteAllOrderDetail(APIView):
    """
          Get fields = []
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        order = user.get_order_active()
        if order:
            order.clear_order()
        else:
            raise exceptions.OrderNotFound
        return Response(200)


class ChangeCountOrderDetail(APIView):
    """
        Get fields = [
            id : id is orderdetail id,
            count
        ]
        Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}

        data = request.data
        orderdetail_id = str(data.get('id'))
        count = str(data.get('count'))
        user = request.user
        if orderdetail_id and count and count.isdigit() and orderdetail_id.isdigit():
            order = user.get_order_active()
            if order:
                try:
                    orderdetail = OrderDetail.objects.get(id=orderdetail_id, order=order)
                    meal_stock = orderdetail.meal.stock
                    if 0 < int(count) <= meal_stock:
                        orderdetail.count = count
                        orderdetail.save()
                        data_response = {
                            'id': orderdetail_id,
                            'count': count,
                            'price_detail': orderdetail.get_price(),
                            'order': serializers.OrderBasicSerializer(order)
                        }
                    else:
                        raise exceptions.FieldsIsWrong
                except:
                    raise exceptions.OrderDetailNotFound
            else:
                raise exceptions.OrderNotFound
        else:
            raise exceptions.FieldsIsWrong

        return Response(200, data_response)


class GetDashboardInfo(APIView):
    """
          Get fields = []
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}

        user = request.user
        data_response = {
            'user': serializers.UserBasicSerializer(user).data,
            'address': serializers.AddressSerializer(user.get_address()),
            'orders': serializers.OrderDashboardSerializer(user.get_orders()),
            'comments': FoodSerializers.CommentFullSerializer(user.get_comments(), many=True).data,
            'notifications': serializers.NotificationSerializer(user.get_notifications(), many=True).data,
            'lastvisits': serializers.VisitSerializer(user.get_visits(), many=True).data[:8]
        }
        return Response(200, data_response)


class PaymentOrder(APIView):
    """
          Get fields = [
                address_id,
                description=optional
          ]
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        data = request.data
        address_id = data.get('address_id') or 0
        description_order = data.get('description') or ''
        user = request.user
        order_active = user.get_order_active()
        if address_id and str(address_id).isdigit():
            address = user.address_set.filter(id=address_id).first()
            if address:
                if order_active:
                    if order_active.order_is_not_empty():
                        if order_active.is_available():
                            for detail in order_active.get_details():
                                detail.payment_orderdetail()
                            order_active.description = description_order
                            order_active.is_paid = True
                            order_active.time_pay = tools.GetDateTime()
                            order_active.status_order = order_active.STATUS_ORDER[1][0]
                            order_active.address = address
                            total = float(order_active.get_price_meals()) + float(address.cost)
                            order_active.detail = f"""
                                address : {address.address} -
                                address cost : {address.cost} -
                                address postal code :{address.postal_code}
                                details count : {order_active.get_details().count()} -
                                Total : {total}
                            """
                            order_active.price_paid = total
                            order_active.save()
                        else:
                            raise exceptions.OrderDetailNotFound
                    else:
                        raise exceptions.OrderIsEmpty
                else:
                    raise exceptions.OrderNotFound
            else:
                raise exceptions.AddressNotFound
        else:
            raise exceptions.FieldsIsWrong
        return Response(200)


class AddAddress(APIView):
    """
          Get fields = [
                address : address is text address,
                postalcode,
          ]
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}

        data = request.data
        user = request.user
        address_text = data.get('address') or ''
        postalcode = data.get('postalcode') or ''

        if address_text and postalcode and tools.ValidationText(address_text, 3, 200) and tools.ValidationText(
                postalcode, 3, 15) and postalcode.isdigit():
            # For now cost is 0.0 , this will be completed when use google maps , i cant use google maps because sanction :)
            cost = 0.0
            address = Address.objects.create(user=user, address=address_text, postal_code=postalcode, cost=cost)
            data_response = {
                'address': serializers.AddressSerializer([address])[0]
            }
            message = 'Your address created successfully'
        else:
            raise exceptions.FieldsIsEmpty
        return Response(200, data_response, message)


class EditAddress(APIView):
    """
          Get fields = [
                address_id,
                address : address is text address,
                postalcode,
          ]
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}

        data = request.data
        user = request.user

        address_id = data.get('address_id') or None
        address_text = data.get('address') or ''
        postalcode = data.get('postalcode') or ''


        if address_id and address_text and postalcode and tools.ValidationText(address_text, 3, 200) and tools.ValidationText(
                postalcode, 3, 15) and postalcode.isdigit():
            address = Address.objects.filter(id=address_id).first()
            if address:
                address.address = address_text
                address.postal_code = postalcode
                address.save()
                data_response = {
                    'address':serializers.AddressSerializer([address])[0]
                }
                message = 'Your address changed successfully'
            else:
                raise exceptions.AddressNotFound
        else:
            raise exceptions.FieldsIsEmpty
        return Response(200,data_response,message)

class DeleteAddress(APIView):
    """
          Get fields = [
                address_id,
          ]
          Auth = True
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data_response = {}

        data = request.data
        address_id = data.get('address_id') or 0
        user = request.user
        address = user.get_address().filter(id=address_id).first()
        if address:
            address.delete()
            message = 'Your Address deleted successfully'
        else:
            raise exceptions.AddressNotFound
        return Response(200, message=message)
