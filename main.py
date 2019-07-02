# coding=utf-8
from packages import account, currency_pair
from OKEx import okex
import time

# initialize account, okex instance, mysql interface

market="OKEx"
account= account.Account("test")
okex1= okex.OKEx(account)
currency_pair_of_bch_usdt= currency_pair.CurrencyPair('bch', 'usdt').get_currency_pair()

# initialize the currency pairs:
currency_pairs=[]
currencies=["bch","eth","itc"]
references=["btc"]

'''
for item1 in currencies:
    for item2 in references:
        currency_pairs.append(item1 + "_" + item2)

def determine_table_name(market, currency_pair):
    localtime=time.localtime()
    table_name="depth_"+ market +"_" + currency_pair + "_" + str( localtime[1]).rjust(2,"0") + str(localtime[2]).rjust(2,"0")
    return table_name


# 1. create the schema


# 2. create the datatables, and the corresponding columns
'''




t1=time.time()
# for vnt in range(1,11):
#     t2=time.time()
#     depth=okex1.depth(currency_pair_of_bch_usdt,False)
#     t3=time.time()
#     depth=json.dumps(depth)
#     sql_string="insert into test4 values(null," + str(int(t3)) +",'" +currency_pair_of_bch_usdt + "','"+ str(depth) +"')"
#     mysql_manager.insert_data(sql_string)
#     t4=time.time()
#     print("get takes: %s \tinsertion takes: %s" % (str(t3-t2), str(t4-t3)))

# def job_func():
#     try:
#         t=0
#         mysql_manager=mysql_API.MySQLManager("root","caichong","okex")
#         for currency_pair in currency_pairs:
#             depth=okex1.depth(currency_pair,False)
#             depth=json.dumps(depth)
#             table_name=determine_table_name("OKEx",currency_pair)
#             t=int(time.time())
#             sql_string="insert into " + table_name + " values(null," + str(t) +",'" +currency_pair + "','"+ str(depth) +"')"
#             mysql_manager.insert_data(sql_string)
#         print(t)
#         mysql_manager.close()
#     except Exception as e:
#         print(e)
#         print(depth)
#         print(sql_string)
#
#
# sched=BlockingScheduler()
# sched.add_job(job_func,  'interval', max_instances=20,seconds=1)
# sched.start()

# 1. get the 50 currency pairs which have the most trading vol:
top_50_currency_pairs_in_trading_vol=okex1.get_currency_pair_order(50)
for item in top_50_currency_pairs_in_trading_vol:
    print(item[0] + '\t' + str(item[1]))

# choose the top 3 ones,
currency_pairs=[item[0],item[1],item[2]]

# run robot1
