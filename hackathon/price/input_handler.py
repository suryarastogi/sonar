# Import required libaries
import time
import json

import requests


# Add timestamp
def create_time_stamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))


# Poloniex handler
class Poloniex(object):

    def __init__(self):
        self.url_endpoint = 'https://poloniex.com/public?command='

    def api_query(self, command, params={}):
        command_endpoint = self.url_endpoint + command
        response = requests.get(command_endpoint, params=params)
        return response.json()

    def get_order_book(self, currency_pair, depth=100):
        return self.api_query("returnOrderBook", params={'currencyPair': currency_pair, 'depth': depth})

    def get_trade_history(self, currency_pair):
        return self.api_query('returnTradeHistory', params={"currencyPair": currency_pair})


# Bittrex handler
class Bittrex(object):

    def __init__(self):
        self.url_endpoint = 'https://bittrex.com/api/v1.1/public/'

    def api_query(self, command, params={}):
        command_endpoint = self.url_endpoint + command + '?market=' + str(params['currency_pair'])
        del params['currency_pair']

        response = requests.get(command_endpoint, params=params)
        return response.json()['result']

    def get_order_book(self, currency_pair):
        return self.api_query("getOrderBook", params={'currency_pair': currency_pair.replace('_', '-'), 'type': 'both'})

    def get_trade_history(self, currency_pair):
        return self.api_query('getMarketHistory', params={'currency_pair': currency_pair.replace('_', '-')})


# Cryptopia handler
class Cryptopia(object):

    def __init__(self):
        self.url_endpoint = 'https://www.cryptopia.co.nz/api/'

    def api_query(self, command, params={}):

        command_endpoint = self.url_endpoint + command + '/' + str(params['currency_pair'])
        del params['currency_pair']
        for param in params:
            command_endpoint += '/'
            command_endpoint += str(params[param])

        response = requests.get(command_endpoint)
        return response.json()['Data']

    def get_order_book(self, currency_pair, depth=100):
        return self.api_query("GetMarketOrders", params={'currency_pair': '_'.join(currency_pair.split('_')[::-1]), 'depth': depth})

    def get_trade_history(self, currency_pair, hours=48):
        return self.api_query('GetMarketHistory', params={'currency_pair': '_'.join(currency_pair.split('_')[::-1]), 'hours': hours})


# Testing
if __name__ == '__main__':
    p = Poloniex()
    p.get_order_book('BTC_ETH')
    p.get_trade_history('BTC_ETH')
    b = Bittrex()
    b.get_order_book('BTC_ETH')
    b.get_trade_history('BTC_ETH')
    c = Cryptopia()
    c.get_order_book('BTC_ETH')
    c.get_trade_history('BTC_ETH')

    print('Done!')
