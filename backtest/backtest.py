# encoding=utf-8
# this project is powered by Jeff Omega
# as author is a newbie to python, code style of this project is rubyish

import sys

sys.path.append("..")
from packages import error_code
import json
import time
import math
import copy
from packages import digifinex as DIGIFINEX
from packages import currency_pair as CP
from strategies import strategy as STRATEGY

class Backtest:

    def __init__(self):
        pass

    # @classmethod
    # def backtest(cls, strategy, trades, params):
    #     '''
    #
    #     :param strategy: a Strategy instance which specifies the starting timestamp, action trigger etc.
    #     :param trades: a Trades instance
    #     :return:
    #     '''
    #
    #     initial_fund=params['initial_fund']
    #     result={
    #         'total_return':0,
    #         'annual_return_percentage':0,
    #         'execution_time':0,
    #         'trade_time_span':0,
    #         'trade_number':0,
    #         'initial_fund':initial_fund,
    #         'total_retuan_percentage':0,
    #         'sharp_ratio':0,
    #         'max_drawback':0,
    #         'trades':[]
    #     }
    #     base=initial_fund
    #     reference=0
    #     price=trades.trades[0].price
    #     last_price=price
    #     current_timestamp = trades.trades[0].timestamp
    #     current_price = price
    #
    #     target_action=1
    #     for cnt in range(1,len(trades.trades)):
    #         trade = trades.trades[cnt]
    #         trade_type = trade.trade_type
    #         amount = trade.amount
    #         price = trade.price
    #
    #         if trade_type == 1:
    #             if price > high:
    #                 high = price
    #                 bid_vol_at_peak = amount
    #             elif price == high:
    #                 bid_vol_at_peak += amount
    #             else:
    #                 pass
    #         if trade_type==0 and target_action==1 and price<=
    #             if price < low:
    #                 low = price
    #                 ask_vol_at_bottom = amount
    #             elif price == low:
    #                 ask_vol_at_bottom += amount
    #             else:
    #                 pass
    #         timestamp = trade.timestamp
    #     return result