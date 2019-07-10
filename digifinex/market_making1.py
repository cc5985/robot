import sys
sys.path.append("..")
from packages import digifinex as DIGIFINEX
from packages import account as ACCOUNT
from packages import currency_pair as CURRENCYPAIR
from packages import universal as UNIVERSAL
import time
from threading import Thread

account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)

currency_pair=CURRENCYPAIR.CurrencyPair('ltc','usdt')

# global variables are defined here:
CURRENCY_PAIR_INFOS=None
PRICE_PRECISION={}
CHANGING_UNIT=None
MINIMUM_AMOUNT=None
INITIAL_FUNDS=None
FEES={
    'maker':0,
    'taker':0.002
}
depths=[]
balance=None
my_pending_orders=None

def initialize():
    # 0. read exchange-based constants
    global CURRENCY_PAIR_INFOS
    global PRICE_PRECISION
    global CHANGING_UNIT
    global MINIMUM_AMOUNT

    CURRENCY_PAIR_INFOS=digifinex.get_currency_pairs_info()
    PRICE_PRECISION[currency_pair.toString()]=CURRENCY_PAIR_INFOS.currency_pair_infos[currency_pair.toString()].price_precision
    CHANGING_UNIT=1*10**(-PRICE_PRECISION[currency_pair.toString()])
    MINIMUM_AMOUNT=CURRENCY_PAIR_INFOS.currency_pair_infos[currency_pair.toString()].minimum_amount
    # 1. get my balance
    # balance=digifinex.balances()

    # 2. re-allocate initial funds
    global INITIAL_FUNDS
    INITIAL_FUNDS={
        'ltc':0.3,
        'btc':0.01
    }

    # 2.
    pass
    a=1

def should_cancel_order(price, order):
    if price==order.price:
        return False
    else:
        return True

def cache_depths():
    '''
    This method run a seperate routine that periodically queries the depth,
    and push it into global depths variable
    :return: modify the global variable depths
    '''
    global depths
    while True:
        depth = digifinex.depth(currency_pair)
        depths.append(depth)
        time.sleep(0.5)
        depths=depths[-3:]

def get_my_balance():
    global balance
    balance=digifinex.balances()

def get_my_pending_orders():
    global my_pending_orders
    my_pending_orders=digifinex.order_list()

def trade():
    # -1 globalize variables:

    # 0. get my balance and pending orders
    thread1=Thread(target=get_my_balance)
    thread2=Thread(target=get_my_pending_orders)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # 1. get the filtered depth
    filtered_depth=UNIVERSAL.Depth.filter(depths)

    # 2. determine the bid and ask point, problem is how much accumulated volume should it be?
    # let's just assume the accumulated volume should be 5 or 10
    # and we'll soon find out a way to determine the accumulated volume
    supporting_bid_price,supporting_ask_price=UNIVERSAL.Depth.get_supporting_points(filtered_depth,'vol',0.5)
    my_bid_price=round(supporting_bid_price+CHANGING_UNIT,PRICE_PRECISION[currency_pair.toString()])
    my_ask_price=round(supporting_ask_price-CHANGING_UNIT,PRICE_PRECISION[currency_pair.toString()])

    a=1
    # 2.1 if the spread percent is less than 1‰, make it 1‰,
    #     else make the spread
    spread_percentage=(my_ask_price-my_bid_price)/my_bid_price
    if spread_percentage<0.001:
        mid_price=(my_bid_price+my_ask_price)/2
        my_ask_price=mid_price*1.005
        my_bid_price=mid_price*0.995

    # 3. determine the amount you should buy/sell, base on balance and initial_fund
    threads_for_cancel_orders=[]
    free_reference=dict(balance.free).get(currency_pair.reference,0)
    free_base=dict(balance.free).get(currency_pair.base,0)
    frozen_reference=dict(balance.frozen).get(currency_pair.reference,0)
    frozen_base=dict(balance.frozen).get(currency_pair.base,0)

    for order in my_pending_orders.orders:

        if order.trade_type==1:
            __price = my_bid_price
            if should_cancel_order(__price, order) == True:
                thread = Thread(target=digifinex.cancel_order, args=(currency_pair, order.id,))
                threads_for_cancel_orders.append(thread)
                frozen_reference-=(order.total_amount-order.trade_amount)*order.price
                free_reference+=(order.total_amount-order.trade_amount)*order.price
        else:
            __price=my_ask_price
            if should_cancel_order(__price, order) == True:
                thread = Thread(target=digifinex.cancel_order, args=(currency_pair, order.id,))
                threads_for_cancel_orders.append(thread)
                frozen_base-=(order.total_amount-order.trade_amount)
                free_base+=(order.total_amount-order.trade_amount)

    # 4. cancel the orders that have the wrong order price, and wait till the threads have done
    for thread in threads_for_cancel_orders:
        thread.start()
    for thread in threads_for_cancel_orders:
        thread.join()

    # 5. determine the real amount that you should buy or sell
    my_bid_amount=max(2*INITIAL_FUNDS[currency_pair.base]-(free_base+frozen_base),0)
    my_ask_amount=free_base

    # 6. do the trade
    threads_for_submitting_orders=[]
    if my_bid_amount>MINIMUM_AMOUNT:
        threads_for_submitting_orders.append(Thread(target=digifinex.submit_order,args=(1,currency_pair,my_bid_price,my_bid_amount,)))
    if my_ask_amount>MINIMUM_AMOUNT:
        threads_for_submitting_orders.append(Thread(target=digifinex.submit_order,args=(0,currency_pair,my_ask_price,my_ask_amount,)))
    for thread in threads_for_submitting_orders:
        thread.start()
    for thread in threads_for_submitting_orders:
        thread.join()
    a=1

    pass


def main():
    cache_depths_thread=Thread(target=cache_depths)
    cache_depths_thread.start()

if __name__ == '__main__':
    initialize()
    main()
    while True:
        if len(depths) < 3:
            time.sleep(1)
            continue
        trade()
        time.sleep(5)
    a=1

