# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import json
import time
import requests
import copy
from websocket import create_connection

from packages import error_code as ERRORCODE
from packages import exchange as EXCHANGE
from packages import universal


# 根据 CurrencyPair 实例构造一个request的字符串
def make_currency_pair_string(currency_pair):
    # base = AEX.COINNAMEMAPPING.get(currency_pair.base, currency_pair.base)
    # reference = AEX.COINNAMEMAPPING.get(currency_pair.reference, currency_pair.reference)
    result=Kraken.COINNAMEMAPPING.get(currency_pair.base,currency_pair.base) +'/' + Kraken.COINNAMEMAPPING.get(currency_pair.reference,currency_pair.reference)
    return result

def append_api_key(params, api_key):
    return params+'&apiKey=' + api_key

def sign(account, params):
    import hashlib
    import copy
    params['apiKey'] = account.api_key
    _params=copy.deepcopy(params)
    m = hashlib.md5()
    # params = {'symbol': 'usdt_btc', 'type': 'kline_1m', 'timestamp': TimeStampNow, 'apiKey': APIKEY, 'apiSecret': APISECRET}
    _params['apiSecrect']=account.secret_key
    _params['apiKey']=account.api_key
    keys = sorted(_params.keys())
    string = ''
    for key in keys:
        string = string + str(_params[key])
    m.update(string.encode(encoding='UTF-8'))
    encodestr = m.hexdigest()
    return encodestr

