'''
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox, ttk
from sqlite3 import dbapi2 as sqlite
from log_maker import *
import time
from tkinter.tix import *
from datetime import date as dat
import mysql.connector

now = dat.today()

c=mysql.connector.connect(host="localhost" , user="root" , password="mysql2025" , database="cfms")
cur=c.cursor()




def insert_labour():
    global date,name,hour
    success = True
    try:
        sql = "insert into ot(adate,name,hour) values(date('%s'),'%s',%i)"%(date.get(),name.get(),hour.get())
        print(sql)
        cur.execute(sql)
    except Exception as exp:
        c.rollback()
        success = False
        print(exp)
        insert_error(exp)
    if success:
        c.commit()
        insert_info("ot Successfully Inserted")
        messagebox.showinfo('Successfull', 'OT Successfully Inserted')
        get_ot()	
	
def get_ot():
    global ot_view
	
    for widget in ot_view.winfo_children():
        widget.destroy()
    Label(ot_view,text="-"*80,font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=1,column=1,columnspan=3)
    Label(ot_view,text="Date",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=2,column=1)
    Label(ot_view,text="Name",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=2,column=2)
    Label(ot_view,text="Hour",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=2,column=3)



    try:
        sql = "select adate,name,hour from ot"
        cur.execute(sql)
        i=3
        for result in cur:
            Label(ot_view,text=result[0],font=("Belwe lt BT",10),background="black",foreground="white").grid(row=i,column=1)
            Label(ot_view,text=result[1],font=("Belwe lt BT",10),background="black",foreground="white").grid(row=i,column=2)
            Label(ot_view,text=result[2],font=("Belwe lt BT",10),background="black",foreground="white").grid(row=i,column=3)
            i+=1
    except Exception as exp:
        insert_error(exp)
	
def main():
    global flag,entry_frame,ot_view,date,name,hour
    flag='overtime'

    overtime=Tk()
    overtime.configure(background="black")
    overtime.state("zoomed")
    column_frame = tk.Frame(overtime,background="black")
	
    overtime.title('Over time')
    #overtime.wm_iconbitmap('favicon.ico')
    Label(column_frame,text='-'*80,font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=2, column=0,columnspan=3)



    column_frame.pack()
	
    entry_frame = tk.Frame(overtime,background="black")
    Label(entry_frame,text="Date",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=0, column=1)
    Label(entry_frame,text="Name",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=0, column=2)
    Label(entry_frame,text="Hour",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=0, column=3)

    date = StringVar(entry_frame,value=now)
    name = StringVar(entry_frame)
    hour = IntVar(entry_frame)
    i=0

    date_entry = Entry(entry_frame,font=("Belwe lt BT",10),textvariable=date)
    date_entry.grid(row=1,column=1)

    sql  = "select name from labour_details"
    cur.execute(sql)

    name_choices = [result[0] for result in cur]
    name_option = ttk.OptionMenu(entry_frame, name, *name_choices)
    name_option.grid(row=1,column=2)

    hour_entry = Entry(entry_frame,font=("Belwe lt BT",10),textvariable=hour)
    hour_entry.grid(row=1,column=3)
   
    entry_frame.pack()




   
    button_frame = tk.Frame(overtime,background="black")
    Label(button_frame,text="",font=("Belwe Bd BT",10),background="black",foreground="white").grid(row=0,column=0)
    tk.Button(button_frame,width=10,text='Insert Details',font=("Belwe Bd BT",10),background="green",foreground="white",command=lambda:insert_labour()).grid(row=1, column=2)
    tk.Button(button_frame,width=20,text='Return to Main Menu',font=("Belwe Bd BT",10),background="green",foreground="white",command=overtime.destroy).grid(row=1, column=4)
    Label(button_frame,background="black",foreground="white").grid(row=2, column=0)
	
    button_frame.pack()
    
    sw= ScrolledWindow(overtime)
    sw.pack()

    ot_view = tk.Frame(sw.window,background="black")
    
    get_ot()


    ot_view.pack(fill=BOTH, expand=1)

    overtime.mainloop()


def mainmenu():
    if flag=='expirychk':
        expirychk.destroy()



# expiry()
#view_client()
'''
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox, ttk
from datetime import date as dat
import mysql.connector

