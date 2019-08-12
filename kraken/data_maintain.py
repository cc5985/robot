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

currency_pair=CURRENCYPAIR.CurrencyPair('btc','usd')
fees=KRAKEN.Kraken.get_fees(volume=200000)


def digest_data(interval=86400):
    _name_map='XXBT'+'Z'+currency_pair.reference.upper()
    table_name = 'trades_' + currency_pair.base + '_' + currency_pair.reference + '_kraken'

    rows=pgmanager.select('select max(timestamp) from '+table_name)
    if rows[0][0] is None:
        starting_timestamp=int(1546272000)*10**9
    else:
        starting_timestamp=int(rows[0][0])*10**9
    if interval==0:
        ending_timestamp=int(time.time()*10**9)
    else:
        ending_timestamp=int(starting_timestamp/(10**9)+interval)*10**9
    trades=[]
    cnt=0
    while starting_timestamp<ending_timestamp-1000:
        _trades=kraken.trades(currency_pair,since=starting_timestamp,raw=True)
        symbol=KRAKEN.make_currency_pair_string_for_restful(currency_pair)
        _trades=json.loads(_trades)
        _trades=_trades['result'][_name_map]
        trades.extend(_trades)
        starting_timestamp=(int(_trades[-1][2])*10**9)
        local_time = time.gmtime(starting_timestamp/(10**9))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        print(str(otherStyleTime))
        cnt+=1
        time.sleep(6)

    sqls=[]
    for trade in trades:
        param={
            'timestamp':int(trade[2]),
            'tid':None,
            'price':trade[0],
            'amount':trade[1],
            'trade_type':1 if trade[3]=='b' else 0,
            'status':2,
            'order_type':trade[4]
        }
        sqls.append(param)

    pgmanager.execute_many(
        "insert into " + table_name + "(timestamp,tid,price,amount,trade_type,status,order_type) values(%(timestamp)s,%(tid)s,%(price)s,%(amount)s,%(trade_type)s,%(status)s,%(order_type)s)",sqls)

for i in range(20):
    digest_data(10000)