from django.urls import path
from . import views

app_name = 'Food'
urlpatterns = [
    path('get-meals-discounts',views.GetMealsWithDiscount.as_view(),name='get_discounts'),
    path('get-meals-popular',views.GetMealsWithPopular.as_view(),name='get_popular'),
    path('get-meals-by-search',views.GetMealsBySearch.as_view(),name='get_by_search'),
    path('get-meals',views.GetMeals.as_view(),name='get_meals'),
    path('get-meal',views.GetMeal.as_view(),name='get_meal'),
    path('get-categories',views.GetCategories.as_view(),name='get_categories'),
]




