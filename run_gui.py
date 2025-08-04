#!/usr/bin/env python3
"""
Launch script for the Preppy PyQt6 GUI application.
This script ensures the correct Python environment is used.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main application
from src.gui.main import main

if __name__ == "__main__":
    main()
