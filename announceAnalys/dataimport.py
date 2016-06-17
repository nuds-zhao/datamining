
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
    
def PlotOfAnnounce(stockid):
    stock=stockid
    dfclose=DataToSeries(stock,'close')
    announcedate=LinkMysql(stock)
    announcedate=announcedate[5:-5]
    pricelist={}
    pricelistadd1={}
    pricelistadd2={}
    pricelistadd3={}
    pricelistadd4={}
    pricelistadd5={}
    pricelistminus1={}
    pricelistminus2={}
    pricelistminus3={}
    pricelistminus4={}
    pricelistminus5={}
    for i in announcedate:
        try:
            pricelist[i]=round(dfclose[i],4)
        except KeyError:
            i=i+datetime.timedelta(1)
    for i in pricelist.keys():
        for j in range(len(dfclose)):
            if(dfclose.index[j]==i):
                try:
                    pricelistadd1[i]=round(dfclose[j+1],4)
                    pricelistadd2[i]=round(dfclose[j+2],4)
                    pricelistadd3[i]=round(dfclose[j+3],4)
                    pricelistadd4[i]=round(dfclose[j+4],4)
                    pricelistadd5[i]=round(dfclose[j+5],4)
                    pricelistminus1[i]=round(dfclose[j-1],4)
                    pricelistminus2[i]=round(dfclose[j-2],4)
                    pricelistminus3[i]=round(dfclose[j-3],4)
                    pricelistminus4[i]=round(dfclose[j-4],4)
                    pricelistminus5[i]=round(dfclose[j-5],4)
                except IndexError:
                    pass

    priceFrame=DataFrame(pricelist.values(),index=pricelist.keys(),columns=['price'])
    priceFrame['priceadd1']=np.zeros(len(priceFrame.index))
    priceFrame['priceadd2']=np.zeros(len(priceFrame.index))
    priceFrame['priceadd3']=np.zeros(len(priceFrame.index))
    priceFrame['priceadd4']=np.zeros(len(priceFrame.index))
    priceFrame['priceadd5']=np.zeros(len(priceFrame.index))
    priceFrame['priceminus1']=np.zeros(len(priceFrame.index))
    priceFrame['priceminus2']=np.zeros(len(priceFrame.index))
    priceFrame['priceminus3']=np.zeros(len(priceFrame.index))
    priceFrame['priceminus4']=np.zeros(len(priceFrame.index))
    priceFrame['priceminus5']=np.zeros(len(priceFrame.index))
    for i in priceFrame.index:
        priceFrame['priceadd1'][i]=priceFrame['priceadd1'][i]+pricelistadd1[i]
    for i in priceFrame.index:
        priceFrame['priceadd2'][i]=priceFrame['priceadd2'][i]+pricelistadd2[i]
    for i in priceFrame.index:
        priceFrame['priceadd3'][i]=priceFrame['priceadd3'][i]+pricelistadd3[i]
    for i in priceFrame.index:
        priceFrame['priceadd4'][i]=priceFrame['priceadd4'][i]+pricelistadd4[i]
    for i in priceFrame.index:
        priceFrame['priceadd5'][i]=priceFrame['priceadd5'][i]+pricelistadd5[i]
    for i in priceFrame.index:
        priceFrame['priceminus1'][i]=priceFrame['priceminus1'][i]+pricelistminus1[i]
    for i in priceFrame.index:
        priceFrame['priceminus2'][i]=priceFrame['priceminus2'][i]+pricelistminus2[i]
    for i in priceFrame.index:
        priceFrame['priceminus3'][i]=priceFrame['priceminus3'][i]+pricelistminus3[i]
    for i in priceFrame.index:
        priceFrame['priceminus4'][i]=priceFrame['priceminus4'][i]+pricelistminus4[i]
    for i in priceFrame.index:
        priceFrame['priceminus5'][i]=priceFrame['priceminus5'][i]+pricelistminus5[i]
    '''
    priceFrame['priceadd1']=pricelistadd1.values()
    priceFrame['priceadd2']=pricelistadd2.values()
    priceFrame['priceadd3']=pricelistadd3.values()
    priceFrame['priceadd4']=pricelistadd4.values()
    priceFrame['priceadd5']=pricelistadd5.values()
    priceFrame['priceminus1']=pricelistminus1.values()
    priceFrame['priceminus2']=pricelistminus2.values()
    priceFrame['priceminus3']=pricelistminus3.values()
    priceFrame['priceminus4']=pricelistminus4.values()
    priceFrame['priceminus5']=pricelistminus5.values()'''
    return priceFrame


def ShowAboutAnnounce(stockid):
    stock=stockid
    priceFrame=PlotOfAnnounce(stock)
    logadd1={}
    for i in priceFrame.index:
        #logadd1[i]=math.log(priceFrame['priceadd1'][i])-math.log(priceFrame['price'][i])
        logadd1[i]=round((priceFrame['priceadd5'][i]-priceFrame['price'][i])/(priceFrame['price'][i]),4)*100
        +round((priceFrame['price'][i]-priceFrame['priceminus5'][i])/(priceFrame['priceminus5'][i]),4)*100
    
    return logadd1

def MeanOfStock():
    N=281
    meandict={}
    for i in range(N):
        try:
            sto=int(i)+600000
            stock='sh'+str(sto)
            logadd1=ShowAboutAnnounce(stock)
            logadd1=logadd1.values()
            logadd1=np.array(logadd1)
            meandict[stock]=logadd1.mean()
        except IOError,e:
            print e
    
    '''meanseries=Series(np.zeros(len(meandict.keys())),index=meandict.keys())
    for i in meanseries.index:
        meanseries[i]=meandict[i]'''
    meanseries=Series()
    for i in meandict.keys():
        meanseries[i]=meandict[i]
            
    return meanseries
    
def AnnounceFromCompany(stockid):
    stock=stockid
    connect=MySQLdb.connect('localhost','root','','financialdata')
    cursor=connect.cursor()
    query=("select pubtime from a_companyannouncements where code="+stock+";")
    cursor.execute(query)
    connect.commit()
    curlist=[]
    for i in cursor:
        curlist.append(i)
    for i in range(len(curlist)):
        curlist[i]=list(curlist[i])[0]
    curdict={}
    for i in range(len(curlist)):
        curdict[curlist[i]]=0
    for i in curlist:
        for j in curdict.keys():
            if(j==i):
                curdict[j]=curdict[j]+1
    announcedate=[day for day in curdict.keys() if day.year<2016]
    datetoremove=[]
    for i in range(24):
        datetoremove.append(datetime.date(2015,11,i+6))
    for i in range(30):
        datetoremove.append(datetime.date(2015,12,i+1))
    
    for i in datetoremove:
        try:
            announcedate.remove(i)
        except ValueError:
            pass
        
    
    return announcedate
    
    
    
    
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
    
    return curSeries
    