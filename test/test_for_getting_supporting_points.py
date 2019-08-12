import sys
sys.path.append("..")
from packages import aex as AEX
from packages import kraken as KRAKEN
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
from packages import universal
import time
import threading

account=ACCOUNT.Account('26q2SGG+j42h3PlrA2g2IWfynAQ+YsIAKWrQ6ms2es5GTSQjnTXbuguB','LkpL2am9qfRWA6f3ZPAJqytCHrNk9m9XdQlu5bx95PFzvHh1/e+heb2gKgsSrQ3mfQXUiRQksmqvUEsDgKmIFQ==')
kraken=KRAKEN.Kraken(account)
currency_pair=CP.CurrencyPair('btc','usdt')
TRADES=[]

def get_recent_trades(timestamp):
    global TRADES
    trades=kraken.trades(currency_pair)
    trades=trades.trades
    trades=list(filter(lambda x:x.timestamp>=timestamp, trades))
    TRADES=trades

def order_be_filled_in_trades(order, trades):
    for trade in trades:
        if order.trade_type==0:
            if trade.trade_type==1 and trade.price>=order.price:
                return True
        else:
            if trade.trade_type==0 and trade.price<=order.price:
                return True
    return False

while True:
    # test for Depth.filter-------------------------------------------------------------------------------------
    t1=time.time()
    # depths=[]
    # for cnt in range(0,15):
    #     depth=kraken.depth(currency_pair,100)
    #     time.sleep(0.14)
    #     depths.append(depth)
    # t2=time.time()
    # import copy
    # depth0=copy.deepcopy(depths[0])
    # print(t2-t1)
    # depth=universal.Depth.filter(depths)
    depth = kraken.depth(currency_pair, 100)

    supporting_points1=universal.Depth.get_supporting_points(depth,'price',11)
    local_time=time.gmtime(time.time())
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print(str(otherStyleTime)+'\t\tbid: '+str(supporting_points1[0])+'\t\task: '+str(supporting_points1[1]))
    orders=[]
    bid_order=universal.SubmittedOrder(currency_pair,None,supporting_points1[0],1,0.01,1,1,1,1)
    ask_order=universal.SubmittedOrder(currency_pair,None,supporting_points1[1],1,0.01,1,1,1,0)
    orders.append(bid_order)
    orders.append(ask_order)
    t3 = time.time()
    # assume you have submitted a set of orders....
    time.sleep(2)
    thread = threading.Thread(target=get_recent_trades, args=(t3,))
    thread.start()
    for order in orders:
        if order_be_filled_in_trades(order,TRADES)==True:
            print('order of ' + (' BID' if order.trade_type==1 else 'ASK') + ' has been filled at the price of ' + str(order.price))
    print()
    print()
a=1
