from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Config.response import Response
from Config.permissions import IsAuthenticated
from Config import exceptions
from Config import tools
from .models import GallerySite
from .serializers import ImageSerializer



class Index(APIView):
    # permission_classes = (IsAuthenticated,)


    def post(self, request):
        return Response(200)



class GetImageSite(APIView):
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
        if str(page).isdigit():
            page = int(page)
            galley = GallerySite.objects.first()
            images = []
            if galley:
                images = galley.images.all()
            data_response = {
                'images': ImageSerializer(images, many=True).data
            }
        else:
            raise exceptions.FieldsIsWrong()
        return Response(200,data_response)
