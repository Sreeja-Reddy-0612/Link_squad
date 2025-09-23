from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def search_profiles():
    results = []

    if request.method == 'POST':
        # Get input values from form
        name = request.form.get('name', '').strip()
        skills = request.form.get('skills', '').strip()
        soft_skills = request.form.get('soft_skills', '').strip()
        hackathons = request.form.get('hackathons', '').strip()
        internships = request.form.get('internships', '').strip()
        certifications = request.form.get('certifications', '').strip()
        projects = request.form.get('projects', '').strip()
        roles = request.form.get('roles', '').strip()
        experience = request.form.get('experience', '').strip()
        college = request.form.get('college', '').strip()
        location = request.form.get('location', '').strip()
        platforms = request.form.get('platforms', '').strip()

        query = "SELECT name, email FROM users WHERE 1=1"
        values = []

        def add_like_clause(field, value):
            nonlocal query, values
            for item in value.split(','):
                item = item.strip()
                if item:
                    query += f" AND {field} LIKE ?"
                    values.append(f"%{item}%")

        if name:
            query += " AND name LIKE ?"
            values.append(f"%{name}%")

        add_like_clause("skills", skills)
        add_like_clause("soft_skills", soft_skills)
        add_like_clause("hackathons", hackathons)
        add_like_clause("internships", internships)
        add_like_clause("certifications", certifications)
        add_like_clause("projects", projects)
        add_like_clause("roles", roles)
        add_like_clause("experience", experience)

        if college:
            query += " AND college LIKE ?"
            values.append(f"%{college}%")
        if location:
            query += " AND location LIKE ?"
            values.append(f"%{location}%")
        if platforms:
            query += " AND platforms = ?"
            values.append(platforms)

        conn = sqlite3.connect('link_sqard/database.db')
        cursor = conn.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        conn.close()

    return render_template('open_to_work.html', profiles=results)
