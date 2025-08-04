import tkinter as tk
from tkinter import ttk
import sqlite3

DB_NAME = "database/expense_tracker.db"

def fetch_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def fetch_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, transaction_date, payee_description, amount FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def fetch_transaction_category(transaction_id):
    """Returns category_id for a given transaction_id, or None if not assigned."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT category_id FROM transaction_categories WHERE transaction_id = ?", (transaction_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_transaction_category(transaction_id, category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Remove existing category assignment for this transaction (if any)
    cursor.execute("DELETE FROM transaction_categories WHERE transaction_id = ?", (transaction_id,))
    # Only insert if category is not "unassigned"
    if category_id is not None:
        cursor.execute("INSERT INTO transaction_categories (transaction_id, category_id) VALUES (?, ?)", (transaction_id, category_id))
    conn.commit()
    conn.close()

def main():
    categories = fetch_categories()
    transactions = fetch_transactions()

    # Insert "unassigned" at the start of the choices
    category_choices = ["unassigned"] + [cat[1] for cat in categories]
    category_id_map = {cat[1]: cat[0] for cat in categories}

    root = tk.Tk()
    root.title("Assign Categories to Transactions (Junction Table)")
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Configure column widths to make it behave more like a table
    frame.grid_columnconfigure(0, weight=0, minsize=50)   # ID - fixed small width
    frame.grid_columnconfigure(1, weight=0, minsize=100)  # Date - fixed medium width
    frame.grid_columnconfigure(2, weight=1, minsize=200)  # Payee - expandable
    frame.grid_columnconfigure(3, weight=0, minsize=100)  # Amount - fixed medium width
    frame.grid_columnconfigure(4, weight=0, minsize=150)  # Category - fixed medium width
    frame.grid_columnconfigure(5, weight=0, minsize=80)   # Action - fixed small width

    headers = ["ID", "Date", "Payee", "Amount", "Category", "Action"]
    header_alignments = ["w", "w", "w", "e", "e", "w"]  # left, left, left, right, right, left
    for col_num, header in enumerate(headers):
        tk.Label(frame, text=header, font=("Verdana", 10, "bold")).grid(row=0, column=col_num, padx=4, pady=4, sticky=header_alignments[col_num])

    dropdown_vars = []
    for row_num, txn in enumerate(transactions, start=1):
        txn_id, txn_date, txn_payee, txn_amount = txn

        tk.Label(frame, text=txn_id).grid(row=row_num, column=0, padx=2, pady=2, sticky="w")
        tk.Label(frame, text=txn_date).grid(row=row_num, column=1, padx=2, pady=2, sticky="w")
        tk.Label(frame, text=txn_payee).grid(row=row_num, column=2, padx=2, pady=2, sticky="w")
        tk.Label(frame, text=txn_amount).grid(row=row_num, column=3, padx=2, pady=2, sticky="e")

        # Get current category assignment via junction table
        assigned_cat_id = fetch_transaction_category(txn_id)
        if assigned_cat_id is not None:
            # Find matching category name
            default_cat_name = next((cat[1] for cat in categories if cat[0] == assigned_cat_id), "unassigned")
        else:
            default_cat_name = "unassigned"

        var = tk.StringVar(value=default_cat_name)
        dropdown_vars.append(var)
        dropdown = ttk.OptionMenu(frame, var, default_cat_name, *category_choices)
        dropdown.grid(row=row_num, column=4, padx=2, pady=2, sticky="ew")  # Fill width and align right

        def make_update_callback(transaction_id, var):
            def callback():
                selected = var.get()
                if selected == "unassigned":
                    update_transaction_category(transaction_id, None)
                else:
                    update_transaction_category(transaction_id, category_id_map[selected])
            return callback

        btn = tk.Button(frame, text="Update", command=make_update_callback(txn_id, var))
        btn.grid(row=row_num, column=5, padx=2, pady=2, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    main()