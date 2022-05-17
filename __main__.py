import app
import yaml
from datetime import datetime
import pandas as pd
import TradeListing as trade

#main starts here
config_stream=open('config.yaml','r')
configs=yaml.safe_load(config_stream)
configs['dc']['CSVdtf']=configs['dc']['CSVdf']+'.'+configs['dc']['CSVtf']
configs['dc']['UIdtf']=configs['dc']['UItf']+' on '+configs['dc']['UIdf']
class CSV:
    trade_listings=[]
    
    @staticmethod
    def read():
        data=pd.read_csv(configs['data_file'])
        CSV.trade_listings=[]
        for index,row in data.iterrows():
            result=trade.TradeListing(
                    tradeDate=datetime.strptime(str(int(row['TradeDate'])),configs['dc']['CSVdf']),
                    mkt=row['mkt'],
                    qty=row['qty'],
                    entryTime=datetime.strptime(str(row['entryTime']),configs['dc']['CSVdtf']),
                    exitTime=datetime.strptime(str(row['exitTime']),configs['dc']['CSVdtf']),
                    _type=row['type'],
                    lmtPrc=row['lmtPrc'],
                    ptPrc=row['ptPrc'],
                    slPrc=row['slPrc'])  

            CSV.trade_listings.append(result)

    @staticmethod
    def write():
        result={'TradeDate': [],'acc': [],'mkt': [],'qty': [],'entryTime': [],'exitTime': [],'type': [],'lmtPrc': [],'ptPrc': [],'slPrc': []}
        for each in CSV.trade_listings:
            result['TradeDate'].append(int(each.tradeDate.strftime(configs['dc']['CSVdf'])))
            result['acc'].append(40)
            result['mkt'].append(int(each.mkt))
            result['qty'].append(each.qty)
            result['entryTime'].append(each.entryTime.strftime(configs['dc']['CSVdtf']))
            result['exitTime'].append(each.exitTime.strftime(configs['dc']['CSVdtf']))
            result['type'].append(int(each._type))
            result['lmtPrc'].append(int(each.lmtPrc))
            result['ptPrc'].append(int(each.ptPrc))
            result['slPrc'].append(int(each.slPrc))

        dataframe=pd.DataFrame(result)
        dataframe.set_index('TradeDate')
        dataframe.to_csv(configs['data_file'])

CSV.read()

main=app.GUI(CSV.trade_listings,**configs)
