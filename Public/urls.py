from django.urls import path
from . import views


app_name = 'Public'
urlpatterns = [
    path('',views.Index.as_view()),
    # Galley & Image
    path('gallery/get', views.GetImageSite.as_view(), name='get_gallery_site'),
]