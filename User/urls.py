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
    path('get-dashboard', views.GetDashboardInfo.as_view(), name='get_dashboard'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('get-user', views.GetUser.as_view(), name='get_user'),
    path('reset-password/get-code', views.ResetPasswordGetCode.as_view(), name='reset_password_code'),
    path('reset-password/validate-code', views.ResetPasswordValidateCode.as_view(), name='reset_password_validate'),
    path('reset-password/set-password', views.ResetPasswordSetPassword.as_view(), name='reset_password_set_password'),
    path('info/edit', views.EditInfo.as_view(), name='change_info'),

    # Cart
    path('cart/pay', views.PaymentOrder.as_view(),name='payment_cart'),
    path('cart/add', views.AddToCart.as_view(),name='add_to_cart'),
    path('cart/get', views.GetCart.as_view(),name='get_cart'),
    path('cart/orderdetail/changecount', views.ChangeCountOrderDetail.as_view(),name='change_count_orderdetail'),
    path('cart/orderdetail/delete', views.DeleteOrderDetail.as_view(),name='delete_orderdetail'),
    path('cart/orderdetail/delete-all', views.DeleteAllOrderDetail.as_view(),name='delete_all_orderdetail'),

    # Address
    path('address/add',views.AddAddress.as_view(),name='add_address'),
    path('address/edit',views.EditAddress.as_view(),name='edit_address'),
    path('address/delete',views.DeleteAddress.as_view(),name='delete_address'),
]

