import sqlite3

DB_NAME = "database/expense_tracker.db"

def fetch_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def main():
    categories = fetch_categories()
    print("Original categories:", [cat[1] for cat in categories])

    # Reorder categories to put "other expenses", "income", "no category" at the end
    special_categories = ["other expenses", "income", "no category"]
    regular_categories = [cat[1] for cat in categories if cat[1] not in special_categories]
    final_categories = [cat[1] for cat in categories if cat[1] in special_categories]
    
    print("Regular categories:", regular_categories)
    print("Final categories found:", final_categories)
    
    # Ensure the final categories appear in the desired order
    ordered_final = []
    for special_cat in special_categories:
        if special_cat in final_categories:
            ordered_final.append(special_cat)
    
    category_choices = ["unassigned"] + regular_categories + ordered_final
    print("Final category choices order:", category_choices)

if __name__ == "__main__":
    main()
