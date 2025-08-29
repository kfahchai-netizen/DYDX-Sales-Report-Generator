import sqlite3

# Create a reports table and update initialize_database function
def initialize_database():
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()

    # Table for storing individual entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS report_entries (
                        id INTEGER PRIMARY KEY,
                        report_id INTEGER,
                        item_code TEXT,
                        item_name TEXT,
                        selling_price TEXT,
                        quantity INTEGER,
                        total TEXT,
                        cost TEXT,
                        profit_deficit TEXT,
                        FOREIGN KEY(report_id) REFERENCES reports(id))''')

    # Table for storing metadata about each report
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY,
                        sales_person TEXT,
                        report_date TEXT,
                        total_sales_amount TEXT,
                        total_profit_deficit TEXT,
                        roi TEXT)''')

    conn.commit()
    conn.close()

# Save report's metadata
def save_report(sales_person, report_date, total_sales, total_profit_deficit, roi):
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reports (sales_person, report_date, total_sales_amount, total_profit_deficit, roi) VALUES (?, ?, ?, ?, ?)',
                   (sales_person, report_date, total_sales, total_profit_deficit, roi))
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id

# Save individual entries for a report
def save_report_entry(report_id, item_code, item_name, selling_price, quantity, total, cost, profit_deficit):
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO report_entries (report_id, item_code, item_name, selling_price, quantity, total, cost, profit_deficit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (report_id, item_code, item_name, selling_price, quantity, total, cost, profit_deficit))
    conn.commit()
    conn.close()

# Fetch all reports
def fetch_reports():
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports')
    reports = cursor.fetchall()
    conn.close()
    return reports

# Fetch entries for a specific report
def fetch_report_entries(report_id):
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM report_entries WHERE report_id = ?', (report_id,))
    entries = cursor.fetchall()
    conn.close()
    return entries

# Delete report at history
def delete_report(report_id):
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()

    # Delete associated entries first
    cursor.execute('DELETE FROM report_entries WHERE report_id = ?', (report_id,))
    # Then delete the report
    cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))

    conn.commit()
    conn.close()

# Save data from table to history
def save_table_data(data):
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS temp_table (item_code TEXT, item_name TEXT, selling_price TEXT, quantity INTEGER, total TEXT, cost TEXT, profit_deficit TEXT)')
    cursor.execute('DELETE FROM temp_table')  # Clear existing data
    cursor.executemany('INSERT INTO temp_table VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()  # Commit changes after data insertion
    conn.close()   # Close the connection

# Load data from history to table
def load_table_data():
    conn = sqlite3.connect('sales_report.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS temp_table (item_code TEXT, item_name TEXT, selling_price TEXT, quantity INTEGER, total TEXT, cost TEXT, profit_deficit TEXT)')
    cursor.execute('SELECT * FROM temp_table')
    data = cursor.fetchall()  # Fetch all rows from the table
    conn.close()  # Close the connection
    return data


