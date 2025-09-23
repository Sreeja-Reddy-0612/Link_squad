import sqlite3
import os

# Absolute path to current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file directly in current folder
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Check existence
if not os.path.exists(DB_PATH):
    print("Database file not found at:", DB_PATH)
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM profiles")
        rows = cursor.fetchall()

        if rows:
            print("Profiles in the database:\n")
            for row in rows:
                print(row)
        else:
            print("No profiles found in the database.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    conn.close()
