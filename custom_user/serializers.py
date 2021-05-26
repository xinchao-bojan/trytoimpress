from rest_framework import serializers

from .models import CustomUser, Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['position']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'first_name', 'last_name', 'university', 'group']


class CustomUserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'position']

    position = PositionSerializer(many=True)
