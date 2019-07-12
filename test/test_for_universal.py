import sys
sys.path.append("..")
from packages import aex as AEX
from packages import digifinex as DIGIFINEX
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
from packages import universal
import time

account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)
currency_pair=CP.CurrencyPair('btc','usdt')


# test for Depth.filter-------------------------------------------------------------------------------------
# t1=time.time()
# depths=[]
# for cnt in range(0,2):
#     depth=digifinex.depth(currency_pair)
#     time.sleep(1)
#     depths.append(depth)
# t2=time.time()
# import copy
# depth0=copy.deepcopy(depths[0])
# print(t2-t1)
# depth=universal.Depth.filter(depths)
# t3=time.time()
# print(t3-t2)
# test for Depth.filter-------------------------------------------------------------------------------------

# test for Depth.update----------------------------------------------------------------------
asks=[]
bids=[]
for cnt in range(0,5):
    ask=universal.Ask(cnt+5.1,1)
    asks.append(ask)
    bid=universal.Bid(-cnt+5-0.1,1)
    bids.append(bid)
depth0=universal.Depth('test',currency_pair,None,bids,asks)
asks=[]
bids=[]
for cnt in range(0,5):
    ask=universal.Ask(cnt+5.1,2)
    asks.append(ask)
    bid=universal.Bid(1+0.5*cnt,2)
    bids.append(bid)
depth1 = universal.Depth('test', currency_pair, None, bids, asks)

depth2=depth0.update(depth1)
# test for Depth.update----------------------------------------------------------------------


# test for Depth.get_supporting_points----------------------------------------------------------------------
# depth=digifinex.depth(currency_pair)
# supporting_points1=universal.Depth.get_supporting_points(depth,'vol',1)
# supporting_points10=universal.Depth.get_supporting_points(depth,'vol',2)
# supporting_points50=universal.Depth.get_supporting_points(depth,'vol',5)
# supporting_points100=universal.Depth.get_supporting_points(depth,'vol',8)
# test for Depth.get_supporting_points----------------------------------------------------------------------

a=1
