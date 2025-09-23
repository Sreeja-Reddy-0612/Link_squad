from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import requests
from urllib.parse import quote
from git_linkedin import generate_linkedin_url, generate_github_url

app = Flask(__name__, static_folder='static', template_folder='templates')
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
GITHUB_SEARCH_ENGINE_ID = os.getenv("GITHUB_SEARCH_ENGINE_ID")
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
LINKEDIN_CX = os.getenv("LINKEDIN_CX")
DEVPOST_API_KEY = os.getenv("DEVPOST_API_KEY")
DEVPOST_CX_ID = os.getenv("DEVPOST_CX_ID")

# DB path (relative, not hardcoded)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "users.db"))

# ----------------- INIT DB -----------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# ----------------- AUTH ROUTES -----------------
@app.route('/')
def home():
    email = session.get('email')
    return render_template('index.html', email=email)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                flash('Email already registered.', 'error')
                return redirect(url_for('signup'))

            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()

            if user:
                session['email'] = email
                session['username'] = user[1]
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# ----------------- DEVPOST HACKATHON ROUTE -----------------
def get_devpost_events(query="upcoming hackathons site:devpost.com"):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={DEVPOST_API_KEY}&cx={DEVPOST_CX_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        events = []
        for item in results.get("items", []):
            events.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return events
    else:
        print("❌ Error fetching Devpost events:", response.status_code)
        return []

@app.route("/competitions")
def competitions():
    if 'email' in session:
        events = get_devpost_events()
        return render_template("competitions.html", events=events, email=session['email'])
    else:
        flash('Please login to view competitions.', 'warning')
        return redirect(url_for('login'))

# ----------------- RESUME / OPEN TO WORK -----------------
@app.route('/resume')
def resume():
    if 'email' in session:
        return render_template('resume.html', username=session.get('username'))
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/home_work')
def home_work():
    if 'email' in session:
        return render_template('home_work.html', username=session.get('username'))
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))

# ----------------- TEAMMATE FINDER -----------------
@app.route('/foot.html')
def foot():
    return render_template('foot.html')

@app.route('/git_linked.html', methods=['GET', 'POST'])
def git_linked():
    linkedin_url = ""
    github_url = ""

    if request.method == "POST":
        linkedin_data = { key: request.form.get(key, "") for key in [
            "skills", "jobTitle", "company", "experience", "college",
            "location", "softSkills", "hackathon", "internship", "date",
            "open_to_work", "other"
        ]}
        github_data = { key: request.form.get(key, "") for key in [
            "language", "projectName", "followers", "repoCount",
            "createdAfter", "size", "license"
        ]}
        linkedin_url = generate_linkedin_url(linkedin_data)
        github_url = generate_github_url(github_data)

    return render_template('git_linked.html', linkedin_url=linkedin_url, github_url=github_url)

# ----------------- LINKEDIN FORM -----------------
@app.route('/linkedin_form.html', methods=["GET", "POST"])
def linkedin_form():
    profiles = []
    user_input = { key: "" for key in [
        "skills", "job", "experience", "company", "location",
        "college", "soft_skills", "hackathons", "internships", "other", "open_to_work"
    ]}

    if request.method == "POST":
        for key in user_input:
            user_input[key] = request.form.get(key, "")
        query = build_search_query(user_input)
        profiles = search_linkedin_profiles(query)

    return render_template("linkedin_form.html", profiles=profiles, user_input=user_input)

# ----------------- GITHUB FORM -----------------
@app.route('/github_form.html', methods=['GET', 'POST'])
def github_form():
    results = []
    if request.method == 'POST':
        language = request.form.get('language')
        project_name = request.form.get('project_name')
        creation_date = request.form.get('creation_date')

        search_query = f'site:github.com "{project_name}" language:{language} created:>{creation_date}'
        api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={GITHUB_API_KEY}&cx={GITHUB_SEARCH_ENGINE_ID}"
        response = requests.get(api_url)
        data = response.json()
        if 'items' in data:
            results = data['items']

    return render_template('github_form.html', results=results)

# ----------------- LINKEDIN + GITHUB API -----------------
@app.route('/generate-linkedin', methods=['POST'])
def generate_linkedin():
    data = request.get_json()
    query_parts = []

    for key in ['skills', 'jobTitle', 'company', 'experience', 'college', 'location', 'softSkills', 'hackathon', 'internship', 'other']:
        value = data.get(key)
        if value:
            if "," in value:
                query_parts.append(" OR ".join(v.strip() for v in value.split(",")))
            else:
                query_parts.append(value.strip())
    if data.get("date"):
        query_parts.append(data["date"].strip())
    if data.get("open_to_work", "").lower() == "yes":
        query_parts.append("open to work")

    query = " AND ".join(query_parts)
    linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(query)}&origin=GLOBAL_SEARCH_HEADER"
    return jsonify({"linkedin_url": linkedin_url})

@app.route('/find_partners.html')
def find_partners():
    return render_template('find_partners.html')

@app.route('/search_form.html')
def search_form():
    return render_template('search_form.html')
@app.route('/generate-github', methods=['POST'])
def generate_github():
    data = request.get_json()
    query_parts = []

    if data.get("language"):
        query_parts.append(f'language:{data["language"]}')
    if data.get("projectName"):
        query_parts.append(data["projectName"])
    if data.get("followers"):
        query_parts.append(f'followers:>{data["followers"]}')
    if data.get("repoCount"):
        query_parts.append(f'repos:>{data["repoCount"]}')
    if data.get("createdAfter"):
        query_parts.append(f'created:>{data["createdAfter"]}')
    if data.get("size"):
        query_parts.append(f'size:>{data["size"]}')
    if data.get("license"):
        query_parts.append(f'license:{data["license"]}')

    github_query = "+".join(query_parts)
    github_url = f"https://github.com/search?q={github_query}&type=Users"
    return jsonify({"github_url": github_url})

# ----------------- UTILITY: LINKEDIN QUERY -----------------
def build_search_query(data):
    query_parts = []
    for key, value in data.items():
        if value.strip() and key != "open_to_work":
            if "," in value:
                query_parts.append(" OR ".join(f'"{v.strip()}"' for v in value.split(",")))
            else:
                query_parts.append(f'"{value.strip()}"')
    if data.get("open_to_work") == "yes":
        query_parts.append('"open to work"')
    return " AND ".join(query_parts) + " site:linkedin.com/in/"

def search_linkedin_profiles(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": LINKEDIN_API_KEY,
        "cx": LINKEDIN_CX,
        "num": 10
    }
    response = requests.get(url, params=params)
    results = response.json()
    return results.get("items", [])

DB_PATH = r"C:\Users\APPLE\Desktop\Link_squad\database.db"
print("Using DB file at:", os.path.abspath(DB_PATH))

@app.route('/')
def homes():
    return '<h2>Welcome! Go to <a href="/find_partners">Find a Partner</a> to start.</h2>'

@app.route('/find_partners', methods=['GET', 'POST'])
def find_partner_alt():
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
# ----------------- MAIN -----------------



def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
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
            )
        ''')
        conn.commit()


@app.route('/submit_profile', methods=['GET', 'POST'])
def submit_profile():
    submitted = False
    if request.method == 'POST':
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

        conn = sqlite3.connect(DB_PATH)
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

    return render_template('home_work.html', submitted=submitted, username=session.get('username'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
