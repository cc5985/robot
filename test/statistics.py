import sys
sys.path.append("..")
from packages import digifinex as DIGIFINEX
from packages import aex as AEX
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
from packages import universal
import time

# test for aex-------------------------------------------------------
# USER_ID=472702
# account=ACCOUNT.Account('426817f2228d6d8f485dff7b8a9aee71','41ebfb59508cd77031a25228758755dc10f566c18b19f13c52e39ca4c69d775f')
# aex=AEX.AEX(account,USER_ID)
# currency_pair=CP.CurrencyPair('btc','usdt')
#
# t1=time.time()
# trades=aex.trades(currency_pair,6282136-500)
# statistics=universal.Trades.statistics(trades)
# ---------------------------------------------------------------------


# test for digifinex---------------------------------------------------
account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)
currency_pair=CP.CurrencyPair('btc','usdt')

t1=time.time()
trades=digifinex.trades(currency_pair)
statistics=universal.Trades.statistics(trades)
# ---------------------------------------------------------------------
a=1
