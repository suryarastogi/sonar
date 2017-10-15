# Import required libraries
import numpy as np

from price.input_handler import Poloniex, Bittrex, Cryptopia


# Settings
DUAL_LEG = False
BASE_PAIR = 'BTC_ETH'
DEPTH = 100
TOTAL_DEPTH = 50
SPREAD = 0.005

poloniex = Poloniex()
bittrex = Bittrex()
cryptopia = Cryptopia()


class OutputHandler(object):
    tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'ETH']
    minor_tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT']

    @staticmethod
    def build_order_book(pair, depth, total_depth, spread):

        poloniex_data = poloniex.get_order_book(pair)
        bittrex_data = bittrex.get_order_book(pair)
        cryptopia_data = cryptopia.get_order_book(pair)

        # Normalize everything into list of tuples
        bid = []
        ask = []

        if 'error' not in poloniex_data:
            for row in poloniex_data['bids'][:depth]:
                bid.append((0.9975 * float(row[0]), float(row[1])))

            for row in poloniex_data['asks'][:depth]:
                ask.append((1.0025 * float(row[0]), float(row[1])))

        if bittrex_data:
            for row in bittrex_data['buy'][:depth]:
                bid.append((0.9975 * row['Rate'], row['Quantity']))

            for row in bittrex_data['sell'][:depth]:
                ask.append((1.0025 * row['Rate'], row['Quantity']))

        if cryptopia_data:
            for row in cryptopia_data['Buy'][:depth]:
                bid.append((0.995 * row['Price'], row['Volume']))

            for row in cryptopia_data['Sell'][:depth]:
                ask.append((1.005 * row['Price'], row['Volume']))

        bid.sort(key=lambda x: x[0], reverse=True)
        np_bid = np.array(bid[:total_depth])
        np.cumsum(np_bid[:, 1], axis=0, out=np_bid[:, 1])
        np_bid[:, 0] *= (1 - spread / 2)

        ask.sort(key=lambda x: x[0])
        np_ask = np.array(ask[:total_depth])
        np.cumsum(np_ask[:, 1], axis=0, out=np_ask[:, 1])
        np_ask[:, 0] *= (1 + spread / 2)

        return np_bid, np_ask

    @staticmethod
    def get_quantity_pairs():

        data = {}
        initial_base_tickers = ['ETH_ZRX', 'ETH_MTL', 'ETH_DNT', 'ETH_OMG', 'ETH_ANT']

        if DUAL_LEG:
            # Internal dual leg trade
            base_tickers = [ticker.replace('ETH', 'BTC') for ticker in initial_base_tickers]
            base_bid, base_ask = OutputHandler.build_order_book(BASE_PAIR, DEPTH, TOTAL_DEPTH, spread=0)

            # Hard assumption for now
            eth_to_btc = base_bid[0][0]
            btc_to_eth = 1/(base_ask[0][0])

            # Round trip should lose 0.5%
            # print(1/(base_ask[0][0]) * base_bid[0][0])
        else:
            base_tickers = initial_base_tickers

        for i, ticker in enumerate(base_tickers):
            bid, ask = OutputHandler.build_order_book(ticker, DEPTH, TOTAL_DEPTH, SPREAD)

            if DUAL_LEG:
                bid = bid * btc_to_eth
                ask = ask * 1/eth_to_btc

            data[initial_base_tickers[i]] = (bid, ask)

        # Bid then top of L2 then price not volume

        payload = {
            'WETH': {
                'ZRX': (data['ETH_ZRX'][0][0][1], data['ETH_ZRX'][0][0][0] * data['ETH_ZRX'][0][0][1], False),
                'MTL': (data['ETH_MTL'][0][0][1], data['ETH_MTL'][0][0][0] * data['ETH_MTL'][0][0][1], False),
                'DNT': (data['ETH_DNT'][0][0][1], data['ETH_DNT'][0][0][0] * data['ETH_DNT'][0][0][1], False),
                'OMG': (data['ETH_OMG'][0][0][1], data['ETH_OMG'][0][0][0] * data['ETH_OMG'][0][0][1], False),
                'ANT': (data['ETH_ANT'][0][0][1], data['ETH_ANT'][0][0][0] * data['ETH_ANT'][0][0][1], False)
            },
            'ZRX': {
                'WETH': (data['ETH_ZRX'][1][0][0] * data['ETH_ZRX'][1][0][1], data['ETH_ZRX'][1][0][1], False),
                'MTL': (data['ETH_ZRX'][1][0][0] * data['ETH_MTL'][0][0][1], data['ETH_MTL'][0][0][0] * data['ETH_MTL'][0][0][1], False),
                'DNT': (data['ETH_ZRX'][1][0][0] * data['ETH_DNT'][0][0][1], data['ETH_DNT'][0][0][0] * data['ETH_DNT'][0][0][1], False),
                'OMG': (data['ETH_ZRX'][1][0][0] * data['ETH_OMG'][0][0][1], data['ETH_OMG'][0][0][0] * data['ETH_OMG'][0][0][1], False),
                'ANT': (data['ETH_ZRX'][1][0][0] * data['ETH_ANT'][0][0][1], data['ETH_ANT'][0][0][0] * data['ETH_ANT'][0][0][1], False)
            },
            'MTL': {
                'ZRX': (data['ETH_MTL'][1][0][0] * data['ETH_ZRX'][0][0][1], data['ETH_ZRX'][0][0][0] * data['ETH_ZRX'][0][0][1], False),
                'WETH': (data['ETH_MTL'][1][0][0] * data['ETH_MTL'][1][0][1], data['ETH_MTL'][1][0][1], False),
                'DNT': (data['ETH_MTL'][1][0][0] * data['ETH_DNT'][0][0][1], data['ETH_DNT'][0][0][0] * data['ETH_DNT'][0][0][1], False),
                'OMG': (data['ETH_MTL'][1][0][0] * data['ETH_OMG'][0][0][1], data['ETH_OMG'][0][0][0] * data['ETH_OMG'][0][0][1], False),
                'ANT': (data['ETH_MTL'][1][0][0] * data['ETH_ANT'][0][0][1], data['ETH_ANT'][0][0][0] * data['ETH_ANT'][0][0][1], False)
            },
            'DNT': {
                'ZRX': (data['ETH_DNT'][1][0][0] * data['ETH_ZRX'][0][0][1], data['ETH_ZRX'][0][0][0] * data['ETH_ZRX'][0][0][1], False),
                'MTL': (data['ETH_DNT'][1][0][0] * data['ETH_MTL'][0][0][1], data['ETH_MTL'][0][0][0] * data['ETH_MTL'][0][0][1], False),
                'WETH': (data['ETH_DNT'][1][0][0] * data['ETH_DNT'][1][0][1], data['ETH_DNT'][1][0][1], False),
                'OMG': (data['ETH_DNT'][1][0][0] * data['ETH_OMG'][0][0][1], data['ETH_OMG'][0][0][0] * data['ETH_OMG'][0][0][1], False),
                'ANT': (data['ETH_DNT'][1][0][0] * data['ETH_ANT'][0][0][1], data['ETH_ANT'][0][0][0] * data['ETH_ANT'][0][0][1], False)
            },
            'OMG': {
                'ZRX': (data['ETH_OMG'][1][0][0] * data['ETH_ZRX'][0][0][1], data['ETH_ZRX'][0][0][0] * data['ETH_ZRX'][0][0][1], False),
                'MTL': (data['ETH_OMG'][1][0][0] * data['ETH_MTL'][0][0][1], data['ETH_MTL'][0][0][0] * data['ETH_MTL'][0][0][1], False),
                'DNT': (data['ETH_OMG'][1][0][0] * data['ETH_DNT'][0][0][1], data['ETH_DNT'][0][0][0] * data['ETH_DNT'][0][0][1], False),
                'WETH': (data['ETH_OMG'][1][0][0] * data['ETH_OMG'][1][0][1], data['ETH_OMG'][1][0][1], False),
                'ANT': (data['ETH_OMG'][1][0][0] * data['ETH_ANT'][0][0][1], data['ETH_ANT'][0][0][0] * data['ETH_ANT'][0][0][1], False)
            },
            'ANT': {
                'ZRX': (data['ETH_ANT'][1][0][0] * data['ETH_ZRX'][0][0][1], data['ETH_ZRX'][0][0][0] * data['ETH_ZRX'][0][0][1], False),
                'MTL': (data['ETH_ANT'][1][0][0] * data['ETH_MTL'][0][0][1], data['ETH_MTL'][0][0][0] * data['ETH_MTL'][0][0][1], False),
                'DNT': (data['ETH_ANT'][1][0][0] * data['ETH_DNT'][0][0][1], data['ETH_DNT'][0][0][0] * data['ETH_DNT'][0][0][1], False),
                'OMG': (data['ETH_ANT'][1][0][0] * data['ETH_OMG'][0][0][1], data['ETH_OMG'][0][0][0] * data['ETH_OMG'][0][0][1], False),
                'WETH': (data['ETH_ANT'][1][0][0] * data['ETH_ANT'][1][0][1], data['ETH_ANT'][1][0][1], False),
            }
        }

        return payload