# Custom color scheme
BG_COLOR = "#2c3e50"  # Dark blue-gray background
FG_COLOR = "#ecf0f1"  # Light gray text
ACCENT_COLOR = "#3498db"  # Blue accent
DANGER_COLOR = "#e74c3c"  # Red for delete buttons
SUCCESS_COLOR = "#2ecc71"  # Green for success actions
HEADER_COLOR = "#34495e"  # Darker blue-gray for headers
ENTRY_BG = "#bdc3c7"  # Light gray for entry fields
FONT_MAIN = ("Segoe UI", 12)
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_TITLE = ("Segoe UI", 18, "bold")

now = dat.today()

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()


def insert_labour():
    global date, name, hour
    if not all([date.get(), name.get(), hour.get()]):
        messagebox.showerror('Error', 'All fields are required!')
        return

    try:
        sql = "INSERT INTO ot(adate,name,hour) VALUES(date(%s),%s,%s)"
        cur.execute(sql, (date.get(), name.get(), hour.get()))
        c.commit()
        messagebox.showinfo('Success', 'OT Record Added Successfully')
        get_ot()
        hour.set(0)
    except Exception as exp:
        c.rollback()
        messagebox.showerror('Database Error', str(exp))


def update_name_dropdown():
    global name_combobox
    try:
        cur.execute("SELECT name FROM labour_details ORDER BY name")
        names = [result[0] for result in cur]
        name_combobox['values'] = names
        if names:
            name_combobox.current(0)
    except Exception as e:
        messagebox.showerror('Error', f'Failed to load names: {str(e)}')


def delete_ot_record(record):
    try:
        confirm = messagebox.askyesno('Confirm Delete', f'Delete record for {record[1]} on {record[0]}?')
        if confirm:
            sql = "DELETE FROM ot WHERE adate=%s AND name=%s AND hour=%s"
            cur.execute(sql, record)
            c.commit()
            get_ot()
    except Exception as exp:
        c.rollback()
        messagebox.showerror('Error', 'Failed to delete record')


def get_ot():
    global ot_view

    # Clear existing widgets
    for widget in ot_view.winfo_children():
        widget.destroy()

    # Create headers
    headers = ["Date", "Name", "Hours", "Action"]
    for col, header in enumerate(headers):
        tk.Label(ot_view, text=header,
                 bg=HEADER_COLOR, fg=FG_COLOR, font=FONT_HEADER,
                 padx=10, pady=5, width=15).grid(row=0, column=col, sticky="nsew")

    try:
        cur.execute("SELECT adate, name, hour FROM ot ORDER BY adate DESC")
        for row, record in enumerate(cur, start=1):
            # Alternate row colors
            row_bg = "#3d566e" if row % 2 == 0 else "#2c3e50"

            # Date column
            tk.Label(ot_view, text=record[0],
                     bg=row_bg, fg=FG_COLOR, font=FONT_MAIN,
                     padx=10, pady=5, width=15).grid(row=row, column=0, sticky="nsew")

            # Name column
            tk.Label(ot_view, text=record[1],
                     bg=row_bg, fg=FG_COLOR, font=FONT_MAIN,
                     padx=10, pady=5, width=15).grid(row=row, column=1, sticky="nsew")

            # Hours column
            tk.Label(ot_view, text=record[2],
                     bg=row_bg, fg=FG_COLOR, font=FONT_MAIN,
                     padx=10, pady=5, width=15).grid(row=row, column=2, sticky="nsew")

            # Delete button
            tk.Button(ot_view, text="Delete",
                      bg=DANGER_COLOR, fg=FG_COLOR, font=FONT_MAIN,
                      command=lambda r=record: delete_ot_record(r)).grid(
                row=row, column=3, sticky="nsew", padx=5, pady=2)

        # Configure column weights to make the content centered
        for i in range(4):
            ot_view.columnconfigure(i, weight=1)

    except Exception as exp:
        tk.Label(ot_view, text=f"Error loading records: {str(exp)}",
                 bg=BG_COLOR, fg=DANGER_COLOR, font=FONT_MAIN).grid(
            row=1, column=0, columnspan=4, sticky="nsew")


