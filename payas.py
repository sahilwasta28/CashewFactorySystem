'''from tkinter import *
import tkinter as tk
from tkinter import ttk
import win32api
from tkinter import filedialog
import mysql.connector
from datetime import date as dat
from tkinter import messagebox

now = dat.today()
today_date = now

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

def print_file():
    file_to_print = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)


def sell_insert():
    global date, client, items, quantity, rate, total, paid

    # Calculate total as quantity * rate
    total_value = float(quantity.get()) * float(rate.get())  # Calculate total as quantity * rate

    # Print the values to verify everything is correct
    print(date.get(), client.get(), items.get(), quantity.get(), rate.get(), total_value, paid.get())

    success = True
    try:
        # Insert into sell table
        sql = """
        INSERT INTO sell (adate, client, item, quantity, rate, total, paid)
        VALUES (STR_TO_DATE('%s', '%%Y-%%m-%%d'), '%s', '%s', %d, %f, %f, '%s')
        """ % (
            date.get(), client.get(), items.get(),
            int(quantity.get()), float(rate.get()), total_value, paid.get())
        print(sql)
        cur.execute(sql)

        # Update stock_maintenance_payas table for valid items
        item_column_map = {
            'A': 'KokanA',  # Map 'A' to 'KokanA'
            'B': 'KokanB',  # Map 'B' to 'KokanB'
            'C': 'KokanC',  # Map 'C' to 'KokanC'
            'A180': 'KokanA',  # Map 'A180' to 'KokanA' (or appropriate column)
            # Add other mappings as needed
        }

        # Get the corresponding column for the item
        item_column = item_column_map.get(items.get())

        if item_column:
            sql_update = """
            UPDATE stock_maintenance_payas
            SET %s = %s - %d
            WHERE 1
            """ % (item_column, item_column, int(quantity.get()))  # Update stock
            print(sql_update)
            cur.execute(sql_update)
        else:
            raise ValueError("Invalid item selected")

    except Exception as exp:
        print(exp)
        c.rollback()  # Rollback on error
        success = False

    if success:
        c.commit()  # Commit if everything is successful
        messagebox.showinfo('Successful', 'Sell Successfully Inserted')
        get_last_sell()
        get_unpaid_sell()





def get_last_sell():
    global last_sell
    for widget in last_sell.winfo_children():
        widget.destroy()
    Label(last_sell, text="-" * 40 + "Last Five Sells" + "-" * 40, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(
        row=1, column=1, columnspan=7)

    Label(last_sell, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=1)
    Label(last_sell, text="Client", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=2)
    Label(last_sell, text="Type", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=3)
    Label(last_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=4)
    Label(last_sell, text="Rate", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=5)
    Label(last_sell, text="Total", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=6)
    Label(last_sell, text="Paid", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=7)

    try:
        sql = "SELECT * FROM sell ORDER BY adate DESC LIMIT 5"
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(last_sell, text=result[1], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=1)
            Label(last_sell, text=result[2], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=2)
            Label(last_sell, text=result[3], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=3)
            Label(last_sell, text=result[4], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=4)
            Label(last_sell, text=result[5], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=5)
            Label(last_sell, text=result[6], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=6)
            Label(last_sell, text=result[7], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=7)
            i += 1
    except Exception as exp:
        # insert_error(exp)  # Assuming this function is defined elsewhere
        print(exp)

    Label(last_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=i, column=1, columnspan=7)

def update_sell(id):
    success = True
    try:
        sql = "UPDATE sell SET paid='paid' WHERE id=%s" % (id)
        print(sql)
        cur.execute(sql)
    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        # insert_error(exp)  # Assuming this function is defined elsewhere
    if success:
        c.commit()
        # insert_info("Sell Successfully Updated")  # Assuming this function is defined elsewhere
        messagebox.showinfo('Successful', 'Sell Successfully Updated')
        get_last_sell()
        get_unpaid_sell()

def get_unpaid_sell():
    global unpaid_sell
    for widget in unpaid_sell.winfo_children():
        widget.destroy()
    Label(unpaid_sell, text="-" * 40 + "Unpaid Sells List" + "-" * 40, font=("Belwe Bd BT", 15),
          background="black", foreground="white").grid(row=1, column=1, columnspan=9)

    Label(unpaid_sell, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=1)
    Label(unpaid_sell, text="Client", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=2)
    Label(unpaid_sell, text="Type", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=3)
    Label(unpaid_sell, text="Quantity", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=4)
    Label(unpaid_sell, text="Rate", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=5)
    Label(unpaid_sell, text="Total", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=6)
    Label(unpaid_sell, text="Action", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=7)

    try:
        sql = "SELECT * FROM sell WHERE paid='not paid' ORDER BY adate DESC"
        print(sql)
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(unpaid_sell, text=result[1], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=1)
            Label(unpaid_sell, text=result[2], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=2)
            Label(unpaid_sell, text=result[3], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=3)
            Label(unpaid_sell, text=result[4], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=4)
            Label(unpaid_sell, text=result[5], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=5)
            Label(unpaid_sell, text=result[6], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=6)
            tk.Button(unpaid_sell, text="Make Paid", font=("Belwe lt BT", 15), background="green", foreground="white",
                      command=lambda id=result[0]: update_sell(id)).grid(row=i, column=7)
            i += 1
    except Exception as exp:
        # insert_error(exp)  # Assuming this function is defined elsewhere
        print(exp)

    Label(unpaid_sell, text="-" * 80, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=i + 1, column=1,
                                                                                         columnspan=7)

def calculate():
    global date, client, items, quantity, rate, total_var, paid, gst
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

    items_choices = ["Select Cashew", "A180", "A210", "B320", "B240", "C400", "C440"]
    paid_choices = ["Select Option", "paid", "not paid"]

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    client_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=client)
    Label(middle_section, text="Client", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=2)
    client_entry.grid(row=2, column=2)

    items_option = ttk.OptionMenu(middle_section, items, *items_choices)
    Label(middle_section, text="Select Items", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=3)
    items_option.grid(row=2, column=3)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=4)
    quantity_entry.grid(row=2, column=4)

    rate_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=rate)
    Label(middle_section, text="Rate", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=5)
    rate_entry.grid(row=2, column=5)

    Label(middle_section, text="GST", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=6)

    gst = IntVar(middle_section)
    C1 = Checkbutton(middle_section, text="", variable=gst, onvalue=1, offvalue=0)
    C1.grid(row=2, column=6)

    Label(middle_section, text="Total", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=7, columnspan=2)
    total_entry = Label(middle_section, font=("Belwe lt BT", 15), textvariable=total_var)
    tk.Button(middle_section, text="Calculate", font=("Belwe lt BT", 15), background="green", foreground="white", command=calculate).grid(row=2, column=8)
    total_entry.grid(row=2, column=7)

    paid_option = ttk.OptionMenu(middle_section, paid, *paid_choices)
    Label(middle_section, text="Paid/Not", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=9)
    paid_option.grid(row=2, column=9)

    items.set(items_choices[1])
    paid.set(paid_choices[1])

    tk.Button(middle_section, text="Add Sell", font=("Belwe Bd BT", 15), background="green", foreground="white", command=sell_insert).grid(row=2, column=10)

    client_names = tk.Frame(middle_section)
    Label(client_names, text="-" * 10 + "Select Client Names From Here" + "-" * 10, font=("Belwe Bd BT", 15),
          background="black", foreground="white").pack(side=TOP)
    sql = "SELECT name FROM clients"
    cur.execute(sql)

    def onmousewheel(event):
        listbox1.yview('scroll', event.delta, 'units')
        return "break"

    def select_cn(e):
        name = listbox1.curselection()
        client.set(client_names_list[name[0]])

    scrollbar = Scrollbar(client_names)
    listbox1 = Listbox(client_names, height=5)
    listbox1.pack()

    client_names_list = []

    for result in cur:
        listbox1.insert(END, result[0])
        client_names_list.append(result[0])

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
    global date, quantity, raw
    print(date.get(), raw.get(), quantity.get())
    success = True
    try:
        if raw.get() == 'A':
            size = 'sa'
        if raw.get() == 'B':
            size = 'sb'
        if raw.get() == 'C':
            size = 'sc'

        sql = "INSERT INTO raw_material_payas(adate, raw, quantity) VALUES (date('%s'), '%s', %i)" % (date.get(), raw.get(), quantity.get())
        cur.execute(sql)
        print(size)

        sql = "UPDATE stock_maintenance SET %s = %s - %i" % (size, size, quantity.get())
        cur.execute(sql)
        sql = "UPDATE stock_maintenance_payas SET %s = %s + %i" % (size, size, quantity.get())
        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        # insert_error(exp)  # Assuming this function is defined elsewhere
    if success:
        c.commit()
        # insert_info("Raw Material Successfully Inserted")  # Assuming this function is defined elsewhere
        messagebox.showinfo('Successful', 'Raw Material Successfully Inserted')
        get_last_raw()

def get_last_raw():
    global last_raw
    for widget in last_raw.winfo_children():
        widget.destroy()

    # Column headers
    Label(last_raw, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=6, column=1)
    Label(last_raw, text="Cashew Type", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=6, column=2)
    Label(last_raw, text="Quantity", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=6, column=3)

    try:
        # Fetch the latest records from the database
        sql = "SELECT * FROM raw_material_payas ORDER BY id DESC"
        print(sql)  # Debugging: print the SQL query
        cur.execute(sql)
        results = cur.fetchall()  # Fetch all results
        print(results)  # Debugging: print the results

        i = 7
        for result in results:
            # Access data from result tuple
            date_value = result[1]  # Date (2nd column in the result)
            cashew_type = result[2]  # Cashew Type (3rd column in the result)
            quantity = result[4] if result[4] is not None else "N/A"  # Quantity (5th column in the result)

            print(f"Date: {date_value}, Cashew Type: {cashew_type}, Quantity: {quantity}")  # Debugging: print the values

            # Display the values in the labels
            Label(last_raw, text=date_value, background="black", foreground="white").grid(row=i, column=1)  # Date
            Label(last_raw, text=cashew_type, background="black", foreground="white").grid(row=i, column=2)  # Cashew Type
            Label(last_raw, text=quantity, background="black", foreground="white").grid(row=i, column=3)  # Quantity
            i += 1
    except Exception as exp:
        print(exp)  # Debugging: print any exceptions

    # Footer line
    Label(last_raw, text="-" * 80, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=i, column=1, columnspan=3)


def raw_material():
    global middle_section, last_raw, date, quantity, raw

    for widget in middle_section.winfo_children():
        widget.destroy()

    date = StringVar(middle_section, value=today_date)
    raw = StringVar(middle_section)
    quantity = IntVar(middle_section)

    raw_choices = ["", "A", "B", "C"]
    raw.set(raw_choices[1])  # set the default option

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    raw_option = ttk.OptionMenu(middle_section, raw, *raw_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=2)
    raw_option.grid(row=2, column=2)

    quantity_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=quantity)
    Label(middle_section, text="Quantity", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=3)
    quantity_entry.grid(row=2, column=3)

    tk.Button(middle_section, text="Add Raw Material", font=("Belwe Bd BT", 15), background="green", foreground="white", command=insert_raw_material).grid(row=2, column=5)
    Label(middle_section, text="-" * 60 + "Last Raw Material Entry" + "-" * 60, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, columnspan=5)

    tk.Button(middle_section, text="Print", font=("Belwe Bd BT", 15), background="green", foreground="white", command=print_file).grid(row=2, column=4)

    last_raw = tk.Frame(middle_section, background="black")
    get_last_raw()
    last_raw.grid(row=4, column=1, columnspan=4)

def production_insert():
    global middle_section, date, s1, s2, type, size
    total = s1.get() + s2.get()
    l1 = size[0]
    l2 = size[1]
    if type.get() == 'A':
        st = 'sa'
    if type.get() == 'B':
        st = 'sb'
    if type.get() == 'C':
        st = 'sc'

    success = True
    try:
        sql = "INSERT INTO production_payas(adate, type, size1, size2) VALUES (date('%s'), '%s', %i, %i)" % (date.get(), type.get(), s1.get(), s2.get())
        cur.execute(sql)

        sql = "UPDATE stock_maintenance_payas SET %s = %s - %i, %s%s = %s%s + %i, %s%s = %s%s + %i" % (st, st, total, type.get(), l1, type.get(), l1, s1.get(), type.get(), l2, type.get(), l2, s2.get())
        cur.execute(sql)

    except Exception as exp:
        print(exp)
        c.rollback()
        success = False
        # insert_error(exp)  # Assuming this function is defined elsewhere
    if success:
        c.commit()
        # insert_info("Production Successfully Inserted")  # Assuming this function is defined elsewhere
        messagebox.showinfo('Successful', 'Production Successfully Inserted')
        get_last_production()

def get_last_production():
    global last_production
    for widget in last_production.winfo_children():
        widget.destroy()

    Label(last_production, text="-" * 40 + "Last Production" + "-" * 40, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=1, columnspan=4)

    Label(last_production, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=1)
    Label(last_production, text="TYPE", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=2)
    Label(last_production, text="Size", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=3)
    Label(last_production, text="Size", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=3, column=4)

    try:
        sql = "SELECT * FROM production_payas ORDER BY adate DESC"
        cur.execute(sql)
        i = 4
        for result in cur:
            Label(last_production, text=result[0], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=1)
            Label(last_production, text=result[1], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=2)
            Label(last_production, text=result[2], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=3)
            Label(last_production, text=result[3], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=i, column=4)
            i += 1

    except Exception as exp:
        # insert_error(exp)  # Assuming this function is defined elsewhere
        print(exp)

def production():
    global middle_section, type, last_production, date, s1, s2, size

    for widget in middle_section.winfo_children():
        widget.destroy()
    s1 = IntVar(middle_section)
    s2 = IntVar(middle_section)
    type = StringVar(middle_section)
    date = StringVar(middle_section, value=today_date)

    type_choices = ["Select Type", "A", "B", "C"]
    size = ["", ""]

    date_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=date)
    Label(middle_section, text="Date", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    type_option = ttk.OptionMenu(middle_section, type, *type_choices)
    Label(middle_section, text="Select Type", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=2)
    type_option.grid(row=2, column=2)

    def selects():
        global size
        if type.get() == "A":
            size[0] = "180"
            size[1] = "210"
        elif type.get() == 'B':
            size[0] = '240'
            size[1] = '320'
        elif type.get() == 'C':
            size[0] = '400'
            size[1] = '440'
        s1_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=s1)
        Label(middle_section, text=size[0], font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=3)
        s1_entry.grid(row=2, column=3)

        s2_entry = Entry(middle_section, font=("Belwe lt BT", 10), textvariable=s2)
        Label(middle_section, text=size[1], font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=4)
        s2_entry.grid(row=2, column=4)

    selects()

    tk.Button(middle_section, text="Add", font=("Belwe Bd BT", 15), background="green", foreground="white", command=production_insert).grid(row=2, column=5)
    tk.Button(middle_section, text="Refresh", font=("Belwe Bd BT", 15), background="green", foreground="white", command=selects).grid(row=2, column=6)

    last_production = tk.Frame(middle_section, background="black")
    get_last_production()
    last_production.grid(row=4, column=1, columnspan=5)

def stock_maintain():
    global middle_section

    for widget in middle_section.winfo_children():
        widget.destroy()

    bottle_frame = tk.Frame(middle_section, background="black")
    Label(bottle_frame, text="-" * 30 + "Cashew" + "-" * 30, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=1, column=1, columnspan=9)
    Label(bottle_frame, text="A", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=1)
    Label(bottle_frame, text="B", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=2)
    Label(bottle_frame, text="C", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=3)
    Label(bottle_frame, text="A180", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=4)
    Label(bottle_frame, text="A210", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=5)
    Label(bottle_frame, text="B320", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=6)
    Label(bottle_frame, text="B240", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=7)
    Label(bottle_frame, text="C400", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=8)
    Label(bottle_frame, text="C440", font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=9)

    sql = "SELECT * FROM stock_maintenance_payas"
    cur.execute(sql)
    result = cur.fetchone()
    print(result)
    Label(bottle_frame, text=result[0], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=1)
    Label(bottle_frame, text=result[1], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=2)
    Label(bottle_frame, text=result[2], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=3)
    Label(bottle_frame, text=result[3], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=4)
    Label(bottle_frame, text=result[4], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=5)
    Label(bottle_frame, text=result[5], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=6)
    Label(bottle_frame, text=result[6], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=7)
    Label(bottle_frame, text=result[7], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=8)
    Label(bottle_frame, text=result[8], font=("Belwe lt BT", 15), background="black", foreground="white").grid(row=3, column=9)
    bottle_frame.grid(row=1, column=1, sticky="W", columnspan=9)

def main():
    Payas GUI
    global middle_section
    payas = Tk()
    payas.configure(background="black")
    payas.title('Grading')
    payas.state("zoomed")

    side_menu = tk.Frame(payas, background="black")

    tk.Button(side_menu, width=20, text='Sell', font=("Belwe Bd BT", 15), background="green", foreground="white", command=sell).grid(row=0, column=1)
    tk.Button(side_menu, width=20, text='RAW MATERIAL', font=("Belwe Bd BT", 15), background="green", foreground="white", command=raw_material).grid(row=0, column=2)
    tk.Button(side_menu, width=20, text='PRODUCTION', font=("Belwe Bd BT", 15), background="green", foreground="white", command=production).grid(row=0, column=3)
    tk.Button(side_menu, width=20, text='STOCK MAINTENANCE', font=("Belwe Bd BT", 15), background="green", foreground="white", command=stock_maintain).grid(row=0, column=4)
    tk.Button(side_menu, width=20, text='Back to Main Menu', font=("Belwe Bd BT", 15), background="green", foreground="white", command=payas.destroy).grid(row=0, column=5)
    Label(side_menu, text='-' * 200, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=2, column=1, columnspan=5, sticky='N')

    side_menu.pack(side=TOP)

    middle_section = tk.Frame(payas, background="black")
    Label(middle_section, text='-' * 48 + 'Grading' + '-' * 49, font=("Belwe Bd BT", 15), background="black", foreground="white").grid(row=0, column=0, columnspan=9, sticky='N')
    middle_section.pack(fill=BOTH, expand=1)

    payas.mainloop()

if __name__ == "__main__":
    main()'''
