from django.urls import path
from . import views
from Food.views import GetMealsWithDiscount


app_name = 'Public'
urlpatterns = [
    path('',views.Index.as_view())
]