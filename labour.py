'''from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
#from tkinter.tix import *
from PIL import ImageTk, Image
import mysql.connector

from sqlite3 import dbapi2 as sqlite
from log_maker import *
import time


c=mysql.connector.connect(host="localhost" , user="Admin" , password="newpassword123" , database="cfms")
cur=c.cursor()




def addBox():
    global entry_frame,name,other

    # I use len(all_entries) to get nuber of next free column
    next_row = len(name)


    # add entry in second row
    name.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    name[next_row].grid(row=next_row+1, column=1)
    other.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    other[next_row].grid(row=next_row+1, column=2)

def insert_labour():
    global name,other
    success = True
    try:
        for i in range(len(name)):
            sql = "insert into labour_details(name,other) values('%s','%s')"%(name[i].get(),other[i].get())
            cur.execute(sql)
    except Exception as exp:
        c.rollback()
        success = False




        insert_error(exp)
    if success:
        c.commit()
        insert_info("Labours Successfully Inserted")
        messagebox.showinfo('Successfull', 'Labours Successfully Inserted')
        get_labour()

def delete_row(name):
    print(name)
    success = True
    try:
        sql="delete from labour_details where id=%s"%(name)
        cur.execute(sql)
        get_labour()
    except Exception as exp:
        insert_error(exp)
    if success:
        c.commit()
        insert_info("labour Successfully Deleted")
        messagebox.showinfo('Successfull', 'labor Details Deleted')

def get_labour():
    global labour_view

    for widget in labour_view.winfo_children():
        widget.destroy()
    Label(labour_view,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=1,column=1,columnspan=2)
    Label(labour_view,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=1)
    Label(labour_view,text="Other Information",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2,column=2)

    try:
        sql = "select name,other from labour_details"
        cur.execute(sql)
        i=4
        for result in cur:
            Label(labour_view,text=result[0],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=1)
            Label(labour_view,text=result[1],font=("Belwe lt BT",15),background="black",foreground="white").grid(row=i,column=2)
            #tk.Button(labour_view, width=15, text='Delete', font=("Belwe lt BT", 15),command=lambda item=result[0]: delete_row(item)).grid(row=i, column=3)
            i+=1
    except Exception as exp:
        insert_error(exp)
    Label(labour_view,text="-"*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=14,column=1,columnspan=2)

def add_labour():
    global flag,entry_frame,labour_view,name,other
    flag='add_labour'

    add_labour=Tk()
    add_labour.configure(background="black")
    add_labour.state("zoomed")
    add_labour.title('Add labour Details')
    add_labour.bg = ImageTk.PhotoImage(file="background.png")
    add_labour.bg_image = Label(add_labour, image=add_labour.bg).place(x=0, y=0, relwidth=1, relheight=1)

    sw= ScrolledWindow(add_labour)
    sw.pack()


    full_labour_frame = tk.Frame(sw.window,background="black")
    column_frame = tk.Frame(full_labour_frame,background="black")

    #full_labour_frame.wm_iconbitmap('favicon.ico')
    Label(column_frame,text='-'*80,font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=2, column=0,columnspan=3)

    column_frame.pack(anchor=CENTER)

    entry_frame = tk.Frame(full_labour_frame,background="black")
    Label(entry_frame,text="Name",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=1)
    Label(entry_frame,text="Other Information",font=("Belwe Bd BT",15),background="black",foreground="white").grid(row=0, column=2)

    name = []
    other = []
    i=0
    name.append(Entry(entry_frame,font=("Belwe lt BT",15), relief=GROOVE))
    name[i].grid(row=i+1, column=1)
    other.append(Entry(entry_frame,font=("Belwe lt BT",15)))
    other[i].grid(row=i+1, column=2)

    entry_frame.pack(anchor=CENTER)

    button_frame = tk.Frame(full_labour_frame,background="black")
    Label(button_frame,text="",background="black",foreground="white").grid(row=0, column=0)
    tk.Button(button_frame,width=10,font=("Belwe Bd BT",15),background="green",foreground="white",text='Add Box',command=addBox).grid(row=1, column=0)
    tk.Button(button_frame,width=15,font=("Belwe Bd BT",15),background="green",foreground="white",text='Insert Details',command=lambda:insert_labour()).grid(row=1, column=2)
    tk.Button(button_frame,width=20,font=("Belwe Bd BT",15),background="green",foreground="white",text='Return to Main Menu',command=add_labour.destroy).grid(row=1, column=4)

    button_frame.pack(anchor=CENTER)

    labour_view = tk.Frame(full_labour_frame,background="black")

    get_labour()


    labour_view.pack(anchor=CENTER)
    full_labour_frame.pack(fill=BOTH,expand=1)
    add_labour.mainloop()




def mainmenu():
    if flag=='expirychk':
        expirychk.destroy()



# expiry()
#view_labour()
'''

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector
from tkinter.font import Font

