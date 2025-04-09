# from tkinter import *
# import tkinter as tk
# from tkinter.ttk import *
# from tkinter import messagebox
# from sqlite3 import dbapi2 as sqlite
# from log_maker import *
# import time
# from tkinter.tix import *
# import mysql.connector
"""
c=mysql.connector.connect(host="localhost" , user="Admin" , password="newpassword123" , database="cfms")
cur=c.cursor()




def addBox():
    global entry_frame,name,address,m_no,p_no

    # I use len(all_entries) to get nuber of next free column
    next_row = len(name)


    # add entry in second row
    name.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    name[next_row].grid(row=next_row+1, column=1)
    address.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    address[next_row].grid(row=next_row+1, column=2)
    m_no.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    m_no[next_row].grid(row=next_row+1, column=3)
    p_no.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    p_no[next_row].grid(row=next_row+1, column=4)

def insert_client():
    global name,address,m_no,p_no
    success = True
    try:
        for i in range(len(name)):
            sql = "insert into clients(name,address,mobile,phone) values('%s','%s','%s','%s')"%(name[i].get(),address[i].get(),m_no[i].get(),p_no[i].get())
            cur.execute(sql)
    except Exception as exp:
        c.rollback()
        success = False
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Clients Successfully Inserted")
        messagebox.showinfo('Successfull', 'Clients Successfully Inserted')
        get_client()	
def delete_row(id):
    print(id)
    success = True
    try:
        sql="delete from clients where id=%s"%(id)
        sql="delete from clients where id=%s"%(id)
        cur.execute(sql)
        get_client()
    except Exception as exp:
        insert_error(exp)
    if success:
        c.commit()
        insert_info("Clients Successfully Deleted")
        messagebox.showinfo('Successfull', 'Clients Details Deleted')
	
def get_client():
    global client_view
	
    for widget in client_view.winfo_children():
        widget.destroy()
    Label(client_view,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1,columnspan=2)
    Label(client_view,text="name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=1)
    Label(client_view,text="Action",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=2)



    try:
        sql = "select id,name from clients"
        cur.execute(sql)
        i=3
        for result in cur:
            Label(client_view,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=1)
            tk.Button(client_view,width=15,text='Delete',font=("Belwe lt BT",15),command=lambda item=result[0]:delete_row(item)).grid(row=i, column=2)
            i+=1
    except Exception as exp:
        insert_error(exp)
	
def add_client():
    global flag,entry_frame,client_view,name,address,m_no,p_no
    flag='add_client'

    add_client=Tk()
    add_client.configure(background="black")
    add_client.state("zoomed")

    sw= ScrolledWindow(add_client)
    sw.pack(fill=BOTH,expand=1)
    add_client_main_frame = tk.Frame(sw.window,background="black")
    column_frame = tk.Frame(add_client_main_frame,background="black")
	
    add_client.title('Add Client Details')
    #add_client.wm_iconbitmap('favicon.ico')
    Label(column_frame,text='-'*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2, column=0,columnspan=3)

    column_frame.pack()
	
    entry_frame = tk.Frame(add_client_main_frame,background="black")
    Label(entry_frame,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=1)
    Label(entry_frame,text="Address",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=2)
    Label(entry_frame,text="Mobile Number",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=3)
    Label(entry_frame,text="Phone Number",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=4)

    name = []
    address = []
    m_no = []
    p_no = []
    i=0
    name.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    name[i].grid(row=i+1, column=1)
    address.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    address[i].grid(row=i+1, column=2)
    m_no.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    m_no[i].grid(row=i+1, column=3)
    p_no.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    p_no[i].grid(row=i+1, column=4)
    
    entry_frame.pack()
    
    button_frame = tk.Frame(add_client_main_frame,background="black")
    Label(button_frame,background="black",foreground="white").grid(row=0, column=0)
    tk.Button(button_frame,width=15,text='Add Box',font=("Belwe Bd BT",15),command=addBox).grid(row=1, column=0)
    tk.Button(button_frame,width=15,text='Insert Details',font=("Belwe Bd BT",15),command=lambda:insert_client()).grid(row=1, column=2)
    tk.Button(button_frame,width=20,text='Return to Main Menu',font=("Belwe Bd BT",15),command=add_client.destroy).grid(row=1, column=4)
    Label(button_frame,background="black",foreground="white").grid(row=2, column=0)
	
    button_frame.pack()
    

    client_view = tk.Frame(add_client_main_frame,background="black")
    
    get_client()
	
	
    client_view.pack()
    add_client_main_frame.pack(fill=BOTH,expand=1)
    add_client.mainloop()
def get_detail(c_name):
    top = Tk()
    sw= ScrolledWindow(top)
    sw.pack()
    top.configure(background="black")
	
    c_view = tk.Frame(sw.window	,background="black")
    sql = "select * from sell where client='%s'"%(c_name)
    print(sql)
    cur.execute(sql)
    i=0
    for result in cur:
        Label(c_view,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=0)
        Label(c_view,text=result[2],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=1)
        Label(c_view,text=result[3],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=2)
        Label(c_view,text=result[4],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=3)
        Label(c_view,text=result[5],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=4)
        Label(c_view,text=result[6],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=5)
        Label(c_view,text=result[7],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=6)
        i+=1   
    c_view.pack(fill=BOTH, expand=1)
	
	
def view_client():
    flag='view_client'

    view_client=Tk()
    view_client.configure(background="black")
    view_client.state("zoomed")

    sw= ScrolledWindow(view_client)
    sw.pack(fill=BOTH,expand=1)

    view_client_main_frame = tk.Frame(sw.window,background="black")
    column_frame = tk.Frame(view_client_main_frame,background="black")
	
    view_client.title('View Client Details')
    #view_client.wm_iconbitmap('favicon.ico')
    Label(column_frame,text="View Clients Details",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1, column=0,columnspan=3)
    Label(column_frame,text='-'*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2, column=0,columnspan=3)

    column_frame.pack()
    entry_frame = tk.Frame(view_client_main_frame,background="black")
    Label(entry_frame,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=1)
    Label(entry_frame,text="Address",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=2)
    Label(entry_frame,text="Mobile Number",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=3)
    Label(entry_frame,text="Phone Number",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=4)
    Label(entry_frame,text="View Transaction Deatils",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=5)

    i=0
    
    sql = "select * from clients"
    cur.execute(sql)	
	
    for result in cur:
        Label(entry_frame,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i+1, column=1)
        Label(entry_frame,text=result[2],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i+1, column=2)
        Label(entry_frame,text=result[3],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i+1, column=3)
        Label(entry_frame,text=result[4],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i+1, column=4)
        tk.Button(entry_frame,width=15,text='Payment Details',font=("Belwe lt BT",15),command=lambda c_name=result[1]: get_detail(c_name)).grid(row=i+1, column=5)
        i+=1
    
    entry_frame.pack()

    button_frame = tk.Frame(view_client,background="black",foreground="white")
    Label(button_frame,background="black",foreground="white").grid(row=0,column=0)
    tk.Button(button_frame,width=20,text='Return to Main Menu',font=("Belwe Bd BT",15),command=view_client.destroy).grid(row=1, column=4)
	
    button_frame.pack()

    
    view_client_main_frame.pack(fill=BOTH,expand=1)
    """
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Global variables
flag = None
name, address, m_no, p_no = [], [], [], []

