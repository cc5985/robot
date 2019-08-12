from matplotlib import pyplot as plt
# import matplotlib.finance as mpf
from mpl_finance import candlestick_ochl
from matplotlib.pylab import date2num
import pandas as pd
import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

quotes = []
stock = pd.read_csv('999999.csv', index_col=0)

for row in range(420):
    if row == 0:
        # sdate = str(stock.loc[row, 'trade_date'])
        sdate='2017-11-20'
        sdate_change_format = sdate[0:4] + sdate[4:6] + sdate[6:]
        sdate_num = date2num(datetime.datetime.strptime(sdate_change_format, '%Y-%m-%d'))
        sdate_plt = sdate_num
    else:
        sdate_plt = sdate_num + row

    sopen = stock.iloc[row, 0]
    shigh = stock.iloc[row, 1]
    slow = stock.iloc[row, 2]
    sclose = stock.iloc[row, 3]
    datas = (sdate_plt, sopen, shigh, slow, sclose)
    quotes.append(datas)


fig, ax = plt.subplots(facecolor=(0, 0.3, 0.5), figsize=(12, 8))
fig.subplots_adjust(bottom=0.1)
ax.xaxis_date()
plt.xticks(rotation=45)
plt.title('600000')
plt.xlabel('time')
plt.ylabel('price')
candlestick_ochl(ax, quotes, width=0.7)
plt.grid(True)
plt.show()