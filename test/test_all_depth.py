import sys
sys.path.append("..")

from threading import Thread
import time

from packages import account as ACCOUNT
from packages import currency_pair as CP

from packages import binance as BN
from packages import bitfinex as BF
from packages import bitso as BS
from packages import bitstamp as BST
from packages import bittrex as BTT
from packages import coinbase as CB
from packages import digifinex as DF
from packages import gate as G
from packages import huobi as HB
from packages import itbit as IB
from packages import kraken_rest1 as KK
from packages import kucoin as KC
from packages import liquid as LQ
from packages import okex as OK
from packages import poloniex as PL
from packages import zb as ZB

virtual_account=ACCOUNT.Account('','')
binance=BN.Binance(virtual_account)
bitfinex=BF.Bitfinex(virtual_account)
bitso=BS.Bitso(virtual_account)
bitstamp=BST.Bitstamp(virtual_account)
bittrex=BTT.Bittrex(virtual_account)
coinbase=CB.Coinbase(virtual_account)
digifinex=DF.DigiFinex(virtual_account)
gate=G.Gateio(virtual_account)
huobi=HB.Huobi(virtual_account)
itbit=IB.Itbit(virtual_account)
kraken=KK.KrakenRest(virtual_account)
kucoin=KC.Kucoin(virtual_account)
liquid=LQ.Liquid(virtual_account)
okex=OK.Okex(virtual_account)
poloniex=PL.Poloniex(virtual_account)
zb=ZB.Zb(virtual_account)

exchanges=[binance,bitfinex,bitso,bitstamp,bittrex,coinbase,digifinex,gate,huobi,itbit,kraken,kucoin,liquid,okex,poloniex,zb]
currency_pair=CP.CurrencyPair('btc','usdt')

threads=[]
depths=[]

def add_to_depths(exchange,currency_pair):
    global depths
    t0=time.time()
    depth=exchange.depth(currency_pair)
    t0=time.time()-t0
    print('Time used for fetching data on ', depth.market, ' takes ', t0)
    depths.append(depth)

print(time.time())
for exchange in exchanges:
    thread=Thread(target=add_to_depths,args=(exchange,currency_pair))
    threads.append(thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
for depth in depths:
    if len(depth.asks)>0:
        print('%-10s'%depth.market,"\t:",round(depth.asks[0].price,2),"\t",round(depth.bids[0].price,2))
    else:
        print('%-10s'%depth.market,depth.market,' does not support usdt pair')
print(time.time())