from hackathon.celery import app

from price.models import PriceData

import random

@app.task(bind=True)
def seed_data(self):
	tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']
	for b in tokens:
			for s in tokens:
				if s is not b:
					bq = random.uniform(.5, 2) 
					sq = random.uniform(.5, 2)
					PriceData.objects.create(buy_token=b, buy_quantity=bq, sell_token=s, sell_quantity=sq, cancel_order=False)

