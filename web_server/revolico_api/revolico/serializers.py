from rest_framework import serializers
from .models import Ads, BPerson


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ("title", "content")


class BPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPerson
        fields = ("name", "phone")
