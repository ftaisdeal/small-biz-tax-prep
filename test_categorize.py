#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the project root to Python path
sys.path.append('.')
from src.gui.main_window import MainWindow

def test_categorize_window():
    """Test opening the categorize window"""
    try:
        print("Creating main window...")
        main_window = MainWindow()
        main_window.show()
        
        print("Opening categorize window...")
        main_window.open_categorize_window()
        
        print("Categorize window opened successfully!")
        
        # Close after a short delay
        QTimer.singleShot(2000, main_window.close)
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_categorize_window()
    sys.exit(app.exec())
