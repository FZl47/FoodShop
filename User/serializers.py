from rest_framework.serializers import ModelSerializer
from Food import serializers as FoodSerializers
from Config import tools
from . import models


class UserBasicSerializer(ModelSerializer):

    def to_representation(self, instance):
        # Base Fields
        d = {
            'name': instance.first_name,
            'family': instance.last_name,
            'full_name': instance.get_name(),
            'email': instance.email,
            'phone_number': instance.phone_number
        }
        # Order
        order = instance.get_order_active()
        if order:
            d.update({
                'order_count_meal': order.get_details().count()
            })

        return d


class UserSerializer(ModelSerializer):
    def to_representation(self, instance):
        d = UserBasicSerializer(instance).data
        d.update({
            'address': AddressSerializer(instance.get_address())
        })
        return d


def AddressSerializer(addresses, many=True):
    def _(address):
        return {
            'id': address.id,
            'address': address.address,
            'address_short': tools.TextToShortText(address.address, 20),
            'postal_code': address.postal_code,
            'cost': str(address.cost),
            'is_free': address.is_free()
        }

    if many:
        results = []
        for address in addresses:
            results.append(_(address))
        return results
    else:
        return _(addresses)


class NotificationSerializer(ModelSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'meal': {
                'title': instance.meal.title,
                'title_short': tools.TextToShortText(instance.meal.title, 15),
                'image': instance.meal.get_image_cover(),
                'slug': instance.meal.slug,
            }
        }


class VisitSerializer(ModelSerializer):
    def to_representation(self, instance):
        return {
            'meal': {
                'title': instance.meal.title,
                'image': instance.meal.get_image_cover(),
                'slug': instance.meal.slug,
            },
            'time_past': instance.get_time_past(),
        }


def OrderDetailSerializer(orderdetails):
    results = []
    for orderdetail in orderdetails:
        meal = orderdetail.get_meal()
        meal_is_available = False if meal == None else meal.is_available()
        # Check if meal is not available delete object order detail
        if meal and meal_is_available:
            results.append(
                {
                    'id': orderdetail.id,
                    'count': orderdetail.count,
                    'meal': FoodSerializers.MealOrderDetailSerializer(meal).data,
                    'price': orderdetail.get_price()
                }
            )
        else:
            orderdetail.delete()
    return results


def OrderBasicSerializer(order):
    d = {
        'price': order.get_price_meals(),
        'price_without_discount': order.get_price_meals_without_discount()
    }
    return d


def OrderSerializer(order):
    details = OrderDetailSerializer(order.get_details())
    d = {
        'details': details,
        'is_not_empty': True if len(details) > 0 else False,
        'price': order.get_price_meals(),
        'price_without_discount': order.get_price_meals_without_discount()
    }
    return d


def OrderDashboardSerializer(orders):
    results = []
    for order in orders:
        d = OrderSerializer(order)
        address_obj = order.address
        address = None
        if address_obj:
            address = AddressSerializer(order.address,many=False)

        d.update({
            'status': order.status_order,
            'address': address,
            'time_paid': order.get_time_past(),
            'description': order.description
        })
        results.append(d)

    return results
