class TradeListing:
    def __init__(self,tradeDate,mkt,qty,entryTime,exitTime,_type,lmtPrc,ptPrc,slPrc):
        self.tradeDate=tradeDate
        self.mkt=mkt
        self.qty=qty
        self.entryTime=entryTime
        self.exitTime=exitTime
        self._type=_type
        self.lmtPrc=lmtPrc
        self.ptPrc=ptPrc
        self.slPrc=slPrc 
