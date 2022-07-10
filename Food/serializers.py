from rest_framework import serializers
from Config.tools import TextToShortText
from .models import Meal


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
                'count_food':instance.foods.count(),
                'count_drink':instance.drinks.count()
            })

        return d
