from packages import currency_pair as CP
from packages import account as ACCOUNT

account=ACCOUNT.Account('15d12cfa0a69be','c6d6a4b051b36e373bb47eede7c1675d05d12cfa0')
currency_pairses=CP.CurrencyPair.find_triangle_arbitragable_currency_pairs('digifinex',account)
for currency_pairs in currency_pairses:
    for currency_pair in currency_pairs:
        print(currency_pair.toString()+'\t', end='')
    print()


# currency_pair=CP.CurrencyPair('btc','usdt')
# other=currency_pair.subtract('abc')
# result1=currency_pair.contains('abc')
# result2=currency_pair.contains('btc')
# print(result1,result2)
a=1