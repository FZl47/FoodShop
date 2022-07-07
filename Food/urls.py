from django.urls import path
from .views import GetMealsWithDiscount

app_name = 'Food'
urlpatterns = [
    # path('all'),
    path('get-meal-discounts',GetMealsWithDiscount.as_view(),name='get_discounts')
]