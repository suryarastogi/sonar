from price.models import PriceData
#from price.price_handler import PriceHandler
import random

class Utils(object):
	tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']

	@staticmethod
	def seed_dummy():

		for b in tokens:
			for s in tokens:
				if s is not b:
					bq = random.uniform(.5, 2) 
					sq = random.uniform(.5, 2)
					PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=False)

'''
	# Called every 10 seconds
	@staticmethod
	def seed_new_orders():
		price_pairs = PriceHandler.get_quantity_pairs()
		for b in tokens:
			for s in tokens:
				if s is not b:
					bq, sq, cancel = price_pairs[b][s]
					PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=cancel)
'''