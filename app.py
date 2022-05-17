#File contains the main GUI elements
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#pip install tkcalendar if dont have
from tkcalendar import *
from datetime import *
import time
from PIL import Image, ImageTk
import pandas as pd

#Trade Listing class in TradeListing.py
import TradeListing as trade
import __main__ as main

class GUI:
    def __init__(self,full_trade_listings,**configs):
        self.configs=configs

#tkinter interpreter
        self.root=Tk()
        self.root.title('Quick CSV Editor')
        self.root.geometry(str(self.configs['dc']['framesize-x'])+'x'+str(self.configs['dc']['framesize-y']))

        style=ttk.Style(self.root)
        style.theme_use('clam')

#canvas set-up
        self.main_frame=Frame(self.root)
        self.main_frame.pack()

#scroll bar set-up
        scroll_canvas=Canvas(self.main_frame,width=self.configs['dc']['leftsize-x'],height=self.configs['dc']['framesize-y'])

        self.left_frame=Frame(scroll_canvas)
        self.left_frame.pack(side=LEFT)

        scrollbar=Scrollbar(self.main_frame,orient='vertical',command=scroll_canvas.yview,width=30)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=LEFT,fill='y')
        scroll_canvas.pack(side=LEFT)

        scroll_canvas.create_window((0,0),window=self.left_frame,anchor='nw')
        self.left_frame.bind('<Configure>',
            lambda e:scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))

        self.right_frame=Frame(self.main_frame)
        self.right_frame.pack(side=RIGHT)
 
#main widget set-up
        self.fields_list=self.createNewTradeEditor()

        self.change_color(self.configs['theme']['color'][1],self.right_frame)
        
        self.full_trade_listings=[]
        self.full_trade_listings_widgets=[]
        for each in main.CSV.trade_listings:
            self.shiftTradeListings()
            self.createTradeListingTab(each,0)
        
        self.root.resizable(False,False)
        self.root.mainloop()

#displays listings
#sort_by
# 0=default/TradeDate sort
# 1=entryTime sort
# 2=exitTime sort
    def displayTradeListings(self,sort_by=0,mkt=None,qty_min=None,qty_max=None,entryTime=None,exitTime=None,_type=None,lmtPrc=None,ptPrc=None,slPrc=None):
        for i in range(len(self.full_trade_listings)):
            for j in range(len(self.full_trade_listings)):
                pass

    def shiftTradeListings(self):
        j=1
        for each in self.full_trade_listings_widgets:
            each.grid(row=j,column=0)
            j+=1

#changes the color of a component
    def change_color(self,color,container):
        if type(container) is not Frame and type(container) is not Button and type(container) is not OptionMenu and type(container) is not Label and type(container) is not Radiobutton and type(container) is not Canvas:
            return

        container.config(bg=color)
        if type(container) is Button:
            container.config(highlightbackground=color)

        for child in container.winfo_children():
            self.change_color(color,child)

#creates a new dropdown menu
#returns: selected option,menu
    def createNewMenu(self,field_name,options,row,where,existing_value='Empty',column=0):
        self.createNewDescLabel(field_name,row,where)

        selected=StringVar()
        selected.set(existing_value)

        menu=OptionMenu(where,selected,*options)
        menu.grid(row=row,column=column+1,padx=(5,10),pady=10)
        
        return selected,menu

#creates a list of new mutually exclusive radio buttons
    def createNewOption(self,field_names,row,where,column=0):
        var=IntVar()
        for i in range(len(field_names)):
            button=Radiobutton(where,text=field_names[i],variable=var,value=i)
            button.grid(row=row,column=column+i,padx=10,pady=10)

        return var

#create a new entry without desc
    def createNewEntry(self,row,where,column=0,existing_value=0):
        entryText=StringVar()

        entry=Entry(where,width=10,textvariable=entryText)
        entry.grid(row=row,column=column+1,padx=(5,10),pady=10)
        entry.insert(0,existing_value)

        return entryText

#creates a desc label
    def createNewDescLabel(self,field_name,row,where,column=0):
        desc=Label(where,text=field_name)
        desc.grid(row=row,column=column,padx=(10,5),pady=10)

#creates a new entry field
    def createNewDescEntry(self,field_name,row,where,column=0,existing_value=0):
        self.createNewDescLabel(field_name,row,where,column=column)
        entry=self.createNewEntry(row,where,column=column,existing_value=existing_value)

        return entry

#creates a new label
    def createNewLabel(self,field_name,row,where,column=0,existing_value=0):
        self.createNewDescLabel(field_name,row,where)

        value=Label(where,text=existing_value)
        value.grid(row=row,column=column+1,padx=(5,10),pady=10)

#creates a drop down calendar
    def createNewDatePicker(self,field_name,row,where,column=0,existing_value=0):
        self.createNewDescLabel(field_name,row,where,column=column)

        today=datetime.now()
        calendar=DateEntry(where,width=10,year=today.year,month=today.month,day=today.day)
        calendar.grid(row=row,column=column+1,padx=10,pady=10)

        entry=self.createNewEntry(row,where,column+1,existing_value=today.strftime(self.configs['dc']['UItf']))

        return calendar,entry

    def checkForErrors(self):
        if self.fields_list['mkt'].get()=='Empty':
            self.showErrorMessage('Form Entry Error','Market field is empty')
            return True

    def showErrorMessage(self,error_type,error_message):
        messagebox.showerror(error_type,error_message)

