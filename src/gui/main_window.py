import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QScrollArea, 
                             QFrame, QComboBox)
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
        self.current_tax_year = 2025  # Current tax year
        self.setup_ui()
        self.refresh_totals()
        
    def setup_ui(self):
        self.setWindowTitle("Schedule C Prep")
        
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
        layout.setContentsMargins(20, 60, 20, 20)
        layout.setSpacing(10)
        
        # Create summary container with gray border and background
        summary_container = QFrame()
        summary_container.setFixedWidth(600)  # Set fixed width to 600 pixels
        summary_container.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #aaaaaa;
                border-radius: 8px;
            }
            QFrame QLabel, QFrame QScrollArea, QFrame QWidget {
                border: none;
            }
        """)
        summary_layout = QVBoxLayout(summary_container)
        summary_layout.setContentsMargins(40, 40, 40, 40)
        summary_layout.setSpacing(10)
        
        # Subtitle label
        subtitle_label = QLabel("Schedule C Prep")
        subtitle_font = QFont("Verdana", 38)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #888; margin-top: 20px; margin-bottom: 16px;")
        summary_layout.addWidget(subtitle_label)
        
        # Year selector dropdown
        year_selector_layout = QHBoxLayout()
        year_selector_layout.addStretch()
        
        self.year_combo = QComboBox()
        self.year_combo.addItem("Current Tax Year (2025)", 2025)
        self.year_combo.addItem("Previous Tax Year (2024)", 2024)
        self.year_combo.setCurrentIndex(0)  # Default to current tax year
        combo_font = QFont("Verdana", 12)
        self.year_combo.setFont(combo_font)
        self.year_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: #e8e8e8;
                color: black;
                min-width: 180px;
            }
            QComboBox:hover {
                border: 1px solid #999;
                background-color: #ddd;
            }
            QComboBox:focus {
                border: 1px solid #2196F3;
                outline: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                selection-background-color: #e3f2fd;
                selection-color: black;
                outline: none;
            }
        """)
        self.year_combo.currentIndexChanged.connect(self.on_year_changed)
        year_selector_layout.addWidget(self.year_combo)
        
        year_selector_layout.addStretch()
        summary_layout.addLayout(year_selector_layout)
        
        # Financial summary labels
        summary_font = QFont("Verdana", 14)
        
        self.revenue_label = QLabel()
        self.revenue_label.setFont(summary_font)
        self.revenue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.revenue_label)
        
        self.expenses_label = QLabel()
        self.expenses_label.setFont(summary_font)
        self.expenses_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.expenses_label)
        
        self.profit_loss_label = QLabel()
        self.profit_loss_label.setFont(summary_font)
        self.profit_loss_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.profit_loss_label)
        
        # Category breakdown section
        breakdown_title = QLabel("Expenses by Category")
        breakdown_title_font = QFont("Verdana", 16, QFont.Weight.Bold)
        breakdown_title.setFont(breakdown_title_font)
        breakdown_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        breakdown_title.setStyleSheet("margin-top: 40px; margin-bottom: 0px;")
        summary_layout.addWidget(breakdown_title)
        
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
        self.breakdown_layout.setContentsMargins(5, 0, 5, 5)
        self.breakdown_scroll.setWidget(self.breakdown_widget)
        
        summary_layout.addWidget(self.breakdown_scroll)
        
        # Add the summary container to the main layout with centering
        container_layout = QHBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(summary_container)
        container_layout.addStretch()
        layout.addLayout(container_layout)
        
        # Add spacing between summary and buttons
        layout.addSpacing(20)
        
        # Buttons section
        button_font = QFont("Verdana", 12)
        
        # Import button
        import_btn = QPushButton("import")
        import_btn.setFont(button_font)
        import_btn.setFixedSize(90, 36)
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        import_btn.clicked.connect(self.open_import_dialog)
        
        # Categorize button
        categorize_btn = QPushButton("categorize")
        categorize_btn.setFont(button_font)
        categorize_btn.setFixedSize(90, 36)
        categorize_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        categorize_btn.clicked.connect(self.open_categorize_window)
        
        # Review button
        review_btn = QPushButton("review")
        review_btn.setFont(button_font)
        review_btn.setFixedSize(90, 36)
        review_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        review_btn.clicked.connect(self.open_review_dialog)
        
        # Print button
        print_btn = QPushButton("print")
        print_btn.setFont(button_font)
        print_btn.setFixedSize(90, 36)
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        print_btn.clicked.connect(self.open_print_dialog)
        
        # Center the buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(import_btn)
        button_layout.addSpacing(20)  # Space between buttons
        button_layout.addWidget(categorize_btn)
        button_layout.addSpacing(20)  # Space between buttons
        button_layout.addWidget(review_btn)
        button_layout.addSpacing(20)  # Space between buttons
        button_layout.addWidget(print_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def on_year_changed(self):
        """Handle year selection change"""
        selected_year = self.year_combo.currentData()
        self.current_tax_year = selected_year
        
        # Refresh all data for the selected year
        self.refresh_totals()
    
    def refresh_totals(self):
        """Refresh the revenue, expenses, and profit/loss display"""
        total_revenue = self.db.get_total_categorized_revenue(self.current_tax_year)
        total_expenses = self.db.get_total_categorized_expenses(self.current_tax_year)
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
        category_expenses = self.db.get_expense_totals_by_category(self.current_tax_year)
        
        if not category_expenses:
            no_data_label = QLabel("No categorized expenses found")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #666; font-style: italic; padding: 4px;")
            self.breakdown_layout.addWidget(no_data_label)
            return
        
        # Create category expense entries
        category_font = QFont("Verdana", 14)
        for i, (category_name, total_amount) in enumerate(category_expenses):
            # Create a container widget for each row
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(0)  # Remove default spacing
            
            # Combined category and amount label
            combined_text = f"{category_name.title()}: ${abs(total_amount):,.2f}"
            combined_label = QLabel(combined_text)
            combined_label.setFont(category_font)
            combined_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            combined_label.setStyleSheet("color: #333; border: none; background: transparent; font-size: 14px;")
            
            # Center the combined label
            row_layout.addStretch()  # Left stretch to center
            row_layout.addWidget(combined_label)
            row_layout.addStretch()  # Right stretch to center
            
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
    
    def open_import_dialog(self):
        """Open the import file dialog for QIF and CSV files"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        import os
        
        # Set default directory to project's data/imports folder
        default_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'imports')
        
        # Open file dialog to select QIF or CSV file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Import",
            default_dir,
            "Financial Files (*.qif *.csv);;QIF Files (*.qif);;CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                # Determine file type by extension
                file_ext = os.path.splitext(file_path)[1].lower()
                
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cli'))
                
                if file_ext == '.qif':
                    # Import QIF file
                    from import_qif import qif_to_sql
                    sql_statements = qif_to_sql(file_path)
                    
                elif file_ext == '.csv':
                    # Import CSV file
                    from import_csv import csv_to_sql
                    sql_statements = csv_to_sql(file_path)
                    
                else:
                    # Try to detect format by content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                    
                    if first_line.startswith('!Type:'):
                        # QIF format detected
                        from import_qif import qif_to_sql
                        sql_statements = qif_to_sql(file_path)
                    elif ',' in first_line:
                        # CSV format detected
                        from import_csv import csv_to_sql
                        sql_statements = csv_to_sql(file_path)
                    else:
                        raise ValueError("Unsupported file format. Please use QIF or CSV files.")
                
                # Execute the SQL statements using the database
                for statement in sql_statements.split('\n'):
                    if statement.strip():
                        self.db.execute_sql(statement)
                
                # Refresh the totals after import
                self.refresh_totals()
                
                QMessageBox.information(self, "Import Complete", f"Successfully imported transactions from {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import file: {str(e)}")
    
    def open_review_dialog(self):
        """Open the review dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Review", "Review functionality will be implemented here.")
    
    def open_print_dialog(self):
        """Open the print dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Print", "Print functionality will be implemented here.")
