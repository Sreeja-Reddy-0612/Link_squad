from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create the database and table
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        linkedin TEXT,
        github TEXT,
        technicalSkills TEXT,
        softSkills TEXT,
        hackathons TEXT,
        internships TEXT,
        certifications TEXT,
        projects TEXT,
        experience_company TEXT,
        experience_designation TEXT,
        experience_years TEXT,
        college TEXT,
        location TEXT,
        modeOfWork TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def form():
    submitted = False
    if request.method == 'POST':
        # Collect data
        data = (
            request.form.get('name'),
            request.form.get('email'),
            request.form.get('linkedin'),
            request.form.get('github'),
            request.form.get('technicalSkills'),
            request.form.get('softSkills'),
            request.form.get('hackathons'),
            request.form.get('internships'),
            request.form.get('certifications'),
            request.form.get('projects'),
            request.form.get('experience_company'),
            request.form.get('experience_designation'),
            request.form.get('experience_years'),
            request.form.get('college'),
            request.form.get('location'),
            request.form.get('modeOfWork'),
        )

        # Insert into database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO profiles (
                name, email, linkedin, github, technicalSkills, softSkills,
                hackathons, internships, certifications, projects,
                experience_company, experience_designation, experience_years,
                college, location, modeOfWork
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()

        submitted = True

    return render_template('home_work.html', submitted=submitted)



    

if __name__ == '__main__':
    init_db()
    app.run(debug=True)