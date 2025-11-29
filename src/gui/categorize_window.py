import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QScrollArea,
                             QGridLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.db import Database


class CategorizeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.db = Database()
        self.pending_changes = {}  # Store changes before database update
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        self.setWindowTitle("Categorize Transactions")
        self.setGeometry(100, 0, 1100, self.screen().availableGeometry().height())
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Add update button at the top
        from PyQt6.QtWidgets import QPushButton
        update_btn = QPushButton("Update Database")
        update_btn.setFixedHeight(35)
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        update_btn.clicked.connect(self.update_all_categories)
        layout.addWidget(update_btn)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create scrollable widget
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        
        # Create grid layout for the scrollable content
        self.grid_layout = QGridLayout(scroll_widget)
        self.grid_layout.setSpacing(1)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(scroll_area)
        
    def load_data(self):
        # Clear existing layout
        for i in reversed(range(self.grid_layout.count())): 
            child = self.grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get data from database
        categories = self.db.fetch_categories()
        transactions = self.db.fetch_uncategorized_transactions()
        
        # Check if there are any uncategorized transactions
        if not transactions:
            # Show message when no uncategorized transactions
            no_data_label = QLabel("No uncategorized transactions found.\n\nAll transactions have been categorized.")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setFont(QFont("Verdana", 16))
            no_data_label.setStyleSheet("color: #666; margin: 50px; line-height: 1.5;")
            self.grid_layout.addWidget(no_data_label, 0, 0, 1, 5)
            return
        
        self.category_choices = [cat[1] for cat in categories]
        self.category_id_map = {cat[1]: cat[0] for cat in categories}
        
        # Create headers
        headers = ["ID", "Date", "Payee", "Amount", "Category", "Note"]
        header_font = QFont("Verdana", 14, QFont.Weight.Bold)
        
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(header_font)
            header_label.setStyleSheet("background-color: #e0e0e0; padding: 8px; border: 1px solid #ccc;")
            self.grid_layout.addWidget(header_label, 0, col)
        
        # Add transaction rows
        for row_num, txn in enumerate(transactions, start=1):
            txn_id, txn_date, txn_payee, txn_amount = txn
            
            # Alternate row colors
            row_bg = "#ffffff" if row_num % 2 == 1 else "#f8f8f8"
            style = f"background-color: {row_bg}; padding: 4px; border: 1px solid #ddd;"
            
            # Create labels for transaction data
            id_label = QLabel(str(txn_id))
            id_label.setStyleSheet(style)
            id_label.setFixedWidth(50)
            self.grid_layout.addWidget(id_label, row_num, 0)
            
            date_label = QLabel(str(txn_date))
            date_label.setStyleSheet(style)
            date_label.setFixedWidth(80)  # Set width for exactly 10 characters
            self.grid_layout.addWidget(date_label, row_num, 1)
            
            payee_label = QLabel(str(txn_payee))
            payee_label.setStyleSheet(style)
            payee_label.setFixedWidth(150)  # Half the original width
            self.grid_layout.addWidget(payee_label, row_num, 2)
            
            amount_label = QLabel(f"{float(txn_amount):.2f}")
            amount_label.setStyleSheet(style)
            amount_label.setFixedWidth(70)  # Set width for maximum 8 characters
            amount_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.grid_layout.addWidget(amount_label, row_num, 3)
            
            # Create category dropdown - EXACT copy from working test
            dropdown = QComboBox()
            dropdown.addItem("-- Select Category --")
            dropdown.addItems(self.category_choices)
            dropdown.setFixedWidth(180)  # Set width for 22 characters
            # Remove custom styling that's causing hover issues
            # dropdown.setStyleSheet(f"background-color: {row_bg}; border: 1px solid #ddd;")
            
            # Store transaction ID for later use
            dropdown.setProperty("transaction_id", txn_id)
            
            # Connect using EXACT same method as working test
            dropdown.currentIndexChanged.connect(
                lambda index, dd=dropdown: self.handle_selection(index, dd)
            )
            
            self.grid_layout.addWidget(dropdown, row_num, 4)
            
            # Create note input field - moved to last column
            from PyQt6.QtWidgets import QLineEdit
            note_input = QLineEdit()
            note_input.setStyleSheet(style)
            note_input.setFixedWidth(240)  # Double the original width
            note_input.setProperty("transaction_id", txn_id)
            self.grid_layout.addWidget(note_input, row_num, 5)
        
        # Set column stretch factors
        self.grid_layout.setColumnStretch(0, 0)  # ID column - fixed
        self.grid_layout.setColumnStretch(1, 1)  # Date
        self.grid_layout.setColumnStretch(2, 1)  # Payee - reduced width
        self.grid_layout.setColumnStretch(3, 1)  # Amount
        self.grid_layout.setColumnStretch(4, 1)  # Category
        self.grid_layout.setColumnStretch(5, 2)  # Note - wider
    
    def handle_selection(self, index, dropdown):
        """Handle dropdown selection - store change for later update"""
        if index > 0:  # Skip placeholder
            # Get selected text
            selected_category = dropdown.itemText(index)
            
            # Get transaction ID
            txn_id = dropdown.property("transaction_id")
            
            # Store the pending change (don't update database yet)
            category_id = self.category_id_map[selected_category]
            self.pending_changes[txn_id] = category_id
            
            # Visual feedback that change is pending
            dropdown.setStyleSheet("background-color: #fff3cd; border: 2px solid #ffc107;")
    
    def update_all_categories(self):
        """Update all pending category changes and notes to database"""
        if not self.pending_changes:
            return
            
        # Collect notes from all note input fields
        from PyQt6.QtWidgets import QLineEdit
        
        # Update database with all pending changes and notes
        for txn_id, category_id in self.pending_changes.items():
            # Find the note input field for this transaction
            note_text = ""
            for row in range(1, self.grid_layout.rowCount()):
                widget = self.grid_layout.itemAtPosition(row, 5)
                if widget and isinstance(widget.widget(), QLineEdit):
                    input_widget = widget.widget()
                    if input_widget.property("transaction_id") == txn_id:
                        note_text = input_widget.text()
                        break
            
            # Update category
            self.db.update_transaction_category(txn_id, category_id)
            
            # Update note if provided
            if note_text.strip():
                escaped_note = note_text.replace("'", "''")
                self.db.execute_sql(f"UPDATE transactions SET note = '{escaped_note}' WHERE id = {txn_id}")
        
        # Also update notes for transactions that don't have category changes
        for row in range(1, self.grid_layout.rowCount()):
            widget = self.grid_layout.itemAtPosition(row, 5)
            if widget and isinstance(widget.widget(), QLineEdit):
                input_widget = widget.widget()
                txn_id = input_widget.property("transaction_id")
                note_text = input_widget.text()
                
                # Update note if there's text and this transaction wasn't already updated above
                if note_text.strip() and txn_id not in self.pending_changes:
                    escaped_note = note_text.replace("'", "''")
                    self.db.execute_sql(f"UPDATE transactions SET note = '{escaped_note}' WHERE id = {txn_id}")
        
        # Clear pending changes
        self.pending_changes.clear()
        
        # Refresh parent window
        if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
            self.parent_window.refresh_totals()
            
        # Reload the categorize window to show updated data
        self.load_data()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
            self.parent_window.refresh_totals()
        event.accept()
