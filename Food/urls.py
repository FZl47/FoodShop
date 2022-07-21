from django.urls import path
from . import views

app_name = 'Food'
urlpatterns = [
    # Meals
    path('get-meals-discounts',views.GetMealsWithDiscount.as_view(),name='get_discounts'),
    path('get-meals-popular',views.GetMealsWithPopular.as_view(),name='get_popular'),
    path('get-meals-by-search',views.GetMealsBySearch.as_view(),name='get_by_search'),
    path('get-meals-by-category',views.GetMealsByCategory.as_view(),name='get_by_category'),
    path('get-meals',views.GetMeals.as_view(),name='get_meals'),
    path('get-meal',views.GetMeal.as_view(),name='get_meal'),
    path('get-categories',views.GetCategories.as_view(),name='get_categories'),
    # Comments
    path('submit-comment',views.SubmitComment.as_view(),name='submit_comment'),
    # Notify
    path('notify-me',views.NotifyMeView.as_view(),name='notify_me')
]