# Database connection
c = mysql.connector.connect(host="localhost", user="Admin", password="newpassword123", database="cfms")
cur = c.cursor()

# Global variables
name = []
other = []
flag = None

# Color scheme for professional UI
COLORS = {
    "primary": "#2c3e50",  # Dark blue-gray
    "secondary": "#34495e",  # Slightly lighter blue-gray
    "accent": "#3498db",  # Bright blue
    "success": "#2ecc71",  # Green
    "danger": "#e74c3c",  # Red
    "warning": "#f39c12",  # Amber
    "text_light": "#ecf0f1",  # Off-white
    "text_dark": "#2c3e50"  # Dark blue-gray
}


def create_custom_button(parent, text, command, bg_color, fg_color="#ffffff", width=15, height=2):
    """Create a stylized button with hover effect"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        font=("Helvetica", 12, "bold"),
        width=width,
        height=height,
        relief=tk.FLAT,
        borderwidth=0,
        activebackground=bg_color,
        activeforeground=fg_color
    )

    # Hover effects
    def on_enter(e):
        button['background'] = adjust_color(bg_color, -20)

    def on_leave(e):
        button['background'] = bg_color

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button


def adjust_color(hex_color, amount):
    """Adjust a hex color by the given amount (+/-255)"""
    r = max(0, min(255, int(hex_color[1:3], 16) + amount))
    g = max(0, min(255, int(hex_color[3:5], 16) + amount))
    b = max(0, min(255, int(hex_color[5:7], 16) + amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def create_heading(parent, text, font_size=16, padx=10, pady=10):
    """Create a standardized heading"""
    heading = Label(
        parent,
        text=text,
        font=("Helvetica", font_size, "bold"),
        bg=COLORS["primary"],
        fg=COLORS["text_light"],
        padx=padx,
        pady=pady
    )
    return heading


def create_styled_entry(parent, width=20):
    """Create a styled entry widget"""
    entry = Entry(
        parent,
        font=("Helvetica", 12),
        relief=GROOVE,
        bg=COLORS["text_light"],
        fg=COLORS["text_dark"],
        insertbackground=COLORS["text_dark"],
        width=width,
        highlightthickness=1,
        highlightbackground=COLORS["accent"],
        highlightcolor=COLORS["accent"],
        justify=CENTER  # Center text in entries
    )
    return entry


def addBox():
    global entry_frame, name, other

    # Add entry in the next row
    next_row = len(name)
    name.append(create_styled_entry(entry_frame))
    name[next_row].grid(row=next_row + 1, column=1, padx=15, pady=10, sticky=EW)

    other.append(create_styled_entry(entry_frame, width=30))
    other[next_row].grid(row=next_row + 1, column=2, padx=15, pady=10, sticky=EW)


def insert_labour():
    global name, other
    success = True

    # Validate entries
    for i in range(len(name)):
        if not name[i].get().strip():
            messagebox.showwarning('Validation Error', 'Name field cannot be empty')
            return

    try:
        for i in range(len(name)):
            sql = "INSERT INTO labour_details(name, other) VALUES (%s, %s)"
            values = (name[i].get().strip(), other[i].get().strip())
            cur.execute(sql, values)
    except Exception as exp:
        c.rollback()
        success = False
        messagebox.showerror('Database Error', f"Error: {exp}")

    if success:
        c.commit()
        messagebox.showinfo('Success', 'Labour records successfully added')
        get_labour()


def delete_labour(name_value):
    """Function to delete a labour record by name"""
    global cur, c

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{name_value}'?",
        icon='warning'
    )

    if confirm:
        try:
            sql = "DELETE FROM labour_details WHERE name = %s"
            cur.execute(sql, (name_value,))
            c.commit()
            messagebox.showinfo("Success", f"Labour '{name_value}' deleted successfully.")
            get_labour()  # Refresh table after deletion
        except Exception as exp:
            c.rollback()
            messagebox.showerror("Error", f"Failed to delete {name_value}.\n{exp}")


def get_labour():
    """Function to display labour details along with Delete buttons"""
    global labour_view

    for widget in labour_view.winfo_children():
        widget.destroy()

    # Create a frame for the table with a white background
    table_frame = Frame(labour_view, bg=COLORS["text_light"], padx=10, pady=10, relief=RIDGE, borderwidth=1)
    table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Calculate column widths and ensure they're consistent
    name_width = 20
    other_width = 30
    action_width = 10

    # Create a header with column names
    header_frame = Frame(table_frame, bg=COLORS["secondary"])
    header_frame.pack(fill=X, padx=2, pady=2)

    # Configure grid columns to maintain alignment
    header_frame.columnconfigure(0, weight=1, minsize=name_width)
    header_frame.columnconfigure(1, weight=1, minsize=other_width)
    header_frame.columnconfigure(2, weight=1, minsize=action_width)

    # Header labels - centered
    Label(header_frame, text="Name", font=("Helvetica", 12, "bold"), bg=COLORS["secondary"],
          fg=COLORS["text_light"], width=name_width, padx=10, pady=8, anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
    Label(header_frame, text="Other Information", font=("Helvetica", 12, "bold"), bg=COLORS["secondary"],
          fg=COLORS["text_light"], width=other_width, padx=10, pady=8, anchor=CENTER).grid(row=0, column=1, sticky=NSEW)
    Label(header_frame, text="Action", font=("Helvetica", 12, "bold"), bg=COLORS["secondary"],
          fg=COLORS["text_light"], width=action_width, padx=10, pady=8, anchor=CENTER).grid(row=0, column=2,
                                                                                            sticky=NSEW)

    # Container for data rows
    data_frame = Frame(table_frame, bg=COLORS["text_light"])
    data_frame.pack(fill=BOTH, expand=True)

    # Configure grid columns to match header columns
    data_frame.columnconfigure(0, weight=1, minsize=name_width)
    data_frame.columnconfigure(1, weight=1, minsize=other_width)
    data_frame.columnconfigure(2, weight=1, minsize=action_width)

    try:
        sql = "SELECT name, other FROM labour_details"
        cur.execute(sql)
        results = cur.fetchall()

        if not results:
            # Show empty state message - centered
            empty_label = Label(data_frame, text="No labour records found", font=("Helvetica", 12, "italic"),
                                bg=COLORS["text_light"], fg=COLORS["text_dark"], pady=20)
            empty_label.grid(row=0, column=0, columnspan=3, sticky=NSEW)
        else:
            # Create rows for each result with alternating colors
            for i, result in enumerate(results):
                # Alternate row colors for better readability
                row_bg = "#f9f9f9" if i % 2 == 0 else COLORS["text_light"]

                # Create cells with exact alignment to headers
                Label(data_frame, text=result[0], font=("Helvetica", 11), bg=row_bg,
                      fg=COLORS["text_dark"], width=name_width, padx=10, pady=8, anchor=CENTER).grid(
                    row=i, column=0, sticky=NSEW)

                Label(data_frame, text=result[1], font=("Helvetica", 11), bg=row_bg,
                      fg=COLORS["text_dark"], width=other_width, padx=10, pady=8, anchor=CENTER).grid(
                    row=i, column=1, sticky=NSEW)

                # Center the delete button in its cell
                btn_frame = Frame(data_frame, bg=row_bg)
                btn_frame.grid(row=i, column=2, sticky=NSEW)

                # Delete button - centered in its container
                delete_btn = Button(btn_frame, text="Delete", font=("Helvetica", 10, "bold"),
                                    bg=COLORS["danger"], fg=COLORS["text_light"],
                                    relief=FLAT, command=lambda name=result[0]: delete_labour(name))
                delete_btn.pack(padx=10, pady=3, anchor=CENTER, expand=True)

    except Exception as exp:
        error_label = Label(data_frame, text=f"Error loading data: {exp}",
                            font=("Helvetica", 11, "italic"), bg=COLORS["text_light"],
                            fg=COLORS["danger"], pady=20)
        error_label.grid(row=0, column=0, columnspan=3, sticky=NSEW)


def add_labour():
    global flag, entry_frame, labour_view, name, other
    flag = 'add_labour'

    add_labour_window = Tk()
    add_labour_window.configure(background=COLORS["primary"])
    add_labour_window.state("zoomed")  # Maximize the window
    add_labour_window.title('Labour Management System')

    # Add app icon if available
    try:
        add_labour_window.iconbitmap('icon.ico')  # Replace with your icon path
    except:
        pass

    # Add a title bar at the top
    title_bar = Frame(add_labour_window, bg=COLORS["secondary"], height=60)
    title_bar.pack(fill=X)

    title_label = Label(title_bar, text="LABOUR MANAGEMENT SYSTEM", font=("Helvetica", 18, "bold"),
                        bg=COLORS["secondary"], fg=COLORS["text_light"], pady=10)
    title_label.pack()

    # Create a main container frame with center alignment
    main_frame = Frame(add_labour_window, background=COLORS["primary"])
    main_frame.pack(fill=BOTH, expand=True)

    # Create a centered container for all content
    main_container = Frame(main_frame, background=COLORS["primary"], padx=30, pady=20)
    main_container.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Top section with heading - centered
    top_section = Frame(main_container, bg=COLORS["primary"])
    top_section.pack(fill=X, pady=(0, 20))

    heading = create_heading(top_section, "MANAGE LABOUR DETAILS", font_size=16, pady=10)
    heading.pack(fill=X)

    # Create a card-like container for entry fields
    entry_card = Frame(main_container, bg=COLORS["text_light"], relief=RIDGE, borderwidth=1)
    entry_card.pack(fill=X, pady=10)

    entry_card_header = Frame(entry_card, bg=COLORS["accent"], pady=10)
    entry_card_header.pack(fill=X)

    # Centered header text
    Label(entry_card_header, text="Add New Labour", font=("Helvetica", 14, "bold"),
          bg=COLORS["accent"], fg=COLORS["text_light"]).pack(anchor=CENTER)

    # Entry frame for input fields with white background
    entry_frame = Frame(entry_card, background=COLORS["text_light"], padx=20, pady=20)

    # Configure columns for alignment
    entry_frame.columnconfigure(1, weight=1, minsize=200)
    entry_frame.columnconfigure(2, weight=1, minsize=300)

    # Column headers - centered
    Label(entry_frame, text="Name", font=("Helvetica", 12, "bold"),
          bg=COLORS["text_light"], fg=COLORS["text_dark"], anchor=CENTER).grid(
        row=0, column=1, padx=15, pady=5, sticky=NSEW)
    Label(entry_frame, text="Other Information", font=("Helvetica", 12, "bold"),
          bg=COLORS["text_light"], fg=COLORS["text_dark"], anchor=CENTER).grid(
        row=0, column=2, padx=15, pady=5, sticky=NSEW)

    # Initialize entry widgets
    name = []
    other = []
    name.append(create_styled_entry(entry_frame))
    name[0].grid(row=1, column=1, padx=15, pady=10, sticky=EW)
    other.append(create_styled_entry(entry_frame, width=30))
    other[0].grid(row=1, column=2, padx=15, pady=10, sticky=EW)

    entry_frame.pack(fill=X)

    # Button frame for actions - centered buttons
    button_frame = Frame(entry_card, background=COLORS["text_light"], padx=20, pady=15)

    # Center the buttons in the frame
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    # Add modern-looking buttons
    add_box_btn = create_custom_button(
        button_frame,
        text='Add More',
        command=addBox,
        bg_color=COLORS["accent"],
        width=12,
        height=1
    )
    add_box_btn.grid(row=0, column=0, padx=10, pady=5)

    insert_btn = create_custom_button(
        button_frame,
        text='Save Records',
        command=insert_labour,
        bg_color=COLORS["success"],
        width=15,
        height=1
    )
    insert_btn.grid(row=0, column=1, padx=10, pady=5)

    exit_btn = create_custom_button(
        button_frame,
        text='Return to Main Menu',
        command=add_labour_window.destroy,
        bg_color=COLORS["danger"],
        width=18,
        height=1
    )
    exit_btn.grid(row=0, column=2, padx=10, pady=5)

    button_frame.pack(fill=X)

    # Labour view section
    view_section = Frame(main_container, bg=COLORS["primary"], pady=20)
    view_section.pack(fill=BOTH, expand=True)

    # Centered header
    view_header = create_heading(view_section, "CURRENT LABOUR RECORDS", font_size=16)
    view_header.pack(fill=X, pady=(0, 10))

    # Labour view frame for displaying records
    labour_view = Frame(view_section, background=COLORS["primary"])
    labour_view.pack(fill=BOTH, expand=True)

    # Populate labour records
    get_labour()

    # Status bar at the bottom
    status_bar = Frame(add_labour_window, bg=COLORS["secondary"], height=25)
    status_bar.pack(fill=X, side=BOTTOM)

    # Center the copyright text
    status_label = Label(status_bar, text="© 2025 | Sawant Cashew Industries",
                         font=("Helvetica", 9), bg=COLORS["secondary"], fg=COLORS["text_light"])
    status_label.pack(pady=3)

    add_labour_window.mainloop()


# Main function to trigger the labor details functionality
def mainmenu(expirychk=None):
    if flag == 'expirychk':
        expirychk.destroy()
    add_labour()
# Run the program
#if __name__ == "__main__":
 #   mainmenu()


