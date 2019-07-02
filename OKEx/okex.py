# it's highly suggested to use ENGLISH only in this project
# encoding=utf-8
from packages import universal
import time
from OKEx.HttpMD5Util import buildMySign,httpGet,httpPost

class OKEx:

    __market="OKEx"

    def __init__(self,account, base_url = 'www.okex.com'):
        "account represents a key pair, base_url represents the prefix of the restFUL resources"
        self.account=account
        self.base_url=base_url

    # 获取OKCOIN现货行情信息
    def ticker(self, currency_pair='btc_usdt'):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        result= universal.Ticker(self.__market, currency_pair, httpGet(self.base_url, TICKER_RESOURCE, params))
        return result

    # 获取OKCOIN现货市场深度信息
    def depth(self, currency_pair='btc_usdt', raw=True):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        result=httpGet(self.base_url, DEPTH_RESOURCE, params)
        if raw==False:
            return result
        else:
            result= universal.Depth(self.__market, currency_pair, result)
            return result

    # 获取OKCOIN现货历史交易信息
    def trades(self, currency_pair=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        result=httpGet(self.base_url, TRADES_RESOURCE, params)
        result= universal.Trades(self.__market, currency_pair, result, 2)
        return result

    # 获取用户现货账户信息
    def balances(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.account.api_key
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=httpPost(self.base_url, USERINFO_RESOURCE, params)
        result= universal.BalanceInfo(self.__market, result)
        return result

    # 现货交易
    def submit_order(self, type="buy", currency_pair='btc_usdt',  price='', amount=''):
        if type==1 or type=="1" or type.lower()=="buy":
            type="buy"
        else:
            type="sell"
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'type': type
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount
        p=params.copy()
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=httpPost(self.base_url, TRADE_RESOURCE, params)
        result= universal.OrderInfo(self.__market, currency_pair, result, p)
        return result

    #现货取消订单
    def cancel_order(self,currency_pair,order_id):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key':self.account.api_key,
            'symbol':currency_pair,
            'order_id':order_id
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        return httpPost(self.base_url,CANCEL_ORDER_RESOURCE,params)

    #现货订单信息查询, 此方法为独享方法
    def orderinfo(self,symbol,orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'order_id':orderId
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,ORDER_INFO_RESOURCE,params)

    # order_list这个方法是取得未成交订单的列表！
    def order_list(self,currency_pair, current_page=1, page_length=200):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'status': 0,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=httpPost(self.base_url, ORDER_HISTORY_RESOURCE, params)
        result= universal.SubmittedOrderList(currency_pair,self.__market, result)
        return result

    # trade_list这个方法是取得已成交订单的列表！
    def trade_list(self,currency_pair, current_page=1, page_length=200):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'status': 1,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = buildMySign(params, self.account.secret_key)
        return httpPost(self.base_url, ORDER_HISTORY_RESOURCE, params)

    #现货批量下单
    def batch_trade(self,currency_pair,type,orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key':self.account.api_key,
            'symbol':currency_pair,
            'type':type,
            'orders_data':orders_data
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        result=httpPost(self.base_url,BATCH_TRADE_RESOURCE,params)
        # print(result)
        # result=universal.OrderInfo(currency_pair,result,{})
        return result

    # 获取OKEx币币K线数据
    def k_line(self, currency_pair, interval='1min', size=None):
        KLINE_RESOURCE = "/api/v1/kline.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s&type=%(interval)s' % {'symbol': currency_pair, 'interval': interval}
        result=httpGet(self.base_url, KLINE_RESOURCE, params)
        result= universal.Klines(self.__market, currency_pair, result)
        return result

    def trade_history(self, currency_pair, since):
        TRADE_HISTORY_RESOURCE="/api/v1/trade_history.do"
        params={
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'since': since,
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        return httpPost(self.base_url, TRADE_HISTORY_RESOURCE, params)

    def get_all_currencies(self):
        import json
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.account.api_key
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=json.loads(httpPost(self.base_url, USERINFO_RESOURCE, params))
        result=result["info"]["funds"]["free"]
        result=dict(result).keys()
        currencies=[]
        for item in result:
            currencies.append(item)
        return currencies

    def get_all_currency_pairs(self):
        from packages import currency_pair
        currencies=self.get_all_currencies()
        references= currency_pair.CurrencyPair().get_referencial_currencies("okex")
        currency_pairs=[]
        for reference in references:
            for currency in currencies:
                if str(currency).lower()!=str(reference).lower():
                    currency_pairs.append(str(currency)+"_"+str(reference))
        return currency_pairs

    def get_currency_pair_order(self, top_n=10, ordered_by="trading volume"):
        '''
        this method returns a list of currency pairs ordered by trading volume
        :param top_n: how many currency pairs you want to list
        :param ordered_by: either of 'trading volume', 'market cap', 'price', etc.
        :return: a list of currency pairs ordered by trading volume
        '''
        # get all the currency pairs:
        from packages import currency_pair as cp
        all_currency_pairs=self.get_all_currency_pairs()

        # get the ratio of ref1 to usdt
        cp1=cp.CurrencyPair()
        referencial_currencies=cp1.get_referencial_currencies("okex")
        prices_of_referencial_currencies={}
        for currency in referencial_currencies:
            if currency!="usdt":
                ticker=self.ticker(currency+"_usdt")
                price=ticker.last
                prices_of_referencial_currencies[ticker.currency_pair]=price

        tickers=[]
        turn_volumes={}

        for currency_pair in all_currency_pairs:
            referencial_currency=cp1.get_referencial_currency(str(currency_pair))
            time.sleep(0.1)
            ticker=self.ticker(currency_pair)
            if referencial_currency!="usdt":
                if ticker.message=="True" or "'操作成功'":
                    turn_volume=(ticker.high+ticker.low)*ticker.vol*prices_of_referencial_currencies[referencial_currency+"_usdt"]/2
                    turn_volumes[ticker.currency_pair]=turn_volume
            else:
                if ticker.message=="True" or "'操作成功'":
                    turn_volume=(ticker.high+ticker.low)*ticker.vol*1/2
                    turn_volumes[ticker.currency_pair]=turn_volume

        turn_volumes=sorted(turn_volumes.items(), key=lambda x:x[1], reverse=True)
        return turn_volumes[:top_n-1]

    def determine_the_tid_of_a_timestamp(self, currency_pair, target_timestamp):
        '''
        because the trade_history method takes only a tid param, you have to calculate this value in the first place
        :param timestamp:
        :return: a long value, repre tid
        '''
        # 0. initialize some vals:
        import json
        import time
        cnt=0

        # 1. get the current tid using trade  method
        result=self.trades(currency_pair)
        tid_now=int(result[0]['tid'])
        current_timestamp=int(result[0]['date'])

        result=self.trade_history(currency_pair,1)
        result=json.loads(result)
        result=result[0]
        tid0=int(result['tid'])
        tid=tid0
        current_timestamp=int(result['date'])

        # 2. using binary chop algo to generate a candidate tid whose corresponding timestamp should be compared with the target timestamp which is stated in the params

        # 2.1 calculate the stroke counts per second
        # find the current timestamp, and the initial timestamp, and tid
        diff=int(time.time())-current_timestamp
        estimated_stroke_count_per_second=tid_now/diff # 425tid/second

        print(diff, estimated_stroke_count_per_second)
        diff=target_timestamp-current_timestamp
        try:
            while abs(diff)>100:
                print(cnt)
                tid+=int((diff)*estimated_stroke_count_per_second)
                # elif abs(diff)>8640:
                #     tid+=int(((diff)*estimated_stroke_count_per_second)/1.6)
                # elif abs(diff)>864:
                #     tid+=int(((diff)*estimated_stroke_count_per_second)/1.8)
                # elif abs(diff)>20:
                #     tid+=int(((diff)*estimated_stroke_count_per_second)/2)
                result=self.trade_history(currency_pair,tid)
                print(result)
                result=json.loads(result)
                result=result[0]
                tid=int(result['tid'])
                current_timestamp=int(result['date'])
                cnt+=1
                diff=target_timestamp-current_timestamp
                print("now is: " + str(time.gmtime(current_timestamp)))
                print(diff)
                time.sleep(1)

        except Exception as e:
            print(e)
        print(result)
        print(tid,current_timestamp)
        return tid-1000

    def determine_best_currency_pairs(self,top_n=10):
        '''
        we should consider the trading volume, which has a weight of 20%, of the last 600 trades
        we should consider the depth gap, which has a weight of 20%, of the last 10 seconds snapshot
        we should consider the
        :param top_n:
        :return:
        '''
        # get all currency pair trading vol of last 600 trades using ticker method:
        from packages import currency_pair as cp
        all_currency_pairs=self.get_all_currency_pairs()

        # get the ratio of ref1 to usdt
        cp1=cp.CurrencyPair()
        referencial_currencies=cp1.get_referencial_currencies("okex")
        prices_of_referencial_currencies={}
        for currency in referencial_currencies:
            if currency!="usdt":
                ticker=self.ticker(currency+"_usdt")
                price=ticker.last
                prices_of_referencial_currencies[ticker.currency_pair]=price



        currency_pair_trading_vol_list={}
        for currency_pair in all_currency_pairs:
            trades=self.trades(currency_pair)
            buy_volume_in_past_2_minute=0
            sell_volume_in_past_2_minute=0
            total_volume_in_past_2_minute=0
            for trade in trades.trades:
                trade_type=trade.trade_type
                timestamp=trade.timestamp
                if int(time.time())-timestamp<=120:
                    if trade_type==1:
                        buy_volume_in_past_2_minute+=trade.amount
                    else:
                        sell_volume_in_past_2_minute+=trade.amount
                    total_volume_in_past_2_minute+=trade.amount
            # print(buy_volume_in_past_600_trades,sell_volume_in_past_600_trades)
            max_vol=max(sell_volume_in_past_2_minute,buy_volume_in_past_2_minute)
            min_vol=min(sell_volume_in_past_2_minute,buy_volume_in_past_2_minute)
            if total_volume_in_past_2_minute!=0 and min_vol/max_vol>0.5 and min_vol/max_vol<2:
                ratio_of_referencial_currency_to_usdt=1
                referencial_currency=cp1.get_referencial_currency(currency_pair)
                ratio_of_currency_to_referencial_currency=trades.trades[-1].price

                if referencial_currency!="usdt":
                    ratio_of_referencial_currency_to_usdt=prices_of_referencial_currencies[referencial_currency + '_usdt']
                turn_vol=total_volume_in_past_2_minute*ratio_of_currency_to_referencial_currency* ratio_of_referencial_currency_to_usdt
                currency_pair_trading_vol_list[currency_pair]=turn_vol

        currency_pair_trading_vol_list=sorted(currency_pair_trading_vol_list.items(), key=lambda x:x[1], reverse=True)
        a=1
        # for each of the currency:



