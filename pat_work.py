from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Define absolute path to the database
DB_PATH = r"C:\Users\APPLE\OneDrive\Desktop\Link_squad\database.db"
print("Using DB file at:", os.path.abspath(DB_PATH))  # Debug print (optional)

@app.route('/')
def home():
    return '<h2>Welcome! Go to <a href="/find_partners">Find a Partner</a> to start.</h2>'

@app.route('/find_partners', methods=['GET', 'POST'])
def find_partners():
    matches = []

    if request.method == 'POST':
        user_input = {
            'skills': [s.strip().lower() for s in request.form.get('technicalSkills', '').split(',')],
            'location': request.form.get('location', '').lower(),
            'projects': request.form.get('projects', '').lower(),
            'college': request.form.get('college', '').lower(),
            'mode': request.form.get('mode', '').lower(),
            'internships': request.form.get('internships', '').lower()
        }

        # Connect using the absolute DB path
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, technicalSkills, location, projects, college, modeOfWork, internships FROM profiles")
        all_profiles = cursor.fetchall()
        conn.close()

        for profile in all_profiles:
            name, email, skills, location, projects, college, mode_of_work, internships = map(str.lower, map(str, profile))
            profile_skills = [s.strip() for s in skills.split(',')]

            # Match if ANY of the user's skills partially match ANY profile skill
            skill_match = any(any(user_skill in ps for ps in profile_skills) for user_skill in user_input['skills'])

            if (
                skill_match and
                user_input['location'] in location and
                user_input['projects'] in projects and
                user_input['college'] in college and
                user_input['mode'] in mode_of_work and
                user_input['internships'] in internships
            ):
                matches.append({'name': name.title(), 'email': email})

    return render_template('find_partners.html', matches=matches)


if __name__ == '__main__':
    app.run(debug=True)