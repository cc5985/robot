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
import math
import copy
from packages import digifinex as DIGIFINEX
from packages import currency_pair as CP

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
            if market=='digifinex':
                result=json.loads(result)
                self.order_id = ""
                if result['code']==0:
                    self.order_id=result['order_id']
                    self.price = params["price"]
                    self.amount = params["amount"]
                    self.type = params["type"]
                    self.message = "操作成功"
                else:
                    self.message = error_code.Error_code_for_DigiFinex[result["code"]]
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
        if market=='digifinex':
            result=json.loads(result)
            if result['code']==0:
                self.orders=[]
                for order in result['orders']:
                    currency_pair=CP.CurrencyPair(str(order['symbol']).split('_')[1],str(order['symbol']).split('_')[0])
                    id=order['order_id']
                    price=float(order['price'])
                    total_amount=float(order['amount'])
                    trade_amount=float(order['executed_amount'])
                    status=int(order['status'])
                    trade_price=float(order['avg_price'])
                    trade_money=float(order['cash_amount'])
                    trade_type = (1 if order["type"] == "buy" else 0)
                    this_order = SubmittedOrder(currency_pair, id, price, status, total_amount, trade_amount,
                                                trade_money, trade_price, trade_type)
                    self.orders.append(this_order)
                self.message='操作成功'
            else:
                self.message=error_code.Error_code_for_DigiFinex[result['code']]

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
        if market=="digifinex":
            result=json.loads(result)
            if result['code']==0:
                self.message='操作成功'
                self.successful_orders_ids=result['success']
                self.failed_orders_ids = result['error']
            else:
                self.failed_orders_ids=order_id
                self.message=error_code.Error_code_for_DigiFinex[result['code']]

class Order:
    def __init__(self,price , amount):
        self.price=float(price)
        self.amount=float(amount)


class Bid(Order):
    pass

class Ask(Order):
    pass


