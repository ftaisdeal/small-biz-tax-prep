import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.db import Database

def open_categorize_window():
    """Open the categorize transactions window"""
    db = Database()
    categories = db.fetch_categories()
    transactions = db.fetch_transactions()

    category_choices = ["unassigned"] + [cat[1] for cat in categories]
    category_id_map = {cat[1]: cat[0] for cat in categories}

    categorize_window = tk.Toplevel()
    categorize_window.title("Assign Categories to Transactions")
    
    # Set window size and position at top of screen
    window_width = 1000
    
    # Get screen dimensions
    screen_width = categorize_window.winfo_screenwidth()
    screen_height = categorize_window.winfo_screenheight()
    
    # Use full screen height
    window_height = screen_height
    
    # Calculate position - center horizontally, full height from top
    x = (screen_width - window_width) // 2
    y = 0  # Start from top of screen
    
    categorize_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Add callback to refresh main window when this window is closed
    def on_window_close():
        categorize_window.destroy()
        # Trigger refresh of main window if there's a refresh function available
        if hasattr(open_categorize_window, 'refresh_callback'):
            open_categorize_window.refresh_callback()
    
    categorize_window.protocol("WM_DELETE_WINDOW", on_window_close)
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(categorize_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    # Configure scrollable frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Use scrollable_frame instead of frame for content
    frame = scrollable_frame

    # Create header row frame
    header_frame = tk.Frame(frame, bg="white")
    header_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=2, pady=2)
    
    # Configure header frame column weights to match data rows
    header_frame.grid_columnconfigure(0, weight=0, minsize=50)  # ID column - fixed width
    for i in range(1, 5):
        header_frame.grid_columnconfigure(i, weight=1)
    
    headers = ["ID", "Date", "Payee", "Amount", "Category"]
    for col_num, header in enumerate(headers):
        tk.Label(header_frame, text=header, font=("Arial", 14,), bg="white").grid(row=0, column=col_num, padx=4, pady=4, sticky="w")

    dropdown_vars = []
    for row_num, txn in enumerate(transactions, start=1):
        txn_id, txn_date, txn_payee, txn_amount = txn
        
        # Alternate row colors: white for odd rows, light gray for even rows
        row_bg = "white" if row_num % 2 == 1 else "#f8f8f8"
        
        # Create a frame for the entire row with background color
        row_frame = tk.Frame(frame, bg=row_bg)
        row_frame.grid(row=row_num, column=0, columnspan=5, sticky="ew", padx=2, pady=1)
        
        # Configure grid weights for the row frame
        # Give ID column less weight to keep it compact and clearly left-aligned
        row_frame.grid_columnconfigure(0, weight=0, minsize=50)  # ID column - fixed width
        for i in range(1, 5):
            row_frame.grid_columnconfigure(i, weight=1)
        
        # For white rows, ensure all backgrounds are white; for gray rows, use row_bg
        label_bg = "white" if row_num % 2 == 1 else row_bg
        
        tk.Label(row_frame, text=txn_id, bg=label_bg).grid(row=0, column=0, padx=2, pady=2, sticky="w")
        tk.Label(row_frame, text=txn_date, bg=label_bg).grid(row=0, column=1, padx=2, pady=2, sticky="w")
        tk.Label(row_frame, text=txn_payee, bg=label_bg).grid(row=0, column=2, padx=2, pady=2, sticky="w")
        tk.Label(row_frame, text=txn_amount, bg=label_bg).grid(row=0, column=3, padx=2, pady=2, sticky="w")

        assigned_cat_id = db.fetch_transaction_category(txn_id)
        if assigned_cat_id is not None:
            default_cat_name = next((cat[1] for cat in categories if cat[0] == assigned_cat_id), "unassigned")
        else:
            default_cat_name = "unassigned"

        var = tk.StringVar(value=default_cat_name)
        dropdown_vars.append(var)
        
        def make_live_update_callback(transaction_id, var):
            def callback(*args):
                selected = var.get()
                if selected == "unassigned":
                    db.update_transaction_category(transaction_id, None)
                else:
                    db.update_transaction_category(transaction_id, category_id_map[selected])
                # Refresh the main window if callback is available
                if hasattr(open_categorize_window, 'refresh_callback'):
                    open_categorize_window.refresh_callback()
            return callback
        
        # Set up live update when dropdown value changes
        var.trace('w', make_live_update_callback(txn_id, var))
        
        # Use tk.OptionMenu instead of ttk.OptionMenu to control background color
        dropdown = tk.OptionMenu(row_frame, var, *category_choices)
        dropdown.config(bg=label_bg, relief="solid", bd=1)
        dropdown["menu"].config(bg="white")
        dropdown.grid(row=0, column=4, padx=2, pady=2, sticky="e")
    
    # Add mouse wheel scrolling after all widgets are created
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_mousewheel_linux_up(event):
        canvas.yview_scroll(-1, "units")
        
    def _on_mousewheel_linux_down(event):
        canvas.yview_scroll(1, "units")
    
    # Bind mouse wheel to all widgets in the window
    def bind_mousewheel_to_all(widget):
        try:
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel_linux_up)
            widget.bind("<Button-5>", _on_mousewheel_linux_down)
        except tk.TclError:
            pass  # Some widgets don't support binding
        
        for child in widget.winfo_children():
            bind_mousewheel_to_all(child)
    
    # Apply mouse wheel binding to the entire window hierarchy
    bind_mousewheel_to_all(categorize_window)

