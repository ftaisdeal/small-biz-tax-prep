import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QScrollArea, 
                             QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.db import Database
from src.gui.categorize_window import CategorizeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.categorize_window = None
        self.setup_ui()
        self.refresh_totals()
        
    def setup_ui(self):
        self.setWindowTitle("Small Biz Tax Prep")
        
        # Set window size
        window_width = 800
        window_height = 800
        
        # Get screen geometry to center the window
        screen = self.screen().availableGeometry()
        screen_width = screen.width()
        
        # Calculate x position to center horizontally, y position 100px from top
        x = (screen_width - window_width) // 2
        y = 100
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Create central widget and main layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title label
        title_label = QLabel("Small Biz Tax Prep")
        title_font = QFont("Arial", 32)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #444; margin-top: 10px; margin-bottom: 6px;")
        layout.addWidget(title_label)
        
        # Subtitle label
        subtitle_label = QLabel("Current Profit / Loss")
        subtitle_font = QFont("Arial", 18, QFont.Weight.Bold)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #000; margin-top: 40px; margin-bottom: 0px;")
        layout.addWidget(subtitle_label)
        
        # Financial summary labels
        summary_font = QFont("Arial", 14, QFont.Weight.Bold)
        
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
        
        # Category breakdown section
        breakdown_title = QLabel("Expenses by Category")
        breakdown_title_font = QFont("Arial", 18, QFont.Weight.Bold)
        breakdown_title.setFont(breakdown_title_font)
        breakdown_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        breakdown_title.setStyleSheet("margin-top: 40px; margin-bottom: 0px;")
        layout.addWidget(breakdown_title)
        
        # Create scroll area for category breakdown
        self.breakdown_scroll = QScrollArea()
        self.breakdown_scroll.setMaximumHeight(250)
        self.breakdown_scroll.setMinimumHeight(150)
        self.breakdown_scroll.setWidgetResizable(True)
        self.breakdown_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.breakdown_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.breakdown_scroll.setStyleSheet("border: none; background-color: transparent;")
        
        # Create widget for breakdown content
        self.breakdown_widget = QWidget()
        self.breakdown_layout = QVBoxLayout(self.breakdown_widget)
        self.breakdown_layout.setSpacing(2)
        self.breakdown_layout.setContentsMargins(5, 5, 5, 5)
        self.breakdown_scroll.setWidget(self.breakdown_widget)
        
        layout.addWidget(self.breakdown_scroll)
        
        # Add some spacing
        layout.addStretch()
        
        # Categorize button
        categorize_btn = QPushButton("categorize transactions")
        button_font = QFont("Arial", 12)
        categorize_btn.setFont(button_font)
        categorize_btn.setFixedSize(150, 40)
        categorize_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b8;
                color: black;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8c8;
            }
            QPushButton:pressed {
                background-color: #8a8;
            }
        """)
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
        
        # Update category breakdown
        self.refresh_category_breakdown()
    
    def refresh_category_breakdown(self):
        """Refresh the category breakdown section"""
        # Clear existing breakdown
        for i in reversed(range(self.breakdown_layout.count())): 
            child = self.breakdown_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get expense data by category
        category_expenses = self.db.get_expense_totals_by_category()
        
        if not category_expenses:
            no_data_label = QLabel("No categorized expenses found")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #666; font-style: italic; padding: 4px;")
            self.breakdown_layout.addWidget(no_data_label)
            return
        
        # Create category expense entries
        category_font = QFont("Arial", 14)
        for i, (category_name, total_amount) in enumerate(category_expenses):
            # Create a container widget for each row
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(0)  # Remove default spacing
            
            # Category name label (right-aligned)
            name_label = QLabel(category_name.title())
            name_label.setFont(category_font)
            name_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            name_label.setStyleSheet("color: #333; border: none; background: transparent; font-weight: bold; font-size: 14px; margin-right: 4px;")
            name_label.setFixedWidth(150)  # Fixed width for consistent column alignment
            
            # Amount label (right-aligned)
            amount_label = QLabel(f"${abs(total_amount):,.2f}")
            amount_label.setFont(category_font)
            amount_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            amount_label.setStyleSheet("color: #333; border: none; background: transparent; font-size: 14px;")
            amount_label.setFixedWidth(100)  # Fixed width for consistent column alignment
            
            # Add labels to row layout with no extra spacing
            row_layout.addStretch()  # Left stretch to center the table
            row_layout.addWidget(name_label)
            row_layout.addWidget(amount_label)
            row_layout.addStretch()  # Right stretch to center the table
            
            self.breakdown_layout.addWidget(row_widget)
        
        # Add stretch at the end to push items to the top
        self.breakdown_layout.addStretch()
    
    def open_categorize_window(self):
        """Open the categorize transactions window"""
        if self.categorize_window is None or not self.categorize_window.isVisible():
            self.categorize_window = CategorizeWindow(self)
            self.categorize_window.show()
        else:
            self.categorize_window.raise_()
            self.categorize_window.activateWindow()