#creates a new trade listing from gui elements
    def saveTradeListing(self):
        if self.checkForErrors():
            return

        entrydt=self.fields_list['entryTime']
        exitdt=self.fields_list['exitTime']

        result=trade.TradeListing(
            tradeDate=datetime.now(),
            mkt=self.fields_list['mkt'].get(),
            qty=self.fields_list['qty'].get(),
            entryTime=datetime.combine(entrydt[0].get_date(),datetime.strptime(entrydt[1].get(),self.configs['dc']['UItf']).time()),
            exitTime=datetime.combine(exitdt[0].get_date(),datetime.strptime(exitdt[1].get(),self.configs['dc']['UItf']).time()),
            _type=self.fields_list['type'].get() if self.fields_list['reloadable']=='False' else -1*self.fields_list['type'].get(),
            lmtPrc=self.fields_list['lmtPrc'].get(),
            ptPrc=self.fields_list['ptPrc'].get(),
            slPrc=self.fields_list['slPrc'].get())

        main.CSV.trade_listings.append(result)

        self.shiftTradeListings()
        self.createTradeListingTab(result,0)
        
        main.CSV.write()
        main.CSV.read()

        return result

#creates the trade listing editor
    def createNewTradeEditor(self):
        fields_list={}
#Buy/Sell
        fields_list['buy/sell']=self.createNewOption(['Buy','Sell'],0,self.right_frame)

#Fixed/Limit/Stop
        fields_list['type']=self.createNewOption(['Fixed Time','Limit Order','Stop Order'],1,self.right_frame)

#Reloadable
        fields_list['reloadable']=self.createNewMenu('Reloadable',['True','False'],2,self.right_frame,existing_value='False')[0]

#Market
        fields_list['mkt']=self.createNewMenu('Market',[i for i in range(10)],3,self.right_frame,'Empty')[0]

#Fund Qty
        fields_list['qty']=self.createNewDescEntry('Fund Qty',4,self.right_frame)

#Constants
        self.createNewLabel('Fund Mult: ',5,self.right_frame,existing_value=self.configs['lc']['fund_mult'])
        self.createNewLabel('Sig Qty: ',6,self.right_frame,existing_value=self.configs['lc']['sig_qty'])

#Entry date time
        fields_list['entryTime']=self.createNewDatePicker('Entry DateTime',7,self.right_frame)

#Exit date time
        fields_list['exitTime']=self.createNewDatePicker('Exit DateTime',8,self.right_frame)

#Limit Price
        fields_list['lmtPrc']=self.createNewDescEntry('Limit Price',9,self.right_frame)

#P/T Price
        fields_list['ptPrc']=self.createNewDescEntry('P/T Price',10,self.right_frame)

#S/L Price
        fields_list['slPrc']=self.createNewDescEntry('S/L Price',11,self.right_frame)

#create save button
        save_button=Button(self.right_frame,text='Save',command=self.saveTradeListing)
        save_button.grid(row=12,column=1)

        return fields_list

#updates the trade listing editor with the values of a trade listing
    def updateTradeEditor(self,trade_listing):
        self.fields_list['buy/sell'].set('Buy' if trade_listing.qty<=0 else 'Sell')
        self.fields_list['mkt'].set(int(trade_listing.mkt))
        self.fields_list['qty'].set(float(trade_listing.qty))
        self.fields_list['entryTime'][0].set_date(trade_listing.entryTime)
        self.fields_list['exitTime'][0].set_date(trade_listing.exitTime)
        self.fields_list['entryTime'][1].set(trade_listing.entryTime.strftime(self.configs['dc']['UItf']))
        self.fields_list['exitTime'][1].set(trade_listing.exitTime.strftime(self.configs['dc']['UItf']))
        self.fields_list['reloadable'].set('True' if trade_listing._type<0 else 'False')
        self.fields_list['lmtPrc'].set(int(trade_listing.lmtPrc))
        self.fields_list['ptPrc'].set(int(trade_listing.ptPrc))
        self.fields_list['slPrc'].set(int(trade_listing.slPrc))

#creates a sidebar tab to select a trade listing
    def createTradeListingTab(self,trade_listing,row,column=0):
        self_frame=Frame(self.left_frame)
        self_frame.grid(row=row,column=column,padx=2,pady=2)

        desc_text='Trade Date: {tradeDate}\nEntry Time: {entryTime}\nExit Time: {exitTime}\nmkt: {mkt}\nqty: {qty}'.format(
                tradeDate=trade_listing.tradeDate.strftime(self.configs['dc']['UIdf']),
                entryTime=trade_listing.entryTime.strftime(self.configs['dc']['UIdtf']),
                exitTime=trade_listing.exitTime.strftime(self.configs['dc']['UIdtf']),
                mkt=trade_listing.mkt,
                qty=trade_listing.qty)
        desc=Label(self_frame,text=desc_text)
        desc.grid(row=0,column=0,padx=(25,5),pady=10)
        
        button=Button(self_frame,text='Edit Trade',command=lambda: self.updateTradeEditor(trade_listing))
        button.grid(row=1,column=0,padx=10,pady=5)

        button=Button(self_frame,text='Remove Trade',command=lambda: self.updateTradeEditor(trade_listing))
        button.grid(row=2,column=0,padx=10,pady=5)

        self.change_color(self.configs['theme']['color'][2],self_frame)
            
        self.full_trade_listings_widgets.append(self_frame)
        self.full_trade_listings.append(trade_listing)

        return self_frame
