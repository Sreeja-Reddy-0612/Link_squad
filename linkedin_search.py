import requests

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("LINKEDIN_API_KEY")
CX = os.getenv("LINKEDIN_CX")

def search_linkedin_profiles(query, api_key=API_KEY, cx=CX):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " site:linkedin.com/in/",
        "key": api_key,
        "cx": cx,
        "num": 5
    }
    response = requests.get(url, params=params)
    results = response.json()

    profiles = []
    for item in results.get("items", []):
        profiles.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })
    return profiles


# Test
if __name__ == "__main__":
    query = "Python Developer IIT Hyderabad"
    results = search_linkedin_profiles(query)
    for result in results:
        print(result["title"], result["link"])
