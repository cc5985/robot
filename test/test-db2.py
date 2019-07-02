from net import ssh, mysql_API
from packages import account, currency_pair
from OKEx import okex

market="OKEx"
currency_pairs=[]
account= account.Account("test")
okex1= okex.OKEx(account)
currency_pair_of_bch_usdt= currency_pair.CurrencyPair('bch', 'usdt').get_currency_pair()
currencies=["bch","eth","itc"]
references=["btc"]
mysql_local_manager= mysql_API.MySQLManager("root", "caichong", "okex", "localhost")
date="0102"

for item1 in currencies:
    for item2 in references:
        currency_pairs.append(item1 + "_" + item2)

server1= ssh.SSHServer()
server1.start()
mysql_manager= mysql_API.MySQLManager(user_name="root", password="caichong", schema="okex", target_server_ip="127.0.0.1", port=server1.server.local_bind_port)
length={}
for currency_pair in currency_pairs:
    sql_string='select count(*) from depth_OKEx_' + currency_pair + '_' +date
    result=mysql_manager.execute(sql_string)[0][0]
    length[currency_pair]=result

for currency_pair in currency_pairs:
    pointer=0
    while pointer<=length[currency_pair]-5:
        import time
        print(time.time())
        sql_string='select * from depth_OKEx_' + currency_pair + '_' + date + ' where id>=' + str(1+pointer) + ' and ' + ' id<=' +str(5+pointer)
        results=mysql_manager.execute(sql_string)
        for result in results:
            result=(str(result))
            sql_string="insert into " + 'depth_OKEx_' + currency_pair + '_' + date + " values" +result
            mysql_local_manager.insert_data(sql_string)
        print(time.time())
        pointer+=5

# sql_string='select * from depth_OKEx_itc_btc_0102'
# result=mysql_manager.execute(sql_string)
# print(result)
server1.stop()
