# coding=utf-8

# triangle arbitrage:
'''
    0. 这是一个交易策略，
    1. 该策略基于三角套利模型，在三个标的间寻找瞬间的不平衡点，并试图进行交易套利
    2. 目前选取的两个交易组为 (btc,cny,usdt) 和 (eth,cny,usdt)
    3. 以上两个交易组的三角套利的重要性为0，即所有其他交易模型必须优先考虑这个策略
    4. 该三角套利模型原则上不进行‘限价单’操作，所有操作均为‘市价单’操作，即在充分掌握信息的情况下出手操作
    5. 高度抽象化，主程序体内尽量不出现字符串和数值
'''

import sys
sys.path.append("..")
import copy
import packages.color as CL
from packages import account as AC, coin as CN, currency_pair as CP, currency_pair
import time
import threading
from packages import digifinex as DIGIFINEX
# CONSTANTS，所有的外部参数、数值常量、字符串全都在这里定义----------------------------------------
FEE={
    'maker':0,
    'taker':0
}
FEE0 = 0
FEE1 = 0
market = "DigiFinex"
account = AC.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)
color = CL.Colored()
# -----------------------------------------------------------------------------------------

# assume we have c0 c1 c2, each of which has a quantity q0 q1 q2
# we should re-buy c0,c1,c2 in different market/pair at possible low price:
# the c0 we can buy at different markets are:
# you can only buy c0 by selling c2 in pairs[2] or selling c1 in pairs[0]:
# so the quantities of c0 you can buy are:
# f(depths[2],buy='c0',q2)---->in pairs[2]
# f(depths[0],buy='c0',q1)---->in pairs[0]
# the quantities of c1 you can buy are::
# f(depths[0],buy='c1',q0)
# f(depths[1],buy='c1',q2)
# the quantities of c2 you can buy are:
# f(depths[1],buy='c2',q1)
# f(depths[2],buy='c2',q0)

def swap(depth, currency1, amount1, action='buy'):
    '''
    the params mean that YOU DO ACTION ON CURRENCY1 FOR AMOUNT1
    参数的意思是： 你实施action在currency1上面，例如，action是buy，则买入currency1
    this function returns a dict {target_currency:target_currency, target_amount:target_amount}
    :param depth:
    :param currency1:
    :param amount1:
    :param action:
    :return:
    '''
    cp1 = CP.CurrencyPair()
    currency_pair = depth.currency_pair
    target_currency=currency_pair.subtract(currency1)
    target_amount=0  #

    if currency1==currency_pair.base:
        current_amount = 0  #
        if action=='buy':
            for ask in depth.asks:
                amount=ask.amount
                price=ask.price
                if current_amount+amount>=amount1:
                    target_amount+=price*(amount1-current_amount)
                    break
                else:
                    target_amount+=amount*price
                    current_amount+=amount
        else:
            for bid in depth.bids:
                amount=bid.amount
                price=bid.price
                if current_amount+amount>=amount1:
                    target_amount+=price*(amount1-current_amount)
                    break
                else:
                    target_amount+=amount*price
                    current_amount+=amount
    if currency1==currency_pair.reference:
        current_expense=0
        if action=='sell':
            for ask in depth.asks:
                amount=ask.amount
                price=ask.price
                if current_expense+amount*price>=amount1:
                    target_amount+=(amount1-current_expense)/price
                    break
                else:
                    current_expense+=amount*price
                    target_amount+=amount
        else:
            for bid in depth.bids:
                amount=bid.amount
                price=bid.price
                if current_expense+amount*price>=amount1:
                    target_amount+=(amount1-current_expense)/price
                    break
                else:
                    current_expense += amount * price
                    target_amount += amount

    return {'target_currency':target_currency,'target_amount':target_amount}

def trade(ref_coin, target_coin, price, amount, trade_type):
    # _currency_pair = target_coin + '_' + ref_coin
    # result = aex.submit_order(trade_type, _currency_pair, price, amount)
    # if result.message == "操作成功":
    #     print(color.green(trade_type + ' ' + target_coin + ' at ' + str(price) + ' of ' + str(amount)))
    # else:
    #     print(color.red(trade_type + ' ' + target_coin + ' at ' + str(price) + ' of ' + str(amount)))
    #     print(result.message)
    # return result
    pass

class TriangleArbitrage():

    def __init__(self, account, exchange, tradable_currency_pairs, initial_funds, fee={
        'maker':0,
        'taker':0
    }):
        self.account=account
        self.exchange=exchange
        self.tradable_currency_pairs=tradable_currency_pairs
        self.currencies = self.all_currencies()
        self.set_initial_funds(initial_funds)
        self.fee=fee


    def all_currencies(self):
        currencies=[]
        for currency_pair in self.tradable_currency_pairs:
            currencies.append(currency_pair.base)
            currencies.append(currency_pair.reference)
        currencies=list(set(currencies))
        currencies.sort()
        return currencies


    def set_initial_funds(self, initial_funds):
        self.initial_funds={}
        currencies=self.currencies
        try:
            self.initial_funds[currencies[0]]=initial_funds[currencies[0]]
            self.initial_funds[currencies[1]] = initial_funds[currencies[1]]
            self.initial_funds[currencies[2]] = initial_funds[currencies[2]]
        except:
            print('The currencies are: '+str(currencies) + '\nPlease check the initial funds param, whose keys should correspond to currencies')

    def find_paths(self):
        return [(0,1,2),(1,0,2),(2,0,1)]

    def find_arbitrage_points(self):
        currencies=self.currencies
        # depths 是深度列表，读取深度列表
        depths = []
        for pair in self.tradable_currency_pairs:
            depth = digifinex.depth(pair)
            depths.append(depth)

        time1 = time.time()

        # 计算所有套利路径：
        paths=self.find_paths()

        profits = []

        for path in paths:
            # coin00 represents how many btc you buy in terms of CNY
            # target_currency=self.tradable_currency_pairs[0].base
            target_currency = self.tradable_currency_pairs[path[0]].base
            initial_currency = target_currency
            coin00 = swap(depths[path[0]], target_currency, self.initial_funds[target_currency])['target_amount']

            target_currency=self.tradable_currency_pairs[path[0]].subtract(target_currency)
            # 确定第二条路径
            if depths[path[1]].currency_pair.contains(target_currency):
                coin11 = swap(depths[path[1]], target_currency, coin00)['target_amount']
                target_currency=self.tradable_currency_pairs[path[1]].subtract(target_currency)
                coin22 = swap(depths[path[2]], target_currency, coin11)['target_amount']
            else:
                coin11 = swap(depths[path[2]], target_currency, coin00)['target_amount']
                target_currency = self.tradable_currency_pairs[path[2]].subtract(target_currency)
                coin22 = swap(depths[path[1]], target_currency, coin11)['target_amount']

            profit = (self.initial_funds[initial_currency] - coin22) / coin22 * 100
            if profit<-2 or profit>0.1:
                a=1
            profits.append(profit)
            a=1
        a=1
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),end='')
        for p in profits:
            if p > 0:
                print(color.green(('\t\twin=%(win)f\t' % {'win': p})),end='')
            elif p < -1:
                print(color.red(('win=%(win)f\t' % {'win': p})),end='')
            else:
                print(color.red(('win=%(win)f\t' % {'win': p})),end='')
        print()

# while True:
#     show_time()
#     time.sleep(10)