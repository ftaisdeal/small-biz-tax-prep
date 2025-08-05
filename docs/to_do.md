# To Do
- buttons: import | categorize | profit/loss
- Add a button to the dashboard for profit/loss
- Add UI and functionality to select a time period to show income and expenses
- Import all of the other .qif files
- Add all the code for 1099 forms
- Make the whole thing look really good
- Make the system an app that can be started from an icon

## Notes:
- To open tax_prep.sqbpro:
Press Cmd+Shift+P
Type "Tasks: Run Task"
Select "Open in DB Browser"

- Use: python scripts/setup_database.py to recreate database

- Correct INSERT syntax: INSERT INTO accounts (account_type, account_name) VALUES ('checking', 'B of A checking');