# Color scheme - professional but maintain original layout
PRIMARY_BG = "#1e3d59"  # Dark blue background
HEADER_BG = "#4a536b"  # Subtle blue for headers
TEXT_COLOR = "#f5f5f5"  # White text
ACCENT_COLOR = "#ff6e40"  # Orange accent
SUCCESS_COLOR = "#52b788"  # Green for success actions
DELETE_COLOR = "#d90429"  # Red for delete buttons
ENTRY_BG = "#ffffff"  # White for input fields


def addBox():
    global entry_frame, name, address, m_no, p_no
    next_row = len(name)

    # Labels and Entry fields for each row - maintaining original layout
    Label(entry_frame, text="Name:", font=("Arial", 12), bg=PRIMARY_BG, fg=TEXT_COLOR).grid(row=next_row + 2, column=0,
                                                                                            padx=10, pady=5, sticky="e")
    name.append(Entry(entry_frame, font=("Arial", 12), bg=ENTRY_BG, fg="black"))
    name[next_row].grid(row=next_row + 2, column=1, padx=10, pady=5)

    Label(entry_frame, text="Address:", font=("Arial", 12), bg=PRIMARY_BG, fg=TEXT_COLOR).grid(row=next_row + 2,
                                                                                               column=2, padx=10,
                                                                                               pady=5, sticky="e")
    address.append(Entry(entry_frame, font=("Arial", 12), bg=ENTRY_BG, fg="black"))
    address[next_row].grid(row=next_row + 2, column=3, padx=10, pady=5)

    Label(entry_frame, text="Mobile Number:", font=("Arial", 12), bg=PRIMARY_BG, fg=TEXT_COLOR).grid(row=next_row + 2,
                                                                                                     column=4, padx=10,
                                                                                                     pady=5, sticky="e")
    m_no.append(Entry(entry_frame, font=("Arial", 12), bg=ENTRY_BG, fg="black"))
    m_no[next_row].grid(row=next_row + 2, column=5, padx=10, pady=5)

    Label(entry_frame, text="Phone Number:", font=("Arial", 12), bg=PRIMARY_BG, fg=TEXT_COLOR).grid(row=next_row + 2,
                                                                                                    column=6, padx=10,
                                                                                                    pady=5, sticky="e")
    p_no.append(Entry(entry_frame, font=("Arial", 12), bg=ENTRY_BG, fg="black"))
    p_no[next_row].grid(row=next_row + 2, column=7, padx=10, pady=5)


