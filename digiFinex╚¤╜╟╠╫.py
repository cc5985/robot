# coding=utf-8

# triangle arbitrage:
'''
    0. 这是一个针对Digifinex交易平台的交易策略，
    1. 该策略基于三角套利模型，在三个标的间寻找瞬间的不平衡点，并试图进行交易套利
    2. 目前选取的两个交易组为 (btc,cny,usdt) 和 (eth,cny,usdt)
    3. 以上两个交易组的三角套利的重要性为0，即所有其他交易模型必须优先考虑这个策略
    4. 该三角套利模型原则上不进行‘限价单’操作，所有操作均为‘市价单’操作，即在充分掌握信息的情况下出手操作
    5. 高度抽象化，主程序体内尽量不出现字符串和数值
'''


import copy
import packages.color as CL
from packages import account as AC, coin as CN, currency_pair as CP, currency_pair
import time
import threading
from packages import digifinex as DIGIFINEX
# CONSTANTS，所有的外部参数、数值常量、字符串全都在这里定义----------------------------------------
FEE={
    'maker':0,
    'taker':0
}
FEE0 = 0
FEE1 = 0
market = "DigiFinex"
account = AC.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)
color = CL.Colored()

coins = []
coin0 = CN.Coin('btc', 1, 0.01)
coin1 = CN.Coin('cny', 1, 900)
coin2 = CN.Coin('usdt', 1, 128)
coins.append(coin0)
coins.append(coin1)
coins.append(coin2)
btc = coin0
cny = coin1
usdt = coin2
pairs = [
    CP.CurrencyPair('btc','cny'),
    CP.CurrencyPair('btc','usdt'),
    CP.CurrencyPair('usdt','cny'),
]
money_reserved={
    'btc':0.01,
    'cny':900,
    'usdt':128
}

# -----------------------------------------------------------------------------------------

# assume we have c0 c1 c2, each of which has a quantity q0 q1 q2
# we should re-buy c0,c1,c2 in different market/pair at possible low price:
# the c0 we can buy at different markets are:
# you can only buy c0 by selling c2 in pairs[2] or selling c1 in pairs[0]:
# so the quantities of c0 you can buy are:
# f(depths[2],buy='c0',q2)---->in pairs[2]
# f(depths[0],buy='c0',q1)---->in pairs[0]
# the quantities of c1 you can buy are::
# f(depths[0],buy='c1',q0)
# f(depths[1],buy='c1',q2)
# the quantities of c2 you can buy are:
# f(depths[1],buy='c2',q1)
# f(depths[2],buy='c2',q0)

def get_the_quantity_of_coin_you_can_buy(depth, buy_target, coin):
    cp1 = CP.CurrencyPair()
    currency_pair = depth.currency_pair
    base_currency = cp1.get_base_currency(currency_pair)
    quantity_of_coin = copy.copy(coin.quantity)
    referencial_currency = cp1.get_referencial_currency(currency_pair)
    total_amount_we_can_buy = 0
    if buy_target == base_currency:  # means we just buy buy_target is OK
        for ask in depth.asks:
            total_money_they_ask = ask.price * ask.amount
            if quantity_of_coin >= total_money_they_ask:
                amount_we_can_buy = ask.amount
                quantity_of_coin -= total_money_they_ask
            else:
                amount_we_can_buy = quantity_of_coin / ask.price
                quantity_of_coin = 0
            total_amount_we_can_buy += amount_we_can_buy
            if quantity_of_coin == 0:
                break
    else:  # means that we should sell the
        for bid in depth.bids:
            total_money_they_bid = bid.price * bid.amount
            total_coins_they_bid = bid.amount
            if quantity_of_coin >= total_coins_they_bid:
                amount_we_can_buy = bid.amount * bid.price
                quantity_of_coin -= total_money_they_bid
            else:
                amount_we_can_buy = quantity_of_coin * bid.price
                quantity_of_coin = 0
            total_amount_we_can_buy += amount_we_can_buy
            if quantity_of_coin == 0:
                break

    return total_amount_we_can_buy * (1 - FEE1)


def get_the_money_you_shall_spend(depth, target_coin, target_amount):
    '''

    :param depth:
    :param target_coin:
    :param target_amount:
    :return:
    '''
    cp1 = CP.CurrencyPair()
    currency_pair = depth.currency_pair
    base_currency = currency_pair.base
    money_we_shall_spend = 0
    current_amount = 0
    if target_coin.name == base_currency:  # we just buy it
        for ask in depth.asks:
            amount = ask.amount
            price = ask.price
            if current_amount + amount >= target_amount:
                money_we_shall_spend += price * (target_amount - current_amount)
                break
            else:
                money_we_shall_spend += amount * price
                current_amount += amount
    else:
        for bid in depth.bids:
            amount = bid.amount
            price = bid.price
            amount_in_this_level = price * amount
            if current_amount + amount_in_this_level < target_amount:
                money_we_shall_spend += amount
                target_amount += current_amount
            else:
                money_we_shall_spend += (target_amount - current_amount) / price
                break
    return money_we_shall_spend


def trade(ref_coin, target_coin, price, amount, trade_type):
    # _currency_pair = target_coin + '_' + ref_coin
    # result = aex.submit_order(trade_type, _currency_pair, price, amount)
    # if result.message == "操作成功":
    #     print(color.green(trade_type + ' ' + target_coin + ' at ' + str(price) + ' of ' + str(amount)))
    # else:
    #     print(color.red(trade_type + ' ' + target_coin + ' at ' + str(price) + ' of ' + str(amount)))
    #     print(result.message)
    # return result
    pass


