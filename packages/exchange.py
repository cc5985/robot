# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from packages import universal
import time

class Exchange:

    _market=None
    MARKET_BASEURL_MAPPING={
        'AEX':'https://api.aex.zone',
        'OKEx': 'www.okex.com',
        'DigiFinex':'https://openapi.digifinex.vip'
    }

    def __init__(self, account, base_url=None):
        self.account = account
        if not base_url is None:
            self.base_url = base_url

    def get_currency_pairs_info(self):
        pass

    def ticker(self, currency_pair):
        pass

    def depth(self, currency_pair, raw=True):
        pass

    def trades(self, currency_pair):
        pass

    def balances(self):
        pass

    def submit_order(self, type, currency_pair, price, amount):
        pass

    def order_list(self,currency_pair, current_page=1, page_length=200):
        pass

    def trade_list(self,currency_pair, current_page=1, page_length=200):
        pass
