import sys
sys.path.append("..")
from packages import okex as OKEX
from packages import account as ACCOUNT
from packages import currency_pair as CP

account=ACCOUNT.Account('d956060d-0892-492c-bf31-20181aeaa09b','46E6B82DC46915C09614F2EF5C0DDAC4')
okex=OKEX.Okex(account)

currency_pair=CP.CurrencyPair('btc','usdt')
depth=okex.depth(currency_pair)
a=1

