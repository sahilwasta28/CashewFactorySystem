'''from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from sqlite3 import dbapi2 as sqlite
from log_maker import *
from tkinter import messagebox
#from tkinter.tix import *
from math import ceil
import random
from datetime import date as dat
import mysql.connector

now = dat.today()
today_date = now
columns = ('Item_No', 'Item_Name', 'Item_Type', 'Quantity_Remain', 'Item_Cost', 'Expiry_Date', 'Manufactured_By')

c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()


def submit():
    return 0


def sell_insert():
    global middle_section, date, client, items, quantity, rate, total_var, paid
    print(date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get())

    success = True
    try:
        sql = "insert into sell(adate,client,item,quantity,rate,total,paid) values(date('%s'),'%s','%s',%s,%s,%s,'%s')" % (
        date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get())
        print(sql)
        cur.execute(sql)
        if items.get() == 'A':
            ss = 'sa'
            ww = quantity.get()
        if items.get() == 'B':
            ss = 'sb'
            ww = quantity.get()

        if items.get() == 'C':
            ss = 'sc'
            ww = quantity.get()

        print(ss)
        sql = "update stock_maintenance set %s=%s-%i" % (ss, ss, ww)
        print(sql)

        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Sell Successfully Inserted")
        messagebox.showinfo('Successfull', 'Sell Successfully Inserted')
        get_last_sell()
        get_unpaid_sell()


def get_last_sell():
    global last_sell
    for widget in last_sell.winfo_children():
        widget.destroy()
    Label(last_sell, text="-" * 40 + "Last Five Sells" + "-" * 40, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(
        row=1, column=1, columnspan=7)

    Label(last_sell, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(last_sell, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(last_sell, text="Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(last_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(last_sell, text="Rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=5)
    Label(last_sell, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=6)
    Label(last_sell, text="Paid", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=7)

    try:
        sql = "select * from sell order by adate desc limit 5"
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(last_sell, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=1)
            Label(last_sell, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=2)
            Label(last_sell, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=3)
            Label(last_sell, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=4)
            Label(last_sell, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=5)
            Label(last_sell, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=6)
            Label(last_sell, text=result[7], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=7)
            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(last_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=i, column=1, columnspan=7)


def update_sell(id):
    success = True
    try:
        sql = "update sell set paid='paid' where id=%s" % (id)
        print(sql)
        cur.execute(sql)
    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Sell Successfully Updated")
        messagebox.showinfo('Successfull', 'Sell Successfully Updated')
        get_last_sell()
        get_unpaid_sell()


def get_unpaid_sell():
    global unpaid_sell
    for widget in unpaid_sell.winfo_children():
        widget.destroy()
    Label(unpaid_sell, text="-" * 40 + "Unpaid Sells List" + "-" * 40, font=("Belwe Bd BT", 15),
          background="black",foreground="white").grid(row=1, column=1, columnspan=9)

    Label(unpaid_sell, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(unpaid_sell, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(unpaid_sell, text="Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(unpaid_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(unpaid_sell, text="Rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=5)
    Label(unpaid_sell, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=6)
    Label(unpaid_sell, text="Action", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=7)

    try:
        sql = "select * from sell where paid='not paid' order by adate desc "
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(unpaid_sell, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=1)
            Label(unpaid_sell, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=2)
            Label(unpaid_sell, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=3)
            Label(unpaid_sell, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=4)
            Label(unpaid_sell, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=5)
            Label(unpaid_sell, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=6)
            tk.Button(unpaid_sell, text="Make Paid", font=("Belwe lt BT", 15),background="green",foreground="white",
                      command=lambda id=result[0]: update_sell(id)).grid(row=i, column=7)
            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(unpaid_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=i + 1, column=1,
                                                                                         columnspan=7)


def calculate():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst
    print(gst.get())
    if gst.get() == 1:
        total_var.set(round(int((quantity.get()) * rate.get() * 112) / 100, 2))
    else:
        total_var.set(round(int(quantity.get()) * rate.get(), 2))


def sell():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst
    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    client = StringVar(middle_section)
    items = StringVar(middle_section)
    quantity = IntVar(middle_section)
    rate = DoubleVar(middle_section)
    total_var = DoubleVar(middle_section)
    paid = StringVar(middle_section)

    # Dictionary with options

    items_choices = ["Select Cashew", "A", "B", "C"]
    paid_choices = ["Select Option", "paid", "not paid"]

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    client_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=client)
    Label(middle_section, text="Client", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=2)
    client_entry.grid(row=2, column=2)

    items_option = ttk.OptionMenu(middle_section, items, *items_choices)
    Label(middle_section, text="Select Items", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=3)
    items_option.grid(row=2, column=3)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=4)
    quantity_entry.grid(row=2, column=4)

    rate_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=rate)
    Label(middle_section, text="rate", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=5)
    rate_entry.grid(row=2, column=5)

    Label(middle_section, text="GST", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=6)

    gst = IntVar(middle_section)
    C1 = Checkbutton(middle_section, text="", variable=gst, onvalue=1, offvalue=0)
    C1.grid(row=2, column=6)

    Label(middle_section, text="Total", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=7,
                                                                                           columnspan=2)
    total_entry = Label(middle_section, font=("Belwe lt BT", 15), textvariable=total_var)
    tk.Button(middle_section, text="calculate", font=("Belwe lt BT", 15),background="green",foreground="white", command=lambda: calculate()).grid(row=2,
                                                                                                            column=8)
    total_entry.grid(row=2, column=7)

    paid_option = ttk.OptionMenu(middle_section, paid, *paid_choices)
    Label(middle_section, text="Paid/Not", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=9)
    paid_option.grid(row=2, column=9)

    items.set(items_choices[1])
    paid.set(paid_choices[1])

    tk.Button(middle_section, text="Add Sell", font=("Belwe Bd BT", 15),background="green",foreground="white", command=lambda: sell_insert()).grid(row=2,column=10)

    client_names = tk.Frame(middle_section, background="black")
    Label(client_names, text="-" * 10 + "Select Client Names From Here" + "-" * 10, font=("Belwe Bd BT", 15),
          background="black",foreground="white").pack(side=TOP)
    sql = "select name from clients"
    cur.execute(sql)

    def onmousewheel(event):
        print(event.delta)
        listbox1.yview('scroll', event.delta, 'units')
        return "break"

    def select_cn(e):
        name = listbox1.curselection()
        client.set(client_names_list[name[0]])
        print(listbox1)

    scrollbar = Scrollbar(client_names)

    listbox1 = Listbox(client_names, height=5)
    listbox1.pack()

    client_names_list = []

    for result in cur:
        listbox1.insert(END, result[0])
        client_names_list.append(result[0])

        # tk.Button(client_names,text=result[0],font=("Belwe lt BT",15),command=lambda name=result[0]: client.set(name) ).pack()
    listbox1.config(yscrollcommand=scrollbar.set)
    listbox1.bind('<MouseWheel>', onmousewheel)
    listbox1.bind('<<ListboxSelect>>', select_cn)

    client_names.grid(row=3, column=1, columnspan=2, sticky="W")

    # View Last Sells
    last_sell = tk.Frame(middle_section, background="black")

    get_last_sell()
    last_sell.grid(row=3, column=3, columnspan=7, sticky="E")

    # View unpaid Sells
    unpaid_sell = tk.Frame(middle_section, background="black")
    get_unpaid_sell()
    unpaid_sell.grid(row=6, column=1, columnspan=9, sticky="S")


def insert_raw_material():
    global middle_section, date, type, quantity, raw
    print(date.get(), type.get(), quantity.get())
    success = True
    try:

        sql = "insert into raw_material(adate,raw,type,quantity) values(date('%s'),'%s','%s',%i)" % (date.get(), raw.get(), type.get(), quantity.get())
        cur.execute(sql)

        print(sql)
        sql = "update stock_maintenance set %s=%s+%i" % (type.get() + raw.get(), type.get() + raw.get(), quantity.get())
        print(sql)
        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Raw Material Successfully Inserted")
        messagebox.showinfo('Successfull', 'Raw Material Successfully Inserted')
        get_last_raw()


def get_last_raw():
    global last_raw

    for widget in last_raw.winfo_children():
        widget.destroy()

    Label(last_raw, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=6, column=1)
    Label(last_raw, text="Cashew", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=6, column=2)
    Label(last_raw, text="Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=6, column=3)
    Label(last_raw, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=6, column=4)

    try:
        sql = "select * from raw_material order by id desc"
        print(sql)
        cur.execute(sql)
        i = 7
        for result in cur:
            Label(last_raw, text=result[1], background="black",foreground="white").grid(row=i, column=1)
            Label(last_raw, text=result[2], background="black",foreground="white").grid(row=i, column=2)
            Label(last_raw, text=result[3], background="black",foreground="white").grid(row=i, column=3)
            Label(last_raw, text=result[4], background="black",foreground="white").grid(row=i, column=4)

            i += 1
    except Exception as exp:
        insert_error(exp)

    Label(last_raw, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=i, column=1, columnspan=4)


def raw_material():
    global middle_section, last_raw, date, type, quantity, raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    type = StringVar(middle_section)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)

    type_choices = ["", "Kokan", "Benin", "African", "Ghana"]
    type.set(type_choices[1])  # set the default option
    raw_choices = ["", "A", "B", "C"]
    raw.set(raw_choices[1])  # set the default option

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    raw_option = ttk.OptionMenu(middle_section, raw, *raw_choices)
    Label(middle_section, text="Select size", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=2)
    raw_option.grid(row=2, column=2)

    type_option = ttk.OptionMenu(middle_section, type, *type_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=3)
    type_option.grid(row=2, column=3)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=4)
    quantity_entry.grid(row=2, column=4)

    tk.Button(middle_section, text="Add Raw material", font=("Belwe Bd BT", 15),background="green",foreground="white",
              command=lambda: insert_raw_material()).grid(row=2, column=5)
    Label(middle_section, text="-" * 60 + "Last Raw Material Entry" + "-" * 60, font=("Belwe Bd BT", 15),
          background="black",foreground="white").grid(row=3, columnspan=5)

    last_raw = tk.Frame(middle_section, background="black")

    get_last_raw()

    last_raw.grid(row=4, column=1, columnspan=4)


def production_insert():
    global middle_section, date, sa, sb, sc ,type,ka, kb, kc, aa, ab, ac, ba, bb, bc, ga, gb, gc

    print(type.get(), date.get(), sa.get(), sb.get(), sc.get())

    success = True
    try:

        sql = "insert into production(adate,type,sa,sb,sc) values(date('%s'),'%s',%i,%i,%i)" % (date.get(),type.get(), sa.get(), sb.get(), sc.get())
        cur.execute(sql)

        print(sql)
        #sql = "update stock_maintenance set sa=sa+%i,sb=sb+%i,sc=sc+%i,KokanA=KokanA-%i,KokanB=KokanB-%i,KokanC=KokanC-%i,AfricanA=AfricanA-%i,AfricanB=AfricanB-%i,AfricanC=AfricanC-%i,BeninA=BeninA-%i,BeninB=BeninB-%i,BeninC=BeninC-%i,GhanaA=GhanaA-%i,GhanaB=GhanaB-%i,GhanaC=GhanaC-%i" % (sa.get(), sb.get(), sc.get(), ka, kb, kc, aa, ab, ac, ba, bb, bc, ga, gb, gc)
        sql = "update stock_maintenance set sa=sa+%i,sb=sb+%i,sc=sc+%i,%sA=%sA-%i,%sB=%sB-%i,%sC=%sC-%i" % (sa.get(), sb.get(), sc.get(),type.get(),type.get(),sa.get(),type.get(),type.get(),sb.get(),type.get(),type.get(),sc.get())

        print(sql)
        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Production Successfully Inserted")
        messagebox.showinfo('Successfull', 'Production Successfully Inserted')
        get_last_production()


def get_last_production():
    global last_production
    for widget in last_production.winfo_children():
        widget.destroy()

    Label(last_production, text="-" * 40 + "Last Production" + "-" * 40, font=("Belwe Bd BT", 15),
          background="black",foreground="white").grid(row=1, column=1, columnspan=6)

    Label(last_production, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(last_production, text="TYPE", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=2)
    Label(last_production, text="A", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=3)
    Label(last_production, text="B", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=4)
    Label(last_production, text="C", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=3, column=5)

    try:
        sql = "select * from production order by adate desc"
        cur.execute(sql)
        i = 5
        for result in cur:
            Label(last_production, text=result[0], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=1)
            Label(last_production, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=2)
            Label(last_production, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=3)
            Label(last_production, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=4)
            Label(last_production, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=i, column=5)

            i += 1

    except Exception as exp:
        insert_error(exp)

    #Label(last_production, text="-" * 80, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=14, column=1,columnspan=6)


def production():
    global middle_section, last_production, date, sa, sb, sc ,type

    for widget in middle_section.winfo_children():
        widget.destroy()
    sa = IntVar(middle_section)
    sb = IntVar(middle_section)
    sc = IntVar(middle_section)
    date = StringVar(middle_section, value=today_date)

    type_choices = ["Select Type", "Kokan", "Benin", "African", "Ghana"]


    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)


    type_option = ttk.OptionMenu(middle_section, type, *type_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=2)
    type_option.grid(row=2, column=2)
    type.set(type_choices[1])

    sa_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=sa)
    Label(middle_section, text="A.", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=3)
    sa_entry.grid(row=2, column=3)

    sb_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=sb)
    Label(middle_section, text="B.", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=4)
    sb_entry.grid(row=2, column=4)

    sc_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=sc)
    Label(middle_section, text="C.", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1, column=5)
    sc_entry.grid(row=2, column=5)


    tk.Button(middle_section, text="Add", font=("Belwe Bd BT", 15),background="green",foreground="white", command=lambda: production_insert()).grid(row=2,column=6)

    last_production = tk.Frame(middle_section, background="black")

    get_last_production()

    last_production.grid(row=4, column=1, columnspan=5)


def stock_maintain():
    global middle_section

    for widget in middle_section.winfo_children():
        widget.destroy()

    bottle_frame = tk.Frame(middle_section, background="black")
    Label(bottle_frame, text="-" * 30 + "Cashews" + "-" * 30, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=1,
                                                                                                                 column=1,
                                                                                                                 columnspan=4)
    Label(bottle_frame, text="", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=1)
    Label(bottle_frame, text="A", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=2)
    Label(bottle_frame, text="B", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=3)
    Label(bottle_frame, text="C", font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=4)

    sql = "select * from stock_maintenance"
    cur.execute(sql)
    result = cur.fetchone()
    print(result)
    Label(bottle_frame, text="", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=3, column=1)
    Label(bottle_frame, text="Cashew", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=4, column=1)
    Label(bottle_frame, text=result[0], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=4, column=2)
    Label(bottle_frame, text=result[1], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=4, column=3)
    Label(bottle_frame, text=result[2], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=4, column=4)
    Label(bottle_frame, text="Kokan", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=5, column=1)
    Label(bottle_frame, text=result[3], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=5, column=2)
    Label(bottle_frame, text=result[4], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=5, column=3)
    Label(bottle_frame, text=result[5], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=5, column=4)
    Label(bottle_frame, text="African", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=6, column=1)
    Label(bottle_frame, text=result[6], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=6, column=2)
    Label(bottle_frame, text=result[7], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=6, column=3)
    Label(bottle_frame, text=result[8], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=6, column=4)
    Label(bottle_frame, text="Benin", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=7, column=1)
    Label(bottle_frame, text=result[9], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=7, column=2)
    Label(bottle_frame, text=result[10], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=7, column=3)
    Label(bottle_frame, text=result[11], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=7, column=4)
    Label(bottle_frame, text="Ghana", font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=8, column=1)
    Label(bottle_frame, text=result[12], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=8, column=2)
    Label(bottle_frame, text=result[13], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=8, column=3)
    Label(bottle_frame, text=result[14], font=("Belwe lt BT", 15), background="black",foreground="white").grid(row=8, column=4)

    bottle_frame.grid(row=1, column=1, sticky="W", columnspan=4)


def main():
    Future Choice GUI
    global middle_section
    flag = 'Future Choice'
    future_choice = Tk()
    future_choice.configure(background="black")
    future_choice.title('Cutting')
    future_choice.state("zoomed")
    # billingsto.wm_iconbitmap('favicon.ico')
    # Label(future_choice,text='-'*48+'Future Choice'+'-'*49).grid(row=0,column=0,columnspan=7,sticky='W')

    side_menu = tk.Frame(future_choice, background="black")

    tk.Button(side_menu, width=20, text='SELLS', font=("Belwe Bd BT", 15),background="green",foreground="white", command=sell).grid(row=0, column=1)
    tk.Button(side_menu, width=20, text='RAW MATERIAL', font=("Belwe Bd BT", 15),background="green",foreground="white", command=raw_material).grid(row=0,
                                                                                                             column=2)
    tk.Button(side_menu, width=20, text='PRODUCTION', font=("Belwe Bd BT", 15),background="green",foreground="white", command=production).grid(row=0,column=3)
    tk.Button(side_menu, width=20, text='STOCK MAINTENANCE', font=("Belwe Bd BT", 15),background="green",foreground="white", command=stock_maintain).grid(row=0, column=4)
    tk.Button(side_menu, width=20, text='Back to Main Menu', font=("Belwe Bd BT", 15),background="green",foreground="white",
              command=future_choice.destroy).grid(row=0, column=5)
    Label(side_menu, text='-' * 200, font=("Belwe Bd BT", 15), background="black",foreground="white").grid(row=2, column=1, columnspan=5,sticky='N')

    side_menu.pack(side=TOP)
    sw = ScrolledWindow(future_choice)
    sw.pack()

    middle_section = tk.Frame(sw.window, background="black")
    Label(middle_section, text='-' * 48 + 'Cutting' + '-' * 49, font=("Belwe Bd BT", 15),
          background="black",foreground="white").grid(row=0, column=0, columnspan=9, sticky='N')
    middle_section.pack(fill=BOTH, expand=1)

    future_choice.mainloop()


def mainmenu():
    if flag == 'sto':
        sto.destroy()
    elif flag == 'billingsto':
        billingsto.destroy()
    elif flag == 'dailyinco':
        dailyinco.destroy()


main()
'''
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from sqlite3 import dbapi2 as sqlite
from math import ceil
import random
from datetime import date as dat
import mysql.connector
from tkinter import messagebox

