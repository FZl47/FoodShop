from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views


app_name = 'User'
urlpatterns = [
    # JWT
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/get-access-token', views.GetAccessToken.as_view(), name='get_token_refresh'),
    # User
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('reset-password/get-code', views.ResetPasswordGetCode.as_view(), name='reset_password_code'),
    path('reset-password/validate-code', views.ResetPasswordValidateCode.as_view(), name='reset_password_validate'),
    path('reset-password/set-password', views.ResetPasswordSetPassword.as_view(), name='reset_password_set_password'),
]

