import random
from price.output_handler import OutputHandler
from price.models import PriceData
from hackathon.celery import update_signal
from django.dispatch import receiver

class Utils(object):

	@staticmethod
	def clear_db():
		PriceData.objects.all().delete()

	@staticmethod
	def seed_db():
		price_pairs = OutputHandler.get_quantity_pairs()
		#tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']
		tokens = ['ZRX', 'MTL', 'WETH']

		for b in tokens:
				for s in tokens:
					if s is not b:
						if PriceData.objects.filter(buy_token=b, sell_token=s).exists():
							trade = PriceData.objects.filter(buy_token=b, sell_token=s).all()[0]
							bq, sq, cancel = price_pairs[b][s]
							#bq = random.uniform(.5, 2) 
							#sq = random.uniform(.5, 2)
							trade.buy_quantity = bq
							trade.sell_quantity = sq
							trade.save()
						else:
							bq, sq, cancel = price_pairs[b][s]
							#bq = random.uniform(.5, 2) 
							#sq = random.uniform(.5, 2)
							PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=False)

# Hacky functions
#from price.price_handler import PriceHandler
'''update_signal.connect(seed_db)
print("test")
@receiver(update_signal)
def seed_db():
	print("Received Signal")
	tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']
	for b in tokens:
			for s in tokens:
				if s is not b:
					bq = random.uniform(.5, 2) 
					sq = random.uniform(.5, 2)
					PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=False)
'''
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