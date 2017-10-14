from price.models import PriceData
import random

class Utils(object):

	@staticmethod
	def seed_dummy():
		tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']

		for b in tokens:
			for s in tokens:
				if s is not b:
					bq = random.uniform(.5, 2)
					sq = random.uniform(.5, 2)
					PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=False)