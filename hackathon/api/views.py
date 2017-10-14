from django.shortcuts import render
from rest_framework import generics

from price.models import PriceData
from api.serializers import PriceSerializer

from django.conf import settings
from django.http import HttpResponse
# Create your views here.

class PriceDataList(generics.ListCreateAPIView):
    queryset = PriceData.objects.all()
    serializer_class = PriceSerializer

def JSFrontEnd(request):
	file_loc = settings.BASE_DIR+"/static/index.html"
	f = open(file_loc, 'r')
	return HttpResponse(f)
