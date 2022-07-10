from django.urls import path
from . import views

app_name = 'Food'
urlpatterns = [
    path('get-meal-discounts',views.GetMealsWithDiscount.as_view(),name='get_discounts'),
    path('get-meal-popular',views.GetMealsWithPopular.as_view(),name='get_popular'),
]