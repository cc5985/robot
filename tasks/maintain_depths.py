import sys
sys.path.append("..")

from threading import Thread
import time
import json
from packages import timer as TIMER
from packages import db as DB
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

pgmanager=DB.PGManager(database='quantum', user='cc5985', pw='Caichong416', host='localhost', port='5432')

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
# exchanges=[bittrex,zb]
currency_pair=CP.CurrencyPair('btc','usdt')
depths=[]
def add_to_depths(exchange,currency_pair):
    global depths
    t0=time.time()
    depth=exchange.depth(currency_pair)
    t0=time.time()-t0
    # print('Time used for fetching data on ', depth.market, ' takes ', t0)
    depths.append(depth)

def main():
    global depths
    t00=time.time()
    threads=[]
    depths=[]
    invalid_exchanges=[]
    for exchange in exchanges:
        thread=Thread(target=add_to_depths,args=(exchange,currency_pair))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    timestamp=time.time()
    for depth in depths:
        if len(depth.asks)>0:
            j={
                'asks':[],
                'bids':[]
            }
            for ask in depth.asks:
                j['asks'].append([ask.price,ask.amount])
            for bid in depth.bids:
                j['bids'].append([bid.price,bid.amount])
            j=json.dumps(j)
            t0=time.time()
            pgmanager.execute("insert into depths ( market, timestamp, depth) values('"+depth.market+"',"+str(timestamp)+",'"+j+"')")
            # print('%-10s'%depth.market,' uses ' ,'%-10s'%str(time.time()-t0),' to do insertion, the total length of depth json is ',len(j))
        else:
            invalid_exchanges.append(depth.market)
            print('%-10s'%depth.market,depth.market,' does not support usdt pair')

    print('This round uses ', time.time()-t00, ' seconds. And invalid exchanges are: ', invalid_exchanges)

timer=TIMER.Timer(10,main)
timer.run()