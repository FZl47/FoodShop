from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views


app_name = 'User'
urlpatterns = [
    # JWT
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # User
    path('reset-password', views.ResetPassword.as_view(), name='reset_password'),
]

