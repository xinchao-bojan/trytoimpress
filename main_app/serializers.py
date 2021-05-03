from rest_framework import serializers

from .models import *
from custom_user.serializers import CustomUserSerializer


class ReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyStatus
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckStatus
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'owner', 'start_date', 'readystatus', 'checkstatus_set']

    readystatus = ReadySerializer()
    owner = CustomUserSerializer()
    checkstatus_set = CheckSerializer(many=True)
