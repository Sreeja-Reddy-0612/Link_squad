import sqlite3

# Connect to your database
conn = sqlite3.connect("link_squad/database.db")
cursor = conn.cursor()

# Print schema (column names and types)
print("📌 Table Schema:")
cursor.execute("PRAGMA table_info(users)")
schema = cursor.fetchall()
for col in schema:
    print(f" - {col[1]} ({col[2]})")

print("\n📌 Sample Data:")
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

if not rows:
    print("❌ No data found in the 'users' table.")
else:
    for row in rows:
        print(row)

conn.close()
