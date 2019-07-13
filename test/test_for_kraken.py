# PASSED

import sys
sys.path.append("..")
import time
import requests
import json
from packages import kraken as KRAKEN
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
kraken=KRAKEN.Kraken(account)

currency_pair=CURRENCYPAIR.CurrencyPair('btc','usdt')
# currency_pair_infos=kraken.get_currency_pairs_info()
# ticker=kraken.ticker(currency_pair)

while True:
    try:
        t1=time.time()
        trades = kraken.trades(currency_pair)
        depth=kraken.depth(currency_pair)

        t2=time.time()
        depth2=json.loads(requests.get('https://api.kraken.com/0/public/Depth?pair=xbtusd&count=10').text)
        t3=time.time()

        depth=depth.is_consumed_by(trades)
        # trades=trades.consume(depth)

        ask0=depth.asks[0].price
        ask1=float(depth2['result']['XXBTZUSD']['asks'][0][0])
        bid0=depth.bids[0].price
        bid1=float(depth2['result']['XXBTZUSD']['bids'][0][0])
        print('ask:%s\t\tbid:%s' % ((ask0-ask1)*100/ask1,(bid0-bid1)/bid1))
        print('1:%s\t\t2:%s'%(str(t2-t1),str(t3-t2)))
        time.sleep(5)
    except Exception as e:
        print(e)
# balance=kraken.balances()
# trades=kraken.trades(currency_pair)
# orderInfo=kraken.submit_order(1,currency_pair,100.01,0.1)
# cancleOrderResult=kraken.cancel_order(currency_pair,'c442b066a18cf3ee9059fc712ea647c2')
# orderList=kraken.order_list(currency_pair)
# tradeList=aex.trade_list(currency_pair)

a=1

