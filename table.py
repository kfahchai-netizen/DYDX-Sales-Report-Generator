from tkinter import *
from tkinter import messagebox, ttk
import database
from datetime import datetime
from tkinter.filedialog import askopenfilename
from utils import format_price, calculate_profit_or_deficit, validate_date
import graph


database.initialize_database()

root = Tk()
root.title("Generate Report")
root.geometry('800x600')  # Set a default window size
root.configure(bg="#fff")
root.withdraw()  # Hide the window initially

def populate_table():
    for row in database.fetch_table_data():
        table.insert('', 'end', values=row[1:])  # Skip the ID column

# Populate summary labels with data from the database
def populate_summary():
    summary_data = database.fetch_summary_data()
    if summary_data:
        sales_amount_label.config(text=summary_data[1])  # Total Sales Amount
        profit_deficit_label.config(text=summary_data[2])  # Total Profit/Deficit
        roi_label.config(text=summary_data[3])  # ROI
        
summary_frame = Frame(root, bg="#fff")
summary_frame.pack(fill=X, padx=10, pady=10)

# Labels for Sales Amount, Total Profit/Deficit, and ROI
Label(summary_frame, text="Sales Amount:", font=('Arial', 12), bg="#fff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
sales_amount_label = Label(summary_frame, text="RM 0.00", font=('Arial', 12), bg="#fff")
sales_amount_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

Label(summary_frame, text="Total Profit/Deficit:", font=('Arial', 12), bg="#fff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
profit_deficit_label = Label(summary_frame, text="RM 0.00", font=('Arial', 12), bg="#fff")
profit_deficit_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

Label(summary_frame, text="ROI:", font=('Arial', 12), bg="#fff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
roi_label = Label(summary_frame, text="0.00%", font=('Arial', 12), bg="#fff")
roi_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
def update_summary():
    total_sales_amount = 0.0
    total_profit_deficit = 0.0
    total_cost = 0.0

    # Calculate totals from the table data
    for item in table.get_children():
        item_data = table.item(item)['values']
        total_sales_amount += float(item_data[4][3:])  # Total (RM XX.XX)
        total_profit_deficit += float(item_data[6][3:])  # Profit/Deficit (RM XX.XX)
        total_cost += float(item_data[5][3:])  # Total Cost (RM XX.XX)

    roi = (total_profit_deficit / total_cost) * 100 if total_cost else 0

    # Update labels on the UI (if needed)
    sales_amount_label.config(text=f"RM {total_sales_amount:.2f}")
    profit_deficit_label.config(text=f"RM {total_profit_deficit:.2f}")
    roi_label.config(text=f"{roi:.2f}%")
        
def load_progress():
    # Clear existing data
    for row in table.get_children():
        table.delete(row)

    # Fetch and insert data
    data = database.load_table_data()  # Pull data from the temporary table
    for row in data:
        table.insert('', 'end', values=row)
    update_summary()



root = Tk()
root.title("Generate Report")
root.geometry('800x600')  # Set a default window size
root.configure(bg="#fff")
root.withdraw()  # Hide the window initially



    
# Function to show the table window
def show_table_window():
    root.deiconify()  # Show the window
    root.lift()  # Bring it to the front
    


def save_state_on_exit():
    rows = [table.item(row)['values'] for row in table.get_children()]
    database.save_table_data(rows)
    root.withdraw()

root.protocol("WM_DELETE_WINDOW", save_state_on_exit)



# Define global variables
item_window = None  # Initialize item_window to None
selected_item = None  # Initialize selected_item to None

# Sales report title
Label(root, text="Sales Report", font=('Arial', 20, 'bold'), bg="#fff").pack(pady=10)

controls_frame = Frame(root, bg="#f0f0f0")
controls_frame.pack(fill=X, pady=10)

# Sales Person Inputs
Label(controls_frame, text="Sales Person:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
sales_person_entry = Entry(controls_frame)
sales_person_entry.grid(row=0, column=1, padx=10, pady=10)

# Date input
Label(controls_frame, text="Date:", bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=10, sticky="w")
date_entry = Entry(controls_frame)
date_entry.grid(row=0, column=3, padx=10, pady=10)

# Table columns 
columns = ('item_code', 'item_name', 'selling_price', 'quantity', 'total', 'cost', 'profit_deficit')

# Frame for table
table_frame = Frame(root)
table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Vertical Scrollbar for the table
y_scroll = Scrollbar(table_frame, orient=VERTICAL)
y_scroll.pack(side=RIGHT, fill=Y)

# Create table with vertical scrollbar
table = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=y_scroll.set)
table.pack(fill=BOTH, expand=True)

# Configure the scrollbar to interact with the table
y_scroll.config(command=table.yview)

# Column headers 
table.heading('item_code', text="Item Code")
table.heading('item_name', text="Item Name")
table.heading('selling_price', text="Selling Price")
table.heading('quantity', text="Quantity")
table.heading('total', text="Total")
table.heading('cost', text="Total Cost")
table.heading('profit_deficit', text="Profit or Deficit")

# Adjust column widths based on root geometry
root_width = root.winfo_reqwidth()
column_width = root_width // len(columns)
for col in columns:
    table.column(col, anchor=CENTER, width=column_width)
    
load_progress()



# Function to open the item form
def item_form(modify=False):
    global item_window, selected_item
    if item_window is not None and item_window.winfo_exists():
        item_window.lift()
        return

    item_window = Toplevel(root)
    item_window.title("Data Entry Form" if not modify else "Modify Item")

    frame = Frame(item_window)
    frame.pack()

    item_info_frame = LabelFrame(frame, text='Item Information')
    item_info_frame.grid(row=0, column=0, padx=20, pady=20)

    Label(item_info_frame, text='Item code:').grid(row=0, column=0, padx=10, pady=10)
    Label(item_info_frame, text='Item name:').grid(row=1, column=0, padx=10, pady=10)
    Label(item_info_frame, text='Selling price:').grid(row=2, column=0, padx=10, pady=10)
    Label(item_info_frame, text='Quantity:').grid(row=3, column=0, padx=10, pady=10)
    Label(item_info_frame, text='Cost:').grid(row=4, column=0, padx=10, pady=10)

    item_code_entry = Entry(item_info_frame, width=30)
    item_code_entry.grid(row=0, column=1, padx=10, pady=10)
    item_name_entry = Entry(item_info_frame, width=30)
    item_name_entry.grid(row=1, column=1, padx=10, pady=10)
    selling_price_entry = Entry(item_info_frame, width=30)
    selling_price_entry.grid(row=2, column=1, padx=10, pady=10)
    quantity_entry = Entry(item_info_frame, width=30)
    quantity_entry.grid(row=3, column=1, padx=10, pady=10)
    cost_entry = Entry(item_info_frame, width=30)
    cost_entry.grid(row=4, column=1, padx=10, pady=10)

    if modify and selected_item:
        item_data = table.item(selected_item)['values']
        item_code_entry.insert(0, item_data[0])
        item_name_entry.insert(0, item_data[1])
        selling_price_entry.insert(0, item_data[2])
        quantity_entry.insert(0, item_data[3])
        cost_entry.insert(0, item_data[5])

    def submit_form():
     item_code = item_code_entry.get()
     item_name = item_name_entry.get()
     selling_price = selling_price_entry.get()
     cost = cost_entry.get()
     quantity = quantity_entry.get()

     if not quantity.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for quantity.")
        return

     formatted_selling_price = format_price(selling_price)
     formatted_cost = format_price(cost)

     if formatted_selling_price == "Invalid Price" or formatted_cost == "Invalid Price":
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for selling price and cost.")
        return

     total_cost = float(formatted_cost[3:]) * int(quantity)
     total = float(formatted_selling_price[3:]) * int(quantity)
     profit_deficit = calculate_profit_or_deficit(selling_price, quantity, cost)

     if modify and selected_item:
        table.item(selected_item, values=(item_code, item_name, formatted_selling_price, quantity, f"RM {total:.2f}", f"RM {total_cost:.2f}", profit_deficit))
     else:
        table.insert('', 'end', values=(item_code, item_name, formatted_selling_price, quantity, f"RM {total:.2f}", f"RM {total_cost:.2f}", profit_deficit))
    
     # Save changes to the database
     rows = [table.item(row)['values'] for row in table.get_children()]
     database.save_table_data(rows)

     # Close the item form after submission
     close_item_window()


    submit_button_text = "Submit" if not modify else "Update"
    enter_data_button = Button(frame, text=submit_button_text, command=submit_form)
    enter_data_button.grid(row=1, column=0, sticky="news", padx=20, pady=20)


# Add item button
add_item_button = Button(controls_frame, text="Add Item", command=lambda: item_form())
add_item_button.grid(row=0, column=4, padx=20, pady=10)

# Function to close item form after form is submitted
def close_item_window():
    global item_window, selected_item
    item_window.destroy()
    item_window = None
    selected_item = None


# Function to search item
def search_item():
    search_term = search_entry.get().strip().lower()
    if not search_term:
        messagebox.showwarning("Empty Search", "Please enter an item name to search.")
        return

    # Clear previous selections
    for row in table.selection():
        table.selection_remove(row)

    found = False
    for row in table.get_children():
        item_data = table.item(row)['values']
        item_name = str(item_data[1]).lower()
        
        if search_term in item_name:
            table.selection_add(row)
            found = True

    if not found:
        messagebox.showinfo("Not Found", "No matching items found.")
        
# Search item button       
Label(controls_frame, text="Search:").grid(row=1, column=0, padx=5, pady=10)
search_entry = Entry(controls_frame, width=25)
search_entry.grid(row=1, column=1, padx=5, pady=10)
search_button = Button(controls_frame, text="Search Item", command=search_item)
search_button.grid(row=1, column=2, padx=5, pady=10)

# Function of modify item
def modify_item():
    global selected_item
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an item to modify.")
        return
    selected_item = selected_item[0]
    item_form(modify=True)

# Modify item button
modify_item_button = Button(controls_frame, text="Modify Item", command=modify_item)
modify_item_button.grid(row=0, column=5, padx=10, pady=10)

# Function to delete item
def delete_item():
    global selected_item
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return
    response = messagebox.askyesno("Delete Item", "Do you want to delete this data?")
    if response:
        for item in selected_item:
            table.delete(item)

# Delete item button
delete_item_button = Button(controls_frame, text="Delete Item", command=delete_item)
delete_item_button.grid(row=0, column=6, padx=10, pady=10)

def clear_all_data():
    # Confirmation prompt
    response = messagebox.askyesno("Clear All Data", "Are you sure you want to delete all data?")
    if response:
        # Remove all rows from the table
        for row in table.get_children():
            table.delete(row)
        messagebox.showinfo("Data Cleared", "All data has been cleared.")

# Button to clear all data
clear_all_button = Button(controls_frame, text="Clear All Data", command=clear_all_data)
clear_all_button.grid(row=1, column=3, padx=10, pady=10)

def save_report_to_database():
    sales_person = sales_person_entry.get()
    report_date = date_entry.get()
    total_sales = sales_amount_label.cget("text")
    total_profit_deficit = profit_deficit_label.cget("text")
    roi = roi_label.cget("text")

    if not sales_person or not report_date:
        messagebox.showerror("Missing Information", "Please enter the Sales Person and Date.")
        return
    if not validate_date(report_date):
        messagebox.showerror("Invalid Date", "Please enter a valid date in the format DD-MM-YYYY.")
        return

    # Save the report metadata and get the report ID
    report_id = database.save_report(sales_person, report_date, total_sales, total_profit_deficit, roi)

    # Save individual entries
    rows = table.get_children()
    if not rows:
        messagebox.showwarning("No Data", "The table is empty!")
        return

    for row_id in rows:
        row_data = table.item(row_id)['values']
        database.save_report_entry(report_id, *row_data)

    messagebox.showinfo("Success", "Report saved successfully!")
    
def save_progress():
    rows = [table.item(row)['values'] for row in table.get_children()]
    if not rows:
        messagebox.showinfo("No Data", "No data to save.")
        return
    database.save_table_data(rows)
    messagebox.showinfo("Success", "Progress saved!")





# Add Save Report button
save_report_button = Button(controls_frame, text="Save Report", command=save_report_to_database)
save_report_button.grid(row=1, column=4, padx=10, pady=10)

def load_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = []
            for line_number, line in enumerate(file, start=1):
                row = line.strip().split(",")
                # Validate row length
                if len(row) != 5:  # Ensure only required fields are present
                    raise ValueError(f"Invalid format at line {line_number}: {line.strip()}")
                
                # Extract values
                item_code, item_name, selling_price, quantity, cost = row
                
                # Validate numeric fields
                if not quantity.isdigit():
                    raise ValueError(f"Invalid quantity at line {line_number}: {quantity}")
                if not selling_price.startswith("RM ") or not cost.startswith("RM "):
                    raise ValueError(f"Invalid price or cost format at line {line_number}. Expected 'RM XX.XX'.")

                # Remove "RM " prefix and calculate values
                selling_price_value = float(selling_price[3:])
                cost_value = float(cost[3:])
                quantity_value = int(quantity)
                total = selling_price_value * quantity_value
                total_cost = cost_value * quantity_value
                profit_deficit = total - total_cost

                # Append the full row with calculated values
                data.append([
                    item_code,
                    item_name,
                    selling_price,
                    quantity,
                    f"RM {total:.2f}",
                    f"RM {total_cost:.2f}",
                    f"RM {profit_deficit:.2f}",
                ])

        # If all rows are valid, insert them into the table
        for row in data:
            table.insert('', 'end', values=row)
        update_summary()
        messagebox.showinfo("Success", "Data loaded successfully!")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")



def load_file_button():
    # Combined prompt to show file format and ask for confirmation
    response = messagebox.askyesno(
        "File Format",
        "Please ensure the file has the following format:\n"
        "item_code,item_name,selling_price,quantity,cost\n"
        "Each value should be comma-separated, e.g.:\n"
        "001,Pen,RM 2.00,50,RM 1.00\n\n"
        "Do you wish to continue?"
    )
    
    if response:  # If the user chooses "Yes"
        # Open file selection dialog
        file_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:  # Proceed only if a file is selected
            load_from_file(file_path)

Button(controls_frame, text="Load Text File", command=load_file_button).grid(row=1, column=5, padx=10, pady=10)

graph_button = Button(controls_frame, text="Generate Graph", command=lambda:graph.generate_graph(table))
graph_button.grid(row=1, column=6, padx=10, pady=10)

# Function to toggle selection on click
def toggle_selection(event):
    item = table.identify_row(event.y)
    if item in table.selection():
        table.selection_remove(item)
    else:
        table.selection_set(item)

# Bind the Treeview select event to the toggle_selection function
table.bind("<Button-1>", toggle_selection)

# Frame for summary section
summary_frame = Frame(root, bg="#fff")
summary_frame.pack(fill=X, padx=10, pady=10)

# Labels for Sales Amount, Total Profit/Deficit, and ROI
refresh_label = Label(summary_frame, text="(Click to refresh)", font=('Arial', 10), fg="gray", bg="#fff")
refresh_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# Labels for Sales Amount, Total Profit/Deficit, and ROI
Label(summary_frame, text="Sales Amount:", font=('Arial', 12), bg="#fff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
sales_amount_label = Label(summary_frame, text="RM 0.00", font=('Arial', 12), bg="#fff")
sales_amount_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

Label(summary_frame, text="Total Profit/Deficit:", font=('Arial', 12), bg="#fff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
profit_deficit_label = Label(summary_frame, text="RM 0.00", font=('Arial', 12), bg="#fff")
profit_deficit_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

Label(summary_frame, text="ROI:", font=('Arial', 12), bg="#fff").grid(row=3, column=0, padx=5, pady=5, sticky="w")
roi_label = Label(summary_frame, text="0.00%", font=('Arial', 12), bg="#fff")
roi_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")




# Call update_summary whenever items are added, modified, or deleted
table.bind("<<TreeviewSelect>>", lambda e: update_summary())
add_item_button.config(command=lambda: [item_form(), update_summary()])
modify_item_button.config(command=lambda: [modify_item(), update_summary()])
delete_item_button.config(command=lambda: [delete_item(), update_summary()])
clear_all_button.config(command=lambda: [clear_all_data(), update_summary()])






