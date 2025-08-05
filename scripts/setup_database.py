#!/usr/bin/env python3
"""
Database setup script
"""
import sqlite3
import os
from pathlib import Path

def setup_database():
    """Create and initialize the expense tracker database"""
    
    # Define paths
    project_root = Path(__file__).parent.parent
    db_path = project_root / "database" / "tax_prep.db"
    schema_dir = project_root / "database" / "schema"
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute schema files in order
        schema_files = [
            "01_create_tables.sql",
            "02_create_views.sql", 
            "03_insert_reference_data.sql",
            "04_create_indexes.sql"
        ]
        
        for sql_file in schema_files:
            file_path = schema_dir / sql_file
            if file_path.exists():
                print(f"Executing {sql_file}...")
                with open(file_path, 'r') as f:
                    sql_content = f.read()
                    cursor.executescript(sql_content)
            else:
                print(f"Warning: {sql_file} not found")
        
        conn.commit()
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
