import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QScrollArea, 
                             QGridLayout, QComboBox, QFrame)
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
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        self.setWindowTitle("Assign Categories to Transactions")
        self.setGeometry(100, 0, 1100, self.screen().availableGeometry().height())
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
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
        self.grid_layout.setSpacing(2)
        
        layout.addWidget(scroll_area)
        
    def load_data(self):
        # Clear existing layout
        for i in reversed(range(self.grid_layout.count())): 
            child = self.grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get data from database
        categories = self.db.fetch_categories()
        transactions = self.db.fetch_transactions()
        
        self.category_choices = ["unassigned"] + [cat[1] for cat in categories]
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
            
            # Create category dropdown
            assigned_cat_id = self.db.fetch_transaction_category(txn_id)
            if assigned_cat_id is not None:
                default_cat_name = next((cat[1] for cat in categories if cat[0] == assigned_cat_id), "unassigned")
            else:
                default_cat_name = "unassigned"
            
            dropdown = QComboBox()
            dropdown.addItems(self.category_choices)
            dropdown.setCurrentText(default_cat_name)
            dropdown.setStyleSheet(f"background-color: {row_bg}; border: 1px solid #ddd;")
            
            # Connect dropdown change to update function
            dropdown.currentTextChanged.connect(
                lambda text, txn_id=txn_id: self.update_category(txn_id, text)
            )
            
            self.grid_layout.addWidget(dropdown, row_num, 4)
        
        # Set column stretch factors
        self.grid_layout.setColumnStretch(0, 0)  # ID column - fixed
        self.grid_layout.setColumnStretch(1, 1)  # Date
        self.grid_layout.setColumnStretch(2, 2)  # Payee - wider
        self.grid_layout.setColumnStretch(3, 1)  # Amount
        self.grid_layout.setColumnStretch(4, 1)  # Category
    
    def update_category(self, txn_id, selected_category):
        """Update transaction category in database"""
        if selected_category == "unassigned":
            self.db.update_transaction_category(txn_id, None)
        else:
            category_id = self.category_id_map[selected_category]
            self.db.update_transaction_category(txn_id, category_id)
        
        # Refresh parent window if available
        if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
            self.parent_window.refresh_totals()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.parent_window and hasattr(self.parent_window, 'refresh_totals'):
            self.parent_window.refresh_totals()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.categorize_window = None
        self.setup_ui()
        self.refresh_totals()
        
    def setup_ui(self):
        self.setWindowTitle("Small Biz Tax Prep")
        self.setGeometry(200, 50, 800, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title label
        title_label = QLabel("Small Biz Tax Prep")
        title_font = QFont("Arial", 28)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Financial summary labels
        summary_font = QFont("Arial", 16, QFont.Weight.Bold)
        
        self.revenue_label = QLabel()
        self.revenue_label.setFont(summary_font)
        self.revenue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.revenue_label)
        
        self.expenses_label = QLabel()
        self.expenses_label.setFont(summary_font)
        self.expenses_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.expenses_label)
        
        self.profit_loss_label = QLabel()
        self.profit_loss_label.setFont(summary_font)
        self.profit_loss_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.profit_loss_label)
        
        # Add some spacing
        layout.addStretch()
        
        # Categorize button
        categorize_btn = QPushButton("Categorize")
        button_font = QFont("Arial", 12)
        categorize_btn.setFont(button_font)
        categorize_btn.setFixedSize(150, 60)
        categorize_btn.clicked.connect(self.open_categorize_window)
        
        # Center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(categorize_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def refresh_totals(self):
        """Refresh the revenue, expenses, and profit/loss display"""
        total_revenue = self.db.get_total_categorized_revenue()
        total_expenses = self.db.get_total_categorized_expenses()
        profit_loss = total_revenue + total_expenses  # expenses are negative, so we add them
        
        self.revenue_label.setText(f"Revenue: ${total_revenue:,.2f}")
        self.expenses_label.setText(f"Expenses: ${abs(total_expenses):,.2f}")
        
        # Color code profit/loss: green for profit, red for loss
        if profit_loss >= 0:
            profit_loss_color = "black"
            profit_loss_text = f"Profit: ${profit_loss:,.2f}"
        else:
            profit_loss_color = "red"
            profit_loss_text = f"Loss: ${abs(profit_loss):,.2f}"
        
        self.profit_loss_label.setText(profit_loss_text)
        self.profit_loss_label.setStyleSheet(f"color: {profit_loss_color};")
    
    def open_categorize_window(self):
        """Open the categorize transactions window"""
        if self.categorize_window is None or not self.categorize_window.isVisible():
            self.categorize_window = CategorizeWindow(self)
            self.categorize_window.show()
        else:
            self.categorize_window.raise_()
            self.categorize_window.activateWindow()


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')  # Modern cross-platform style
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
