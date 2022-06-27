from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Public.response import Response
from User.Auth.permissions import IsAuthenticated



class Index(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(200)
