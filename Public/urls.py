from django.urls import path
from . import views


app_name = 'Public'
urlpatterns = [
    path('',views.Index.as_view()),
    # Galley & Image
    path('gallery/get', views.GetGallery.as_view(), name='get_gallery_site'),
    # About Us
    path('aboutus/get', views.GetInfoAboutUs.as_view(), name='get_aboutus'),
    # Contact Us
    path('contactus/get', views.GetInfoContactUs.as_view(), name='get_contactus'),
    path('contactus/feedback/submit', views.SubmitFeedBack.as_view(), name='submit_feedback'),
    # Subscribe news
    path('subscribe', views.SubscribeNewsView.as_view(), name='subscribe_news'),
]