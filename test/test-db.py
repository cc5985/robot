#!/usr/bin/python
# -*- coding: UTF-8 -*-

from net import mysql_API

mysql_manager= mysql_API.MySQLManager("root", "caichong", "okex")

'''
basic funtion test for mysql_API
-------------------------------------------------------------------
# test for create a new table
# mysql_manager.create_table("test2","id int not null, age int")

# test for query
# result=mysql_manager.inquire("select * from table12")
# print(result.__class__)  # if successful: a tuple;  else bool
# print(result)

# test for insertion:
# result=mysql_manager.insert_data("insert into table1 (c1,c2) values (7,555) ")
# print(result.__class__)
# print(result)

# test for get the size of a sql schema
# result=mysql_API.MySQLManager.len_of_schema("test","MB")
# print(str(result) + " MB")

# test for get the size of a sql table :failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# result=mysql_manager.len_of_table("table1")
# print(result)
-------------------------------------------------------------------
'''

'''
# create tables 
-------------------------------------------------------------------
# 1. create 365 tables
# each of the tables represents the data set of A day, therefore, there should be 365 tables
# naming rules are as following:
#   1. depth_ ; 2. date_; 3. market

# the coding standard of Depth table:
# name= "depth_OKEx_" + str(month).rjust(2,"0") + str(day).rjust(2,"0")
# table structure of Depth table:

# create tables in database: okex
# _DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# string=""
# string="id int not null AUTO_INCREMENT, timestamp int, currency_pair varchar(15), data json,  PRIMARY KEY (id)"
# print(string)
# currencies=["bch","eth","itc"]
# references=["btc"]
#
# def create_tables(currency_name, reference_name):
#     for month in range(1,13):
#         days=_DAYS_IN_MONTH[month]
#     # print(str(month) + ": " + str(days))
#         for day in range(1,days+1):
#             table_name= "depth_OKEx_" + currency_name + "_" + reference_name + "_" + str(month).rjust(2,"0") + str(day).rjust(2,"0")
#             print(table_name)
#             mysql_manager.create_table(table_name,string)
#
# for currency in currencies:
#     for ref in references:
#         create_tables(currency,ref)

-------------------------------------------------------------------
'''

'''
# first calculate the tid of a given timestamp,
# then fetch trades from the tid:
# but this is not very efficient, because the API: trade_history has been obsolete in the okex interface
-------------------------------------------------------------------

# fetch trades data from okex.server using trade_history method:
import account
import okex
import time
import json
currencies=["btc","eth","itc"]
references=["usdt"]
market="OKEx"
account=account.Account("test")
okex1=okex.OKEx(account)

# timestamp_of_now=int(time.time())
# timestamp_of_target=int(time.mktime(time.strptime('2018-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')))
# okex1.determine_the_tid_of_a_timestamp(currencies[0] + '_' + references[0],timestamp_of_target)
# tid for 2018-1-1 0:0:0 is approximately: 93960502-1000=93959502
timestamp_start=int(time.mktime(time.strptime('2018-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')))
timestamp_end=int(time.mktime(time.strptime('2018-2-1 0:0:0', '%Y-%m-%d %H:%M:%S')))
current_timestamp=timestamp_start
currency_pair=currencies[0]+'_'+references[0]
current_tid=58632799   #93959502
while current_timestamp<timestamp_end:
    results=okex1.trade_history(currency_pair=currency_pair,since=current_tid)
    results=json.loads(results)
    print(results.__class__)
    for result in results:
        timestamp= str(result['date'])
        tid= str(result['tid'])
        type= (1 if str(result['type'])=='buy' else 0)
        amount=str(result['amount'])
        price=str(result['price'])
        sql_string='insert into trades_OKEx_bch_btc0101 values(NULL, '
        mysql_manager.insert_data(sql_string)


-------------------------------------------------------------------
'''