def main():
    root = tk.Tk()
    root.title("Small Biz Tax Prep")
    
    # Set window size
    window_width = 800
    window_height = 800
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position - center horizontally, top of screen vertically
    x = (screen_width - window_width) // 2
    y = 50  # Position near top of screen with small margin
    
    # Set window geometry with position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Title label
    title_label = tk.Label(main_frame, text="Small Biz Tax Prep", font=("Arial", 28))
    title_label.pack(pady=20)
    
    # Initialize database connection
    db = Database()
    
    # Create revenue label (will be updated by refresh function)
    revenue_label = tk.Label(main_frame, font=("Arial", 16, "bold"), fg="black")
    revenue_label.pack(pady=5)
    
    # Create expenses label (will be updated by refresh function)
    expenses_label = tk.Label(main_frame, font=("Arial", 16, "bold"), fg="black")
    expenses_label.pack(pady=5)
    
    # Create profit/loss label (will be updated by refresh function)
    profit_loss_label = tk.Label(main_frame, font=("Arial", 16, "bold"), fg="black")
    profit_loss_label.pack(pady=5)
    
    def refresh_totals():
        """Refresh the revenue, expenses, and profit/loss display"""
        total_revenue = db.get_total_categorized_revenue()
        total_expenses = db.get_total_categorized_expenses()
        profit_loss = total_revenue + total_expenses  # expenses are negative, so we add them
        
        revenue_label.config(text=f"Revenue: ${total_revenue:,.2f}")
        expenses_label.config(text=f"Expenses: ${abs(total_expenses):,.2f}")
        
        # Color code profit/loss: green for profit, red for loss
        if profit_loss >= 0:
            profit_loss_color = "black"
            profit_loss_text = f"Profit: ${profit_loss:,.2f}"
        else:
            profit_loss_color = "black"
            profit_loss_text = f"Loss: ${abs(profit_loss):,.2f}"
        
        profit_loss_label.config(text=profit_loss_text, fg=profit_loss_color)
    
    # Initial load of totals
    refresh_totals()
    
    # Set the refresh callback for the categorize window
    open_categorize_window.refresh_callback = refresh_totals
    
    # Categorize button
    categorize_btn = tk.Button(main_frame, text="Categorize", font=("Arial", 12), 
                              command=open_categorize_window, width=15, height=2)
    categorize_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
