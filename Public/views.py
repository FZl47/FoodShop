from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Config.response import Response
from Config.permissions import IsAuthenticated, AllowAny
from Config import exceptions
from Config import tools
from .models import GallerySite, AboutUs, ContactUs, FeedBack, SubscribeNews
from .serializers import ImageSerializer


class Index(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(200)


class GetInfoAboutUs(APIView):
    """
            Get fields = []
            Auth = False
    """

    def post(self, request):
        data_response = {}

        aboutus = AboutUs.objects.first()
        if aboutus:
            data_response = {
                'story_aboutus': aboutus.story_aboutus,
                'why_chooseus': aboutus.why_chooseus
            }
        else:
            raise exceptions.NotFound

        return Response(200, data_response)


class GetInfoContactUs(APIView):
    """
            Get fields = []
            Auth = False
    """

    def post(self, request):
        data_response = {}

        contactus = ContactUs.objects.first()
        if contactus:
            data_response = {
                'emails': [{'email': email} for email in str(contactus.emails).split(',')],
                'phones': [{'phone': phone} for phone in str(contactus.phones).split(',')],
                'locations': [{'location': location} for location in str(contactus.location).split(',')],
                'location_image': contactus.get_location_image()
            }
        else:
            raise exceptions.NotFound

        return Response(200, data_response)


class SubmitFeedBack(APIView):
    """
            Get fields = [
                email,
                name,
                subject,
                message
            ]
            Auth = False
    """

    def post(self, request):
        data_response = {}

        data = request.data
        email = data.get('email')
        name = data.get('name')
        subject = data.get('subject')
        message = data.get('message')

        if tools.ValidationEmail(email, 3, 100) and tools.ValidationText(name, 3, 100) and tools.ValidationText(subject,
                                                                                                                2,
                                                                                                                100) and tools.ValidationText(
            message, 3, 1000):
            FeedBack.objects.create(email=email, name=name, subject=subject, message=message)
            message_response = 'Thank you , your feedback submited successfully'
        else:
            raise exceptions.FieldsIsWrong
        return Response(200, message=message_response)


class GetGallery(APIView):
    """
            Get fields = [
                page : Default is 1
            ]
            Auth = False
    """

    def post(self, request):
        data_response = {}
        data = request.data
        page = data.get('page') or 1

        count_show_per_page = 3
        if str(page).isdigit():
            page = int(page)
            galley = GallerySite.objects.first()
            images = []
            if galley:
                images = galley.images.all()
            images = ImageSerializer(images, many=True).data
            images, pagination_obj, pagination_dict = tools.pagination(images, count_show_per_page, page)
            data_response = {
                'images': images,
                'pagination': pagination_dict
            }
        else:
            raise exceptions.FieldsIsWrong
        return Response(200, data_response)


class SubscribeNewsView(APIView):
    """
            Get fields = [
                email
            ]
            Auth = False
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        data_response = {}

        data = request.data
        email = data.get('email')

        if tools.ValidationEmail(email, 3, 100):
            sub = SubscribeNews.objects.filter(email=email).first()
            if sub:
                sub.delete()
                message = 'Unsubscribe successfully'
            else:
                SubscribeNews.objects.create(email=email)
                message = 'Subscription was successful'
        else:
            raise exceptions.FieldsIsWrong

        return Response(200, message=message)
