from flask import Flask, request, render_template
import sqlite3
import os
import PyPDF2
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection
DB_PATH = os.path.join(os.getcwd(), 'resumes.db')
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Create resumes table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        location TEXT,
        github TEXT,
        linkedin TEXT,
        skills TEXT,
        certifications TEXT,
        education TEXT,
        cgpa TEXT
    )
''')
conn.commit()

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

# Extract GitHub or LinkedIn links
def extract_link(keyword, text):
    pattern = rf"{keyword}[:\-]?\s*(https?://[^\s]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else "N/A"

# Main extraction logic
def extract_fields(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else "N/A"
    
    email_match = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match[0] if email_match else "N/A"

    github = extract_link("github", text)
    linkedin = extract_link("linkedin", text)

    location_match = re.findall(r"(Hyderabad|Bangalore|Chennai|Delhi|Mumbai|Pune|Kolkata)", text, re.IGNORECASE)
    location = location_match[0] if location_match else "N/A"

    # Skills extraction
    skills = "N/A"
    for i, line in enumerate(lines):
        if "skill" in line.lower():
            collected = []
            for j in range(i+1, min(i+6, len(lines))):
                if not any(kw in lines[j].lower() for kw in ["education", "experience", "project"]):
                    collected.append(lines[j])
            skills = " | ".join(collected)
            break

    # Certifications extraction
    certifications = "N/A"
    for i, line in enumerate(lines):
        if "certification" in line.lower():
            cert_lines = []
            for j in range(i+1, min(i+4, len(lines))):
                if not any(kw in lines[j].lower() for kw in ["education", "project"]):
                    cert_lines.append(lines[j])
            certifications = " | ".join(cert_lines)
            break

    # Education
    education_lines = []
    for i, line in enumerate(lines):
        if "education" in line.lower():
            for j in range(i+1, min(i+6, len(lines))):
                if lines[j].strip():
                    education_lines.append(lines[j].strip())
            break
    education = " | ".join(education_lines) if education_lines else "N/A"

    # CGPA
    cgpa_match = re.findall(r"(?:CGPA|SGPA)[:\-]?\s*(\d\.\d{1,2})", text)
    cgpa = cgpa_match[0] if cgpa_match else "N/A"

    return {
        "name": name,
        "email": email,
        "location": location,
        "github": github,
        "linkedin": linkedin,
        "skills": skills.strip(),
        "certifications": certifications.strip(),
        "education": education.strip(),
        "cgpa": cgpa
    }

# Insert extracted data into DB
def insert_into_db(data):
    c.execute('''
        INSERT INTO resumes (name, email, location, github, linkedin, skills, certifications, education, cgpa)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['email'], data['location'], data['github'],
        data['linkedin'], data['skills'], data['certifications'],
        data['education'], data['cgpa']
    ))
    conn.commit()

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    data = None

    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            text = extract_text_from_pdf(path)
            data = extract_fields(text)
            insert_into_db(data)

    return render_template('resume.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
