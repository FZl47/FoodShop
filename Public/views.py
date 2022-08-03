from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Config.response import Response
from Config.permissions import IsAuthenticated
from Config import exceptions
from Config import tools
from .models import GallerySite, AboutUs
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

    def post(self,request):
        data_response = {}

        aboutus = AboutUs.objects.first()
        if aboutus:
            data_response = {
                    'story_aboutus':aboutus.story_aboutus,
                    'why_chooseus':aboutus.why_chooseus
            }
        else:
            raise exceptions.NotFound

        return Response(200,data_response)



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
                'pagination':pagination_dict
            }
        else:
            raise exceptions.FieldsIsWrong()
        return Response(200, data_response)
