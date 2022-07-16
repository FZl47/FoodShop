from rest_framework.serializers import ModelSerializer


class UserBasicSerializer(ModelSerializer):

    def to_representation(self, instance):
        # Base Fields
        d = {
            'name': instance.first_name,
            'family': instance.last_name,
            'full_name': instance.getName(),
        }
        # Order
        order = instance.get_order_active()
        if order:
            d.update({
                'order_count_meal': order.get_details().count()
            })

        return d
