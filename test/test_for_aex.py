from packages import aex as AEX
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
account=ACCOUNT.Account('426817f2228d6d8f485dff7b8a9aee71','41ebfb59508cd77031a25228758755dc10f566c18b19f13c52e39ca4c69d775f')
aex=AEX.AEX(account,472702)

currency_pair=CURRENCYPAIR.CurrencyPair('btc','cny')
# ticker=aex.ticker(currency_pair)
# depth=aex.depth(currency_pair)
# trades=aex.trades(currency_pair)
# balance=aex.balances()
# orderInfo=aex.submit_order(2,currency_pair,100000,0.01)
# cancleOrderResult=aex.cancel_order(currency_pair,'29207338')
# orderList=aex.order_list(currency_pair)
tradeList=aex.trade_list(currency_pair)

a=1

