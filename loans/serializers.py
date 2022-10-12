from rest_framework import serializers

from . import models


class UserCreateSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return models.User.objects.create(name=validated_data.get('user'))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['name']
