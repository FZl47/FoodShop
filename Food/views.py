from django.shortcuts import render
from rest_framework.views import APIView
from Config.response import Response
from .models import Meal, Category
from .serializers import MealSerializer, CategorySerializer


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


class GetCategories(APIView):
    """
          Get fields = []
    """

    def post(self,request):
        categories = Category.get_objects.all()
        data_response = CategorySerializer(categories, many=True).data
        return Response(200, data_response)


class GetMeals(APIView):
    """
          Get fields = [
             category_slug=optional,
             sort_by=optional
          ]
    """

    def post(self,request):
        data = request.data
        category_slug = data.get('category_slug') or 'all'
        sort_by = data.get('sort_by') or 'most-visited'

        meals = Meal.get_objects.get_meals(category_slug=category_slug,sort_by=sort_by)

        data_response = {
            'meals':MealSerializer(meals,many=True).data
        }
        return Response(200,data_response)

class GetMealsBySearch(APIView):
    """
          Get fields = [search_value]
    """

    def post(self,request):
        data_response = {}

        data = request.data
        search_value = data.get('search_value') or ''
        if search_value:
            meals = Meal.get_objects.get_by_search(search_value)
        else:
            meals = Meal.get_objects.all()
        meals = meals.select_subclasses()

        data_response = {
            'meals': MealSerializer(meals, many=True).data
        }

        return Response(200,data_response)