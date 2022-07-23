from rest_framework.serializers import ModelSerializer
from Food import serializers as Food_Serializers


class UserBasicSerializer(ModelSerializer):

    def to_representation(self, instance):
        # Base Fields
        d = {
            'name': instance.first_name,
            'family': instance.last_name,
            'full_name': instance.get_name(),
        }
        # Order
        order = instance.get_order_active()
        if order:
            d.update({
                'order_count_meal': order.get_details().count()
            })

        return d


def OrderDetailSerializer(orderdetails):
    results = []
    for orderdetail in orderdetails:
        meal = orderdetail.get_meal()
        # Check if meal is not available delete object order detail
        if meal:
            results.append(
                {
                    'count': orderdetail.count,
                    'meal': Food_Serializers.MealOrderDetailSerializer(meal).data,
                }
            )
        else:
            orderdetail.delete()
    return results


def OrderSerializer(order, user):
    d = {
        'details': OrderDetailSerializer(order.get_details()),
        'price': order.get_price_meals(),
        'price_without_discount': order.get_price_meals_without_discount()
    }
    return d
