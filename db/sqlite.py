import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "fruits.db"

def init_database():
    """Initialize the database and create the fruits table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_fruit(fruit_name):
    """Insert a fruit name into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO fruits (name) VALUES (?)', (fruit_name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def insert_fruits(fruit_names):
    """Insert multiple fruit names into the database."""
    init_database()
    results = []
    for fruit in fruit_names:
        success = insert_fruit(fruit)
        results.append((fruit, success))
    return results

def get_all_fruits():
    """Retrieve all fruits from the database."""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, created_at FROM fruits ORDER BY created_at')
    fruits = cursor.fetchall()
    conn.close()
    return fruits

def delete_fruit(fruit_name):
    """Delete a fruit from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fruits WHERE name = ?', (fruit_name,))
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()
    return affected_rows > 0

def clear_all_fruits():
    """Clear all fruits from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fruits')
    conn.commit()
    conn.close()