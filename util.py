"""
Alex Xu
(alex1xu)
alexxugn@gmail.com

util.py
-CSV class which handles reading and writing
-TradListing class which contains the information in a trade
"""

from datetime import *
import pandas as pd
import __main__ as main


class CSV:
    trade_listings=[]

    @staticmethod
    def read():
        data=pd.read_csv(main.configs['trade_file'],dtype=str)
        CSV.trade_listings=[]
        for index,row in data.iterrows():
            result=TradeListing(
                tradeDate=datetime.strptime(str(int(row['TradeDate'])),main.configs['dc']['CSVdf']),
                mkt=int(row['mkt']),
                qty=float(row['qty']),
                entryTime=datetime.strptime(str(row['entryTime']),main.configs['dc']['CSVdtf']),
                exitTime=datetime.strptime(str(row['exitTime']),main.configs['dc']['CSVdtf']),
                _type=int(row['type']),
                lmtPrc=float(row['lmtPrc']),
                ptPrc=float(row['ptPrc']),
                slPrc=float(row['slPrc']))

            CSV.trade_listings.append(result)

    @staticmethod
    def write():
        result={'TradeDate': [],'acc': [],'mkt': [],'qty': [],'entryTime': [],'exitTime': [],'type': [],'lmtPrc': [],'ptPrc': [],'slPrc': []}
        for each in CSV.trade_listings:
            result['TradeDate'].append(int(each.tradeDate.strftime(main.configs['dc']['CSVdf'])))
            result['acc'].append(40)
            result['mkt'].append(int(each.mkt))
            result['qty'].append(float(each.qty))
            result['entryTime'].append(each.entryTime.strftime(main.configs['dc']['CSVdtf']))
            result['exitTime'].append(each.exitTime.strftime(main.configs['dc']['CSVdtf']))
            result['type'].append(int(each._type))
            result['lmtPrc'].append(float(each.lmtPrc))
            result['ptPrc'].append(float(each.ptPrc))
            result['slPrc'].append(float(each.slPrc))

        dataframe=pd.DataFrame(result)
        dataframe.set_index('TradeDate')
        dataframe.to_csv(main.configs['trade_file'],index=False)


class TradeListing:
    def __init__(self,tradeDate,mkt,qty,entryTime,exitTime,_type,lmtPrc,ptPrc,slPrc,frame=None):
        self.tradeDate=tradeDate
        self.mkt=mkt
        self.qty=qty
        self.entryTime=entryTime
        self.exitTime=exitTime
        self._type=_type
        self.lmtPrc=lmtPrc
        self.ptPrc=ptPrc
        self.slPrc=slPrc
        self.frame=frame