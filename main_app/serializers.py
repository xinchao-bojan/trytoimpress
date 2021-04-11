from rest_framework import serializers

from .models import *


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
        fields = '__all__'

    ready = ReadySerializer()
    check = CheckSerializer()
