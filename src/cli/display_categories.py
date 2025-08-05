import tkinter as tk
from tkinter import ttk
import sqlite3

def show_categories():
    conn = sqlite3.connect('tax_prep.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def main():
    categories = show_categories()
    # Prepare display names (you can use just names, or "id - name")
    category_options = [f"{cat[1]}" for cat in categories]  # Just names

    root = tk.Tk()
    root.title("Select Category")

    label = tk.Label(root, text="Choose a category:")
    label.pack(pady=10)

    selected_category = tk.StringVar()
    if category_options:
        selected_category.set(category_options[0])  # Default value
    else:
        category_options = ["No categories found"]
        selected_category.set(category_options[0])

    dropdown = ttk.OptionMenu(root, selected_category, selected_category.get(), *category_options)
    dropdown.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()