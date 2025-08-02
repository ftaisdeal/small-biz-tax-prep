# GUI Refactoring

## Overview
The GUI code has been refactored to improve maintainability and separation of concerns. The monolithic `main.py` file has been split into focused, single-responsibility modules.

## New Structure

### `/src/gui/main.py`
- **Purpose**: Application entry point
- **Responsibilities**: 
  - Initialize the PyQt6 application
  - Set application style
  - Launch the main window
  - Handle application lifecycle

### `/src/gui/main_window.py`
- **Purpose**: Main dashboard window
- **Responsibilities**:
  - Display financial summary (revenue, expenses, profit/loss)
  - Show category breakdown table
  - Handle window layout and styling
  - Manage main window interactions
  - Launch categorize window

### `/src/gui/categorize_window.py`
- **Purpose**: Transaction categorization interface
- **Responsibilities**:
  - Display transaction grid with dropdowns
  - Handle category assignment
  - Update database with category changes
  - Refresh parent window when changes are made

## Benefits of This Refactoring

1. **Single Responsibility Principle**: Each file has a clear, focused purpose
2. **Maintainability**: Easier to find and modify specific functionality
3. **Testability**: Individual components can be tested in isolation
4. **Reusability**: Window classes can be imported and used elsewhere
5. **Collaboration**: Multiple developers can work on different components simultaneously

## Future Enhancements

Consider further breaking down components:
- Extract the category breakdown table into a reusable widget
- Create a separate module for styling constants
- Add a base window class for common functionality
- Implement model-view separation for data handling

## Import Structure
```
main.py
├── main_window.py
│   ├── categorize_window.py
│   └── src.core.db
└── PyQt6 components
```

All modules properly handle the Python path setup to import from the project root.
