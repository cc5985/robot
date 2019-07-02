# encoding=utf-8
# this project is powered by Jeff Omega
# as author is a newbie to python, code style of this project is rubyish
# as a convention, class name is capitalized and instance is lower-cased
# and this project is migrated from btc38_1 project which is forked from
# a btc38 gem from github

import sys
sys.path.append("..")
from packages import error_code
import json
import time
from packages import digifinex as DIGIFINEX

class OrderInfo:
    def __init__(self,market, currency_pair, result, params):
        try:
            market=str(market).lower()
            if market=='okex':
                result=json.loads(result)
                self.order_id=""
                if result.__contains__("result") and result["result"]==True:
                    self.order_id=result["order_id"]
                    self.price=params["price"]
                    self.amount=params["amount"]
                    self.type=params["type"]
                    self.message="操作成功"
                else:
                    self.message= error_code.Error_code_for_OKEx[result["error_code"]]
                    self.message=result["error_code"]
            if market=='aex':
                self.order_id = ""
                if len(result)>0 :
                    if str(result[0]).find('succ')!=-1:
                        result=str(result[0],'utf-8')
                        self.order_id = result.split('|')[1]
                        self.price = params["price"]
                        self.amount = params["amount"]
                        self.type = params["type"]
                        self.message = "操作成功"
                    if str(result[0]).find('overBalance')!=-1:
                        self.message = "操作失败，余额不足"
                else:
                    self.message = error_code.Error_code_for_OKEx[result["error_code"]]
                    self.message = result["error_code"]
        except Exception as e:
            self.order_ids=[]
            self.message=e

#  this class represents the orders that you HAVE already submitted,
# NOT the orders you are submitting!!!
class SubmittedOrderList:
    def __init__(self,currency_pair,market,result):
        market=str(market).lower()
        if market=='okex':
            result=json.loads(result)
            if result.__contains__("result") and result["result"]==True:
                if result.__contains__("total"):
                    self.orders=[]
                    self.total=result["total"]
                    orders=result["orders"]
                    for order in orders:
                        currency_pair=order["symbol"]
                        id=int(order["order_id"])
                        price=float(order["price"])
                        total_amount=float(order["amount"])
                        trade_amount=float(order["deal_amount"])
                        status=int(order["status"])
                        trade_price=float(order["avg_price"])
                        trade_money=trade_amount*trade_price
                        trade_type=(1 if order["type"]=="buy" else 0)
                        this_order=SubmittedOrder(currency_pair,id,price,status,total_amount,trade_amount,trade_money,trade_price,trade_type)
                        self.orders.append(this_order)
                        self.message="操作成功"
            else:
                self.message= error_code.Error_code_for_OKEx[result["error_code"]]
        if market=='aex':
            # TODO: 下面的遍历中的SubmittedOrder实例化方法传参不太对，需要对原始数据进行详尽分析才能正确生成
            if len(result)>=0:
                self.orders = []
                self.total = len(result)
                for order in result:
                    order_=json.loads(str(order,'utf-8'))[0]
                    id=order_['id']
                    price=float(order_['price'])
                    amount=float(order_['amount'])
                    type=int(order_['type'])
                    this_order=SubmittedOrder(currency_pair,id,price,0,amount,amount,0,price,type)
                    self.orders.append(this_order)
                self.message='操作成功'
            else:
                self.message= error_code.Error_code_for_OKEx[result["error_code"]]

class SubmittedOrder:
    def __init__(self, currency_pair, id, price, status, total_amount,
                 trade_amount,  trade_money, trade_price, trade_type):
        self.currency_pair=currency_pair
        self.id=id
        self.price=price
        self.status=status
        self.total_amount =total_amount
        self.trade_amount=trade_amount
        self.trade_money=trade_money
        self.trade_price=trade_price
        self.trade_type=trade_type

