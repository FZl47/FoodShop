from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from Config import exceptions

# JWT Need
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings

class EmailBackend(ModelBackend):
    def authenticate(self, request,email=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = {h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES}


class CustomeJWTAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token):
        """
            Custome Validation
        """
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except:
                # Custome Error
                raise exceptions.TokenExpiredOrInvalid()

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            # Custome Here !
            """
                if token sended and user not found return None instead error
            """
            return None

            # raise AuthenticationFailed(
            #     _("Authorization header must contain two space-delimited values"),
            #     code="bad_authorization_header",
            # )

        return parts[1]



class CustomeJWTAuthenticationAllowAny(CustomeJWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = ''
        try:
            validated_token = self.get_validated_token(raw_token)
        except:
            return AnonymousUser() , validated_token
        return self.get_user(validated_token), validated_token


    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            # raise exceptions.TokenExpiredOrInvalid
            return AnonymousUser()

        try:
            user_model = get_user_model()
            user = user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except user_model.DoesNotExist:
            return AnonymousUser()
        if not user.is_active:
            return AnonymousUser()

        return user

