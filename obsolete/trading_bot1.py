# coding=utf-8

from OKEx import okex
from packages import account
import time

# test 1, plot a 2-dimension array
# arr=([1,2,3],[5,7,4])
# plt.plot(arr)
# plt.show()

# test 2, plot 2 lines
# x = [1,2,3]
# y = [5,7,4]
#
# x2 = [1,2,3]
# y2 = [10,14,12]
#
# plt.xlabel('Plot Number')
# plt.ylabel('Important var')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
#
# plt.plot(x,y, label='1st line')
# plt.plot(x2,y2, label='2nd line')
# plt.show()

# test 3, bar graph
# plt.bar([1,3,5,7,9],[5,2,7,8,2], label="Example one", color='r')
#
# plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
# plt.legend()
# plt.xlabel('bar number')
# plt.ylabel('bar height')
#
# plt.title('Epic Graph\nAnother Line! Whoa')
#
# plt.show()

# test 4, scatter graph
#
# x = [1,2,3,4,5,6,7,8]
# y = [5,2,4,2,1,4,5,2]
#
# plt.scatter(x,y, label='skitscat', color='k', s=25, marker="o")
#
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()

# mysql_manager=mysqlAPI.MySQLManager('root','caichong','okex')
# results=mysql_manager.execute('select * from trades_OKEx_bch_btc_01')
# X1=[]
# Y1=[]
# Z1=[]
# X2=[]
# Y2=[]
# cnt1=0
# cnt2=0
# total_buy=0
# total_sell=0
#
# for result in results:
#     t=result[3]
#     if t==1:
#         X1.append(cnt1)
#         Y1.append(result[5])
#         cnt1+=1
#         total_buy+=result[4]
#     else:
#         X2.append(cnt2)
#         Y2.append(result[5])
#         cnt2+=1
#         total_sell+=result[4]
#
#
# print(total_sell, total_buy)


#
def build_batch_data(param):
    # "[{price:10001.1,amount:0.01,type:'sell'},"
    # "{price:10002.2,amount:0.01,type:'sell'}]"
    # data=json.dumps(param, sort_keys=True)
    link=","
    seq=[]
    for item in param:
        seq.append("{price:" + str(item["price"]) + ",amount:" + str(item["amount"]) + ",type:'" + item["type"] + "'}")
    data="[" + link.join(seq) +"]"

    return data

def cancel_previous_orders():
    result=okex1.order_list(currency_pair)
    for order in result.orders:
        if order.status==0 or order.status==1:
            okex1.cancel_order(currency_pair,order.id)

def cancel_all_orders(account, orders):
    # inquire my account occasionally, if there are any pending orders, cancel all
    import time
    global currency_pair
    if int(time.time()) % 60 == 0:
        cancel_previous_orders()
    # cancel the orders, that are created last time
    if len(orders)>0:
        for order in orders:
            okex1.cancel_order(currency_pair,order.id)


def summit_orders(account,prices):
    # clarify the account situation, and reallocate money to different usage:
    global my_info
    my_info=okex1.balances()
    free_btc=float(my_info.free["btc"])
    free_bch=float(my_info.free["bch"])
    frozen_btc=float(my_info.frozen["btc"])
    frozen_bch=float(my_info.frozen["bch"])
    my_bid=prices[0]
    my_ask=prices[1]

    # use free btc to buy bch
    bid_amount=free_btc/my_bid-0.001
    # use free bch to sell for btc
    ask_amount=free_bch-0.001

    # param=[]
    # if bid_amount>0.001:
    #     o=okex1.submit_order(currency_pair=currency_pair,type="buy",price=my_bid,amount=bid_amount)
    #     if o.message=="操作成功":
    #         orders.append(o)
    # if ask_amount>0.001:
    #     p=okex1.submit_order(currency_pair=currency_pair,type="sell",price=my_ask,amount=ask_amount)
    #     if p.message=="操作成功":
    #         orders.append(p)

def if_price_changed():
    pass


currency_pair='bch_btc'
previous_bid=0
previous_ask=999

account= account.Account("test")
okex1= okex.OKEx(account)
my_info=okex1.balances()
ask_order=None
bid_order=None
account.set_balance(my_info)

cancel_previous_orders()
while True:
    depth=okex1.depth(currency_pair)
    ask0=depth.asks[0].price
    bid0=depth.bids[0].price
    my_ask=999
    my_bid=0

    # determine the offering price:
    if ask0-bid0<=0.00000002:
        my_ask=ask0
        my_bid=bid0
    else:
        my_ask=ask0-0.00000001
        my_bid=bid0+0.00000001

    # determine the balance:
    my_info=okex1.balances()
    free_btc=float(my_info.free["btc"])
    free_bch=float(my_info.free["bch"])
    frozen_btc=float(my_info.frozen["btc"])
    frozen_bch=float(my_info.frozen["bch"])

    # use free btc to buy bch
    bid_amount=free_btc/my_bid-0.001
    # use free bch to sell for btc
    ask_amount=free_bch-0.001

    if previous_ask==my_ask:
        print("the ask price stays no change, skip the round")
    else:
        # cancel pending orders
        if ask_order!=None:
            okex1.cancel_order(currency_pair,ask_order.order_id)
        # submit new orders
        if ask_amount>=0.001:
            ask_order = okex1.submit_order(currency_pair=currency_pair,type="sell",price=my_ask,amount=ask_amount)
            previous_ask=my_ask
            print("sell:\tprice: %f\tamount: %f" % ( ask_order.price, ask_order.amount))
    if previous_bid==my_bid:
        print("the bid price stays no change, skip the round")
    else:
        # cancel pending orders
        if bid_order!=None:
            okex1.cancel_order(currency_pair,bid_order.order_id)
        # submit new orders
        if bid_amount>=0.001:
            bid_order = okex1.submit_order(currency_pair=currency_pair,type="buy",price=my_bid,amount=bid_amount)
            previous_bid=my_bid
            print("buy:\tprice: %f\tamount: %f" % ( bid_order.price, bid_order.amount))
    time.sleep(2)
