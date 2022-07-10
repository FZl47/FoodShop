from django.shortcuts import render
from rest_framework.views import APIView
from Config.response import Response
from .models import Meal
from .serializers import MealSerializer

class GetMeals(APIView):
    pass


class GetMealsWithDiscount(APIView):
    """
          Get fields = [
                count_show=optional : can set "all" for get all meals with discount
           ]
    """

    def post(self,request):
        data = request.data
        count_show = data.get('count_show') or 8
        meals = Meal.get_objects.get_with_discount()
        if count_show != 'all':
            meals = Meal.get_objects.get_with_discount()[:count_show]

        data_response = MealSerializer(meals,many=True).data
        return Response(200,data_response)


class GetMealsWithPopular(APIView):
    """
          Get fields = [
                count_show=optional : can set "all" for get all meals with discount
           ]
    """

    def post(self,request):
        data = request.data
        count_show = data.get('count_show') or 8
        meals = Meal.get_objects.sort_by_popularity()
        if count_show != 'all':
            meals = Meal.get_objects.sort_by_popularity()[:count_show]

        data_response = MealSerializer(meals,many=True).data
        return Response(200,data_response)