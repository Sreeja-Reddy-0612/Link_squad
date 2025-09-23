from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/search/repositories"

# Build GitHub query
def build_github_api_query(data):
    query = []

    if data.get("project_name"):
        query.append(data["project_name"])

    if data.get("language"):
        query.append(f"language:{data['language']}")

    if data.get("creation_date"):
        query.append(f"created:>{data['creation_date']}")

    return "+".join(query)

# Search GitHub repos using API
def search_github_repos(query):
    url = f"{GITHUB_API_URL}?q={query}&per_page=5"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    items = response.json().get("items", [])

    projects = []
    for item in items:
        projects.append({
            "title": item["name"],
            "link": item["html_url"],
            "snippet": item["description"] or "No description provided."
        })

    return projects

@app.route('/github-search', methods=['GET', 'POST'])
def github_search():
    results = None
    if request.method == 'POST':
        form_data = {
            "language": request.form.get("language", "").strip(),
            "project_name": request.form.get("project_name", "").strip(),
            "creation_date": request.form.get("creation_date", "").strip()
        }

        query = build_github_api_query(form_data)
        results = search_github_repos(query)

    return render_template("github_form.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)






{% comment %} <div class="box1 box" onclick="window.location.href='/git_linked.html'">
            <div class="box-content">
                <h2>LinkedIn & GitHub</h2>
                <div class="box-img" style="background-image: url('hlinkgit.jpg');"></div>
                <p>Learn more</p>
            </div>
        </div>

        <div class="box2 box">
            <div class="box-content2">
                <div class="sub-box">
                    <h2>LinkedIn</h2>

                    <img src="hLinkedin.jpg" alt="LinkedIn">
                    <p style="color: white; font-size: 18px; font-weight: bold;"></p>
                </div>
                <div class="sub-box">
                    <h2>GitHub</h2>

                    <img src="hgithub.jpg" alt="Git">
                    <p style="color: white; font-size: 18px; font-weight: bold;"></p>
                </div>
            </div>
        </div> {% endcomment %}





        location: document.getElementById("ghLocation").value,