class CancelOrderResult:
    def __init__(self, market, currency_pair, result, order_id):
        self.currency_pair=currency_pair
        market=str(market).lower()
        if market=="chbtc":
            pass
        if market=="okex":
            result = json.loads(result)
            if result.__contains__("result"):
                self.result=True
                self.message="操作成功"
                self.id=order_id
            else:
                self.result=False
                self.message= error_code.Error_code_for_OKEx[result["error_code"]]
                self.id=order_id
        if market=="aex":
            if len(result)==0:
                self.result = False
                self.message = "操作失败"
                self.id = order_id
            else:
                result=str(result[0],'utf-8')
                if result.find('succ')!=-1:
                    self.result=True
                    self.message="操作成功"
                    self.id=order_id
                else:
                    self.result=False
                    self.message= error_code.Error_code_for_OKEx[result["error_code"]]
                    self.id=order_id

class Order:
    def __init__(self,price , amount):
        self.price=price
        self.amount=amount


class Bid(Order):
    pass

class Ask(Order):
    pass


class Depth(object):
    def __init__(self, market, currency_pair, result):
        '''
        the Depth class instance has the following data members:
        bids:  Array of Bid
        asks:  Array of Ask
        timestamp:  Long
        message:  String
        market:  String
        currency_pair:  String
        :param market:  represents which market you are in
        :param currency_pair: represents which currency pair you are trading with
        :param result: represents the json that the server returns to you
        '''
        self.bids=[]
        self.asks=[]
        self.timestamp=int(time.time())
        self.market=market
        self.currency_pair=currency_pair
        self.message="True"
        try:
            market=str(market).lower()
            # result=json.loads(str(result))
            if market=="okex":
                if dict(result).__contains__("asks"):
                    bss=result['bids']  # the bids object in the json
                    ass=result['asks']  # the asks object in the json
                    for b in bss:
                        bid=Bid(b[0],b[1])
                        self.bids.append(bid)
                    for a in ass:
                        ask=Ask(a[0],a[1])
                        self.asks.append(ask)
                    self.asks.reverse()
                elif dict(result).__contains__("error_code"):
                    self.message= error_code.Error_code_for_OKEx[result["error_code"]]
            elif market=="chbtc":
                pass
            elif market=="aex":
                result = json.loads(str(result))
                if result.__contains__("asks"):
                    bss=result['bids']  # the bids object in the json
                    ass=result['asks']  # the asks object in the json
                    for b in bss:
                        bid=Bid(b[0],b[1])
                        self.bids.append(bid)
                    for a in ass:
                        ask=Ask(a[0],a[1])
                        self.asks.append(ask)
                elif dict(result).__contains__("error_code"):
                    self.message= error_code.Error_code_for_OKEx[result["error_code"]]
            elif market=="digifinex":
                result = json.loads(str(result))
                self.timestamp = result['date']
                self.message = "操作成功"

                bss=result['bids']  # the bids object in the json
                ass=result['asks']  # the asks object in the json
                for b in bss:
                    bid=Bid(b[0],b[1])
                    self.bids.append(bid)
                for a in ass:
                    ask=Ask(a[0],a[1])
                    self.asks.append(ask)
                self.asks.reverse()
        except Exception as e:
            self.message=e
        finally:
            pass

    def __sub__(self, other):
        import copy
        result=copy.deepcopy(self)
        size_of_bids=len(result.bids)
        size_of_asks=len(result.asks)
        if other.__class__ is Depth:
            for bid in other.bids:
                price=bid.price
                amount=bid.amount
                cnt=0
                while cnt<size_of_bids:
                    if result.bids[cnt].price==price:
                        result.bids[cnt].amount-=amount
                    cnt+=1

            for ask in other.asks:
                price=ask.price
                amount=ask.amount
                cnt=0
                while cnt<size_of_asks:
                    if result.asks[cnt].price==price:
                        result.asks[cnt].amount-=amount
                    cnt+=1
        else:
            pass

    def get_supporting_points(self, weighted_by=None, distance=1, referencial_currency=''):
        CONSTANT=1
        if referencial_currency=='usdt':
            CONSTANT=10000
        supporting_points=[0,0]
        if weighted_by==None:
            ask0=self.asks[0].price
            bid0=self.bids[0].price
            my_ask=99999
            my_bid=0

            if ask0-bid0<=0.00000002*CONSTANT:
                my_ask=ask0
                my_bid=bid0
            else:
                my_ask=ask0-0.00000001*CONSTANT
                my_bid=bid0+0.00000001*CONSTANT
            return [my_bid,my_ask]
        elif weighted_by=="vol":
            acc_bid_vol=0
            acc_ask_vol=0
            cnt=0
            bid_price=self.bids[-1].price  # in case can not find a proper point, set this price to a very distant price in the 1st place
            ask_price=self.asks[-1].price
            for bid in self.bids:
                acc_bid_vol+=bid.amount
                if acc_bid_vol>=distance:
                    bid_price=bid.price
                    break
            for ask in self.asks:
                acc_ask_vol+=ask.amount
                if acc_ask_vol>=distance:
                    ask_price=ask.price
                    break
            supporting_points=[bid_price,ask_price]
            return supporting_points
    '''
    here distance means accumulated amount, e.g:
    bid0: 0.1
    bid1: 0.05
    bid2: 0.11
    bid3: 0.07
    here, if the distance is 0.2, 
    bid0+bid1+bid2 is just beyond the distance, then
    the price of bid3 is the target price
    
    but when you think about it, you dont really need this function,
    because before long, you would use tensorflow as the backend to
    calculate and deduce the pattern, then this strategy is useless!
    
    but anyway, you have to use this function before you implement this into tensorflow...............
    '''

