from packages import digifinex as DIGIFINEX
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)

currency_pair=CURRENCYPAIR.CurrencyPair('btc','usdt')
# ticker=digifinex.ticker()
# depth=digifinex.depth(currency_pair)
balance=digifinex.balances()

# trades=aex.trades(currency_pair)
# orderInfo=aex.submit_order(2,currency_pair,100000,0.01)
# cancleOrderResult=aex.cancel_order(currency_pair,'29207338')
# orderList=aex.order_list(currency_pair)
# tradeList=aex.trade_list(currency_pair)

a=1

