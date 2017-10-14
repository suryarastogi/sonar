class PriceHandler(object):
	tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'WETH']

	@staticmethod
	def get_quantity_pairs():
		pairs = {}
		return None #Expecting something like (buy_q, sell_q, cancel) = pairs[Buy Token][Sell Token]