from rest_framework import serializers
from price.models import PriceData, HistoricalData


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceData
        fields = '__all__'


class HistoricalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalData
        fields = '__all__'
