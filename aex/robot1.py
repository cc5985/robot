import sys
sys.path.append("..")
from packages import aex as AEX
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
import time

USER_ID=472702
account=ACCOUNT.Account('426817f2228d6d8f485dff7b8a9aee71','41ebfb59508cd77031a25228758755dc10f566c18b19f13c52e39ca4c69d775f')
aex=AEX.AEX(account,USER_ID)

# get all tradable currency pairs:
currency_pairses=CP.CurrencyPair.find_triangle_arbitragable_currency_pairs('aex',account,USER_ID)

# get all distinctive currency pair:
distinctive_currency_pairs=[]
for currency_pairs in currency_pairses:
    for currency_pair in currency_pairs:
        if not distinctive_currency_pairs.__contains__(currency_pair):
            distinctive_currency_pairs.append(currency_pair)

# get relative prices of all currency pairs:
initial_funds={}
tickers = {}
tickers['cny'] = aex.ticker(CP.CurrencyPair('all', 'cny'), True)
tickers['usdt'] = aex.ticker(CP.CurrencyPair('all', 'usdt'), True)
# reformat tickers
_tickers = {}
for key1 in tickers.keys():
    for key2 in tickers[key1]:
        if key1 + '_' + key2 == 'usdt_tusd' or key1 + '_' + key2 == 'usdt_pax':
            continue
        _tickers[key2 + '_' + key1] = tickers[key1][key2]['ticker']
tickers = _tickers
initial_funds['cny']=100
# inquire the relative price of currency N to cny
for currency_pair in distinctive_currency_pairs:
    currencies=[currency_pair.base,currency_pair.reference]
    for currency in currencies:
        if currency!='cny':
            __currency_pairs = currency+ '_cny'
            initial_funds[currency] = initial_funds['cny']/tickers[__currency_pairs]['last']


while True:
    try:

        # get all depths one-to-one corresponding to currency pairs in distinctive currency pairs:
        depths = {}
        for currency_pair in distinctive_currency_pairs:
            depth = aex.depth(currency_pair)
            depths[currency_pair] = depth

        for tradable_currency_pairs in currency_pairses:
            depth = [depths[tradable_currency_pairs[0]], depths[tradable_currency_pairs[1]],
                     depths[tradable_currency_pairs[2]]]

            strategy = TRI.TriangleArbitrage(account, 'digifinex', tradable_currency_pairs, initial_funds=initial_funds)
            print('Now:\t'+str(tradable_currency_pairs[0].toString())+'\t'+str(tradable_currency_pairs[1].toString())+'\t'+str(tradable_currency_pairs[2].toString()))
            strategy.find_arbitrage_points(depth)
        print('\n\n')
        time.sleep(3)
    except Exception as e:
        print(e)
    a=1
a=1


currency_pair=CP.CurrencyPair('btc','cny')
# ticker=aex.ticker(currency_pair)
# depth=aex.depth(currency_pair)
# trades=aex.trades(currency_pair)
# balance=aex.balances()
# orderInfo=aex.submit_order(2,currency_pair,100000,0.01)
# cancleOrderResult=aex.cancel_order(currency_pair,'29207338')
# orderList=aex.order_list(currency_pair)
tradeList=aex.trade_list(currency_pair)

a=1

