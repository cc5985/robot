import sys
sys.path.append("..")
from packages import kucoin as KUCOIN
from packages import account as ACCOUNT
from packages import currency_pair as CP

account=ACCOUNT.Account('gBAyXDQx4SWJ1FKI5cG4xaYJVwTNnMWUVcrvHjNVAKjxmt0JrpLpowQ85Kg49Ak9','EZaHgc67HCNeniUGiLbTBHZJyYsq5MyVPuwOugXUSeTz1mKma1wWaPm3yTeAN7En')
kucoin=KUCOIN.Kucoin(account)

currency_pair=CP.CurrencyPair('btc','usdt')
depth=kucoin.depth(currency_pair)
a=1

