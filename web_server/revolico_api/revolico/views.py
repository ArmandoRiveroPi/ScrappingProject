from rest_framework import generics
from .models import Ads, BPerson
from .serializers import AdsSerializer, BPersonSerializer
from django.shortcuts import render


class ListAdsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer


class ListBPersonView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = BPerson.objects.all()
    serializer_class = BPersonSerializer


# @login_required(login_url='/login/')
def home(request):
    return render(request, 'index.html')
