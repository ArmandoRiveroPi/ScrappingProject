from django.urls import path
from .views import ListAdsView, ListBPersonView

urlpatterns = [
    path('ads/', ListAdsView.as_view(), name="ads-all"),
    path('bpersons/', ListBPersonView.as_view(), name="bperson-all"),
]
