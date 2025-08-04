#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropdown Test")
        self.setGeometry(100, 100, 400, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create a simple dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItem("-- Select Category --")
        self.dropdown.addItems(["sales", "advertising", "office expense", "rent"])
        
        # Connect signal
        self.dropdown.currentIndexChanged.connect(self.on_selection)
        
        # Add label to show what was selected
        self.label = QLabel("Nothing selected")
        
        layout.addWidget(self.dropdown)
        layout.addWidget(self.label)
        
    def on_selection(self, index):
        if index > 0:
            selected = self.dropdown.itemText(index)
            self.label.setText(f"Selected: {selected}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
