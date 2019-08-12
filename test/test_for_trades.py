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
        sql='select * from ' + table_name + ' order by timestamp asc'
    else:
        sql='select * from ' + table_name + ' order by timestamp asc limit ' + str(limit)
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

trades=digest_data_from_db(limit=0,agregational=False)
r=UNIVERSAL.Trades.sectionize(trades,10)
file=open('./section_' + _name_map + '_' + str(int(time.time()))+'.csv','w')
file.write(u'分段,总卖,总买\n')
for key in sorted(r['buy'].keys()):
    file.write(str(key)+','+str(r['buy'][key])+','+str(r['sell'][key])+'\n')
file.close()
# open a file with a name of statistics+timestamp.csv

a=1

