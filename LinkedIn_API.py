from flask import Flask, render_template, request
import requests

app = Flask(__name__)

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("LINKEDIN_API_KEY")
CX = os.getenv("LINKEDIN_CX")
# LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
# LINKEDIN_CX = os.getenv("LINKEDIN_CX")

def build_search_query(data):
    query_parts = []

    for key, value in data.items():
        if value.strip() and key != "open_to_work":
            query_parts.append(f'"{value.strip()}"')

    if data.get("open_to_work") == "yes":
        query_parts.append('"open to work"')

    query = " AND ".join(query_parts)
    return query + " site:linkedin.com/in/"

def search_linkedin_profiles(query, filters):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
        "num": 10
    }
    response = requests.get(url, params=params)
    results = response.json()

    filtered_profiles = []
    for item in results.get("items", []):
        snippet = item.get("snippet", "").lower()
        matches = all(value.lower() in snippet for key, value in filters.items() if value.strip() and key != "open_to_work")
        
        if filters.get("open_to_work") == "yes" and "open to work" not in snippet:
            continue
        
        if matches and "linkedin.com/in/" in item.get("link", "").lower():
            filtered_profiles.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
    return filtered_profiles

@app.route("/", methods=["GET", "POST"])
def partner_search():
    profiles = []
    user_input = {
        "skills": "",
        "job": "",
        "experience": "",
        "company": "",
        "location": "",
        "college": "",
        "soft_skills": "",
        "hackathons": "",
        "internships": "",
        "other": "",
        "open_to_work": "no"
    }

    if request.method == "POST":
        for key in user_input:
            user_input[key] = request.form.get(key, "")
        
        query = build_search_query(user_input)
        profiles = search_linkedin_profiles(query, user_input)

    return render_template("linkedin_form.html", profiles=profiles, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)