def show_time():
    depths=[]
    for pair in pairs:
        depth = digifinex.depth(pair)
        depths.append(depth)

    # coin0_in_pairs0_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[0],coin0.name,coin1)
    # coin0_in_pairs2_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[2],coin0.name,coin2)
    # coin1_in_pairs0_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[0],coin1.name,coin0)
    # coin1_in_pairs1_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[1],coin1.name,coin2)
    # coin2_in_pairs1_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[1],coin2.name,coin1)
    # coin2_in_pairs2_we_can_buy=get_the_quantity_of_coin_you_can_buy(depths[2],coin2.name,coin0)
    # group1=(coin0_in_pairs0_we_can_buy,coin1_in_pairs1_we_can_buy,coin2_in_pairs2_we_can_buy)
    # group2=(coin0_in_pairs2_we_can_buy,coin1_in_pairs0_we_can_buy,coin2_in_pairs1_we_can_buy)
    # profit1=(group1[0]-coin0.quantity)*16400+(group1[1]-coin1.quantity)*1000+(group1[2]-coin2.quantity)*1
    # profit2=(group2[0]-coin0.quantity)*16400+(group2[1]-coin1.quantity)*1000+(group2[2]-coin2.quantity)*1
    # max_profit=max(profit1,profit2)
    # print()
    #
    # print()
    # print('*'*50)
    # print(color.red((profit1,profit2)))
    time1 = time.time()

    profit = []
    # group1: 下面三个表示的是要交易的资金量
    USDT = money_reserved['usdt']
    BTC = money_reserved['btc']
    CNY = money_reserved['cny']

    # coin00 represents how many btc you buy in terms of CNY
    coin00 = get_the_money_you_shall_spend(depths[0], cny, CNY)
    # coin11 represents how many usdt you buy in terms of btc
    coin11 = get_the_money_you_shall_spend(depths[1], btc, coin00)
    coin22 = get_the_money_you_shall_spend(depths[2], usdt, coin11)
    profit.append((CNY - coin22) / coin22 * 100)
    if (CNY - coin22) / coin22 > 0:
        # use BTC to buy ETH in market0, returns the amount coin00 of btc
        t0 = threading.Thread(target=trade, args=('btc', 'eth', depths[0].bids[0].price * 1.5, CNY, 'buy'))
        # use usdt to buy btc in market2, returns the amount coin11 of usdt
        t1 = threading.Thread(target=trade, args=('usdt', 'btc', depths[2].bids[0].price * 1.5, coin00, 'buy'))
        # sell eth for usdt in market1, returns the amount coin22 of
        t2 = threading.Thread(target=trade, args=('usdt', 'eth', depths[1].bids[0].price * 0.7, CNY, 'sell'))
        t1.start()
        t2.start()
        t0.start()
        t0.join()
        t1.join()
        t2.join()
        return

    coin00 = get_the_money_you_shall_spend(depths[0], btc, BTC)
    coin11 = get_the_money_you_shall_spend(depths[2], cny, coin00)
    coin22 = get_the_money_you_shall_spend(depths[1], usdt, coin11)
    profit.append((BTC - coin22) / coin22 * 100)
    if (BTC - coin22) / coin22 > 0:
        # use BTC to buy ETH in market0, returns the amount coin00 of btc
        t0 = threading.Thread(target=trade, args=('btc', 'eth', depths[0].bids[0].price * 0.7, CNY, 'sell'))
        # use usdt to buy btc in market2, returns the amount coin11 of usdt
        t1 = threading.Thread(target=trade, args=('usdt', 'eth', depths[1].bids[0].price * 1.5, coin00, 'buy'))
        # sell eth for usdt in market1, returns the amount coin22 of
        t2 = threading.Thread(target=trade, args=('usdt', 'btc', depths[2].bids[0].price * 0.7, BTC, 'sell'))
        t1.start()
        t2.start()
        t0.start()
        t0.join()
        t1.join()
        t2.join()
        return

    # if (BTC-coin22)/coin22>0:
    #     return

    coin00 = get_the_money_you_shall_spend(depths[2], cny, CNY)
    coin11 = get_the_money_you_shall_spend(depths[1], usdt, coin00)
    coin22 = get_the_money_you_shall_spend(depths[0], btc, coin11)
    profit.append((CNY - coin22) / coin22 * 100)
    # if (ETH-coin22)/coin22>0:
    #     return

    coin00 = get_the_money_you_shall_spend(depths[2], usdt, USDT)
    coin11 = get_the_money_you_shall_spend(depths[0], cny, coin00)
    coin22 = get_the_money_you_shall_spend(depths[1], btc, coin11)
    profit.append((USDT - coin22) / coin22 * 100)
    # if (USDT-coin22)/coin22>0:
    #     return

    coin00 = get_the_money_you_shall_spend(depths[1], btc, BTC)
    coin11 = get_the_money_you_shall_spend(depths[2], usdt, coin00)
    coin22 = get_the_money_you_shall_spend(depths[0], cny, coin11)
    profit.append((BTC - coin22) / coin22 * 100)
    # if (BTC-coin22)/coin22>0:
    #     return

    coin00 = get_the_money_you_shall_spend(depths[1], usdt, USDT)
    coin11 = get_the_money_you_shall_spend(depths[0], btc, coin00)
    coin22 = get_the_money_you_shall_spend(depths[2], cny, coin11)
    profit.append((USDT - coin22) / coin22 * 100)
    # if (USDT-coin22)/coin22>0:
    #     return

    for p in profit:
        if p > 0:
            print(color.green(('win=%(win)f ' % {'win': p})))
        elif p<-1:
            print(color.red(('win=%(win)f ' % {'win': p})))
        else:
            print(color.red(('win=%(win)f ' % {'win': p})))
    time2 = time.time()

    print(time2 - time1)


while True:
    show_time()
    time.sleep(10)