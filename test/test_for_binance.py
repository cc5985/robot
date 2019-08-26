import sys
sys.path.append("..")
from packages import binance as BINANCE
from packages import account as ACCOUNT
from packages import currency_pair as CP

account=ACCOUNT.Account('gBAyXDQx4SWJ1FKI5cG4xaYJVwTNnMWUVcrvHjNVAKjxmt0JrpLpowQ85Kg49Ak9','EZaHgc67HCNeniUGiLbTBHZJyYsq5MyVPuwOugXUSeTz1mKma1wWaPm3yTeAN7En')
binance=BINANCE.Binance(account)

currency_pair=CP.CurrencyPair('btc','usdt')
depth=binance.depth(currency_pair)
a=1

