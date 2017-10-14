from rest_framework import serializers
from price.models import PriceData

class PriceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PriceData
		fields = '__all__'
