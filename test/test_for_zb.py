import sys
sys.path.append("..")
import json
import time
from packages import zb as ZB
from packages import account as ACCOUNT
from packages import currency_pair as CP
from packages import db as DB


account=ACCOUNT.Account('577e4a03-540f9610-f686d434-qz5c4v5b6n','dd7b02f5-c286e9d4-f2cc78c3-bfab3')
zb=ZB.Zb(account)
pgmanager=DB.PGManager(database='quantum', user='cc5985', pw='Caichong416', host='localhost', port='5432')
currency_pair=CP.CurrencyPair('btc','usdt')


depth=zb.depth(currency_pair)
if len(depth.asks)>0:
    print('%-10s'%depth.market,"\t:",round(depth.asks[0].price,2),"\t",round(depth.bids[0].price,2))
else:
    print('%-10s'%depth.market,depth.market,' does not support usdt pair')

j={
    'asks':[],
    'bids':[]
}
for ask in depth.asks:
    j['asks'].append([ask.price,ask.amount])
for bid in depth.bids:
    j['bids'].append([bid.price,bid.amount])
j=json.dumps(j)
t0=time.time()
pgmanager.execute("insert into depths ( market, timestamp, depth) values('"+depth.market+"',"+str(depth.timestamp)+",'"+j+"')")
print(time.time()-t0)
# pgmanager.execute('insert into depths (id,market,timestamp,depth) values(NULL ,zb,1566888268,jfjfjf)')

a=1

