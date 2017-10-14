from django.shortcuts import render
from rest_framework import generics

from price.models import PriceData
from api.serializers import PriceSerializer

# Create your views here.

class PriceDataList(generics.ListCreateAPIView):
    queryset = PriceData.objects.all()
    serializer_class = PriceSerializer