class Depth(object):
    @classmethod
    def filter(cls, depths):
        '''
        by analyzing several depths, this method determines a Depth instance that is most likely to be an accurate one
        which filters out the flash orders
        :param depths: a list of depths which is ordered by time
        :return: A Depth instance
        '''
        num_depths=len(depths)
        asks=[]
        bids=[]


        # record every price
        for bid in depths[0].bids:
            price=bid.price
            amount=bid.amount
            weight=1  # after having iterated all bids of other depths and find a bid that has the same price as this one, flag+=1
            for cnt in range(1,len(depths)):
                for bid1 in depths[cnt].bids:
                    if bid1.price==price:
                        amount=min(amount,bid1.amount)
                        weight+=1
            if weight==len(depths):
                bids.append(Bid(price,amount))


        for ask in depths[0].asks:
            price = ask.price
            amount = ask.amount
            weight = 1  # after having iterated all bids of other depths and find a bid that has the same price as this one, flag+=1
            for cnt in range(1, len(depths)):
                for ask1 in depths[cnt].asks:
                    if ask1.price == price:
                        amount = min(amount, ask1.amount)
                        weight += 1
            if weight == len(depths):
                asks.append(Ask(price, amount))

        result_depth=Depth(
            market=depths[0].market,
            currency_pair=depths[0].currency_pair,
            result= None,
            asks=asks,
            bids=bids
        )
        return result_depth
        pass

    @classmethod
    def get_supporting_points(cls, depth, weighted_by='vol', distance=1):
        acc_bid_vol = 0
        acc_ask_vol = 0
        cnt = 0
        bid_price = depth.bids[-1].price  # in case can not find a proper point, set this price to a very distant price in the 1st place
        ask_price = depth.asks[-1].price
        for bid in depth.bids:
            acc_bid_vol += bid.amount
            if acc_bid_vol >= distance:
                bid_price = bid.price
                break
        for ask in depth.asks:
            acc_ask_vol += ask.amount
            if acc_ask_vol >= distance:
                ask_price = ask.price
                break
        supporting_points = [bid_price, ask_price]
        return supporting_points
        pass

    def __init__(self, market, currency_pair, result=None, bids=[],asks=[]):
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
        if result is None:
            self.bids = bids
            self.asks = asks
            self.timestamp = int(time.time())
            self.market = market
            self.currency_pair = currency_pair
            self.message = "True"
            return
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
            elif market=="kraken":

                bss=[]
                ass=[]
                if result.__contains__('as'):
                    ass=result['as']
                if result.__contains__('a'):
                    ass=result['a']
                if result.__contains__('bs'):
                    bss=result['bs']
                if result.__contains__('b'):
                    bss=result['b']
                for b in bss:
                    bid=Bid(b[0],b[1])
                    self.bids.append(bid)
                for a in ass:
                    ask=Ask(a[0],a[1])
                    self.asks.append(ask)

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

    def __add__(self, other):
        '''
        untested!!!!!
        :param other:
        :return:
        '''
        import copy
        this=copy.deepcopy(self)
        if other.currency_pair.toString()!=this.currency_pair.toString():
            raise Exception('Depths of different currency pairs can not be added')
        this.bids.extend(other.bids)
        this.asks.extend(other.asks)
        this.bids.sort(key=lambda x:x.price, reverse=True)
        this.asks.sort(key=lambda x:x.price, reverse=True)
        return this

    def update(self, other):
        '''
        PASSED
        update self.bids and self.asks with items in other.bids or asks
        :param other:
        :return:
        '''
        if other.currency_pair.toString()!=self.currency_pair.toString():
            raise Exception('Depths of different currency pairs can not be added')
        this=copy.deepcopy(self)
        for ask in other.asks:
            price=ask.price
            amount=ask.amount
            flag=False
            for ask1 in this.asks:
                if ask1.price==price:
                    ask1.amount=amount
                    flag=True
                    continue
            if flag==False:
                this.asks.append(ask)
        this.asks=list(filter(lambda x:x.amount!=0, this.asks))
        this.asks.sort(key=lambda x:x.price, reverse=False)

        for bid in other.bids:
            price=bid.price
            amount=bid.amount
            flag=False
            for bid1 in this.bids:
                if bid1.price==price:
                    bid1.amount=amount
                    flag=True
            if flag==False:
                this.bids.append(bid)
        this.bids = list(filter(lambda x: x.amount != 0, this.bids))
        this.bids.sort(key=lambda x: x.price, reverse=True)
        return this

    def is_consumed_by(self,trades):
        for trade in trades.trades:
            price=trade.price
            amount=trade.amount
            trade_type=trade.trade_type
            if trade_type==1:
                for ask in self.asks:
                    if abs(ask.price-price)<0.000001:
                        ask.amount-=amount
            else:
                for bid in self.bids:
                    if abs(bid.price-price)<0.000001:
                        bid.amount-=amount
        return self
        # def get_supporting_points(self, weighted_by=None, distance=1, referencial_currency=''):
    #     CONSTANT=1
    #     if referencial_currency=='usdt':
    #         CONSTANT=10000
    #     supporting_points=[0,0]
    #     if weighted_by==None:
    #         ask0=self.asks[0].price
    #         bid0=self.bids[0].price
    #         my_ask=99999
    #         my_bid=0
    #
    #         if ask0-bid0<=0.00000002*CONSTANT:
    #             my_ask=ask0
    #             my_bid=bid0
    #         else:
    #             my_ask=ask0-0.00000001*CONSTANT
    #             my_bid=bid0+0.00000001*CONSTANT
    #         return [my_bid,my_ask]
    #     elif weighted_by=="vol":
    #         acc_bid_vol=0
    #         acc_ask_vol=0
    #         cnt=0
    #         bid_price=self.bids[-1].price  # in case can not find a proper point, set this price to a very distant price in the 1st place
    #         ask_price=self.asks[-1].price
    #         for bid in self.bids:
    #             acc_bid_vol+=bid.amount
    #             if acc_bid_vol>=distance:
    #                 bid_price=bid.price
    #                 break
    #         for ask in self.asks:
    #             acc_ask_vol+=ask.amount
    #             if acc_ask_vol>=distance:
    #                 ask_price=ask.price
    #                 break
    #         supporting_points=[bid_price,ask_price]
    #         return supporting_points
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
        self.amount = float(amount)
        self.price =float(price)
        self.trade_type=int(trade_type)
        self.tid=tid
        self.status=status

