# PASSED

import sys
sys.path.append("..")
from packages import digifinex as DIGIFINEX
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)

currency_pair=CURRENCYPAIR.CurrencyPair('btc','usdt')
# currency_pair_infos=digifinex.get_currency_pairs_info()
# ticker=digifinex.ticker(currency_pair)
# depth=digifinex.depth(currency_pair)
balance=digifinex.balances()
trades=digifinex.trades(currency_pair)

# orderInfo=digifinex.submit_order(1,currency_pair,100.01,0.1)
# cancleOrderResult=digifinex.cancel_order(currency_pair,'c442b066a18cf3ee9059fc712ea647c2')
# orderList=digifinex.order_list(currency_pair)
# tradeList=aex.trade_list(currency_pair)

a=1

