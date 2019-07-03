import sys
sys.path.append("..")
from packages import currency_pair as CP
from packages import account as ACCOUNT
from strategies import triangle_arbitrage as TRI
from packages import digifinex as DIGIFINEX
import time

account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)

# get all tradable currency pairs:
currency_pairses=CP.CurrencyPair.find_triangle_arbitragable_currency_pairs('digifinex',account)

# get all distinctive currency pair:
distinctive_currency_pairs=[]
for currency_pairs in currency_pairses:
    for currency_pair in currency_pairs:
        if not distinctive_currency_pairs.__contains__(currency_pair):
            distinctive_currency_pairs.append(currency_pair)

initial_funds={}
# get relative prices of all currency pairs:
ticker=digifinex.ticker()
# set initial fund of USDT to 11
initial_funds['usdt']=14

# inquire the relative price of currency N to usdt
for currency_pair in distinctive_currency_pairs:
    currencies=[currency_pair.base,currency_pair.reference]
    for currency in currencies:
        if currency!='usdt':
            __currency_pairs = 'usdt_' + currency
            initial_funds[currency] = initial_funds['usdt']/ticker[__currency_pairs]['last']



while True:
    try:

        # get all depths one-to-one corresponding to currency pairs in distinctive currency pairs:
        depths = {}
        for currency_pair in distinctive_currency_pairs:
            depth = digifinex.depth(currency_pair)
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