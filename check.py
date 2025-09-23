import requests

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GITHUB_API_KEY")
CX = os.getenv("GITHUB_SEARCH_ENGINE_ID")

def search_github_projects(query, api_key=API_KEY, cx=CX):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " site:github.com",
        "key": api_key,
        "cx": cx,
        "num": 5
    }
    response = requests.get(url, params=params)
    results = response.json()

    projects = []
    for item in results.get("items", []):
        projects.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })
    return projects


# Test
# if __name__ == "__main__":
#     query = "Library management system"
#     results = search_github_projects(query)
#     for result in results:
#         print(result["title"], result["link"])
if __name__ == "__main__":
    query = "site:github.com chatbot python"
    results = search_github_projects(query)
    if not results:
        print("No results found.")
    else:
        for result in results:
            print(result["title"], result["link"])
# results = response.json()
# print(results)  # 👈 Add this line to see the full response
