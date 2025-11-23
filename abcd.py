import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# --- 1. Database Management Functions ---

DB_NAME = "expense_tracker.db"

def init_db():
    """Connects to the database and creates the expenses table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_expense_to_db(date, category, amount, description):
    """Inserts a new expense record into the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                       (date, category, amount, description))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def get_total_expense():
    """Calculates and returns the sum of all 'amount' entries in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # SQL SUM function calculates the total amount
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()
    # Returns 0.0 if the table is empty (SUM returns None)
    return total if total is not None else 0.0

# --- 2. GUI Logic / Event Handlers ---

def submit_expense():
    """Handles the 'Add Expense' button click."""
    date = date_entry.get()
    category = category_var.get()
    
    try:
        # Input validation for amount
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showerror("Input Error", "Amount must be a positive number.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a valid number.")
        return

    description = description_entry.get()
    
    if add_expense_to_db(date, category, amount, description):
        messagebox.showinfo("Success", f"Expense of ${amount:.2f} added successfully!")
        # Clear fields for next entry
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        # Update the total display immediately (if you were using a label instead of a message box)
    else:
        messagebox.showerror("Error", "Could not add expense to the database.")

def view_summary():
    """Calculates and displays the total expense in a message box."""
    total = get_total_expense()
    
    summary_message = f"Your Total Expense Recorded:\n\n$ {total:,.2f}"
    
    messagebox.showinfo("Expense Summary", summary_message)

# --- 3. GUI Setup ---

# Initialize the database and the main window
init_db()
root = tk.Tk()
root.title("💰 Personal Expense Tracker")

# Configuration for a cleaner look
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(padx=10, pady=10)

# Input Widgets
tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
date_entry = tk.Entry(input_frame, width=25) 
date_entry.grid(row=0, column=1, padx=5, pady=5)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d")) # Default date

tk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
category_var = tk.StringVar(input_frame)
category_var.set("Food") 
categories = ["Food", "Transport", "Bills", "Entertainment", "Income (Negative Expense)", "Other"]
category_menu = tk.OptionMenu(input_frame, category_var, *categories)
category_menu.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

tk.Label(input_frame, text="Amount ($):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
amount_entry = tk.Entry(input_frame, width=25)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
description_entry = tk.Entry(input_frame, width=25)
description_entry.grid(row=3, column=1, padx=5, pady=5)

# --- Buttons Frame ---
button_frame = tk.Frame(root, pady=10)
button_frame.pack()

# Add Expense Button
add_button = tk.Button(button_frame, text="➕ Add Expense", command=submit_expense, width=15, bg='#4CAF50', fg='white')
add_button.pack(side=tk.LEFT, padx=10)

# View Total Button (New Feature)
total_button = tk.Button(button_frame, text="📊 View Total", command=view_summary, width=15, bg='#2196F3', fg='white')
total_button.pack(side=tk.LEFT, padx=10)

root.mainloop()