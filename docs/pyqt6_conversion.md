# PyQt6 Conversion Guide

## Overview
This project has been successfully converted from Tkinter to PyQt6. The conversion provides several benefits:

### Benefits of PyQt6 over Tkinter
- **Modern, Professional Look**: PyQt6 provides a much more modern and professional appearance
- **Better Cross-Platform Support**: Native look and feel on each operating system
- **Enhanced Performance**: Better rendering and responsiveness
- **Rich Widget Set**: More advanced widgets and customization options
- **Better Layout Management**: More flexible and powerful layout systems
- **Improved Styling**: Better theming and styling capabilities

## Key Changes Made

### 1. Dependencies
- Added `PyQt6>=6.4.0` to `requirements.txt`
- Removed dependency on Tkinter (which was built-in)

### 2. Code Structure
The GUI has been completely rewritten using object-oriented PyQt6 patterns:

#### Main Classes
- **`MainWindow`**: The main application window (replaces the root Tkinter window)
- **`CategorizeWindow`**: The transaction categorization window (replaces the Toplevel window)

#### Key Improvements
- **Better Separation of Concerns**: Each window is now a proper class with clear responsibilities
- **Improved Event Handling**: PyQt6's signal-slot mechanism provides better event handling
- **Enhanced Layout Management**: Uses QGridLayout and QVBoxLayout for better responsive design
- **Professional Styling**: CSS-like styling capabilities for a more polished look

### 3. Feature Equivalence
All original functionality has been preserved:
- ✅ Main dashboard with revenue, expenses, and profit/loss display
- ✅ Transaction categorization window with scrollable list
- ✅ Live updating of categories when dropdown values change
- ✅ Alternating row colors for better readability
- ✅ Real-time refresh of financial totals
- ✅ Proper window sizing and positioning

### 4. Visual Improvements
- **Header Row**: Better styled header with gray background and borders
- **Data Rows**: Improved alternating row colors with proper borders
- **Typography**: Better font management and sizing
- **Spacing**: More consistent padding and margins
- **Responsive Design**: Better column sizing and window resizing behavior

## Running the Application

### Method 1: Using the Launch Script
```bash
python run_gui.py
```

### Method 2: Using VS Code Tasks
1. Open the Command Palette (Cmd+Shift+P)
2. Type "Tasks: Run Task"
3. Select "Run PyQt6 GUI"

### Method 3: Direct Python Execution
```bash
.venv/bin/python src/gui/main.py
```

## Development Notes

### Virtual Environment
The project now uses a Python virtual environment (`.venv`) to manage dependencies. This ensures:
- Consistent package versions
- Isolation from system Python packages
- Easier deployment and distribution

### Code Organization
The PyQt6 version follows better object-oriented practices:
- Each window is a separate class
- Clear separation between UI setup and business logic
- Better error handling and resource management

### Future Enhancements
The PyQt6 foundation makes it easier to add:
- Menu bars and toolbars
- Status bars
- Keyboard shortcuts
- Advanced styling and themes
- Icons and images
- More complex layouts
- Data visualization widgets

## Migration Notes
If you need to revert to Tkinter for any reason, the original Tkinter code structure was:
- Functional programming approach
- Global variables for UI elements
- Manual callback management
- Canvas-based scrolling

The PyQt6 version is significantly more maintainable and extensible for future development.
