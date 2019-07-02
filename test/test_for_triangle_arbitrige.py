from packages import currency_pair as CP
from packages import account as ACCOUNT
from strategies import triangle_arbitrage as TRI
import time
account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
currency_pairses=CP.CurrencyPair.find_triangle_arbitragable_currency_pairs('digifinex',account)

# eth_btc	btc_usdt	eth_usdt
tradable_currency_pairs=[
    CP.CurrencyPair('btc','usdt'),
    CP.CurrencyPair('xrp','usdt'),
    CP.CurrencyPair('xrp','btc')
]
strategy=TRI.TriangleArbitrage(account,'digifinex',tradable_currency_pairs,initial_funds={
    'btc':0.001,
    'xrp':0.001/0.00003578,
    'usdt':0.001*11404
})
while True:
    try:
        strategy.find_arbitrage_points()
        time.sleep(3)
    except Exception as e:
        print(e)
a=1