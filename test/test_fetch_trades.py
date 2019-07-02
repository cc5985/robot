#!/usr/bin/python
# -*- coding: UTF-8 -*-

from net import mysql_API
from packages import account
from OKEx import okex
import time

mysql_manager= mysql_API.MySQLManager("root", "caichong", "okex")
currencies=["bch","eth","itc"]
references=["btc"]
market="OKEx"
account= account.Account("test")
okex1= okex.OKEx(account)
currency_pair=currencies[0]+'_'+references[0]

# fetch trades data from okex.server using trade_history method:
last_tid=0


while True:
    results=okex1.trades(currency_pair)
    for result in results:
        timestamp= str(result['date'])
        tid= result['tid']
        type= ("1" if str(result['type'])=='buy' else "0")
        amount=str(result['amount'])
        price=str(result['price'])
        if tid>last_tid:
            sql_string='insert into trades_OKEx_bch_btc_01 values(NULL, ' + timestamp + "," + str(tid) + "," + type + "," + amount + "," + price +")"
            mysql_manager.insert_data(sql_string)
    time.sleep(1)
    last_tid=results[-1]['tid']

