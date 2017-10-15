from django.db import models

# Create your models here.
class PriceData(models.Model):
	# The token and amount the user will be buying
	buy_token = models.CharField(max_length=4)
	buy_quantity = models.FloatField()

	# The token and amount the user will be selling
	sell_token = models.CharField(max_length=4)
	sell_quantity = models.FloatField()

	# To cancel order or not
	cancel_order = models.BooleanField()

class HistoricalData(models.Model):
	buy_token = models.CharField(max_length=4)
	buy_quantity = models.FloatField()

	# The token and amount the user will be selling
	sell_token = models.CharField(max_length=4)
	sell_quantity = models.FloatField()

	timestamp = models.DateTimeField(auto_now_add=True)