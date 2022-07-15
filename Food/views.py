from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.views import APIView
from Config.response import Response
from Config import exceptions
from Config.permissions import AllowAny
from .models import Meal, Category, VisitMeal
from .serializers import MealDetailSerializer, MealSerializer, CategorySerializer

def Pagination(objects,count,page):
    pagination = Paginator(objects, count)
    page_active = pagination.get_page(page)
    objects_active = page_active.object_list
    pagination_dict = {
            'pages': pagination.num_pages,
            'page_active': page_active.number,
            'page_next': page_active.number + 1 if page_active.has_next() else page_active.number,
            'page_previous': page_active.number - 1 if page_active.has_previous() else page_active.number,
            'last_page': pagination.page_range[-1],
            'first_page': pagination.page_range[0],
            'has_next': page_active.has_next(),
            'has_previous': page_active.has_previous()
        }
    return objects_active , pagination , pagination_dict

class GetMealsWithDiscount(APIView):
    """
          Get fields = [
                count_show=optional : can set "all" for get all meals with discount
           ]
           Auth = False
    """

    def post(self, request):
        data = request.data
        count_show = data.get('count_show') or 8
        meals = Meal.get_objects.get_with_discount()
        if count_show != 'all':
            meals = Meal.get_objects.get_with_discount()[:count_show]

        data_response = MealSerializer(meals, many=True).data
        return Response(200, data_response)


class GetMealsWithPopular(APIView):
    """
          Get fields = [
                count_show=optional : can set "all" for get all meals with discount
           ]
           Auth = False
    """

    def post(self, request):
        data = request.data
        count_show = data.get('count_show') or 8
        meals = Meal.get_objects.sort_by_popularity()
        if count_show != 'all':
            meals = Meal.get_objects.sort_by_popularity()[:count_show]
        data_response = MealSerializer(meals, many=True).data
        return Response(200, data_response)


class GetCategories(APIView):
    """
          Get fields = []
          Auth = False
    """

    def post(self, request):
        categories = Category.get_objects.all()
        data_response = CategorySerializer(categories, many=True).data
        return Response(200, data_response)

class GetMeal(APIView):
    """
          Get fields = [slug]
          Auth = optional
    """
    permission_classes = (AllowAny,)


    def post(self,request):
        data_response = {}

        data = request.data
        slug = data.get('slug')
        meal = Meal.get_objects.get_by_slug(slug)
        if meal == None:
            raise exceptions.NotFound()
        user = request.user
        if not user.is_authenticated:
            user = None
        VisitMeal.objects.create(user=user,meal=meal)
        data_response = MealDetailSerializer(meal).data
        return Response(200,data_response)



class GetMeals(APIView):
    """
          Get fields = [
             category_slug=optional,
             sort_by=optional,
             page=optional
          ]
          Auth = False
    """

    def post(self, request):
        count_show_meals_per_page = 9

        data = request.data
        category_slug = data.get('category_slug') or 'all'
        sort_by = data.get('sort_by') or 'most-visited'
        page = data.get('page')

        meals = Meal.get_objects.get_meals(category_slug=category_slug, sort_by=sort_by)
        meals , pagination , pagination_dict = Pagination(meals,count_show_meals_per_page,page)

        meals = MealSerializer(meals, many=True).data
        data_response = {
            'meals': meals,
            'pagination': pagination_dict
        }
        return Response(200, data_response)



class GetMealsBySearch(APIView):
    """
          Get fields = [
             search_value,
             sort_by=optional
          ]
          Auth = False
    """

    def post(self, request):

        count_show_meals_per_page = 9
        data_response = {}

        data = request.data
        search_value = data.get('search_value') or ''
        sort_by = data.get('sort_by') or 'most-visited'
        page = data.get('page')

        if search_value:
            meals = Meal.get_objects.get_by_search(search_value, sort_by)
        else:
            meals = Meal.get_objects.select_subclasses()

        meals, pagination, pagination_dict = Pagination(meals, count_show_meals_per_page, page)
        data_response = {
            'meals': MealSerializer(meals, many=True).data,
            'pagination':pagination_dict
        }

        return Response(200, data_response)