def main():
    global date, name, hour, name_combobox, ot_view

    overtime = tk.Tk()
    overtime.title('Overtime Management System')
    overtime.state("zoomed")
    overtime.configure(bg=BG_COLOR)

    # Main container
    main_frame = tk.Frame(overtime, bg=BG_COLOR)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)

    # Title
    tk.Label(main_frame, text="OVERTIME MANAGEMENT SYSTEM",
             bg=BG_COLOR, fg=FG_COLOR, font=FONT_TITLE).pack(pady=(0, 30))

    # Input section - centered
    input_frame = tk.Frame(main_frame, bg=BG_COLOR)
    input_frame.pack(pady=20)

    # Date
    tk.Label(input_frame, text="Date:", bg=BG_COLOR, fg=FG_COLOR,
             font=FONT_HEADER).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    date = tk.StringVar(value=now.strftime('%Y-%m-%d'))
    tk.Entry(input_frame, textvariable=date, font=FONT_MAIN,
             bg=ENTRY_BG, width=20).grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Name dropdown
    tk.Label(input_frame, text="Labour Name:", bg=BG_COLOR, fg=FG_COLOR,
             font=FONT_HEADER).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    name = tk.StringVar()
    name_combobox = ttk.Combobox(input_frame, textvariable=name,
                                 font=FONT_MAIN, width=20)
    name_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Hours
    tk.Label(input_frame, text="Hours Worked:", bg=BG_COLOR, fg=FG_COLOR,
             font=FONT_HEADER).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    hour = tk.IntVar()
    tk.Entry(input_frame, textvariable=hour, font=FONT_MAIN,
             bg=ENTRY_BG, width=20).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Buttons - centered
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="ADD RECORD",
              bg=SUCCESS_COLOR, fg=FG_COLOR, font=FONT_HEADER,
              command=insert_labour, padx=15, pady=5).grid(row=0, column=0, padx=15)

    tk.Button(button_frame, text="REFRESH",
              bg=ACCENT_COLOR, fg=FG_COLOR, font=FONT_HEADER,
              command=get_ot, padx=15, pady=5).grid(row=0, column=1, padx=15)

    tk.Button(button_frame, text="EXIT",
              bg=DANGER_COLOR, fg=FG_COLOR, font=FONT_HEADER,
              command=overtime.destroy, padx=15, pady=5).grid(row=0, column=2, padx=15)

    # Table section header
    tk.Label(main_frame, text="OVERTIME RECORDS",
             bg=BG_COLOR, fg=FG_COLOR, font=FONT_HEADER).pack(pady=(20, 10))

    # Create a frame to hold the table and center it
    table_container = tk.Frame(main_frame, bg=BG_COLOR)
    table_container.pack(fill=tk.BOTH, expand=True)

    # Create a frame inside the container for the table content
    table_scroll_frame = tk.Frame(table_container, bg=BG_COLOR)
    table_scroll_frame.pack(expand=True, fill=tk.BOTH)

    # Add scrollbar
    scrollbar = tk.Scrollbar(table_scroll_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas to allow scrolling
    canvas = tk.Canvas(table_scroll_frame, bg=BG_COLOR, highlightthickness=0,
                       yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    scrollbar.config(command=canvas.yview)

    # Create a frame for the actual table content
    ot_view = tk.Frame(canvas, bg=BG_COLOR)

    # Add the frame to the canvas
    canvas_window = canvas.create_window((0, 0), window=ot_view, anchor='nw')

    # Make sure the frame expands to fill canvas width
    def configure_canvas(event):
        # Update the scrollregion to include all the canvas contents
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Update the size of the window to match canvas width
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    # Bind the configure event
    ot_view.bind("<Configure>", configure_canvas)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))

    # Initialize data
    update_name_dropdown()
    get_ot()

    overtime.mainloop()


#def mainmenu():
 #   if flag == 'expirychk':
  #      expirychk.destroy()

# Call main() if you want to run the overtime view
# main()
