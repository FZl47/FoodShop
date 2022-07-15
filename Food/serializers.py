from rest_framework import serializers
from Config.tools import TextToShortText, get_decimal_num
from .models import Meal


class ImageMealSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        url = instance.image.url
        return {
            'url': url
        }


class CommentSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            'title': instance.title,
            'text': instance.text,
            'rate': instance.rate,
            'time_send': instance.get_time_send(),
        }


class MealSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        discount = instance.get_max_discount()
        # Base Fields
        d = {
            'type': instance.type_meal,
            'title': instance.title,
            'title_short': TextToShortText(instance.title, 15),
            'description': instance.description,
            'description_short': TextToShortText(instance.description, 50),
            'cover_image': instance.get_image_cover(),
            'price': instance.get_price(discount),
            'slug': instance.slug,
            'rate': instance.get_comments_rate_avg(),
            'discount': False,
        }

        # Discount Fields
        if discount:
            d.update({
                'discount': True,
                'discount_percentage': discount.percentage
            })

        # Group Meal
        if instance.type_meal == 'group':
            d.update({
                'count_food': instance.foods.count(),
                'count_drink': instance.drinks.count()
            })

        return d


class MealDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        discount = instance.get_max_discount()
        # Base Fields
        d = {
            'is_available': True if instance.stock > 0 else False,
            'type': instance.type_meal,
            'title': instance.title,
            'description': instance.description,
            'images': ImageMealSerializer(instance.get_images(), many=True).data,
            'price_base': get_decimal_num(instance.price),
            'price': instance.get_price(discount),
            'stock': instance.stock,
            'slug': instance.slug,
            'rate': instance.get_comments_rate_avg(),
            'category': CategorySerializer(instance.category).data,
            'discount': False,
        }

        # Discount Fields
        if discount:
            d.update({
                'discount': True,
                'discount_percentage': discount.percentage,
                'discount_title': discount.title,
                'discount_timeend': discount.time_end.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Group Meal
        if instance.type_meal == 'group':
            foods = instance.foods
            drinks = instance.drinks
            d.update({
                'count_food': foods.count(),
                'count_drink': drinks.count(),
                'foods': MealSerializer(foods, many=True).data,
                'drinks': MealSerializer(drinks, many=True).data,
            })

        # Comments Fields
        comments = instance.get_comments()
        d.update({
            'comments': CommentSerializer(comments, many=True).data,
            'comments_count': comments.count()
        })

        return d


class CategorySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            'title': instance.title,
            'slug': instance.slug
        }
