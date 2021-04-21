from rest_framework import serializers

from .models import CustomUser, Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['position']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

    position = PositionSerializer()
