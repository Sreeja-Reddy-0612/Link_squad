import sqlite3
import os

# Path to your database file
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def list_columns(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"📋 Columns in '{table_name}':")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")  # col[1] = column name, col[2] = data type
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

# Change 'profiles' to your actual table name
list_columns("profiles")
