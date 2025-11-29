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
    
    Expected CSV format:
    Posted Date, Reference Number, Payee, Address, Amount
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
        if first_row and any(header.lower() in ['date', 'reference', 'payee', 'address', 'amount'] 
                           for header in first_row):
            # This is likely a header row, continue to data
            pass
        else:
            # This is data, process it
            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)
        
        for row in reader:
            if len(row) < 5:
                continue  # Skip rows with insufficient data
            
            posted_date = row[0]
            reference_number = row[1].replace("'", "''") if row[1] else ""
            payee = row[2].replace("'", "''") if row[2] else ""
            address = row[3].replace("'", "''") if row[3] else ""
            amount = clean_amount(row[4])
            
            # Parse date
            parsed_date = parse_csv_date(posted_date)
            
            # Create SQL INSERT statement mapping to database schema
            sql = f"INSERT INTO transactions (account_id, transaction_date, reference_number, payee_description, address_info, amount, note, tax_year) VALUES ({account_id}, '{parsed_date}', '{reference_number}', '{payee}', '{address}', {amount}, NULL, {datetime.now().year});"
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