from django.shortcuts import render
from rest_framework.views import APIView
from Config.response import Response
from .models import Meal
from .serializers import MealSerializer

class GetMeals(APIView):
    pass


class GetMealsWithDiscount(APIView):
    """
          Get fields = []
    """

    def post(self,request):
        data_response = MealSerializer(Meal.get_objects.get_with_discount(),many=True).data
        return Response(200,data_response)