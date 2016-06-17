'''
@import stock date
'''
# -*- coding: utf-8 -*- 

import math
import MySQLdb
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import datetime


 
def TxtToTable(stockid):
    st=stockid
    location=r'd:/zhangbw/datasource/AFirst/'+st+'.txt'
    names=['date','open','high','low','close','trade','count']
    df=pd.read_csv(location,names=names,header=None,delim_whitespace=True)
    del df['count']
    values=df.values[2:-1]
    j=len(df.index)/7
    columns=df.columns
    df=DataFrame(values,columns=columns)
    date=df['date'].values
    for i in range(len(date)-1):
        date[i]=datetime.datetime.strptime(date[i],"%d-%m-%Y").date()
    del df['date']
#    column=[d.date().toordinal() for d in pd.to_datetime(values)]
    df.index=date
    names=['open','high','low','close','trade']
    for i in names:
        for j in range(len(df)-1):
            df[i][j]=float(df[i][j]) 
            
            
    return df

def DataToSeries(stockid,index):
    inde=index
    stock=stockid
    df=TxtToTable(stock)
    close=df[inde]
    names=['open','high','low','close','trade']
    close=close.astype(float)
    
    return close

#switch to plot
#def PlotKLine():
 #   df=StrToDate()
  #  quotes=[]
   # for i in range(df.index.max()):
    #    quotes.append(df.ix[i].tolist())  
    #for i in range(len(quotes)-1):
     #   for j in range(6):
      #      quotes[i][j]=float(quotes[i][j])
  # for i in range(len(quotes)-1):
   #     quotes[i]=tuple(quotes[i])

    #fig,ax=plt.subplots(figsize=(8,5))
    #fig.subplots_adjust(bottom=0.2)
    #mpf.candlestick_ochl(ax,quotes,width=0.6,colorup='b',colordown='r')
    #plt.grid(True)
    #ad.xaxis_date()
    #ax.autoscale_view()
    #plt.setp(plt.gca().get_xticklabels(),rotation=30)  
    #return quotes
#load data from myql server

def ValueToLog(stockid,index):
    stock=stockid
    inde=index
    close=DataToSeries(stock,inde)
    close=close[3:-2]
    index=close.index
    values=close.values
    logvalue=[]
    loglist={}
    ens=len(values)/7
    
    for i in range(ens-1):
        logvalue.append(math.log(values[7*(i+1)])-math.log(values[7*i]))
    for i in range(len(logvalue)-1):
        logvalue[i]=round(logvalue[i],4)
    loglist={}
    for i in range(len(logvalue)-1):
        loglist[logvalue[i]]=0
    for i in range(len(logvalue)-1):
        for j in loglist.keys():
            if(loglist[j]==logvalue[i]):
                loglist[j]=loglist[j]+1
                
    return logvalue

def PlotWithNews(stockid,index):
    inde=index
    stock=stockid
    close=DataToSeries(stock,inde)
    index=close.index
    values=close.values
    logvalue=[]
    loglist={}
    cursor=LinkMysql(stock)
    for i in range(len(cursor)-1):
        try:
            loglist[cursor[i]]=math.log(close[cursor[i]+datetime.timedelta(7)])-math.log(close[cursor[i]])
        except KeyError:
            pass
    logvalues=loglist.values()
    for i in range(len(logvalues)-1):
        logvalues[i]=round(logvalues[i],4)
    
    return logvalues

def LinkMysql(stockid):
    code=stockid
    connect=MySQLdb.connect('localhost','root','','financialdata')
    cursor=connect.cursor()
    query=("select _date from "+code+" where _announce>0;")
    cursor.execute(query)
    connect.commit()
    curlist=[]
    for i in cursor:
        curlist.append(i)
    for i in range(len(curlist)):
        curlist[i]=list(curlist[i])[0]
    return curlist
    
    cursor.close()
    connect.close()
    
    
def PubAnnounce(codename):
    code=codename
    connect=MySQLdb.connect('localhost','root','','financialdata')
    cursor=connect.cursor()
    query=("select _date, _announce from "+code+" where _announce!=0;")
    cursor.execute(query)
    connect.commit()
    curlist=[]
    for i in cursor:
        curlist.append(i)
    for i in curlist:
        i=list(i)
    curlistvalue=[]
    curlistindex=[]
    for i in curlist:
        curlistvalue.append(i[1])
    for i in curlist:
        curlistindex.append(i[0])
    curSeries=Series(curlistvalue,index=curlistindex)
    
    cursor.close()
    connect.close()
    
    
    years=[]
    months=[]
    value=[]
    indexs=[]
    for i in range(17):
        years.append(1999+i)
    for i in range(12):
        months.append(1+i)
    for i in years:
        for j in months:
            indexs.append(datetime.date(i,j,1))
    monthnotw=[]
    for i in years:
        for j in months:
            values=0
            if(j!=12):
                timedelta=(datetime.date(i,j+1,1)-datetime.date(i,j,1)).days
            else:
                timedelta=31
            for k in range(timedelta):
                try:
                    dd=datetime.date(i,j,(k+1))
                    values=values+curSeries[dd]
                except KeyError:
                    pass
            value.append(values)
            
    cursorSeries=Series(value,index=indexs)
    cursorSeries=cursorSeries[11:]
    
    return cursorSeries

