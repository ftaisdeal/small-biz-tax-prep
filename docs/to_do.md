# To Do
- Modify categorize.py to show only those transactions that have not been assigned a category
- Create a new script that displays revenue and expenses by category for the current year
- Create a dashboard that provides a way of accessing the import and categorize functions
- Make the system an app that can be started from an icon
- Make the whole thing look really good
- Import all of the other .qif files
- Add all the tables and code for 1099 forms

## Completed:
- Reorganized project structure with proper directories
- Split SQL.sql into modular schema files
- Created database setup script
- Configured VS Code to open .sqbpro files with DB Browser for SQLite

## Notes:
- To open expense_tracker.sqbpro:
Press Cmd+Shift+P
Type "Tasks: Run Task"
Select "Open in DB Browser"
- Use: python scripts/setup_database.py to recreate database
- Correct INSERT syntax: INSERT INTO accounts (account_type, account_name) VALUES ('checking', 'B of A checking');