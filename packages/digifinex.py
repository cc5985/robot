# -*- coding: UTF-8 -*-
import json
import time
import requests

from packages import error_code as ERRORCODE
from packages import exchange as EXCHANGE
from packages import universal


# 根据 CurrencyPair 实例构造一个request的字符串
def make_currency_pair_string(currency_pair):
    # base = AEX.COINNAMEMAPPING.get(currency_pair.base, currency_pair.base)
    # reference = AEX.COINNAMEMAPPING.get(currency_pair.reference, currency_pair.reference)
    return  currency_pair.reference+'_'+currency_pair.base

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

class DigiFinex(EXCHANGE.Exchange):

    MARKET = 'DigiFinex'
    COINNAMEMAPPING={
        'cny':'cnc',
    }


    def __init__(self,account, base_url=None):
        self.account = account
        if not base_url is None:
            self.base_url = base_url
        else:
            self.base_url=EXCHANGE.Exchange.MARKET_BASEURL_MAPPING['DigiFinex']

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

    def depth(self,currency_pair, limit=150, raw=False):
        # v2: https://openapi.digifinex.vip/v2/depth?symbol=usdt_btc&apiKey=59328e10e296a&timestamp=1410431266&sign=0a8d39b515fd8f3f8b848a4c459884c2
        # v3：https://openapi.digifinex.com/v3/order_book?market=btc_usdt&limit=30
        '''

        :param currency_pair:
        :param raw:
        :return:
        '''
        # there are 4 required params: symbol, apikey, timestamp, sign
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

    def trades(self, currency_pair, raw=False):
        # https://api.aex.zone/trades.php?c=btc&mk_type=cnc
        TRADES_RESOURCE = "/trades.php"
        params = make_currency_pair_string(currency_pair)
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
        from packages import util
        aex2 = util.Client(self.account.api_key, self.account.secret_key, self.user_id)
        result = aex2.submitOrder(type,currency_pair.reference,price,amount,currency_pair.base)
        type="buy" if type==1 else "sell"
        result = universal.OrderInfo(self.MARKET, currency_pair, result, {'price':price,'amount':amount,'type':type})
        return result

    def cancel_order(self,currency_pair,order_id):
        from packages import util
        aex2 = util.Client(self.account.api_key, self.account.secret_key, self.user_id)
        result = aex2.cancelOrder(currency_pair.reference,order_id,currency_pair.base)
        result = universal.CancelOrderResult(self.MARKET,currency_pair,result,order_id)
        return result

    def order_list(self,currency_pair, current_page=1, page_length=200):
        from packages import util
        aex2 = util.Client(self.account.api_key, self.account.secret_key, self.user_id)
        result = aex2.getOrderList(currency_pair.base,currency_pair.reference)
        result=universal.SubmittedOrderList(currency_pair,self.MARKET,result)
        return result

    def trade_list(self,currency_pair, current_page=1, page_length=200):
        from packages import util
        aex2 = util.Client(self.account.api_key, self.account.secret_key, self.user_id)
        result = aex2.getMyTradeList(currency_pair.reference,currency_pair.base,current_page)
        result = universal.Trades(self.MARKET, currency_pair,result,2, self.user_id)
        return result