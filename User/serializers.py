from rest_framework.serializers import ModelSerializer


class UserBasicSerializer(ModelSerializer):

    def to_representation(self, instance):
        return {
            'name':instance.first_name,
            'family':instance.last_name,
            'full_name':instance.getName(),
            'order_count_meal':instance.order_set.first().meals.count()
        }