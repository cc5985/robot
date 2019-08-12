# PASSED
# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import time
import requests
import json
from packages import kraken as KRAKEN
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
from packages import universal as UNIVERSAL

# pgmanager
from packages import db as DB
import CONSTANTS
pgmanager=DB.PGManager(**CONSTANTS.DB_CONNECT_ARGS_LOCAL)


account=ACCOUNT.Account('26q2SGG+j42h3PlrA2g2IWfynAQ+YsIAKWrQ6ms2es5GTSQjnTXbuguB','LkpL2am9qfRWA6f3ZPAJqytCHrNk9m9XdQlu5bx95PFzvHh1/e+heb2gKgsSrQ3mfQXUiRQksmqvUEsDgKmIFQ==')
kraken=KRAKEN.Kraken(account)

currency_pair=CURRENCYPAIR.CurrencyPair('btc','usdt')
currency_pair=CURRENCYPAIR.CurrencyPair('btc','eur')
_name_map='XXBT'+'Z'+currency_pair.reference.upper()
table_name = 'trades_' + currency_pair.base + '_' + currency_pair.reference + '_kraken'

# balance=kraken.balances()
# orderInfo=kraken.submit_order(0,currency_pair,15550.1,0.02)
# cancleOrderResult=kraken.cancel_order(currency_pair,'OCOEAM-QIU63-DSPAU3')
tradeVolume=kraken.trades_volume()
# currency_pair_infos=kraken.get_currency_pairs_info()
fees=KRAKEN.Kraken.get_fees(volume=tradeVolume)
# ticker=kraken.ticker(currency_pair)
starting_timestamp=int((time.time()-3600*240)*10**9)
ending_timestamp=int((time.time()-100)*10**9)
cnt=0

def digest_data_from_db(limit=0, agregational=False):
    trades = UNIVERSAL.Trades('kraken', currency_pair, None, None)
    if limit==0:
        sql='select * from ' + table_name + ' order by timestamp desc'
    else:
        sql='select * from ' + table_name + ' order by timestamp desc limit ' + str(limit)
    rows=pgmanager.select(sql)

    previous_trade=UNIVERSAL.TradeInfo(0,0,0,0,None,2)
    for row in rows:
        date=row[6]
        price=float(row[1])
        amount=float(row[2])
        trade_type=row[3]
        tid=None
        status=2
        if agregational==True:
            if date == previous_trade.timestamp and trade_type == previous_trade.trade_type:
                price = (previous_trade.price * previous_trade.amount + amount * price) / (
                            previous_trade.amount + amount)
                amount += previous_trade.amount
                previous_trade = UNIVERSAL.TradeInfo(date, price, amount, trade_type, tid, status)
            else:
                import copy
                trade = copy.deepcopy(previous_trade)
                trades.trades.append(trade)
                previous_trade = copy.deepcopy(UNIVERSAL.TradeInfo(date, price, amount, trade_type, tid, status))
        else:
            trade = UNIVERSAL.TradeInfo(date, price, amount, trade_type, tid, status)
            trades.trades.append(trade)
    trades.trades.pop(0)
    return trades

for limit in [100000,200000,400000,0]:
    trades=digest_data_from_db(limit=limit,agregational=False)
    statistics=UNIVERSAL.Trades.statistics(trades,'')

    # open a file with a name of statistics+timestamp.csv

    file=open('./statistics_' + _name_map + '_' + str(int(time.time()))+'.csv','w')
    for key in statistics.keys():
        if not isinstance(statistics[key],dict):
            file.write(str(key)+','+str(statistics[key])+'\n')
    file.write('\n\n')
    file.write(u'分段,均卖,均买,总卖,总买,总卖*均卖,总买*均买,价差,总买卖下限,利润\n')
    for key in statistics['avg_sell_by_section_amount'].keys():
        section=str(key)
        avg_sell=statistics['avg_sell_by_section_amount'][key]
        avg_buy=statistics['avg_buy_by_section_amount'][key]
        amount_sell=statistics['total_sell_amount_by_section_amount'][key]
        amount_buy=statistics['total_buy_amount_by_section_amount'][key]
        diff=avg_buy-avg_sell
        profit=diff*(min(amount_sell,amount_buy))
        file.write(section + ',' + str(avg_sell) + ',' + str(avg_buy) + ','
                   + str(amount_sell) + ',' + str(amount_buy) + ','
                   + str(avg_sell*amount_sell) + ','
                   + str(avg_buy*amount_buy) + ','
                   + str(diff) + ','
                   + str(min(amount_buy,amount_sell)) + ','
                   + str(profit) + '\n')
    file.close()

while True:
    try:
        t1=time.time()
        # trades = kraken.trades(currency_pair)
        depth=kraken.depth(currency_pair)

        t2=time.time()
        depth2=json.loads(requests.get('https://api.kraken.com/0/public/Depth?pair=xbtusd&count=10').text)
        t3=time.time()

        ask0=depth.asks[0].price
        ask1=float(depth2['result']['XXBTZUSD']['asks'][0][0])
        bid0=depth.bids[0].price
        bid1=float(depth2['result']['XXBTZUSD']['bids'][0][0])
        print('\n\n----------------------------------------------------------------------------')
        print('Diff of Asks=%s%%\t\tDiff of Bids=%s%%' % ((ask0-ask1)*100/ask1,(bid0-bid1)*100/bid1))
        print('ws=%s\t\trestful=%s'%(str(t2-t1),str(t3-t2)))
        print('----------------------------------------------------------------------------')

        time.sleep(5)
    except Exception as e:
        print(e)
# balance=kraken.balances()
# trades=kraken.trades(currency_pair)
# orderList=kraken.order_list(currency_pair)
# tradeList=aex.trade_list(currency_pair)

a=1

