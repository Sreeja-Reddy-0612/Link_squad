from flask import Flask, render_template
import requests

app = Flask(__name__)

# 👇 Your API config
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("DEVPOST_API_KEY")
CX = os.getenv("DEVPOST_CX_ID")


# 🔍 Function to fetch Devpost hackathons
def get_devpost_events(query="upcoming hackathons site:devpost.com"):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        events = []
        for item in results.get("items", []):
            event = {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            events.append(event)
        return events
    else:
        print("❌ Error fetching events:", response.status_code, response.text)
        return []

# ✅ Homepage
@app.route("/")
def home():
    return "<h2>Welcome! Go to <a href='/competitions'>/competitions</a> to see upcoming Devpost hackathons.</h2>"

# ✅ Devpost Events Page
@app.route("/competitions")
def show_events():
    events = get_devpost_events()
    return render_template("competitions.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
