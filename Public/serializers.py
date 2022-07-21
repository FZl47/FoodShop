from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            'title': instance.title,
            'url': instance.get_url(),
        }