class Kraken(EXCHANGE.Exchange):

    MARKET = 'Kraken'
    COINNAMEMAPPING={
        'cny':'cnc',
        'btc':'XBT',
        'usdt':'USD'
    }


    def __init__(self,account, base_url=None):
        self.account = account
        if not base_url is None:
            self.base_url = base_url
        else:
            self.base_url=EXCHANGE.Exchange.MARKET_BASEURL_MAPPING['Kraken']
        self.is_depth_subscribed=False
        self.initialize_ws()

    def initialize_ws(self):
        for i in range(3):
            try:
                # wscat -c wss://ws.kraken.com/
                self.ws = create_connection(self.base_url)
                self.is_depth_subscribed=False
            except Exception as error:
                print('Caught this errr: ' + repr(error))
                time.sleep(3)
            else:
                break


    def _create_depth_link(self, currency_pair, limit=10):
        self._depth = universal.Depth('Kraken', currency_pair)
        pair=make_currency_pair_string(currency_pair)
        self.ws.send(json.dumps({
            "event": "subscribe",
            # "event": "ping",
            "pair": [pair],
            # "subscription": {"name": "ticker"}
            # "subscription": {"name": "spread"}
            # "subscription": {"name": "trade"}
            "subscription": {"name": "book", "depth": limit}
            # "subscription": {"name": "ohlc", "interval": 5}
        }))
        self.is_depth_subscribed=True
        self._on_reading_depth(currency_pair,limit)

    def _on_reading_depth(self,currency_pair,limit):
        self.responses=[]
        while True:
            try:
                result = self.ws.recv()
                self.responses.append(result)

            except Exception as error:
                print('Caught this error: ' + repr(error))
                time.sleep(3)


    def get_currency_pairs_info(self):
        # GET https://openapi.digifinex.vip/v2/trade_pairs?apiKey=59328e10e296a&timestamp=1410431266&sign=0a8d39b515fd8f3f8b848a4c459884c2
        INFO_RESOURCE='/v2/trade_pairs'
        params = {}
        params['timestamp'] = str(time.time())
        params['sign'] = sign(self.account, params)
        result = requests.get(self.base_url + INFO_RESOURCE, params)
        result = universal.CurrencyPairInfos(self.MARKET, result.text)
        return result

    def ticker(self, currency_pair=None):
        # https://openapi.digifinex.vip/v2/ticker?apiKey=15d12cfa0a69be
        # https://openapi.digifinex.vip/v2/ticker?symbol=usdt_btc&apiKey=15d12cfa0a69be
        TICKER_RESOURCE = "/v2/ticker"
        if currency_pair is None:
            params='apiKey=' + self.account.api_key
            result = requests.get(self.base_url + TICKER_RESOURCE, params)
            if result.status_code != 200:
                return ERRORCODE.Error_Code_For_Status_Code[result.status_code]
            result = json.loads(result.text)
            code = result['code']
            if code != 0:
                return ERRORCODE.Error_code_for_DigiFinex[code]  # 这里要重新写
            result = result['ticker']
            return result
        else:
            params ='symbol=' + make_currency_pair_string(currency_pair)
            params=append_api_key(params,self.account.api_key)
            result=requests.get(self.base_url+TICKER_RESOURCE,params)
            if result.status_code!=200:
                return ERRORCODE.Error_Code_For_Status_Code[result.status_code]
            result=json.loads(result.text)
            code=result['code']
            if code!=0:
                return ERRORCODE.Error_code_for_DigiFinex[code]  #这里要重新写
            # result=result['ticker'][make_currency_pair_string(currency_pair)]
            result = universal.Ticker(self.MARKET, currency_pair, result)
            return result

    def depth(self,currency_pair, limit=10, raw=False):
        # v2: https://openapi.digifinex.vip/v2/depth?symbol=usdt_btc&apiKey=59328e10e296a&timestamp=1410431266&sign=0a8d39b515fd8f3f8b848a4c459884c2
        # v3：https://openapi.digifinex.com/v3/order_book?market=btc_usdt&limit=30
        '''

        :param currency_pair:
        :param raw:
        :return:
        '''
        # there are 4 required params: symbol, apikey, timestamp, sign
        import threading
        while True:
            if self.is_depth_subscribed==False:
                thread=threading.Thread(target=self._create_depth_link,args=(currency_pair,limit))
                thread.start()
            else:
                # deal with self.responses:
                responses=copy.copy(self.responses)
                length=len(responses)
                for item in responses:
                    result=copy.deepcopy(item)
                    result = list(json.loads(result))
                    if len(result) < 2:
                        continue
                    if result[-2] == 'book-' + str(limit) and result[-1] == make_currency_pair_string(currency_pair):
                        _result = copy.deepcopy(result[1])
                        if isinstance(result[2], dict) == True:
                            _result.update(result[2])
                        _temp_depth = universal.Depth('Kraken', currency_pair, _result)
                        self._depth = self._depth.update(_temp_depth)
                self.responses=self.responses[length:]
                return self._depth


        DEPTH_RESOURCE = "/v3/order_book"
        symbol = make_currency_pair_string(currency_pair)
        # 下面的代码仅适用于v2版本的api
        # timestamp=str(int(time.time()))
        # _sign=sign(self.account,{
        #     'symbol':symbol,
        #     'timestamp':timestamp,
        # })
        # params={
        #     'symbol': symbol,
        #     'timestamp': timestamp,
        #     'apiKey':self.account.api_key,
        #     'sign':_sign
        # }
        params='market='+currency_pair.base+'_'+currency_pair.reference+'&limit='+str(limit)
        result = requests.get(self.base_url+DEPTH_RESOURCE,params)
        if result.status_code!=200:
            return ERRORCODE.Error_Code_For_Status_Code[result.status_code]
        if raw == True:
            return result.text
        else:
            result = universal.Depth(self.MARKET, currency_pair, result.text)
            return result

    def trades(self, currency_pair, limit=300, raw=False):
        # https://openapi.digifinex.com/v3/trades?market=btc_usdt&limit=30
        TRADES_RESOURCE = "/v3/trades"
        params = 'market=' + currency_pair.base + '_' + currency_pair.reference + '&limit=' + str(limit)
        result = requests.get(self.base_url + TRADES_RESOURCE, params)
        if result.status_code!=200:
            return ERRORCODE.Error_Code_For_Status_Code[result.status_code]
        if raw == True:
            return result.text
        else:
            result = universal.Trades(self.MARKET, currency_pair, result.text,2)
            return result

    def balances(self):
        # https://openapi.digifinex.vip/v2/myposition?apiKey=59328e10e296a&timestamp=1410431266&sign=0a8d39b515fd8f3f8b848a4c459884c2
        USERINFO_RESOURCE = "/v2/myposition"
        timestamp=int(time.time())
        params={
            'timestamp':timestamp
        }
        params['sign']=sign(self.account,params)
        result = requests.get(self.base_url + USERINFO_RESOURCE, params)
        result=universal.BalanceInfo(self.MARKET,result.text)
        return result

    def submit_order(self, type, currency_pair, price, amount):
        # https: // openapi.digifinex.vip / v2 / trade
        # POST参数:
        # symbol = usdt_btc
        # price = 6000.12
        # amount = 0.1
        # type = buy
        # apiKey = 59328e10e296a
        # timestamp = 1410431266
        # sign = 0a8d39b515fd8f3f8b848a4c459884c2
        SUBMITORDER_RESOURCE='/v2/trade'
        timestamp = int(time.time())
        type="buy" if (type==1 or type=='1' or str(type).lower()=="buy") else "sell"
        params = {
            'timestamp': timestamp,
            'type':type,
            'price':price,
            'amount':amount,
            'symbol':make_currency_pair_string(currency_pair)
        }
        params['sign'] = sign(self.account, params)
        result = requests.post(self.base_url + SUBMITORDER_RESOURCE, data=params)
        result = universal.OrderInfo(self.MARKET, currency_pair, result.text, {'price':price,'amount':amount,'type':type})
        return result

    def cancel_order(self,currency_pair,order_ids):
        # POST https: // openapi.digifinex.vip / v2 / cancel_order
        # POST参数:
        # order_id = 1000001, 1000002, 1000003
        # apiKey = 59328e10e296a
        # timestamp = 1410431266
        # sign = 0a8d39b515fd8f3f8b848a4c459884c2
        CANCEL_ORDER_RESOURCE = '/v2/cancel_order'
        timestamp = int(time.time())
        if isinstance(order_ids,str):
            _order_ids=order_ids
        if isinstance(order_ids,list):
            _order_ids = list(map(lambda x: str(x), order_ids))
            _order_ids = ','.join(_order_ids)

        params = {
            'timestamp': timestamp,
            'order_id': _order_ids,
        }
        params['sign'] = sign(self.account, params)
        result = requests.post(self.base_url + CANCEL_ORDER_RESOURCE, data=params)
        result = universal.CancelOrderResult(self.MARKET, currency_pair, result.text,order_ids)
        return result

    def order_list(self,currency_pair=None, current_page=1, page_length=200):
        # symbol, page, type are optional
        # https://openapi.digifinex.vip/v2/open_orders?symbol=usdt_btc&page=1&apiKey=59328e10e296a&timestamp=1410431266&sign=0a8d39b515fd8f3f8b848a4c459884c2

        ORDER_LIST_RESOURCE='/v2/open_orders'
        params={}
        params['timestamp']=str(time.time())
        if currency_pair:
            params['symbol']= make_currency_pair_string(currency_pair)
        if current_page:
            params['page']=str(current_page)
        params['sign']=sign(self.account,params)

        result = requests.get(self.base_url + ORDER_LIST_RESOURCE, params)
        result = universal.SubmittedOrderList(currency_pair, self.MARKET, result.text )
        return result

    def trade_list(self,currency_pair, current_page=1, page_length=200):
        # TO BE IMPLEMENTED
        pass