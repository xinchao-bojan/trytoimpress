from rest_framework import serializers

from .models import *
from custom_user.serializers import CustomUserSerializer


class ReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyStatus
        exclude = ['application', 'id']


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = CheckStatus
        exclude = ['application', 'id']
        read_only_fields = ['judge']

    judge = CustomUserSerializer()


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'start_date', 'readystatus', 'checkstatus_set']

    readystatus = ReadySerializer()
    checkstatus_set = CheckSerializer(many=True)
