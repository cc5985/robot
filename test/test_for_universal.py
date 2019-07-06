import sys
sys.path.append("..")
from packages import aex as AEX
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
from packages import universal
import time

USER_ID=472702
account=ACCOUNT.Account('426817f2228d6d8f485dff7b8a9aee71','41ebfb59508cd77031a25228758755dc10f566c18b19f13c52e39ca4c69d775f')
aex=AEX.AEX(account,USER_ID)
currency_pair=CP.CurrencyPair('btc','cny')

t1=time.time()
depths=[]
for cnt in range(0,5):
    depth=aex.depth(currency_pair)
    # time.sleep(1)
    depths.append(depth)
t2=time.time()
print(t2-t1)
depth=universal.Depth.filter(depths)
t3=time.time()
print(t3-t2)
a=1
