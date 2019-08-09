from rest_framework import serializers
from .models import Ads, BPerson


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ("ad_id", "title", "content", "phone", "bperson",
                  "price", "classification", "datetime")


class BPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPerson
        fields = ("bperson_id", "name", "phone", "name_set")
