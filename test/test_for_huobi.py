import sys
sys.path.append("..")
from packages import huobi as HUOBI
from packages import account as ACCOUNT
from packages import currency_pair as CP

account=ACCOUNT.Account('577e4a03-540f9610-f686d434-qz5c4v5b6n','dd7b02f5-c286e9d4-f2cc78c3-bfab3')
huobi=HUOBI.Huobi(account)

currency_pair=CP.CurrencyPair('btc','usdt')
depth=huobi.depth(currency_pair)
a=1

