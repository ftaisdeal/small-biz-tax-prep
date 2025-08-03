import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QScrollArea, 
                             QGridLayout, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.db import Database


class CategorizeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.db = Database()
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        self.setWindowTitle("Assign Categories to Uncategorized Transactions")
        self.setGeometry(100, 0, 1100, self.screen().availableGeometry().height())
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        layout.setSpacing(0)  # Remove spacing between items
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Force layout to top
        
        # Add refresh button at the top
        from PyQt6.QtWidgets import QPushButton
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.setFixedHeight(30)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)
        
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
        self.grid_layout.setSpacing(1)  # Reduced spacing
        self.grid_layout.setContentsMargins(0, 0, 0, 0)  # Remove grid margins
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align content to top
        
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
            no_data_label.setFont(QFont("Arial", 16))
            no_data_label.setStyleSheet("color: #666; margin: 50px; line-height: 1.5;")
            self.grid_layout.addWidget(no_data_label, 0, 0, 1, 5)  # Span all columns
            return
        
        self.category_choices = [cat[1] for cat in categories]  # Remove "unassigned" since all are uncategorized
        self.category_id_map = {cat[1]: cat[0] for cat in categories}
        
        # Create headers
        headers = ["ID", "Date", "Payee", "Amount", "Category"]
        header_font = QFont("Arial", 14, QFont.Weight.Bold)
        
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
            self.grid_layout.addWidget(date_label, row_num, 1)
            
            payee_label = QLabel(str(txn_payee))
            payee_label.setStyleSheet(style)
            self.grid_layout.addWidget(payee_label, row_num, 2)
            
            amount_label = QLabel(str(txn_amount))
            amount_label.setStyleSheet(style)
            self.grid_layout.addWidget(amount_label, row_num, 3)
            
            # Create category dropdown - all transactions here are uncategorized
            dropdown = QComboBox()
            dropdown.addItem("-- Select Category --")  # Add placeholder option without data
            dropdown.addItems(self.category_choices)
            dropdown.setCurrentIndex(0)  # Start with placeholder selected
            dropdown.setStyleSheet(f"background-color: {row_bg}; border: 1px solid #ddd;")
            
            # Connect dropdown change to update function
            dropdown.activated.connect(
                lambda index, txn_id=txn_id, dropdown=dropdown: self.update_category_by_index(txn_id, dropdown, index)
            )
            
            self.grid_layout.addWidget(dropdown, row_num, 4)
        
        # Set column stretch factors
        self.grid_layout.setColumnStretch(0, 0)  # ID column - fixed
        self.grid_layout.setColumnStretch(1, 1)  # Date
        self.grid_layout.setColumnStretch(2, 2)  # Payee - wider
        self.grid_layout.setColumnStretch(3, 1)  # Amount
        self.grid_layout.setColumnStretch(4, 1)  # Category
    
    def update_category_by_index(self, txn_id, dropdown, index):
        """Update transaction category in database using dropdown index"""
        if index == 0:  # Skip if placeholder is selected
            return
        
        try:
            # Get the selected category name (index 0 is placeholder, so subtract 1)
            selected_category = self.category_choices[index - 1]
            
            # Apply visual feedback immediately
            dropdown.setStyleSheet(dropdown.styleSheet() + "color: green; font-weight: bold;")
            dropdown.setEnabled(False)  # Disable to show it's been processed
            
            category_id = self.category_id_map[selected_category]
            self.db.update_transaction_category(txn_id, category_id)
            
            # Refresh parent window if available
            if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
                self.parent_window.refresh_totals()
            
            # Don't auto-reload - let user manually refresh if needed
            # QTimer.singleShot(500, self.load_data)
            
        except Exception as e:
            print(f"Error updating category: {e}")
            import traceback
            traceback.print_exc()
    
    def update_category(self, txn_id, selected_category):
        """Update transaction category in database"""
        if selected_category == "-- Select Category --" or not selected_category:
            # Don't update if placeholder is selected
            return
        
        try:
            # Find the dropdown that triggered this and update its display
            sender = self.sender()
            if isinstance(sender, QComboBox):
                # Ensure the dropdown shows the selected category
                sender.setCurrentText(selected_category)
                # Add visual feedback
                sender.setStyleSheet(sender.styleSheet() + "color: green; font-weight: bold;")
                sender.setEnabled(False)  # Disable to show it's been processed
            
            category_id = self.category_id_map[selected_category]
            self.db.update_transaction_category(txn_id, category_id)
            
            # Refresh parent window if available
            if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
                self.parent_window.refresh_totals()
            
            # Use QTimer to defer the reload to avoid crashes during signal handling
            QTimer.singleShot(500, self.load_data)  # Increased delay to show the green feedback
            
        except Exception as e:
            print(f"Error updating category: {e}")
            import traceback
            traceback.print_exc()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
            self.parent_window.refresh_totals()
        event.accept()
