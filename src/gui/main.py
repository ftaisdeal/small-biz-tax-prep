import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')  # Modern cross-platform style
    
    # Set global font to Verdana
    font = QFont("Verdana", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
