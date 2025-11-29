import re
from datetime import datetime

def parse_qif_date(qif_date):
    """
    Converts QIF date formats (like MM/DD'YY or MM/DD/YYYY, possibly with different separators)
    to YYYY-MM-DD format.
    """
    # Remove whitespace
    qif_date = qif_date.strip()
    # QIF date formats can be M/D'YY, MM/DD'YY, MM/DD/YYYY, and use either / or - as separator
    # Examples: 7/18'25, 07/18'25, 07/18/2025, 07-18-2025
    # Try parsing accordingly
    # Replace ' with /
    qif_date = qif_date.replace("'", "/")
    # Try different formats
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            d = datetime.strptime(qif_date, fmt)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # If parsing fails, return as is
    return qif_date

def qif_to_sql(qif_filename):
    with open(qif_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    current_entry = {}
    account_id = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("!Type:"):
            type_val = line.split(":", 1)[1].strip()
            if type_val.lower() == "bank":
                account_id = 1
            elif type_val.lower() == "ccard":
                account_id = 2
            else:
                account_id = None  # Unknown type, skip
            continue

        if line == "^":  # End of transaction entry
            if current_entry and account_id:
                # Prepare SQL statement for this entry - specify columns explicitly
                sql = (
                    "INSERT INTO transactions (account_id, transaction_date, reference_number, payee_description, address_info, amount, note) VALUES ("
                    "{account_id}, '{date}', {ref}, {payee}, {addr}, {amount}, NULL)"
                )
                # Ensure required fields
                transaction_date = parse_qif_date(current_entry.get("D", ""))
                amount = current_entry.get("T", "0.00").replace(",", "")  # Remove commas from amount
                # Optional fields
                reference_number = f"'{current_entry.get('N', '')}'" if current_entry.get("N") else "NULL"
                payee_description = f"'{current_entry.get('P', '')}'" if current_entry.get("P") else "NULL"
                address_info = f"'{current_entry.get('A', '')}'" if current_entry.get("A") else "NULL"

                statement = sql.format(
                    account_id=account_id,
                    date=transaction_date,
                    ref=reference_number,
                    payee=payee_description,
                    addr=address_info,
                    amount=amount
                )
                entries.append(statement)
            current_entry = {}
            continue

        # Transaction field prefixes per QIF spec:
        # D: Date, T: Amount, N: Reference/Num, P: Payee, M: Memo, A: Address, C: Cleared status
        if len(line) > 1 and line[0] in "DTNPMABC":
            key = line[0]
            val = line[1:].strip()
            # If address, allow multiline
            if key == "A":
                if "A" in current_entry:
                    current_entry["A"] += " " + val
                else:
                    current_entry["A"] = val
            else:
                current_entry[key] = val

    return "\n".join(entries)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python qif_to_sql.py <filename.qif>")
        sys.exit(1)
    qif_file = sys.argv[1]
    sql_statements = qif_to_sql(qif_file)
    print(sql_statements)