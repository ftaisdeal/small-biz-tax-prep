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

def get_column_widths(columns, rows):
    # Get max width for each column (header and data)
    col_widths = []
    for col_idx, col in enumerate(columns):
        max_len = len(str(col))
        for row in rows:
            entry_len = len(str(row[col_idx]))
            if entry_len > max_len:
                max_len = entry_len
        col_widths.append(max_len)
    return col_widths

def display_transactions():
    columns, rows = fetch_transactions()
    col_widths = get_column_widths(columns, rows)

    root = tk.Tk()
    root.title("All Transactions")

    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    # Set up columns with calculated widths
    for idx, col in enumerate(columns):
        width_px = col_widths[idx] * 6 + 1  # 8 pixels per character + padding
        tree.heading(col, text=col)
        tree.column(col, width=width_px, anchor=tk.W, stretch=True)

    # Insert rows
    for row in rows:
        tree.insert("", tk.END, values=row)

    root.mainloop()

if __name__ == "__main__":
    display_transactions()