class Kline:
    def __init__(self,o ,c , h, l, v, timestamp):
        self.open=o
        self.close=c
        self.high=h
        self.low=l
        self.vol=v
        self.timestamp=timestamp


class Klines:
    def __init__(self, market, currency_pair, result):
        self.market=market
        self.currency_pair=currency_pair
        self.message='Unknow error'
        self.klines=[]
        try:
            for item in result:
                kline=Kline(timestamp=item[0],o=item[1],h=item[2],l=item[3],c=item[4],v=item[5])
                self.klines.append(kline)
            self.message='操作成功'
        except:
            error_key=result["error_code"]
            self.message= error_code.Error_code_for_OKEx[error_key]


class Ticker(object):
    # :market, :currency, :timestamp, :high,
    # :low, :last, :vol, :buy, :sell, :message

    def __init__(self, market, currency_pair, result):
        if str(market).lower()=='okex':
            try:
                self.market = market
                self.currency_pair = currency_pair
                if dict(result).__contains__("ticker"):
                    ticker = result["ticker"]
                    self.buy = float(ticker["buy"])
                    self.sell = float(ticker["sell"])
                    self.vol = float(ticker["vol"])
                    self.high = float(ticker["high"])
                    self.low = float(ticker["low"])
                    self.last = float(ticker["last"])
                    self.timestamp = int(result["date"])
                    self.message = "操作成功"
                elif dict(result).__contains__("error_code"):
                    self.buy = 0
                    self.sell = 0
                    self.vol = 0
                    self.high = 0
                    self.low = 0
                    self.last = 0
                    self.timestamp = 0
                    error_key = result["error_code"]
                    self.message = error_code.Error_code_for_OKEx[error_key]
            except Exception as e:
                self.message = e
        if str(market).lower()=='digifinex':
            try:
                self.market = market
                self.currency_pair = currency_pair
                self.timestamp=result['date']
                ticker=result['ticker'][DIGIFINEX.make_currency_pair_string(currency_pair)]
                self.buy = float(ticker["buy"])
                self.sell = float(ticker["sell"])
                self.vol = float(ticker["vol"])
                self.high = float(ticker["high"])
                self.low = float(ticker["low"])
                self.last = float(ticker["last"])
                self.message = "操作成功"

            except Exception as e:
                self.message = e
        if str(market).lower()=='aex':
            try:
                self.market = market
                self.currency_pair = currency_pair
                result=json.loads(result)
                if result.__contains__("ticker"):
                    ticker = result["ticker"]
                    self.buy = float(ticker["buy"])
                    self.sell = float(ticker["sell"])
                    self.vol = float(ticker["vol"])
                    self.high = float(ticker["high"])
                    self.low = float(ticker["low"])
                    self.last = float(ticker["last"])
                    self.timestamp = int(time.time())
                    self.message = "操作成功"
                elif dict(result).__contains__("error_code"):
                    self.buy = 0
                    self.sell = 0
                    self.vol = 0
                    self.high = 0
                    self.low = 0
                    self.last = 0
                    self.timestamp = 0
                    error_key = result["error_code"]
                    self.message = error_code.Error_code_for_OKEx[error_key]
            except Exception as e:
                self.message = e



