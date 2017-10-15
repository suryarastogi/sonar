
# Import required libraries
import numpy as np
import pandas as pd

from price.handler import Poloniex, Bittrex, Cryptopia


# Settings
base_pair = 'BTC_ETH'
depth = 100
total_depth = 50
spread = 0.005

poloniex = Poloniex()
bittrex = Bittrex()
cryptopia = Cryptopia()


class OutputHandler(object):
    tokens = ['ZRX', 'MTL', 'DNT', 'OMG', 'ANT', 'ETH']

    @staticmethod
    def build_order_book(pair, depth):

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
        np.cumsum(np_bid[:,1], axis=0, out=np_bid[:,1])
        np_bid[:,0] *= (1 - spread/2)

        ask.sort(key=lambda x: x[0])
        np_ask = np.array(ask[:total_depth])
        np.cumsum(np_ask[:,1], axis=0, out=np_ask[:,1])
        np_ask[:,0] *= (1 + spread/2)

        return np_bid, np_ask


    @staticmethod
    def get_quantity_pairs():

        bid, ask = OutputHandler.build_order_book('BTC_ETH', depth)
        pairs = {}

        payload = {
            'WETH': {'MTL': (bid[0][0], bid[0][0] * bid[1][0], False),
                     'ZRX': (bid[0][0], bid[0][0] * bid[1][0], False),
                   },
            'MTL': {'WETH': (bid[0][0], bid[0][0] * bid[1][0], False),
                     'ZRX': (bid[0][0], bid[0][0] * bid[1][0], False),
                   },
            'ZRX': {'MTL': (bid[0][0], bid[0][0] * bid[1][0], False),
                     'WETH': (bid[0][0], bid[0][0] * bid[1][0], False),
                   }
        }

        return payload