def insert_client():
    global name, address, m_no, p_no
    try:
        for i in range(len(name)):
            client_name = name[i].get().strip()
            client_address = address[i].get().strip()
            client_mobile = m_no[i].get().strip()
            client_phone = p_no[i].get().strip()

            # Check if both mobile and phone are empty
            if not client_mobile and not client_phone:
                messagebox.showerror("Error", "At least one contact number (Mobile or Phone) is required.")
                return  # Stop execution

            # Convert empty values to NULL before inserting
            client_mobile = client_mobile if client_mobile else None
            client_phone = client_phone if client_phone else None

            sql = "INSERT INTO clients (name, address, mobile, phone) VALUES (%s, %s, %s, %s)"
            values = (client_name, client_address, client_mobile, client_phone)
            cur.execute(sql, values)

        c.commit()
        messagebox.showinfo('Success', 'Clients Successfully Inserted')

    except Exception as exp:
        c.rollback()
        messagebox.showerror("Error", str(exp))


def delete_row(id):
    try:
        sql = "DELETE FROM clients WHERE id = %s"
        cur.execute(sql, (id,))
        c.commit()
        messagebox.showinfo('Success', 'Client Details Deleted')
        get_client()
    except Exception as exp:
        messagebox.showerror("Error", str(exp))