class TradeInfo:
    '''
    :timestamp, :price, :amount, :trade_type, :tid
    '''
    def __init__(self,timestamp, price, amount, trade_type, tid, status=-999):
        '''

        :param timestamp:
        :param price:
        :param amount:
        :param trade_type:
        :param tid:
        :param status: -1 for drawn, 0 for pending, 1 for partially traded, 2 for complete, 3 for 撤单处理中
        -999 for unknown
        '''
        self.timestamp = timestamp
        self.amount = amount
        self.price = price
        self.trade_type=trade_type
        self.tid=tid
        self.status=status

class Trades:
    '''
    this class represents a series of trades, whose attribute trades is an array of TradeInfo instances
    this class has 3 data members: :market, :currency, :trades, message
    '''

    def __init__(self,market, currency_pair, result, status, user_id=None):
        self.market=market
        self.currency_pair=currency_pair
        self.trades=[]
        market=str(market).lower()
        try:
            if market=="okex":
                result = list(result)
                for item in result:
                    if item["type"]=="buy":
                        trade_type=1
                    else:
                        trade_type=0
                    trade=TradeInfo(item["date"],item["price"],item["amount"],trade_type,item["tid"],status)
                    self.trades.append(trade)
                self.message="操作成功"
            if market=="aex":
                for item in result:
                    if str(item["buyer_id"])==str(user_id):
                        trade_type=1
                    else:
                        trade_type=0
                    price=float(item['price'])
                    amount=float(item['volume'])
                    date= int(time.mktime(time.strptime(item['time'], '%Y-%m-%d %H:%M:%S')))
                    tid=int(item['id'])
                    trade=TradeInfo(date,price,amount,trade_type,tid,status)
                    self.trades.append(trade)
                self.message="操作成功"
                self.trades.sort()
        except Exception as e:
            self.message=e

class BalanceInfo:
    '''
                :timestamp, :market, :total_asset, :net_asset, :free_cny,:free_btc,:frozen_btc,:free_ltc,:free_bcc,:free_eth,:free_etc,:free_bts,:free_hsr,
                :free_eos,:frozen_cny,:frozen_ltc,:frozen_bcc,:frozen_eth,:frozen_etc,:frozen_bts,:frozen_hsr,:frozen_eos,
                :free_usdt, :frozen_usdt, :free_bch, :frozen_bch, :free_btg, :frozen_btg, :free_gas , :frozen_gas, :free_zec , :frozen_zec, :free_neo , :frozen_neo,
                :free_iota , :frozen_iota, :free_gnt , :frozen_gnt, :free_snt , :frozen_snt, :free_dash , :frozen_dash , :free_xuc , :frozen_xuc, :free_qtum , :frozen_qtum,
                :free_omg , :frozen_omg,
                :message
    this is bewildering....
    fuck that....
    BalanceInfo class should have the following data members:
    1. timestamp
    2. market
    3. total_asset
    4. net_asset
    5. free
    6. frozen
    7. message
    '''

    def __init__(self, market, result):
        self.timestamp=int(time.time())
        self.market=market
        self.free={}
        self.frozen={}
        market=str(market).lower()
        try:
            if market=="okex":
                result=json.loads(result)
                if result["result"]==True:
                    self.message="操作成功"
                    self.free=result["info"]["funds"]["free"]
                    self.free.pop("bcc")
                    self.frozen=result["info"]["funds"]["freezed"]
                    self.frozen.pop("bcc")
                else:
                    self.message= error_code.Error_code_for_OKEx[dict(result)["error_code"]]
            if market=="digifinex":
                result=json.loads(result)
                if result["code"]==0:
                    self.message="操作成功"
                    self.free=result["free"]
                    self.frozen=result["frozen"]
                else:
                    self.message= error_code.Error_code_for_DigiFinex[result["code"]]
            if market=="aex":
                if len(result)>0:
                    self.message="操作成功"
                    for key in result.keys():
                        if str(key).endswith('_lock'):
                            self.frozen[key] = result[key]
                        else:
                            self.free[key] = result[key]
                else:
                    self.message= error_code.Error_code_for_OKEx[dict(result)["error_code"]]
        except Exception as e:
            self.message=e
