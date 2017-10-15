import random
from price.output_handler import OutputHandler
from price.models import PriceData, HistoricalData
from hackathon.celery import update_signal
from django.dispatch import receiver


class Utils(object):

    @staticmethod
    def clear_db():
        PriceData.objects.all().delete()

    @staticmethod
    def seed_db():
        price_pairs = OutputHandler.get_quantity_pairs()
        tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']

        for b in tokens:
            for s in tokens:
                if s is not b:
                    if PriceData.objects.filter(buy_token=b, sell_token=s).exists():
                        trade = PriceData.objects.filter(buy_token=b, sell_token=s).all()[0]

                        bq, sq, cancel = price_pairs[b][s]
                        old_bq = trade.buy_quantity
                        trade.buy_quantity = bq
                        old_sq = trade.sell_quantity
                        trade.sell_quantity = sq
                        trade.save()
                        HistoricalData.objects.create(
                            buy_token=b,
                            buy_quantity=old_bq,
                            sell_token=s,
                            sell_quantity=old_sq)
                    else:
                        bq, sq, cancel = price_pairs[b][s]
                        PriceData.objects.create(
                            buy_token=b,
                            buy_quantity=bq,
                            sell_token=s,
                            sell_quantity=sq,
                            cancel_order=False)