def TradeByWeek(stockid):
    stock=stockid
    df=TxtToTable(stock)
    dftrade=DataToSeries('trade')
    dftrade=dftrade[3:]
    datelast=len(dftrade)-(len(dftrade)/5)*5
    datelast=int(datelast)
    datelast=len(dftrade)-datelast-1
    dftrade=dftrade[:datelast]
    weekCount=len(dftrade)/5
    tradeList={}
    for i in range(weekCount):
        tradeList[i]=0
        dateindex=dftrade.index
    for i in range(weekCount):
        try:
            indexs=dateindex[5*i]
            tradeList[i]=dftrade[indexs]+dftrade[indexs+datetime.timedelta(1)]+dftrade[indexs+datetime.timedelta(2)]+dftrade[indexs+datetime.timedelta(3)]+dftrade[indexs+datetime.timedelta(4)]
        except KeyError:
            tradeList[i]+=dftrade[indexs]
    for i in range(len(tradeList.values())):
        tradeList.values()[i]=int(tradeList.values()[i])

    '''fig,ax=plt.subplots()'''
    tradeSeriesweek=Series(tradeList.values(),index=tradeList.keys())
    
    return tradeSeriesweek

def TradeByMonth(stockid):
    stock=stockid
    df=TxtToTable(stock)
    dftrade=DataToSeries(stock,'trade')
    years=[]
    months=[]
    value=[]
    indexs=[]
    timeoneday=datetime.timedelta(1)
    for i in range(17):
        years.append(1999+i)
    for i in range(12):
        months.append(1+i)
    for i in years:
        for j in months:
            indexs.append(datetime.date(i,j,1))
    monthnotw=[]
    for i in years:
        for j in months:
            values=0
            if(j!=12):
                timedelta=(datetime.date(i,j+1,1)-datetime.date(i,j,1)).days
            else:
                timedelta=31
            for k in range(timedelta):
                try:
                    dd=datetime.date(i,j,(k+1))
                    values=values+dftrade[dd]
                except KeyError:
                    pass
            value.append(values)
    tradeSeries=Series(value,index=indexs)
    tradeSeries=tradeSeries[11:]
    
    return tradeSeries

def LogValueBySell(stockid):
    stock=stockid
    dfclose=DataToSeries(stock,'close')
    dfclose=dfclose[3:]
    datelast=len(dfclose)-(len(dfclose)/5)*5
    datelast=int(datelast)
    datelast=len(dfclose)-datelast-1
    dfclose=dfclose[:datelast]
    weekCount=len(dfclose)/5
    datestart=dfclose.index[0]
    dateend=dfclose.index[-1]
    dfdate=dfclose.index
    indexs=dfclose.index
    valuecolumn=dfclose.values
    closeList={}
    curList={}
    
    connect=MySQLdb.connect('localhost','root','','financialdata')
    cursor=connect.cursor()
    query=("select _date, _announce from "+stock+" ;")
    cursor.execute(query)
    connect.commit()
    curlist=[]
    curlistvalue=[]
    curlistindex=[]
    for i in cursor:
        curlist.append(i)
    for i in range(len(curlist)):
        curlist[i]=list(curlist[i])
        if(curlist[i][1]==None):
            curlist[i][1]=0
        curlist[i][1]=int(curlist[i][1])
    for i in curlist:
        curlistvalue.append(i[1])
    for i in range(len(curlistvalue)):
        curlistvalue[0]=curlistvalue[0]
    for i in curlist:
        curlistindex.append(i[0])
    curSeries=Series(curlistvalue,index=curlistindex)
    curDataframe=DataFrame(np.zeros(len(indexs)),index=indexs,columns=['cursor'])
    for i in indexs:
        curDataframe['cursor'][i]=curSeries[i]
    curDataframe['close']=valuecolumn
    
    ComList=[]
    for i in range(len(curDataframe)):
        ComList.append([])
    frameClose=curDataframe['cursor'].values
    
    for i in range(weekCount):
        closeList[i]=0
        dateindex=dfclose.index
    for i in range(weekCount):
        try:
            closeList[i]=math.log(dfclose[5*(i+1)])-math.log(dfclose[5*i]) 
            closeList[i]=round(closeList[i],4)
        except KeyError:
            pass
    for i in range(weekCount):
        try:
            curList[i]=frameClose[5*i]+frameClose[5*i+1]+frameClose[5*i+2]+frameClose[5*i+3]+frameClose[5*i+4]
            curList[i]=int(curList[i])
        except KeyError:
            pass      
    for i in range(len(curList)-1):
        i=i+1
        curList[0]=curList[0]
        curList[i]=curList[i]-curList[i-1]
    for i in range(len(closeList.values())):
        closeList.values()[i]=round((closeList.values()[i]),4)
    tradeSeriesweek=Series(closeList.values(),index=closeList.keys())
    closeList=closeList.values()
    curList=curList.values()
    for i in range(len(curList)):
        if(curList[i]>0):
            closeList[i]=-closeList[i]
    
    return closeList

   
   
    
    
    
    

    


#import the data