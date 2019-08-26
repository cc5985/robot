import sys
sys.path.append("..")
from packages import bittrex as BT
from packages import account as ACCOUNT
from packages import currency_pair as CP

account=ACCOUNT.Account('577e4a03-540f9610-f686d434-qz5c4v5b6n','dd7b02f5-c286e9d4-f2cc78c3-bfab3')
bt=BT.Bittrex(account)

currency_pair=CP.CurrencyPair('btc','usdt')
depth=bt.depth(currency_pair)
a=1

