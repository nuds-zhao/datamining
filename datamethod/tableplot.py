'''
@seven days kde,use df['close']
'''

# coding: utf-8

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
import datamethod.dataimport as dataimport

#TxtToTable:parameter:tablename return df:dataframe,df.index=date
#DataToSeries:parameter:stockid,columnname return close:series,index=date
#ValueToLog:parameter:stockid,columnname return loglist:list log return of per 7 days
#PlotWithNews:parameter:columnname,stockid return logvalues:list log return with news per 7 days
#LinkMysql:parameter:stockid return logvalue:list return date of stock announcements
#PubAnnounce:parameter:stockid return cursorseries:series stock announcement count per month,index=per month(199,11,1)(1999,12,1)
#TradeByWeek:parameter:stockid return tradeseries:series trade volumn per week
#Trade ByMonth parameter:stockid return tradeseries:series trade volumn per month,index=month((1999,11,1),(1999,12,1))
#LogValueBySell parameter:stockid return closeList:list -(logvalue) for weeks published announcements
   
    

loglist1=dataimport.PlotWithNews('sh600051','close')#logvalue of each week use first day of each week
loglist2=dataimport.ValueToLog('sh600051','close')#logvalue of days of announce days per week
closeList=dataimport.LogValueBySell('sh600051')#-logvalue if announce this week more than next week
xs = np.linspace(-0.2, 0.2, 1000)
fig, ax = plt.subplots()
density1=gaussian_kde(loglist1)
density2=gaussian_kde(loglist2)
density3=gaussian_kde(closeList)
density1.covariance_factor = lambda : .25
density1._compute_covariance()
ax.plot(xs,density1(xs),'r')
ax.plot(xs,density2(xs),'g')
ax.plot(xs,density3(xs),'b')
#plt.show()

tradeSeries=dataimport.TradeByMonth('sh600089')
for i in range(len(tradeSeries.values)):
    tradeSeries.values[i]=round(float(tradeSeries.values[i])/float(tradeSeries.values.max()),4)*1000
cursorSeries=dataimport.PubAnnounce('sh600089')
for i in range(len(cursorSeries.values)):
    cursorSeries.values[i]=round(float(cursorSeries.values[i])/float(cursorSeries.values.max()),4)*1000

tradeFrame=DataFrame(tradeSeries,columns=['tradevolumn'])
tradeFrame['announcevolumn']=cursorSeries.values
tradeFrame.plot(kind='bar')
plt.show()




    
# trade volumn peer month and announce per month, guiyi to 1000

    
    