'''
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar
from datetime import datetime
import mysql.connector
import pandas as pd
import os
import subprocess  # To call index.py from here

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

class MonthlyLogsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Logs")
        self.root.configure(background="black")
        self.root.state("zoomed")  # Set the window to be maximized initially

        # Dropdown for selecting module (Sells, Raw Material, Production, Stock Maintenance)
        self.selected_module = StringVar()
        self.selected_module.set("Sells")  # Default to "Sells"

        self.module_label = tk.Label(self.root, text="Area ? :", font=("Arial", 12), bg="black", fg="white")
        self.module_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.module_dropdown = ttk.Combobox(self.root, textvariable=self.selected_module, values=["Sells", "Raw Material", "Production", "Stock Maintenance"], state="readonly")
        self.module_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown for selecting month
        self.selected_month = StringVar()
        self.selected_month.set(datetime.now().strftime("%B"))  # Set current month by default

        self.month_label = tk.Label(self.root, text="Month:", font=("Arial", 12), bg="black", fg="white")
        self.month_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.month_dropdown = ttk.Combobox(self.root, textvariable=self.selected_month, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], state="readonly")
        self.month_dropdown.grid(row=0, column=3, padx=10, pady=10)

        # Button to load data based on selected month and module
        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=2, padx=10, pady=10)

        # Button to return to main page (index.py)
        self.return_button = tk.Button(root, text="Return to Main Page", command=self.return_to_main_page)
        self.return_button.grid(row=3, column=3, padx=10, pady=10)

        # Table to display data
        self.tree = ttk.Treeview(self.root, columns=(), show="headings")
        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Save button to save data to Excel
        self.save_button = tk.Button(self.root, text="Save to Excel", font=("Arial", 15), background="blue", foreground="white", command=self.save_data_to_excel)
        self.save_button.grid(row=3, column=1, columnspan=2, pady=6)

        # Ensure the table expands to fill the window
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

    def run(self):
        self.root.mainloop()

    def load_data(self):
        """Load data based on selected month and module"""
        selected_month = self.selected_month.get()
        selected_module = self.selected_module.get()

        # Convert the selected month to the corresponding number
        month_number = datetime.strptime(selected_month, "%B").month

        # Clear previous data display
        self.tree.delete(*self.tree.get_children())

        data_found = False

        if selected_module == "Sells":
            self.load_sells_data(month_number)
        elif selected_module == "Raw Material":
            self.load_raw_material_data(month_number)
        elif selected_module == "Production":
            self.load_production_data(month_number)
        elif selected_module == "Stock Maintenance":
            self.load_stock_maintenance_data(month_number)

    def load_sells_data(self, month):
        """Load sells data for the selected month."""
        self.tree["columns"] = ("Date", "Client", "Item", "Quantity", "Rate", "Total", "Paid")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, client, item, quantity, rate, total, paid FROM sell WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data", "No data", "", "", "", "", ""))
        else:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def load_raw_material_data(self, month):
        """Load raw material data for the selected month."""
        self.tree["columns"] = ("Date", "Raw", "Item Type", "Quantity")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, raw, item_type, quantity FROM raw_material WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data", "No data", "", ""))
        else:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def load_production_data(self, month):
        """Load production data for the selected month."""
        self.tree["columns"] = ("Date", "Item Type", "A", "B", "C")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, item_type, sa, sb, sc FROM production WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data", "No data", "", "", ""))
        else:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def load_stock_maintenance_data(self, month):
        """Load stock maintenance data for the selected month."""
        self.tree["columns"] = ("Date", "Region", "Cashew Type", "Change")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT timestamp, region, cashew_type, `change` FROM stock_changes WHERE timestamp BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data", "No data", "", ""))
        else:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def save_data_to_excel(self):
        """Save the currently displayed data to an Excel file in the Downloads folder."""
        selected_module = self.selected_module.get()

        # Get the user's Downloads folder path
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Prepare the file path
        file_path = os.path.join(downloads_folder, f"{selected_module}_{datetime.now().strftime('%Y-%m')}.xlsx")

        # Prepare data for saving
        data = []
        columns = self.tree["columns"]
        for item in self.tree.get_children():
            row = self.tree.item(item)["values"]
            data.append(row)

        # Create a new Excel file and write data
        try:
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def return_to_main_page(self):
        """Close current window and open index.py"""
        self.root.destroy()  # Close the current window
        # subprocess.Popen(["python", "index.py"])  # Open index.py


def main():
    root = tk.Tk()
    app = MonthlyLogsApp(root)
    app.run()  # Running the app

if __name__ == "__main__":
    main()
'''
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar
from datetime import datetime
import mysql.connector
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import qrcode
from PIL import Image, ImageTk
import subprocess
import threading

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Google Drive API Setup
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your service account JSON file

