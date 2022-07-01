from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Config.response import Response
from Config.permissions import IsAuthenticated


from django_q.models import Schedule
from Config import tools
import datetime


class Index(APIView):
    # permission_classes = (IsAuthenticated,)




    def post(self, request):
        time_now = tools.GetDateTime()
        time_now += datetime.timedelta(seconds=20)
        Schedule.objects.create(
            func='Public.views.task',
            args='32,',
            repeats=3,
            next_run=time_now
        )
        return Response(200)


def task(id):
    pass