def get_client():
    global client_view
    for widget in client_view.winfo_children():
        widget.destroy()

    # Create a centering frame inside client_view - keeping original structure
    center_frame = Frame(client_view, bg=PRIMARY_BG)
    center_frame.pack(expand=True, anchor="center")  # Center the frame

    # Add heading title with improved styling
    title_frame = Frame(center_frame, bg=HEADER_BG, padx=15, pady=15)
    title_frame.grid(row=0, column=0, columnspan=8, pady=10, sticky="ew")

    Label(title_frame, text="CLIENT MANAGEMENT SYSTEM",
          font=("Arial", 16, "bold"), bg=HEADER_BG, fg=TEXT_COLOR).pack()
    Label(title_frame, text="View All Clients",
          font=("Arial", 12), bg=HEADER_BG, fg=TEXT_COLOR).pack(pady=5)

    # Column Headers - same position but improved styling
    Label(center_frame, text="Name", font=("Arial", 13, "bold"), bg=PRIMARY_BG, fg=ACCENT_COLOR).grid(row=1, column=0,
                                                                                                      padx=10, pady=5)
    Label(center_frame, text="Address", font=("Arial", 13, "bold"), bg=PRIMARY_BG, fg=ACCENT_COLOR).grid(row=1,
                                                                                                         column=1,
                                                                                                         padx=10,
                                                                                                         pady=5)
    Label(center_frame, text="Mobile Number", font=("Arial", 13, "bold"), bg=PRIMARY_BG, fg=ACCENT_COLOR).grid(row=1,
                                                                                                               column=2,
                                                                                                               padx=10,
                                                                                                               pady=5)
    Label(center_frame, text="Phone Number", font=("Arial", 13, "bold"), bg=PRIMARY_BG, fg=ACCENT_COLOR).grid(row=1,
                                                                                                              column=3,
                                                                                                              padx=10,
                                                                                                              pady=5)
    Label(center_frame, text="Action", font=("Arial", 13, "bold"), bg=PRIMARY_BG, fg=ACCENT_COLOR).grid(row=1, column=4,
                                                                                                        padx=10, pady=5)

    # Create a separator line
    frame_separator = Frame(center_frame, height=2, bg=ACCENT_COLOR)
    frame_separator.grid(row=1, column=0, columnspan=5, pady=(25, 0), sticky="ew")

    try:
        cur.execute(
            "SELECT id, name, address, COALESCE(mobile, 'Not Applicable'), COALESCE(phone, 'Not Applicable') FROM clients")
        for i, (cid, cname, caddress, cmobile, cphone) in enumerate(cur, start=2):
            # Creating frames for each entry to add subtle styling
            name_frame = Frame(center_frame, bg=PRIMARY_BG, padx=5, pady=5)
            name_frame.grid(row=i, column=0, padx=10, pady=5, sticky="nsew")
            Label(name_frame, text=cname, font=("Arial", 11), bg=PRIMARY_BG, fg=TEXT_COLOR).pack(fill="both")

            addr_frame = Frame(center_frame, bg=PRIMARY_BG, padx=5, pady=5)
            addr_frame.grid(row=i, column=1, padx=10, pady=5, sticky="nsew")
            Label(addr_frame, text=caddress, font=("Arial", 11), bg=PRIMARY_BG, fg=TEXT_COLOR).pack(fill="both")

            mobile_frame = Frame(center_frame, bg=PRIMARY_BG, padx=5, pady=5)
            mobile_frame.grid(row=i, column=2, padx=10, pady=5, sticky="nsew")
            Label(mobile_frame, text=cmobile, font=("Arial", 11), bg=PRIMARY_BG, fg=TEXT_COLOR).pack(fill="both")

            phone_frame = Frame(center_frame, bg=PRIMARY_BG, padx=5, pady=5)
            phone_frame.grid(row=i, column=3, padx=10, pady=5, sticky="nsew")
            Label(phone_frame, text=cphone, font=("Arial", 11), bg=PRIMARY_BG, fg=TEXT_COLOR).pack(fill="both")

            # Delete button - same position but better styling
            tk.Button(center_frame, text='Delete', command=lambda id=cid: delete_row(id),
                      bg=DELETE_COLOR, fg=TEXT_COLOR, font=("Arial", 11, "bold"),
                      relief=RAISED, borderwidth=0, padx=10, pady=3).grid(row=i, column=4, padx=10, pady=5)

            # Add alternating row colors for better readability
            row_color = "#2c4c6b" if i % 2 == 0 else PRIMARY_BG
            name_frame.configure(bg=row_color)
            addr_frame.configure(bg=row_color)
            mobile_frame.configure(bg=row_color)
            phone_frame.configure(bg=row_color)

            # Update label backgrounds
            for widget in name_frame.winfo_children() + addr_frame.winfo_children() + \
                          mobile_frame.winfo_children() + phone_frame.winfo_children():
                widget.configure(bg=row_color)

    except Exception as exp:
        messagebox.showerror("Error", str(exp))


