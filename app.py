"""
Alex Xu
(alex1xu)
alexxugn@gmail.com

app.py
-creates the GUI
-populates trade listing widgets
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from datetime import *
import util as util
import __main__ as main


class GUI:

    """
    -creates the GUI
    -populates editor with existing trades
    """
    def __init__(self):
        self.configs=main.configs

# main window set-up
        self.root=Tk()
        self.root.title('Quick CSV Editor')
        self.root.geometry(str(self.configs['dc']['framesize-x'])+'x'+str(self.configs['dc']['framesize-y']))

        style=ttk.Style(self.root)
        style.theme_use('clam')

        self.main_frame=Frame(self.root)
        self.main_frame.pack()

# scroll-bar set-up
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

        self.util_frame=Frame(self.right_frame)
        self.util_frame.pack(side=TOP)

        self.editor_frame=Frame(self.right_frame)
        self.editor_frame.pack(side=TOP)

# widget set-up
        self.right_widget_index=0
        self.filter_fields_list=self.create_utility_editor()
        self.editor_fields_list=self.create_trade_editor()

        self.change_color(self.configs['theme']['color'][0],self.util_frame)
        self.change_color(self.configs['theme']['color'][1],self.editor_frame)

# populates frame with trade widgets
        self.full_trade_listings_widgets=[]
        self.populate_trade_listing_widgets(util.CSV.trade_listings)

        self.inEditMode=False
        self.originalEdit=None

        self.root.resizable(False,False)
        self.root.mainloop()

    """
    *********************************************
    General utility functions
    *********************************************
    """

    """
    changes the color of a subtree of widgets
    """
    def change_color(self,color,container):
        if type(container) is not Frame and type(container) is not Button and type(container) is not OptionMenu and type(container) is not Label and type(container) is not Radiobutton and type(container) is not Canvas:
            return

        if type(container) is Button:
            container.config(highlightbackground=color)
        else:
            container.config(bg=color)

        for child in container.winfo_children():
            self.change_color(color,child)

    """
    TO BE IMPLEMENTED
    
    checks every field for errors
    """
    def check_for_errors(self):
        if self.editor_fields_list['mkt'].get()== 'Empty':
            self.create_new_popup_widget('Form Entry Error', 'Market field is empty')
            return True

    """
    *********************************************
    Trade listing tab display functions
    *********************************************
    """

    """
    TO BE IMPLEMENTED
    
    re-orders the trades based on parameters
    """
    def display_trade_listings(self):
        sub_list=[]
        for each in util.CSV.trade_listings:
            if self.filter_fields_list['active'].get()=='Active' and (each.entryTime>datetime.now() or each.exitTime<datetime.now()): continue
            if self.filter_fields_list['active'].get()=='Inactive' and (each.entryTime<=datetime.now() and each.exitTime>=datetime.now()): continue

            if self.filter_fields_list['mkt']=='Any' and self.filter_fields_list['mkt'].get()!=each.mkt: continue

            sub_list.append(each)

        self.populate_trade_listing_widgets(sub_list)

        return sub_list


    """
    shifts each trade listing tab down, usually used for sorting/adding a new tab
    """
    def shift_trade_listings_down(self):
        j=1
        for each in self.full_trade_listings_widgets:
            each.grid(row=j,column=0)
            j+=1

    """
    -creates a new trade listing from the current values in each field
    -writes the trade listing to the csv
    """
    def save_as_new_trade_listing(self):
        if self.check_for_errors():
            return

        entrydt=self.editor_fields_list['entryTime']
        exitdt=self.editor_fields_list['exitTime']

        result=util.TradeListing(
            tradeDate=datetime.now(),
            mkt=self.editor_fields_list['mkt'].get(),
            qty=self.editor_fields_list['qty'].get(),
            entryTime=datetime.combine(entrydt[0].get_date(),datetime.strptime(entrydt[1].get(),self.configs['dc']['UItf']).time()),
            exitTime=datetime.combine(exitdt[0].get_date(),datetime.strptime(exitdt[1].get(),self.configs['dc']['UItf']).time()),
            _type=self.editor_fields_list['type'].get() if self.editor_fields_list['reloadable'] == 'False' else -1 * self.editor_fields_list['type'].get(),
            lmtPrc=self.editor_fields_list['lmtPrc'].get(),
            ptPrc=self.editor_fields_list['ptPrc'].get(),
            slPrc=self.editor_fields_list['slPrc'].get())

        util.CSV.trade_listings.append(result)

        if self.inEditMode:
            self.delete_matching_trade_listing(self.originalEdit)
            self.inEditMode=False
            self.originalEdit=None

        util.CSV.write()
        util.CSV.read()

        self.populate_trade_listing_widgets(util.CSV.trade_listings)

        return result

    """
    updates each field in editor with a new trade listing
    """
    def update_editor_with_new_trade_listing(self):
        self.inEditMode=False
        self.originalEdit=None

        self.editor_fields_list['buy/sell'].set(0)
        self.editor_fields_list['mkt'].set('Empty')
        self.editor_fields_list['type'].set(0)
        self.editor_fields_list['qty'].set(0)
        self.editor_fields_list['entryTime'][0].set_date(datetime.now())
        self.editor_fields_list['exitTime'][0].set_date(datetime.now())
        self.editor_fields_list['entryTime'][1].set(datetime.now().strftime(self.configs['dc']['UItf']))
        self.editor_fields_list['exitTime'][1].set(datetime.now().strftime(self.configs['dc']['UItf']))
        self.editor_fields_list['reloadable'].set('False')
        self.editor_fields_list['lmtPrc'].set(int(0))
        self.editor_fields_list['ptPrc'].set(int(0))
        self.editor_fields_list['slPrc'].set(int(0))

    """
    updates each of the fields in the editor with the values from a trade listing
    """
    def update_editor_with_trade_listing(self, trade_listing):
        self.inEditMode=True
        self.originalEdit=trade_listing

        self.editor_fields_list['buy/sell'].set('Buy' if trade_listing.qty <= 0 else 'Sell')
        self.editor_fields_list['mkt'].set(int(trade_listing.mkt))
        self.editor_fields_list['qty'].set(float(trade_listing.qty))
        self.editor_fields_list['entryTime'][0].set_date(trade_listing.entryTime)
        self.editor_fields_list['exitTime'][0].set_date(trade_listing.exitTime)
        self.editor_fields_list['entryTime'][1].set(trade_listing.entryTime.strftime(self.configs['dc']['UItf']))
        self.editor_fields_list['exitTime'][1].set(trade_listing.exitTime.strftime(self.configs['dc']['UItf']))
        self.editor_fields_list['reloadable'].set('True' if trade_listing._type < 0 else 'False')
        self.editor_fields_list['lmtPrc'].set(int(trade_listing.lmtPrc))
        self.editor_fields_list['ptPrc'].set(int(trade_listing.ptPrc))
        self.editor_fields_list['slPrc'].set(int(trade_listing.slPrc))

    """
    deletes the matching trade listing from the list
    """
    def delete_matching_trade_listing(self,check):
        for each in util.CSV.trade_listings:
            if each.tradeDate.strftime(self.configs['dc']['CSVdf']) != check.tradeDate.strftime(self.configs['dc']['CSVdf']): continue
            if each.mkt != check.mkt: continue
            if each.qty != check.qty: continue
            if each.entryTime.strftime(self.configs['dc']['CSVdtf']) != check.entryTime.strftime(self.configs['dc']['CSVdtf']): continue
            if each.exitTime.strftime(self.configs['dc']['CSVdtf']) != check.exitTime.strftime(self.configs['dc']['CSVdtf']): continue
            if each._type != check._type: continue
            if each.lmtPrc != check.lmtPrc: continue
            if each.ptPrc != check.ptPrc: continue
            if each.slPrc != check.slPrc: continue

            util.CSV.trade_listings.remove(each)
            return

    """
    recreates all of the trade widgets
    """
    def populate_trade_listing_widgets(self,sub_list):
        for each in self.full_trade_listings_widgets:
            each.destroy()

        self.full_trade_listings_widgets=[]

        for each in sub_list:
            self.shift_trade_listings_down()
            self.create_new_trade_listing_tab(each, 0)

    """
    delete a trade listing
    """
    def delete_trade_listing(self,check):
        self.delete_matching_trade_listing(check)

        util.CSV.write()
        util.CSV.read()

        self.populate_trade_listing_widgets(util.CSV.trade_listings)

    """
    *********************************************
    GUI set-up functions
    *********************************************
    """

    """
    creates utlity widgets
    -new trade button
    -sorting parameters
    """
    def create_utility_editor(self):
        fields_list={}

        fields_list['active']=self.create_new_menu_widget('Range', ['Any', 'Active', 'Inactive'], self.right_widget_index, self.util_frame, existing_value='Any')[0]

        fields_list['mkt']=self.create_new_menu_widget('Market', [i for i in range(10)], self.right_widget_index, self.util_frame, 'Any',column=2)[0]
        self.right_widget_index+=1

        filter_button=Button(self.util_frame, text='Filter', command=self.display_trade_listings)
        filter_button.grid(row=self.right_widget_index,column=1,padx=10,pady=10)
        self.right_widget_index+=1

        filter_button=Button(self.util_frame, text='New Trade', command=self.update_editor_with_new_trade_listing)
        filter_button.grid(row=self.right_widget_index,column=1,padx=10,pady=10)
        self.right_widget_index+=1

        return fields_list

    """
    creates all of the widgets needed to input a new trade listing
    """
    def create_trade_editor(self):
        fields_list={}

        fields_list['buy/sell']=self.create_new_option_button_widget(['Buy', 'Sell'], self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        fields_list['type']=self.create_new_option_button_widget(['Fixed Time', 'Limit Order', 'Stop Order'], self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        fields_list['reloadable']=self.create_new_menu_widget('Reloadable', ['True', 'False'], self.right_widget_index, self.editor_frame, existing_value='False')[0]
        self.right_widget_index+=1

        fields_list['mkt']=self.create_new_menu_widget('Market', [i for i in range(10)], self.right_widget_index, self.editor_frame, 'Empty')[0]
        self.right_widget_index+=1

        fields_list['qty']=self.create_new_entry_label_widget('Fund Qty', self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        self.create_new_label_widget('Fund Mult: ', self.right_widget_index, self.editor_frame, existing_value=self.configs['lc']['fund_mult'])
        self.create_new_label_widget('Sig Qty: ', self.right_widget_index, self.editor_frame, existing_value=self.configs['lc']['sig_qty'])

        fields_list['entryTime']=self.create_new_entry_calendar_widget('Entry DateTime', self.right_widget_index, self.editor_frame, existing_value=datetime.now().strftime(self.configs['dc']['UItf']))
        self.right_widget_index+=1

        fields_list['exitTime']=self.create_new_entry_calendar_widget('Exit DateTime', self.right_widget_index, self.editor_frame, existing_value=datetime.now().strftime(self.configs['dc']['UItf']))
        self.right_widget_index+=1

        fields_list['lmtPrc']=self.create_new_entry_label_widget('Limit Price', self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        fields_list['ptPrc']=self.create_new_entry_label_widget('P/T Price', self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        fields_list['slPrc']=self.create_new_entry_label_widget('S/L Price', self.right_widget_index, self.editor_frame)
        self.right_widget_index+=1

        save_button=Button(self.editor_frame, text='Save', command=self.save_as_new_trade_listing)
        save_button.grid(row=self.right_widget_index,column=1)
        self.right_widget_index+=1

        return fields_list

    """
    creates a tab for a trade listing
    """
    def create_new_trade_listing_tab(self, trade_listing, row, column=0):
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

        self.full_trade_listings_widgets.append(self_frame)

        button=Button(self_frame, text='Edit Trade', command=lambda: self.update_editor_with_trade_listing(trade_listing))
        button.grid(row=1,column=0,padx=10,pady=5)

        button=Button(self_frame, text='Remove Trade', command=lambda: self.delete_trade_listing(trade_listing))
        button.grid(row=2,column=0,padx=10,pady=5)

        self.change_color(self.configs['theme']['color'][2],self_frame)

        return self_frame

    """
    creates an option-menu widget
    """
    def create_new_menu_widget(self, field_name, options, row, where, existing_value='Empty', column=0):
        self.create_new_left_label_widget(field_name, row, where,column=column)

        selected=StringVar()
        selected.set(existing_value)

        menu=OptionMenu(where,selected,*options)
        menu.grid(row=row,column=column+1,padx=(5,10),pady=10)

        return selected,menu

    """
    creates a radio-button widget
    """
    @staticmethod
    def create_new_option_button_widget(field_names, row, where, column=0):
        var=IntVar()
        for i in range(len(field_names)):
            button=Radiobutton(where,text=field_names[i],variable=var,value=i)
            button.grid(row=row,column=column+i,padx=10,pady=10)

        return var

    """
    creates an entry-field widget
    """
    @staticmethod
    def create_new_entry_widget(row, where, column=0, existing_value='0'):
        entryText=StringVar()

        entry=Entry(where,width=10,textvariable=entryText)
        entry.grid(row=row,column=column+1,padx=(5,10),pady=10)
        entry.insert(0,existing_value)

        return entryText

    """
    creates a label, usually to describe a component placed to the right of it
    """
    @staticmethod
    def create_new_left_label_widget(field_name, row, where, column=0):
        desc=Label(where,text=field_name)
        desc.grid(row=row,column=column,padx=(10,5),pady=10)

    """
    creates a label/entry-field pair
    """
    def create_new_entry_label_widget(self, field_name, row, where, column=0, existing_value='0'):
        self.create_new_left_label_widget(field_name, row, where, column=column)
        entry=self.create_new_entry_widget(row, where, column=column, existing_value=existing_value)

        return entry

    """
    creates a label, usually to display a constant
    """
    def create_new_label_widget(self, field_name, row, where, column=0, existing_value=0):
        self.create_new_left_label_widget(field_name, row, where)

        value=Label(where,text=existing_value)
        value.grid(row=row,column=column+1,padx=10,pady=10)

    """
    creates an entry-field/calendar widget
    """
    def create_new_entry_calendar_widget(self, field_name, row, where, column=0, existing_value='00:00'):
        self.create_new_left_label_widget(field_name, row, where, column=column)

        today=datetime.now()
        calendar=DateEntry(where,width=10,year=today.year,month=today.month,day=today.day)
        calendar.grid(row=row,column=column+1,padx=10,pady=10)

        entry=self.create_new_entry_widget(row, where, column + 1, existing_value=existing_value)

        return calendar,entry

    """
    displays a pop-up which displays an error
    """
    @staticmethod
    def create_new_popup_widget(error_type, error_message):
        messagebox.showerror(error_type,error_message)