# Authenticate with Google Drive
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Google Drive Folder ID where files will be uploaded (Replace with your actual folder ID)
DRIVE_FOLDER_ID = "17PryBSaH9_M3dJ042A4sv3kru2UD9TBJ"

# Path to the output file
OUTPUT_FILE_PATH = "demand_prediction_output.png"


class MonthlyLogsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cashew Factory Management System - Monthly Logs")
        self.root.configure(background="#f0f0f0")
        self.root.state("zoomed")  # Maximize window

        # Set application icon (if available)
        try:
            self.root.iconbitmap("app_icon.ico")
        except:
            pass

        # Configure grid weights for dynamic resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=0)
        self.root.grid_rowconfigure(5, weight=0)

        # Create styles for widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the 'clam' theme as a base

        # Configure colors
        bg_color = "#f0f0f0"
        header_bg = "#1e3d59"
        header_fg = "white"
        btn_color = "#ff6e40"
        btn_fg = "white"
        accent_color = "#ffc13b"

        # Configure ttk styles
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("Header.TLabel", background=header_bg, foreground=header_fg, font=("Segoe UI", 14, "bold"),
                             padding=10)
        self.style.configure("TButton", font=("Segoe UI", 11), background=btn_color, foreground=btn_fg)
        self.style.configure("Load.TButton", font=("Segoe UI", 12, "bold"), background=accent_color)
        self.style.configure("Save.TButton", font=("Segoe UI", 12, "bold"), background="#4CAF50", foreground="white")
        self.style.configure("Return.TButton", font=("Segoe UI", 11, "bold"), background="#f44336", foreground="white")

        # Configure Treeview
        self.style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=header_bg,
                             foreground="white")
        self.style.map("Treeview", background=[("selected", accent_color)], foreground=[("selected", "black")])

        # Create main frame with padding
        self.main_frame = ttk.Frame(root, style="TFrame", padding=(20, 20, 20, 20))
        self.main_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Header with title
        self.header_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self.header_frame,
                                     text="MONTHLY LOGS MANAGEMENT",
                                     style="Header.TLabel",
                                     background=header_bg,
                                     foreground=header_fg)
        self.title_label.grid(row=0, column=0, sticky="ew")

        # Create control panel frame
        self.control_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Configure control frame columns
        for i in range(6):
            self.control_frame.grid_columnconfigure(i, weight=1)

        # Area selection
        self.selected_module = StringVar()
        self.selected_module.set("Sales")  # Default to "Sales"

        self.module_label = ttk.Label(self.control_frame, text="Area:", font=("Segoe UI", 12, "bold"))
        self.module_label.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="e")

        module_values = ["Sales", "Raw Material", "Production", "Stock Maintenance"]
        self.module_dropdown = ttk.Combobox(self.control_frame, textvariable=self.selected_module,
                                            values=module_values, state="readonly", width=20,
                                            font=("Segoe UI", 11))
        self.module_dropdown.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Month selection
        self.selected_month = StringVar()
        self.selected_month.set(datetime.now().strftime("%B"))  # Set current month by default

        self.month_label = ttk.Label(self.control_frame, text="Month:", font=("Segoe UI", 12, "bold"))
        self.month_label.grid(row=0, column=2, padx=(5, 5), pady=10, sticky="e")

        month_values = ["January", "February", "March", "April", "May", "June", "July",
                        "August", "September", "October", "November", "December"]
        self.month_dropdown = ttk.Combobox(self.control_frame, textvariable=self.selected_month,
                                           values=month_values, state="readonly", width=20,
                                           font=("Segoe UI", 11))
        self.month_dropdown.grid(row=0, column=3, padx=5, pady=10, sticky="w")

        # Load button with modern styling
        self.load_button = tk.Button(self.control_frame, text="LOAD DATA", font=("Segoe UI", 11, "bold"),
                                     bg=accent_color, fg="black", padx=20, pady=8,
                                     relief=tk.RAISED, borderwidth=0,
                                     command=self.load_data,
                                     activebackground="#e8b935", activeforeground="black",
                                     cursor="hand2")
        self.load_button.grid(row=0, column=4, columnspan=2, padx=20, pady=10, sticky="ew")

        # Create frame for the treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview with scrollbars
        self.tree = ttk.Treeview(self.tree_frame, columns=(), show="headings")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Save button (Uploads to Google Drive)
        self.save_button = tk.Button(self.button_frame, text="SAVE TO GOOGLE DRIVE",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#4CAF50", fg="white",
                                     padx=20, pady=10,
                                     relief=tk.RAISED, borderwidth=0,
                                     command=self.upload_to_drive,
                                     activebackground="#45a049", activeforeground="white",
                                     cursor="hand2")
        self.save_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Return to main page button
        self.return_button = tk.Button(self.button_frame, text="RETURN TO MAIN PAGE",
                                       font=("Segoe UI", 11, "bold"),
                                       bg="#f44336", fg="white",
                                       padx=20, pady=10,
                                       relief=tk.RAISED, borderwidth=0,
                                       command=self.return_to_main_page,
                                       activebackground="#d32f2f", activeforeground="white",
                                       cursor="hand2")
        self.return_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # QR code frame
        self.qr_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.qr_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        self.qr_frame.grid_columnconfigure(0, weight=1)

        # Status bar at the bottom
        self.status_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.status_frame.grid(row=6, column=0, sticky="ew", pady=(10, 0))

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                      font=("Segoe UI", 10), anchor="w")
        self.status_label.grid(row=0, column=0, sticky="w")

        # Generate and display QR code
        #self.generate_qr_code()

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def load_data(self):
        """Load data based on selected month and module"""
        self.status_var.set("Loading data...")
        selected_month = self.selected_month.get()
        selected_module = self.selected_module.get()

        # Convert month to number
        month_number = datetime.strptime(selected_month, "%B").month

        # Clear previous data
        self.tree.delete(*self.tree.get_children())

        # Configure the column widths based on the module
        for col in self.tree["columns"]:
            self.tree.column(col, width=100)  # Default width

        if selected_module == "Sales":
            self.load_sells_data(month_number)
        elif selected_module == "Raw Material":
            self.load_raw_material_data(month_number)
        elif selected_module == "Production":
            self.load_production_data(month_number)
        elif selected_module == "Stock Maintenance":
            self.load_stock_maintenance_data(month_number)

        self.status_var.set(f"Data loaded for {selected_month} - {selected_module}")

    def load_sells_data(self, month):
        """Load sells data for the selected month."""
        self.tree["columns"] = ("Date", "Client", "Item", "Quantity", "Rate", "Total", "Paid")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Client", width=150, anchor="w")
        self.tree.column("Item", width=150, anchor="w")
        self.tree.column("Quantity", width=100, anchor="e")
        self.tree.column("Rate", width=100, anchor="e")
        self.tree.column("Total", width=100, anchor="e")
        self.tree.column("Paid", width=100, anchor="center")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, client, item, quantity, rate, total, paid FROM sell WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", "", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increase row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Format numbers
                if row[3]:  # Quantity
                    formatted_row[3] = f"{float(row[3]):,.2f}"
                if row[4]:  # Rate
                    formatted_row[4] = f"₹{float(row[4]):,.2f}"
                if row[5]:  # Total
                    formatted_row[5] = f"₹{float(row[5]):,.2f}"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Add tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_raw_material_data(self, month):
        """Load raw material data for the selected month."""
        self.tree["columns"] = ("Date", "Raw Material", "Item Type", "Quantity")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Raw Material", width=150, anchor="w")
        self.tree.column("Item Type", width=150, anchor="w")
        self.tree.column("Quantity", width=100, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, raw, item_type, quantity FROM raw_material WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increase row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Format numbers
                if row[3]:  # Quantity
                    formatted_row[3] = f"{float(row[3]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Add tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_production_data(self, month):
        """Load production data for the selected month."""
        self.tree["columns"] = ("Date", "Item Type", "Grade A", "Grade B", "Grade C")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Item Type", width=150, anchor="w")
        self.tree.column("Grade A", width=100, anchor="e")
        self.tree.column("Grade B", width=100, anchor="e")
        self.tree.column("Grade C", width=100, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT adate, item_type, sa, sb, sc FROM production WHERE adate BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increase row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d")

                # Format numbers
                for j in range(2, 5):  # Columns 2, 3, 4 (Grade A, B, C)
                    if row[j] is not None:
                        formatted_row[j] = f"{float(row[j]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Add tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def load_stock_maintenance_data(self, month):
        """Load stock maintenance data for the selected month."""
        self.tree["columns"] = ("Date", "Region", "Cashew Type", "Change")

        # Configure columns with appropriate widths
        self.tree.column("Date", width=120, anchor="center")
        self.tree.column("Region", width=150, anchor="w")
        self.tree.column("Cashew Type", width=150, anchor="w")
        self.tree.column("Change", width=120, anchor="e")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Get first and last date of the selected month
        first_day = f"{datetime.now().year}-{month:02d}-01"
        last_day = f"{datetime.now().year}-{month:02d}-28"  # Assuming 28 days in the month for simplicity

        cur.execute(
            "SELECT timestamp, region, cashew_type, `change` FROM stock_changes WHERE timestamp BETWEEN %s AND %s",
            (first_day, last_day))
        rows = cur.fetchall()

        if not rows:
            self.tree.insert("", "end", values=("No data available", "", "", ""), tags=("nodata",))
            self.style.configure("Treeview", rowheight=50)  # Increase row height for empty state
        else:
            for i, row in enumerate(rows):
                # Format date if needed
                formatted_row = list(row)
                if isinstance(row[0], datetime):
                    formatted_row[0] = row[0].strftime("%Y-%m-%d %H:%M")

                # Format numbers
                if row[3]:  # Change
                    if float(row[3]) > 0:
                        formatted_row[3] = f"+{float(row[3]):,.2f} kg"
                    else:
                        formatted_row[3] = f"{float(row[3]):,.2f} kg"

                # Alternate row colors
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

            # Configure row color tags
            self.style.map("Treeview", background=[("selected", "#ffc13b")])
            self.style.configure("Treeview", rowheight=25)  # Reset row height

        # Add tag configurations for even/odd rows
        self.tree.tag_configure("even", background="#f5f5f5")
        self.tree.tag_configure("odd", background="white")
        self.tree.tag_configure("nodata", background="#f0f0f0")

    def upload_to_drive(self):
        """Save and upload data to Google Drive"""
        selected_module = self.selected_module.get()

        # File name
        file_name = f"{selected_module}_{datetime.now().strftime('%Y-%m')}.xlsx"

        # Prepare data for saving
        data = []
        columns = self.tree["columns"]
        for item in self.tree.get_children():
            row = self.tree.item(item)["values"]
            data.append(row)

        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Save the file temporarily
        temp_file_path = f"{file_name}"  # Store it in the working directory
        df.to_excel(temp_file_path, index=False)

        # Authenticate Google Drive API
        drive_service = build("drive", "v3", credentials=creds)

        # Upload file to Google Drive
        try:
            file_metadata = {
                "name": file_name,
                "parents": [DRIVE_FOLDER_ID],  # Upload to the specified folder
            }
            media = MediaFileUpload(temp_file_path,
                                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            messagebox.showinfo("Success", f"Data uploaded successfully to Google Drive: {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload data: {e}")

    def return_to_main_page(self):
        """Close current window and open index.py"""
        self.root.destroy()  # Close the current window


def main():
    root = tk.Tk()
    app = MonthlyLogsApp(root)
    app.run()


if __name__ == "__main__":
    main()