def add_client():
    global entry_frame, client_view, name, address, m_no, p_no
    add_client_win = Tk()
    add_client_win.title('Client Management')
    add_client_win.state("zoomed")
    add_client_win.configure(bg=PRIMARY_BG)  # Set professional background color

    # Reset lists
    name, address, m_no, p_no = [], [], [], []

    # Main container
    main_frame = Frame(add_client_win, bg=PRIMARY_BG)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Header section
    header_frame = Frame(main_frame, bg=HEADER_BG, padx=15, pady=15)
    header_frame.pack(fill="x", pady=(0, 20))

    Label(header_frame, text="CLIENT SYSTEM",
          font=("Arial", 16, "bold"), bg=HEADER_BG, fg=TEXT_COLOR).pack()
    Label(header_frame, text="Add New Client Records",
          font=("Arial", 12), bg=HEADER_BG, fg=TEXT_COLOR).pack(pady=5)

    # Entry frame - keeping exact same structure
    entry_frame = Frame(main_frame, bg=PRIMARY_BG)
    entry_frame.pack(pady=20)

    # Add initial entry box
    addBox()

    # Buttons with same vertical stacking but improved styling
    button_frame = Frame(main_frame, bg=PRIMARY_BG)
    button_frame.pack(pady=20)

    # Button styling while keeping original layout
    add_btn = tk.Button(button_frame, text='ADD BOX', command=addBox,
                        bg=ACCENT_COLOR, fg=TEXT_COLOR, font=("Arial", 13, "bold"),
                        width=20, relief=RAISED, borderwidth=0, pady=8)
    add_btn.pack(pady=8)

    insert_btn = tk.Button(button_frame, text='INSERT DETAILS', command=insert_client,
                           bg=SUCCESS_COLOR, fg=TEXT_COLOR, font=("Arial", 13, "bold"),
                           width=20, relief=RAISED, borderwidth=0, pady=8)
    insert_btn.pack(pady=8)

    return_btn = tk.Button(button_frame, text='RETURN TO MAIN MENU', command=add_client_win.destroy,
                           bg=DELETE_COLOR, fg=TEXT_COLOR, font=("Arial", 13, "bold"),
                           width=20, relief=RAISED, borderwidth=0, pady=8)
    return_btn.pack(pady=8)

    # Footer for professional look
    footer_frame = Frame(main_frame, bg=HEADER_BG, padx=15, pady=10)
    footer_frame.pack(fill="x", side=BOTTOM)

    Label(footer_frame, text="© 2025 | Sawant Cashew Industries",
          font=("Arial", 10), bg=HEADER_BG, fg=TEXT_COLOR).pack()

    add_client_win.mainloop()


def view_clients():
    view_win = Tk()
    view_win.title("Client Management")
    view_win.state("zoomed")
    view_win.configure(bg=PRIMARY_BG)

    # Main container
    main_container = Frame(view_win, bg=PRIMARY_BG)
    main_container.pack(expand=True, fill="both", padx=20, pady=20)

    global client_view
    client_view = Frame(main_container, bg=PRIMARY_BG)
    client_view.pack(expand=True, fill="both", padx=20, pady=20)

    # Get client data - keeping original function
    get_client()

    # Button frame
    button_frame = Frame(main_container, bg=PRIMARY_BG)
    button_frame.pack(side=BOTTOM, pady=15)

    # Return button - same position
    tk.Button(button_frame, text='RETURN TO MAIN MENU', command=view_win.destroy,
              bg=DELETE_COLOR, fg=TEXT_COLOR, font=("Arial", 14, "bold"),
              width=20, relief=RAISED, borderwidth=0, pady=8).pack()

    # Footer for professional look
    footer_frame = Frame(main_container, bg=HEADER_BG, padx=15, pady=10)
    footer_frame.pack(fill="x", side=BOTTOM)

    Label(footer_frame, text="© 2025 | Sawant Cashew Industries",
          font=("Arial", 10), bg=HEADER_BG, fg=TEXT_COLOR).pack()

    view_win.mainloop()



# Uncomment these to run directly
# add_client()
# view_clients()



# expiry()
#view_client()