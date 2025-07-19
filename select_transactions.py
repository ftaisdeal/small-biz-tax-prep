import tkinter as tk
from tkinter import ttk
import sqlite3

def fetch_transactions():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_date, payee_description, amount FROM transactions")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, rows

def display_transactions():
    columns, rows = fetch_transactions()
    
    root = tk.Tk()
    root.title("All Transactions")

    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    # Set up columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.W)

    # Insert rows
    for row in rows:
        tree.insert("", tk.END, values=row)

    root.mainloop()

if __name__ == "__main__":
    display_transactions()