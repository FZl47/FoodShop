from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from User.Auth.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class Index(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        return Response({
            'a':'aw'
        })
