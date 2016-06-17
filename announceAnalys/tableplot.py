
import math
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import datetime
from pylab import *
import matplotlib.pylab as plt
import datetime
import time
from sklearn.neighbors.kde import KernelDensity
from scipy.stats import gaussian_kde
import announceAnalys.dataimport as dataimport
#TxtToTable:parameter:tablename return df:dataframe,df.index=date
#DataToSeries:parameter:stockid,columnname return close:series,index=date
#ValueToLog:parameter:stockid,columnname return loglist:list log return of per 7 days
#PlotWithNews:parameter:columnname,stockid return logvalues:list log return with news per 7 days
#LinkMysql:parameter:stockid return logvalue:list return date of stock announcements
#PubAnnounce:parameter:stockid return cursorseries:series stock announcement count per month,index=per month(199,11,1)(1999,12,1)
#TradeByWeek:parameter:stockid return tradeseries:series trade volumn per week
#Trade ByMonth parameter:stockid return tradeseries:series trade volumn per month,index=month((1999,11,1),(1999,12,1))
#LogValueBySell parameter:stockid return closeList:list -(logvalue) for weeks published announcements
#PubAnnounce parameter:stockid return curSeries:series pubtime and announce count of table sh6xxxxx
#AnnounceFromCompany parameter:stockid(6xxxxx) return pubtime:list pubtime of table a_companyannouncements
#MeanOfStock parameter:no parameter return:series mean value of each stock on announce day
#ShowAboutAnnounce parameter:stockid return logadd1:mean return of a stock on announce days
#PlotOfAnnounce parameter:stockid return priceFrame:DataFrame price of a stock on two weeks from anouncement days 


#announcedate=dataimport.AnnounceFromCompany('600000')
#curdict=dataimport.AnnounceFromCompany('600000')
priceseries=dataimport.PlotOfAnnounce('sh600000')
logadd1=dataimport.ShowAboutAnnounce('sh600000')
meanseries=dataimport.MeanOfStock()
meanseries.order()
print meanseries
meanseries.plot(kind='bar')
'''xs = np.linspace(-30, 30, 1000)
fig, ax = plt.subplots()
density1=gaussian_kde(logadd1.values())
density1.covariance_factor = lambda : .25
density1._compute_covariance()
ax.plot(xs,density1(xs),'r')'''
plt.show()