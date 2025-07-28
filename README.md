# Expense Tracker

A comprehensive expense tracking system with 1099 tax reporting capabilities.

## Features

- Import transactions from QIF files
- Categorize expenses
- Track 1099-reportable payments to vendors
- Generate tax reports
- SQLite database backend

## Directory Structure

```
finances/
├── config/           # Configuration files
├── database/         # Database files and schema
│   ├── schema/       # SQL schema files
│   └── migrations/   # Database migrations
├── src/              # Source code
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   ├── utils/        # Utility functions
│   └── cli/          # Command-line interfaces
├── gui/              # GUI components
├── tests/            # Unit tests
├── scripts/          # Setup and maintenance scripts
├── data/             # Data files
│   ├── imports/      # Import files (QIF, CSV)
│   ├── exports/      # Generated reports
│   └── backups/      # Database backups
└── docs/             # Documentation
```

## Setup

1. Run the database setup script:
   ```bash
   python scripts/setup_database.py
   ```

2. Import your financial data:
   ```bash
   python src/cli/import_qif.py your_file.qif
   ```

3. Categorize transactions:
   ```bash
   python src/cli/categorize.py
   ```

## Usage

See `docs/usage.md` for detailed usage instructions.