# Constants and Database Connection
now = dat.today()
today_date = now
columns = ('Item_No', 'Item_Name', 'Item_Type', 'Quantity_Remain', 'Item_Cost', 'Expiry_Date', 'Manufactured_By')

# Database connection
try:
    c = mysql.connector.connect(
        host="localhost",
        user="Admin",
        password="newpassword123",
        database="cfms"
    )
    cur = c.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
    exit()


class ScrolledWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#f5f5f5", highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background="#f5f5f5")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame.pack(fill="both", expand=True)


def calculate():
    global quantity, rate, total_var, gst
    try:
        if gst.get() == 1:
            total_var.set(round(int((quantity.get()) * rate.get() * 112) / 100, 2))
        else:
            total_var.set(round(int(quantity.get()) * rate.get(), 2))
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Error in calculation: {e}")


def sell_insert():
    global date, client, items, quantity, rate, total_var, paid, region

    if not all([date.get(), client.get(), items.get(), quantity.get(), rate.get(), region.get()]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = "INSERT INTO sell (adate, client, item, quantity, rate, total, paid, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
        date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_var.get(), paid.get(), region.get())
        cur.execute(sql, values)

        item_type = items.get()
        if item_type not in ['A', 'B', 'C']:
            raise ValueError("Invalid item type")

        column = f"s{item_type.lower()}"
        update_sql = f"UPDATE stock_maintenance SET {column} = {column} - %s"
        cur.execute(update_sql, (quantity.get(),))

        update_sql = f"UPDATE stock_maintenance SET {region.get()}{item_type} = {region.get()}{item_type} - %s"
        cur.execute(update_sql, (quantity.get(),))

        log_sql = "INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)"
        log_values = (region.get(), item_type, f"-{quantity.get()}")
        cur.execute(log_sql, log_values)

        c.commit()
        messagebox.showinfo('Success', 'Sale Successfully Recorded')
        get_last_sell()
        get_unpaid_sell()
        stock_maintain()

    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_sell():
    global last_sell

    for widget in last_sell.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(last_sell, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Last Five Sales", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configure grid columns to center content
    for i in range(8):  # 8 columns
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers
    headers = ["Date", "Client", "Size", "Type", "Quantity", "Rate", "Total", "Paid"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT adate, client, item, quantity, rate, total, paid, region FROM sell ORDER BY adate DESC LIMIT 5"
        cur.execute(sql)

        # Display data with correct column mapping
        for row_idx, result in enumerate(cur, start=1):
            # Map database columns to display columns:
            # 0: adate (Date)
            # 1: client (Client)
            # 2: item (Size)
            # 7: region (Type)
            # 3: quantity (Quantity)
            # 4: rate (Rate)
            # 5: total (Total)
            # 6: paid (Paid)

            date = result[0]
            client = result[1]
            size = result[2]
            cashew_type = result[7]  # region field
            quantity = result[3]
            rate = result[4]
            total = result[5]
            paid_status = result[6]

            # Create the display row
            display_values = [date, client, size, cashew_type, quantity, rate, total, paid_status]

            for col, value in enumerate(display_values):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching sales: {exp}")


def update_sell(id):
    try:
        sql = "update sell set paid='paid' where id=%s" % (id)
        cur.execute(sql)
        c.commit()
        messagebox.showinfo('Success', 'Sale Marked as Paid')
        get_last_sell()
        get_unpaid_sell()
    except Exception as exp:
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_unpaid_sell():
    global unpaid_sell

    # Clear existing widgets
    for widget in unpaid_sell.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(unpaid_sell, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Unpaid Sales List", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configure grid columns to center content
    for i in range(8):  # 8 columns (7 data columns + 1 action column)
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers
    headers = ["Date", "Client", "Size", "Type", "Quantity", "Rate", "Total", "Action"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT id, adate, client, item, quantity, rate, total, region FROM sell WHERE paid='not paid' ORDER BY adate DESC"
        cur.execute(sql)

        # Display data with correct column mapping
        for row_idx, result in enumerate(cur, start=1):
            # Map database columns to display columns:
            # 0: id (hidden, used for the action button)
            # 1: adate (Date)
            # 2: client (Client)
            # 3: item (Size)
            # 7: region (Type)
            # 4: quantity (Quantity)
            # 5: rate (Rate)
            # 6: total (Total)

            sale_id = result[0]  # Used for the action button
            date = result[1]
            client = result[2]
            size = result[3]
            cashew_type = result[7]  # region field
            quantity = result[4]
            rate = result[5]
            total = result[6]

            # Create the display row (without the action button yet)
            display_values = [date, client, size, cashew_type, quantity, rate, total]

            for col, value in enumerate(display_values):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

            # Add action button in the last column
            btn = tk.Button(table_frame, text="Mark Paid", font=("Arial", 10),
                            command=lambda id=sale_id: update_sell(id),
                            bg="#4CAF50", fg="white")
            btn.grid(row=row_idx, column=7, sticky="ew", padx=5, pady=5)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching unpaid sales: {exp}")


def insert_raw_material():
    global date, item_type, quantity, raw

    if not all([date.get(), item_type.get(), quantity.get(), raw.get()]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        sql = "INSERT INTO raw_material (adate, raw, item_type, quantity) VALUES (%s, %s, %s, %s)"
        values = (date.get(), raw.get(), item_type.get(), quantity.get())
        cur.execute(sql, values)
        c.commit()
        messagebox.showinfo('Success', 'Raw Material Successfully Recorded')
        get_last_raw()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_raw():
    global last_raw

    for widget in last_raw.winfo_children():
        widget.destroy()

    # Main container frame that will center everything
    main_container = tk.Frame(last_raw, bg="#f5f5f5")
    main_container.pack(expand=True, fill="both", padx=20, pady=20)

    # Configure the main container to center its contents
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=1)

    # Content frame that will hold all elements
    content_frame = tk.Frame(main_container, bg="#f5f5f5")
    content_frame.grid(row=0, column=0, sticky="nsew")

    # Header frame
    header_frame = tk.Frame(content_frame, bg="#3a7ca5")
    header_frame.pack(fill="x", pady=(0, 10))
    tk.Label(header_frame, text="Recent Raw Material Entries", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table container frame - this will help center the table
    table_container = tk.Frame(content_frame, bg="#f5f5f5")
    table_container.pack(expand=True, fill="both")

    # Actual table frame
    table_frame = tk.Frame(table_container, bg="#f5f5f5")
    table_frame.pack(expand=True)  # This centers the table in the container

    # Column headers
    headers = ["Date", "Cashew", "Type", "Quantity"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5, width=15).grid(
            row=0, column=col, sticky="ew", padx=1, pady=1)

    try:
        sql = "SELECT * FROM raw_material ORDER BY id DESC LIMIT 12"
        cur.execute(sql)

        # Display data
        for row_idx, result in enumerate(cur, start=1):
            for col, value in enumerate(result[1:5]):  # Skip id column
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5, width=15).grid(
                    row=row_idx, column=col, sticky="ew", padx=1, pady=1)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching raw materials: {exp}")


def production_insert():
    global date, item_type, sa, sb, sc

    if not all([date.get(), item_type.get()]) or not any([sa.get(), sb.get(), sc.get()]):
        messagebox.showerror("Error", "All fields are required and at least one quantity!")
        return

    try:
        sql = "INSERT INTO production (adate, item_type, sa, sb, sc) VALUES (%s, %s, %s, %s, %s)"
        values = (date.get(), item_type.get(), sa.get(), sb.get(), sc.get())
        cur.execute(sql, values)

        region = item_type.get()
        for size, qty in [('A', sa.get()), ('B', sb.get()), ('C', sc.get())]:
            if qty > 0:
                update_sql = f"UPDATE stock_maintenance SET s{size.lower()} = s{size.lower()} + %s"
                cur.execute(update_sql, (qty,))

                update_sql = f"UPDATE stock_maintenance SET {region}{size} = {region}{size} + %s"
                cur.execute(update_sql, (qty,))

                log_sql = "INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)"
                log_values = (region, size, f"+{qty}")
                cur.execute(log_sql, log_values)

        c.commit()
        messagebox.showinfo('Success', 'Production Successfully Recorded')
        get_last_production()
        stock_maintain()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_last_production():
    global last_production

    for widget in last_production.winfo_children():
        widget.destroy()

    # Main container frame
    container = tk.Frame(last_production, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame - using tkinter Label for bg color
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Recent Production Entries", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Table frame
    table_frame = tk.Frame(container, bg="#f5f5f5")
    table_frame.pack(expand=True, fill="both")

    # Configure grid columns to center content
    for i in range(5):  # 5 columns
        table_frame.grid_columnconfigure(i, weight=1)

    # Column headers - using tkinter Labels
    headers = ["Date", "Type", "A", "B", "C"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(row=0, column=col, sticky="ew")

    try:
        sql = "SELECT * FROM production ORDER BY adate DESC LIMIT 10"
        cur.execute(sql)

        # Display data - using tkinter Labels
        for row_idx, result in enumerate(cur, start=1):
            display_order = [result[0], result[4], result[1], result[2], result[3]]
            for col, value in enumerate(display_order):
                tk.Label(table_frame, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(row=row_idx, column=col, sticky="ew")

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching production: {exp}")


def update_stock():
    try:
        cur.execute("SELECT * FROM stock_maintenance")
        result = cur.fetchone()

        regions = ["Kokan", "African", "Benin", "Ghana"]
        sizes = ["A", "B", "C"]
        columns = [f"{region}{size}" for region in regions for size in sizes]
        values = [input_fields[col].get() for col in columns]

        if not result:
            sql = f"INSERT INTO stock_maintenance ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        else:
            sql = f"UPDATE stock_maintenance SET {', '.join([f'{col}=%s' for col in columns])}"
            for col in columns:
                old_value = result[3 + columns.index(col)]
                new_value = input_fields[col].get()
                if new_value != old_value:
                    cur.execute("INSERT INTO stock_changes (region, cashew_type, `change`) VALUES (%s, %s, %s)",
                                (col[:-1], col[-1], f"{old_value} -> {new_value}"))

        cur.execute(sql, values)
        c.commit()
        messagebox.showinfo('Success', 'Stock Successfully Updated')
        stock_maintain()
    except Exception as exp:
        print(exp)
        c.rollback()
        messagebox.showerror('Error', f'An error occurred: {exp}')


def get_stock_changes():
    global changes_frame

    for widget in changes_frame.winfo_children():
        widget.destroy()

    # Main container frame - using grid
    container = tk.Frame(changes_frame, bg="#f5f5f5")
    container.pack(expand=True, fill="both", padx=20, pady=10)

    # Header frame - using grid
    header_frame = tk.Frame(container, bg="#3a7ca5")
    header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

    tk.Label(header_frame, text="Recent Stock Changes", font=("Arial", 12, "bold"),
             bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    # Column headers - using grid
    headers = ["Region", "Type", "Change", "Timestamp"]
    for col, header in enumerate(headers):
        tk.Label(container, text=header, font=("Arial", 10, "bold"),
                 bg="#2f6690", fg="white", padx=10, pady=5).grid(
            row=1, column=col, sticky="ew")

    try:
        sql = "SELECT region, cashew_type, `change`, timestamp FROM stock_changes ORDER BY timestamp DESC LIMIT 6"
        cur.execute(sql)

        for row_idx, result in enumerate(cur, start=2):
            for col, value in enumerate(result):
                tk.Label(container, text=value, font=("Arial", 10),
                         bg="#d9dcd6", padx=10, pady=5).grid(
                    row=row_idx, column=col, sticky="ew")

        # Configure column weights
        for col in range(4):
            container.grid_columnconfigure(col, weight=1)

    except Exception as exp:
        messagebox.showerror("Database Error", f"Error fetching stock changes: {exp}")


def sell():
    global middle_section, last_sell, unpaid_sell, date, client, items, quantity, rate, total_var, paid, gst, region

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    client = StringVar(middle_section)
    items = StringVar(middle_section)
    quantity = IntVar(middle_section)
    rate = DoubleVar(middle_section)
    total_var = DoubleVar(middle_section)
    paid = StringVar(middle_section)
    region = StringVar(middle_section)
    gst = IntVar(middle_section)

    items_choices = ["Select Cashew", "A", "B", "C"]
    paid_choices = ["Select Option", "paid", "not paid"]
    region_choices = ["Select Region", "Kokan", "African", "Benin", "Ghana"]

    # Configure grid weights
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_columnconfigure(1, weight=3)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)
    middle_section.grid_rowconfigure(2, weight=0)

    # Input Frame - Extended to full width
    input_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Configure input frame columns to use available space
    for i in range(11):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Client
    Label(input_frame, text="Client", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    client_entry = Entry(input_frame, font=("Arial", 11), textvariable=client)
    client_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    # Region
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    region_option = ttk.OptionMenu(input_frame, region, *region_choices)
    region_option.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    region.set(region_choices[1])

    # Items
    Label(input_frame, text="Select Size", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    items_option = ttk.OptionMenu(input_frame, items, *items_choices)
    items_option.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
    items.set(items_choices[1])

    # Quantity
    Label(input_frame, text="Quantity", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=4, sticky="w")
    quantity_entry = Entry(input_frame, font=("Arial", 11), textvariable=quantity)
    quantity_entry.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Rate
    Label(input_frame, text="Rate", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=5, sticky="w")
    rate_entry = Entry(input_frame, font=("Arial", 11), textvariable=rate)
    rate_entry.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

    # GST
    Label(input_frame, text="GST", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=6, sticky="w")
    C1 = Checkbutton(input_frame, variable=gst, onvalue=1, offvalue=0)
    C1.grid(row=1, column=6, sticky="w", padx=5, pady=5)

    # Total
    Label(input_frame, text="Total", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=7, sticky="w")
    total_entry = Label(input_frame, font=("Arial", 11), textvariable=total_var,
                        background="white", relief="sunken", width=15)
    total_entry.grid(row=1, column=7, sticky="ew", padx=5, pady=5)

    # Calculate Button
    btn = tk.Button(input_frame, text="Calculate", font=("Arial", 11),
                    command=calculate, bg="#4CAF50", fg="white")
    btn.grid(row=1, column=8, sticky="ew", padx=5, pady=5)

    # Paid/Not Paid
    Label(input_frame, text="Paid/Not", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=9, sticky="w")
    paid_option = ttk.OptionMenu(input_frame, paid, *paid_choices)
    paid_option.grid(row=1, column=9, sticky="ew", padx=5, pady=5)
    paid.set(paid_choices[1])

    # Add Sell Button
    btn = tk.Button(input_frame, text="Add Sale", font=("Arial", 11),
                    command=sell_insert, bg="#2196F3", fg="white")
    btn.grid(row=1, column=10, sticky="ew", padx=5, pady=5)

    # Client List (Left Side)
    client_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    client_frame.grid(row=1, column=0, sticky="nsew")

    Label(client_frame, text="Select Client Names", font=("Arial", 12, "bold"),
          background="#f5f5f5").pack(side=TOP, pady=5)

    scrollbar = Scrollbar(client_frame)
    scrollbar.pack(side="right", fill="y")

    listbox1 = Listbox(client_frame, yscrollcommand=scrollbar.set,
                       font=("Arial", 11), background="white")
    listbox1.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox1.yview)

    try:
        cur.execute("SELECT name FROM clients")
        for client_name in cur:
            listbox1.insert(END, client_name[0])
            listbox1.insert(END, "-" * 90)

        def select_client(e):
            selection = listbox1.curselection()
            if selection:
                selected = listbox1.get(selection[0])
                if selected and not selected.startswith("-"):
                    client.set(selected)

        listbox1.bind("<<ListboxSelect>>", select_client)
    except Exception as exp:
        messagebox.showerror("Error", f"Could not load clients: {exp}")

    # Sales Tables (Right Side)
    tables_frame = tk.Frame(middle_section, background="#f5f5f5")
    tables_frame.grid(row=1, column=1, sticky="nsew")
    tables_frame.grid_rowconfigure(0, weight=1)
    tables_frame.grid_rowconfigure(1, weight=1)
    tables_frame.grid_columnconfigure(0, weight=1)

    # Last Sales
    last_sell = tk.Frame(tables_frame, background="#f5f5f5")
    last_sell.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    get_last_sell()

    # Unpaid Sales
    unpaid_sell = tk.Frame(tables_frame, background="#f5f5f5")
    unpaid_sell.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    get_unpaid_sell()


def raw_material():
    global middle_section, last_raw, date, item_type, quantity, raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    item_type = StringVar(middle_section)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)

    item_type_choices = ["Select Type", "Kokan", "Benin", "African", "Ghana"]
    raw_choices = ["Select Size", "A", "B", "C"]

    # Configure middle section to expand properly
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)

    # Main container frame for centering
    container = tk.Frame(middle_section, background="#f5f5f5")
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    container.grid_columnconfigure(0, weight=1)

    # Input Frame - Centered with max width
    input_frame = tk.Frame(container, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Configure input frame columns to use available space
    for i in range(5):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Size
    Label(input_frame, text="Select Size", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    raw_option = ttk.OptionMenu(input_frame, raw, *raw_choices)
    raw_option.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    raw.set(raw_choices[0])

    # Type
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    item_type_option = ttk.OptionMenu(input_frame, item_type, *item_type_choices)
    item_type_option.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    item_type.set(item_type_choices[0])

    # Quantity
    Label(input_frame, text="Quantity", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    quantity_entry = Entry(input_frame, font=("Arial", 11), textvariable=quantity)
    quantity_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    # Add Button
    btn = tk.Button(input_frame, text="Add Raw Material", font=("Arial", 11),
                    command=insert_raw_material, bg="#2196F3", fg="white")
    btn.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Recent Entries - Centered container
    last_raw = tk.Frame(container, background="#f5f5f5", padx=20, pady=10)
    last_raw.grid(row=1, column=0, sticky="nsew")
    last_raw.grid_columnconfigure(0, weight=1)

    get_last_raw()


def production():
    global middle_section, last_production, date, sa, sb, sc, item_type

    for widget in middle_section.winfo_children():
        widget.destroy()

    sa = IntVar(middle_section)
    sb = IntVar(middle_section)
    sc = IntVar(middle_section)
    date = StringVar(middle_section, value=today_date)
    item_type = StringVar(middle_section)

    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=0)
    middle_section.grid_rowconfigure(1, weight=1)

    # Input Frame - Extended to full width
    input_frame = tk.Frame(middle_section, background="#f5f5f5", padx=10, pady=10)
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Configure input frame columns to use available space
    for i in range(6):
        input_frame.grid_columnconfigure(i, weight=1)

    # Date
    Label(input_frame, text="Date", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=0, sticky="w")
    date_entry = Entry(input_frame, font=("Arial", 11), textvariable=date)
    date_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Type
    type_choices = ["Select Type", "Kokan", "African", "Benin", "Ghana"]
    Label(input_frame, text="Select Type", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=1, sticky="w")
    type_option = ttk.OptionMenu(input_frame, item_type, *type_choices)
    type_option.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    item_type.set(type_choices[0])

    # A, B, C
    Label(input_frame, text="A", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=2, sticky="w")
    sa_entry = Entry(input_frame, font=("Arial", 11), textvariable=sa)
    sa_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

    Label(input_frame, text="B", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=3, sticky="w")
    sb_entry = Entry(input_frame, font=("Arial", 11), textvariable=sb)
    sb_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    Label(input_frame, text="C", font=("Arial", 11), background="#f5f5f5").grid(row=0, column=4, sticky="w")
    sc_entry = Entry(input_frame, font=("Arial", 11), textvariable=sc)
    sc_entry.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

    # Add Button
    btn = tk.Button(input_frame, text="Add", font=("Arial", 11),
                    command=production_insert, bg="#2196F3", fg="white")
    btn.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

    # Recent Entries
    last_production = tk.Frame(middle_section, background="#f5f5f5", padx=20, pady=10)
    last_production.grid(row=1, column=0, sticky="nsew")
    get_last_production()


def stock_maintain():
    global middle_section, input_fields, changes_frame

    for widget in middle_section.winfo_children():
        widget.destroy()

    # Configure middle section layout
    middle_section.grid_columnconfigure(0, weight=1)
    middle_section.grid_rowconfigure(0, weight=1)
    middle_section.grid_rowconfigure(1, weight=1)

    # Stock Frame - using grid
    stock_frame = tk.Frame(middle_section, bg="#f5f5f5", padx=20, pady=10)
    stock_frame.grid(row=0, column=0, sticky="nsew")
    stock_frame.grid_columnconfigure(0, weight=1)

    # Header frame - using pack inside its own frame
    header_container = tk.Frame(stock_frame, bg="#f5f5f5")
    header_container.pack(fill="x")

    header_frame = tk.Frame(header_container, bg="#3a7ca5")
    header_frame.pack(fill="x")

    tk.Label(header_frame, text="Current Stock Levels", font=("Arial", 12, "bold"),
            bg="#3a7ca5", fg="white", padx=10, pady=5).pack()

    try:
        cur.execute("SELECT * FROM stock_maintenance")
        result = cur.fetchone()

        input_fields = {}
        regions = ["Kokan", "African", "Benin", "Ghana"]
        sizes = ["A", "B", "C"]

        # Table frame - using grid
        table_frame = tk.Frame(stock_frame, bg="#f5f5f5")
        table_frame.pack(expand=True, fill="both")

        # Column headers - using grid
        tk.Label(table_frame, text="Region", font=("Arial", 10, "bold"),
                bg="#2f6690", fg="white", padx=10, pady=5).grid(
                row=1, column=0, sticky="ew")

        for col, size in enumerate(sizes, start=1):
            tk.Label(table_frame, text=size, font=("Arial", 10, "bold"),
                    bg="#2f6690", fg="white", padx=10, pady=5).grid(
                    row=1, column=col, sticky="ew")

        # Input fields - using grid
        for row_idx, region in enumerate(regions, start=2):
            tk.Label(table_frame, text=region, font=("Arial", 10),
                    bg="#d9dcd6", padx=10, pady=5).grid(
                    row=row_idx, column=0, sticky="ew")

            for col_idx, size in enumerate(sizes, start=1):
                col_name = f"{region}{size}"
                value = result[3 + (row_idx - 2) * 3 + (col_idx - 1)] if result else 0

                var = IntVar(value=value)
                tk.Entry(table_frame, textvariable=var, font=("Arial", 10),
                        justify="center", bg="white").grid(
                        row=row_idx, column=col_idx, sticky="ew", padx=5, pady=5)
                input_fields[col_name] = var

        # Configure table columns
        for col in range(4):
            table_frame.grid_columnconfigure(col, weight=1)

        # Update button - using pack
        btn_frame = tk.Frame(stock_frame, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Update Stock", font=("Arial", 11),
                command=update_stock, bg="#4CAF50", fg="white").pack()

    except Exception as exp:
        messagebox.showerror("Error", f"Could not load stock: {exp}")

    # Changes Frame - using grid
    changes_frame = tk.Frame(middle_section, bg="#f5f5f5", padx=20, pady=10)
    changes_frame.grid(row=1, column=0, sticky="nsew")
    get_stock_changes()


def main():
    global middle_section

    root = tk.Tk()
    root.title("Cashew Factory Coordination System")
    root.state("zoomed")
    root.configure(bg="#f5f5f5")

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')

    # Configure styles
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TButton',
                    foreground='white',
                    background='#4CAF50',
                    bordercolor='#4CAF50',
                    lightcolor='#4CAF50',
                    darkcolor='#45a049',
                    relief='flat',
                    padding=5)
    style.map('TButton',
              background=[('active', '#45a049')],
              foreground=[('active', 'white')])

    style.configure('TLabel',
                    font=('Arial', 10),
                    foreground='#333',
                    background='#f5f5f5',
                    padding=5)
    style.configure('TEntry',
                    fieldbackground='white',
                    foreground='#333',
                    insertcolor='black',
                    relief='sunken')
    style.configure('TMenubutton',
                    font=('Arial', 10),
                    foreground='#333',
                    background='#f5f5f5',
                    relief='raised')

    # Side Menu
    side_menu = tk.Frame(root, bg="#333", padx=10, pady=10)
    side_menu.pack(side="top", fill="x")

    buttons = [
        ('SALES', sell),
        ('RAW MATERIAL', raw_material),
        ('PRODUCTION', production),
        ('STOCK MAINTENANCE', stock_maintain),
        ('EXIT', root.destroy)
    ]

    for idx, (text, command) in enumerate(buttons):
        if text == "EXIT":
            btn = tk.Button(side_menu, text=text, command=command,
                            font=("Arial", 11, "bold"), bg="#e74c3c", fg="white")
        else:
            btn = tk.Button(side_menu, text=text, command=command,
                            font=("Arial", 11, "bold"), bg="#3498db", fg="white")

        btn.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")
        side_menu.grid_columnconfigure(idx, weight=1)

    # Scrollable Middle Section
    sw = ScrolledWindow(root)
    sw.pack(fill="both", expand=True)

    # Middle Section inside the Scrollable Frame
    middle_section = tk.Frame(sw.frame, background="#f5f5f5")
    middle_section.pack(fill="both", expand=True)

    # Initial welcome message
    Label(middle_section, text="Please select the Domain",
          font=("Arial", 14, "bold"), background="#f5f5f5").pack(expand=True)

    root.mainloop()


'''
def mainmenu():
    if flag == 'sto':
        sto.destroy()
    elif flag == 'billingsto':
        billingsto.destroy()
    elif flag == 'dailyinco':
        dailyinco.destroy()
'''

if __name__ == "__main__":
    main()