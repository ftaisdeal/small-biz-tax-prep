import csv
import re
from datetime import datetime


def parse_csv_date(date_str):
    """Parse various date formats commonly found in CSV files"""
    date_formats = [
        '%m/%d/%Y',    # MM/DD/YYYY
        '%Y-%m-%d',    # YYYY-MM-DD
        '%m/%d/%y',    # MM/DD/YY
        '%d/%m/%Y',    # DD/MM/YYYY
        '%Y/%m/%d',    # YYYY/MM/DD
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If no format matches, return original string
    return date_str.strip()


def clean_amount(amount_str):
    """Clean and convert amount string to float"""
    # Remove currency symbols, parentheses, and spaces
    cleaned = re.sub(r'[\$,\s()]', '', amount_str)
    
    # Handle negative amounts in parentheses
    if '(' in amount_str and ')' in amount_str:
        cleaned = '-' + cleaned
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def csv_to_sql(csv_file_path, account_id=1):
    """
    Convert CSV file to SQL INSERT statements for transactions
    
    Expected CSV format (with or without headers):
    Date, Description/Payee, Amount
    or
    Date, Description/Payee, Debit, Credit
    """
    
    sql_statements = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Try to detect delimiter
        sample = file.read(1024)
        file.seek(0)
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        reader = csv.reader(file, delimiter=delimiter)
        
        # Skip header row if it exists
        first_row = next(reader, None)
        if first_row and any(header.lower() in ['date', 'description', 'amount', 'payee'] 
                           for header in first_row):
            # This is likely a header row, continue to data
            pass
        else:
            # This is data, process it
            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)
        
        for row in reader:
            if len(row) < 3:
                continue  # Skip rows with insufficient data
            
            date_str = row[0]
            description = row[1].replace("'", "''")  # Escape single quotes for SQL
            
            # Handle different amount formats
            if len(row) == 3:
                # Single amount column
                amount = clean_amount(row[2])
            elif len(row) >= 4:
                # Separate debit/credit columns
                debit = clean_amount(row[2]) if row[2] else 0.0
                credit = clean_amount(row[3]) if row[3] else 0.0
                amount = credit - debit  # Credit is positive, debit is negative
            else:
                continue
            
            # Parse date
            parsed_date = parse_csv_date(date_str)
            
            # Create SQL INSERT statement
            sql = f"INSERT INTO transactions (account_id, transaction_date, payee_description, amount, tax_year) VALUES ({account_id}, '{parsed_date}', '{description}', {amount}, {datetime.now().year});"
            sql_statements.append(sql)
    
    return '\n'.join(sql_statements)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python import_csv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    sql_output = csv_to_sql(csv_file)
    print(sql_output)