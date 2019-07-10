import sys
sys.path.append("..")
from packages import aex as AEX
from packages import digifinex as DIGIFINEX
from packages import account as ACCOUNT
from packages import currency_pair as CP
from strategies import triangle_arbitrage as TRI
from packages import universal
import time
import copy

account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
digifinex=DIGIFINEX.DigiFinex(account)

def determine_tradable_currency_pairses(num_pairs=5):
    # 0. get all currency pairs:
    currency_pairses=CP.CurrencyPair.get_top_n_currency_pairs_adjusted_by_vol('digifinex',account)

    # 1. calculate avg_buy*buying_amount-avg_sell*selling_amount
    for references in currency_pairses.keys():
        for item in currency_pairses[references]:
            currency_pair=item['currency_pair']
            trades=digifinex.trades(currency_pair)
            result=universal.Trades.statistics(trades)
            item['profit']=result['avg_buy_by_amount']*result['buying_amount']-result['avg_sell_by_amount']*result['selling_amount']
            item['statistics']=copy.deepcopy(result)
        currency_pairses[references]=sorted(currency_pairses[references], key=lambda x: x['profit'], reverse=True)
        a=1
    for references in currency_pairses.keys():
        currency_pairses[references]=currency_pairses[references][:num_pairs]
    return currency_pairses

def calculate_orders_prices(depth, statistics):
    buying_price=None
    selling_price=None


    return (buying_price,selling_price)

# 0. set the tradable currency pairs
currency_pairses=determine_tradable_currency_pairses()
a=1

# 1. set initial position:
initial_positions={
    'cny':100,
    'usdt':15,
    currency_pairses['cny'][0]['currency_pair'].base:100/currency_pairses['cny'][0]['statistics']['avg_buy_by_amount'],
    currency_pairses['cny'][1]['currency_pair'].base:100/currency_pairses['cny'][1]['statistics']['avg_buy_by_amount'],
    currency_pairses['cny'][2]['currency_pair'].base:100/currency_pairses['cny'][2]['statistics']['avg_buy_by_amount'],
    currency_pairses['cny'][3]['currency_pair'].base:100/currency_pairses['cny'][3]['statistics']['avg_buy_by_amount'],
    currency_pairses['cny'][4]['currency_pair'].base:100/currency_pairses['cny'][4]['statistics']['avg_buy_by_amount'],
    currency_pairses['usdt'][0]['currency_pair'].base:15/currency_pairses['usdt'][0]['statistics']['avg_buy_by_amount'],
    currency_pairses['usdt'][1]['currency_pair'].base:15/currency_pairses['usdt'][1]['statistics']['avg_buy_by_amount'],
    currency_pairses['usdt'][2]['currency_pair'].base:15/currency_pairses['usdt'][2]['statistics']['avg_buy_by_amount'],
    currency_pairses['usdt'][3]['currency_pair'].base:15/currency_pairses['usdt'][3]['statistics']['avg_buy_by_amount'],
    currency_pairses['usdt'][4]['currency_pair'].base:15/currency_pairses['usdt'][4]['statistics']['avg_buy_by_amount'],
}
account.set_initial_positions(initial_positions)

# 2. make market
currency_pair=currency_pairses['cny'][0]['currency_pair']
statistics=currency_pairses['cny'][0]['statistics']

# 2.1 determine the safe margin:
# 2.2 get the clean depth
depths=[]
for cnt in range(0,3):
    depth=aex.depth(currency_pair)
    time.sleep(0.1)
    depths.append(copy.deepcopy(depth))
depths=depths[-3:]
depth=universal.Depth.filter(depths)
# 2.3 determine the price that you should make the order
buying_price,selling_price=calculate_orders_prices(depth,statistics)
#
# 2.2
t1=time.time()
# trades=aex.trades(currency_pair,6282136-500)
# statistics=universal.Trades.statistics(trades)
a=1
