import sqlite3
import os
import re

# Define your database path
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Function to normalize text (lowercase, trim spaces, clean commas)
def normalize_text(text):
    if not text or text.strip().lower() == 'no':
        return ''
    text = text.lower()
    text = re.sub(r'\s*,\s*', ',', text)         # Remove spaces around commas
    text = re.sub(r'\s+', ' ', text)             # Replace multiple spaces with one
    return text.strip()

# Fields to normalize in the database
FIELDS_TO_NORMALIZE = [
    "technicalSkills",
    "softSkills",
    "hackathons",
    "internships",
    "certifications",
    "projects",
    "experience_company",
    "experience_designation",
    "college",
    "location",
    "modeOfWork"
]

# Main function to normalize the profiles
def normalize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build SELECT query dynamically
    columns = ["id"] + FIELDS_TO_NORMALIZE
    select_query = f"SELECT {', '.join(columns)} FROM profiles"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for row in rows:
        user_id = row[0]
        values_to_normalize = row[1:]
        normalized_values = [normalize_text(field) for field in values_to_normalize]

        # Build the UPDATE query dynamically
        update_query = f"""
            UPDATE profiles
            SET {', '.join([f"{field} = ?" for field in FIELDS_TO_NORMALIZE])}
            WHERE id = ?
        """
        cursor.execute(update_query, (*normalized_values, user_id))

    conn.commit()
    conn.close()
    print("✅ Data normalization completed.")

if __name__ == "__main__":
    normalize_database()