class Trades:
    '''
    this class represents a series of trades, whose attribute trades is an array of TradeInfo instances
    this class has 3 data members: :market, :currency, :trades, message
    '''
    
    @classmethod
    def statistics(cls, trades):

        sum_price=0
        total_amount=0
        num_of_transactions=0
        num_of_buying_transactions=0
        num_of_selling_transactions=0
        accumulated_buying_amount=0
        accumulated_selling_amount=0
        accumulated_price=0
        accumulated_buying_price=0
        accumulated_selling_price=0
        timespan=trades.trades[0].timestamp-trades.trades[-1].timestamp
        for trade in trades.trades:
            num_of_transactions+=1
            sum_price+=trade.price
            total_amount+=trade.amount
            accumulated_price+=trade.price*trade.amount
            if trade.trade_type==1:
                num_of_buying_transactions+=1
                accumulated_buying_amount+=trade.amount
                accumulated_buying_price+=trade.price*trade.amount
            else:
                num_of_selling_transactions+=1
                accumulated_selling_amount+=trade.amount
                accumulated_selling_price+=trade.amount*trade.price


        avg_price_by_amount= accumulated_price/total_amount
        avg_buy_by_amount= accumulated_buying_price/accumulated_buying_amount
        avg_sell_by_amount= accumulated_selling_price/accumulated_selling_amount
        buying_amount= accumulated_buying_amount
        selling_amount= accumulated_selling_amount
        avg_amount_by_transaction= total_amount/len(trades.trades)
        result = {
            'avg_price_by_amount': avg_price_by_amount,
            'avg_buy_by_amount': avg_buy_by_amount,
            'avg_sell_by_amount': avg_sell_by_amount,
            'total_amount': total_amount,
            'buying_amount': buying_amount,
            'selling_amount': selling_amount,
            'avg_amount_by_transaction': avg_amount_by_transaction,
            'avg_amount_per_second':total_amount/timespan
        }
        return result
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
                result=json.loads(result)
                for item in result:
                    if str(item["type"])=='buy':
                        trade_type=1
                    else:
                        trade_type=0
                    price=float(item['price'])
                    amount=float(item['amount'])
                    date= item['date']
                    tid=int(item['tid'])
                    trade=TradeInfo(date,price,amount,trade_type,tid,status)
                    self.trades.append(trade)
                self.message="操作成功"
                self.trades.reverse()
            if market=="digifinex":
                result=json.loads(result)['data']
                for item in result:
                    if str(item["type"])=='buy':
                        trade_type=1
                    else:
                        trade_type=0
                    price=float(item['price'])
                    amount=float(item['amount'])
                    date= item['date']
                    tid=int(item['id'])
                    trade=TradeInfo(date,price,amount,trade_type,tid,status)
                    self.trades.append(trade)
                self.message="操作成功"
                # self.trades.reverse()
            if market=='kraken':
                for item in result:
                    price=item[0]
                    amount=item[1]
                    date=item[2]
                    tid=None
                    if item[3]=='b':
                        trade_type=1
                    else:
                        trade_type=0
                    status=2
                    trade=TradeInfo(date,price,amount,trade_type,tid,status)
                    self.trades.append(trade)
                self.message="操作成功"
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

class CurrencyPairInfos:
    def __init__(self, market, result):
        # currency_pair, amount_precision, price_precision, minimum_amount=None, minimum_money=None
        market = str(market).lower()
        if market == 'digifinex':
            self.currency_pair_infos={}
            result = json.loads(result)
            if result['code'] == 0:
                data = result['data']
                for key in data.keys():
                    __currencies=str(key).split('_')
                    currency_pair=CP.CurrencyPair(__currencies[1],__currencies[0])
                    amount_precision=data[key][0]
                    price_precision=data[key][1]
                    minimum_amount=data[key][2]
                    minimum_money=data[key][3]
                    currency_pair_info=CurrencyPairInfo(currency_pair,amount_precision,price_precision,minimum_amount,minimum_money)
                    self.currency_pair_infos[currency_pair.toString()]=currency_pair_info
                self.message = '操作成功'
            else:
                self.message = error_code.Error_code_for_DigiFinex[result['code']]

class CurrencyPairInfo:
    '''
    message:

    currency_pair: of CurrencyPair
    amount_precision: 数量精度
    price_precision: 价格精度
    minimum_amount: 最小下单数量
    minimum_money: 最小下单金额
    '''
    def __init__(self, currency_pair, amount_precision, price_precision, minimum_amount=None, minimum_money=None):
        self.currency_pair=currency_pair
        self.amount_precision=amount_precision
        self.price_precision=price_precision
        self.minimum_amount=minimum_amount
        self.minimum_money=minimum_money
