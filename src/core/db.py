import sqlite3

DB_PATH = "database/expense_tracker.db"

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_categories(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories")
            return cursor.fetchall()

    def fetch_transactions(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, transaction_date, payee_description, amount FROM transactions")
            return cursor.fetchall()

    def fetch_transaction_category(self, transaction_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id FROM transaction_categories WHERE transaction_id = ?", (transaction_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def update_transaction_category(self, transaction_id, category_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transaction_categories WHERE transaction_id = ?", (transaction_id,))
            if category_id is not None:
                cursor.execute("INSERT INTO transaction_categories (transaction_id, category_id) VALUES (?, ?)", (transaction_id, category_id))
            conn.commit()

    def get_total_categorized_expenses(self):
        """Calculate the total amount of all categorized transactions (expenses)"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(t.amount) 
                FROM transactions t
                INNER JOIN transaction_categories tc ON t.id = tc.transaction_id
                WHERE t.amount < 0
            """)
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

    def get_total_categorized_revenue(self):
        """Calculate the total amount of transactions categorized as 'income'"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(t.amount) 
                FROM transactions t
                INNER JOIN transaction_categories tc ON t.id = tc.transaction_id
                INNER JOIN categories c ON tc.category_id = c.id
                WHERE c.name = 'income'
            """)
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

    def get_expense_totals_by_category(self):
        """Get the total expenses grouped by category (excluding income)"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.name, SUM(t.amount) as total
                FROM transactions t
                INNER JOIN transaction_categories tc ON t.id = tc.transaction_id
                INNER JOIN categories c ON tc.category_id = c.id
                WHERE t.amount < 0 AND c.name != 'income'
                GROUP BY c.id, c.name
                ORDER BY 
                    CASE c.name
                        WHEN 'contract labor' THEN 1
                        WHEN 'rent' THEN 2
                        WHEN 'advertising' THEN 3
                        WHEN 'supplies' THEN 4
                        WHEN 'office expense' THEN 5
                        WHEN 'no category' THEN 6
                        ELSE 7
                    END
            """)
            return cursor.fetchall()
