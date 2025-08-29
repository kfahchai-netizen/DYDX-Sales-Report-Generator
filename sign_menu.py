from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import table
import database 

history_window = None


def show_history_window():
    global history_window
    # Check whether History window is already open
    if history_window and history_window.winfo_exists():
        history_window.lift()  # Bring existing window to the front
        return
    history_window = Toplevel(root)
    history_window.title("History")
    history_window.geometry('1200x600')
    
    def on_close():
        global history_window
        if history_window:  # Check whether the window exists before trying to destroy it
            history_window.destroy()
            history_window = None  # Reset the variable after the window is destroyed

    history_window.protocol("WM_DELETE_WINDOW", on_close)

    # Frame for history page controls
    history_controls_frame = Frame(history_window, bg="#f0f0f0")
    history_controls_frame.pack(side=BOTTOM, fill=X, pady=10)

    # Delete report function
    def delete_report():
        selected = reports_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a report to delete.")
            return

        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this report?")
        if response:
            report_id = reports[selected[0]][0]  # Assuming report ID is in the first column
            database.delete_report(report_id)
            reports_listbox.delete(selected[0])
            report_table.delete(*report_table.get_children())  # Clear the table
            messagebox.showinfo("Deleted", "Report deleted successfully!")

    # Add Delete Report button
    delete_report_button = Button(history_controls_frame,  text="Delete Report", 
                                   command=delete_report)
    delete_report_button.pack(padx=10, pady=10)

    # Add Transfer Data Button
    def transfer_to_table():
    # Get all data from the report_table (Treeview on the history page)
     rows = [report_table.item(row_id)['values'] for row_id in report_table.get_children()]
     if not rows:
        messagebox.showinfo("No Data", "No data to transfer.")
        return

    # Save data to the temp_table in the database
     database.save_table_data(rows)

    # Call the table window's load_progress method to refresh the table with transferred data
     table.load_progress()
     messagebox.showinfo("Success", "Data transferred to Generate Report table.")

     # Add Transfer Data button to history_controls_frame
    transfer_button = Button(history_controls_frame, text="Transfer Data into Table", command=transfer_to_table)
    transfer_button.pack(padx=20, pady=20)


    # List of reports
    reports_frame = Frame(history_window)
    reports_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    reports_listbox = Listbox(reports_frame, width=30)
    reports_listbox.pack(fill=BOTH, expand=True)

    # Frame for the selected report's table
    report_frame = Frame(history_window)
    report_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    # Scrollbars for the table
    y_scroll = Scrollbar(report_frame, orient=VERTICAL)
    y_scroll.pack(side=RIGHT, fill=Y)

    x_scroll = Scrollbar(report_frame, orient=HORIZONTAL)
    x_scroll.pack(side=BOTTOM, fill=X)

    # Table for displaying entries
    columns = ('item_code', 'item_name', 'selling_price', 'quantity', 'total', 'cost', 'profit_deficit')
    report_table = ttk.Treeview(report_frame, columns=columns, show='headings', yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    report_table.pack(fill=BOTH, expand=True)
    y_scroll.config(command=report_table.yview)
    x_scroll.config(command=report_table.xview)

    for col in columns:
        report_table.heading(col, text=col.replace('_', ' ').title())
        report_table.column(col, anchor=CENTER, width=120)

    # Populate reports listbox with reports from the database
    reports = database.fetch_reports()
    for report in reports:
        reports_listbox.insert(END, f"Report {report[0]} - {report[1]} ({report[2]})")

    # Load selected report entries into the table
    def load_report(event):
        report_table.delete(*report_table.get_children())
        selection = reports_listbox.curselection()
        if selection:
            report_id = reports[selection[0]][0]
            entries = database.fetch_report_entries(report_id)
            for entry in entries:
                report_table.insert('', 'end', values=entry[2:])  # Skip ID and report_id

    reports_listbox.bind('<<ListboxSelect>>', load_report)

    # Close Button
    Button(history_controls_frame, text="Close", command=history_window.destroy).pack(padx=10, pady=10)



def show_menu(root):
    # Clear the existing widgets in root (login screen)
    for widget in root.winfo_children():
        widget.destroy()

    # Menu Screen in the same root window
    root.title("Menu")
    root.geometry('900x550')
    root.configure(bg="#fff")
    root.resizable(False, False)
    
    Label(root, text="Welcome to DYDX Sales Report Generator", font=('Arial', 20, 'bold'), bg="#fff").pack(pady=10)
    
    main_frame = Frame(root, highlightbackground='black', highlightthickness=2)
    main_frame.pack(side=LEFT, fill=Y)
    main_frame.pack_propagate(False)
    main_frame.configure(height=550, width=900)
    

    report_button = Button(main_frame, text='Generate \nReport',width=8,command=table.show_table_window,
                           font=('Arial', 18, 'bold'), bd=3)
    report_button.place(x=375, y=70)
   

    history_button = Button(main_frame, text='History',width=8,
                            font=('Arial', 18, 'bold'), bd=3)
    history_button.place(x=375, y=230)
    history_button.config(command=show_history_window)
    
    def logout():
    # Clear the existing widgets in root (menu screen)
     for widget in root.winfo_children():
        widget.destroy()
    
    # Show the login screen
     login_screen(root)   

    logout_button = Button(main_frame, text='Log out',width=8, 
                           font=('Arial', 18, 'bold'), bd=3, command=logout)
    logout_button.place(x=375, y=350)
 
    

def login_screen(root):
    # Login Screen
    root.title("Login")
    root.geometry('900x550')
    root.configure(bg="#fff")
    root.resizable(False, False)

    # Frame
    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=300, y=85)

    # Heading
    heading = Label(frame, text='Sign in', fg='black', bg='white', font=('Arial', 23, 'bold'))
    heading.place(x=110, y=5)

    # Username
    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        if user.get() == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=45, fg='black', border=0, bg='white', font=('Arial', 12,))
    user.place(x=28, y=105)
    user.insert(0, "Username")
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=23, y=132)

    # Password
    def on_enter_password(e):
        password.delete(0, 'end')
        password.config(show='*')

    def on_leave_password(e):
        if password.get() == '':
            password.config(show='')
            password.insert(0, 'Password')

    password = Entry(frame, width=45, fg='black', border=0, bg='white', font=('Arial', 12,))
    password.place(x=28, y=195)
    password.insert(0, "Password")
    Frame(frame, width=295, height=2, bg='black').place(x=23, y=222)
    password.bind('<FocusIn>', on_enter_password)
    password.bind('<FocusOut>', on_leave_password)

    # Sign in Button
    def signin():
        username = user.get()
        entered_password = password.get()
        if username == 'admin' and entered_password == '123': #username and password validation
            show_menu(root)  # Load menu screen within the same root window
        else:
            messagebox.showerror("Invalid", 'Invalid username and password')

    Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=265)

# Main application start
root = Tk()
login_screen(root)  # Start with the login screen
root.mainloop()
