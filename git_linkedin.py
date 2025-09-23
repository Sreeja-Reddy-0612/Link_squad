# git_linked.py
from urllib.parse import quote_plus

def generate_linkedin_url(data):
    query_parts = []

    if data.get("skills"):
        query_parts.append(data["skills"])
    if data.get("jobTitle"):
        query_parts.append(data["jobTitle"])
    if data.get("company"):
        query_parts.append(f'company "{data["company"]}"')
    if data.get("experience"):
        query_parts.append(f'{data["experience"]} years experience')
    if data.get("college"):
        query_parts.append(data["college"])
    if data.get("location"):
        query_parts.append(f'location "{data["location"]}"')
    if data.get("softSkills"):
        query_parts.append(data["softSkills"])
    if data.get("hackathon"):
        query_parts.append(data["hackathon"])
    if data.get("internship"):
        query_parts.append(data["internship"])
    if data.get("date"):
        query_parts.append(f'> {data["date"]}')

    final_query = " ".join(query_parts)
    encoded_query = quote_plus(final_query)
    linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}&origin=GLOBAL_SEARCH_HEADER"
    return linkedin_url


def generate_github_url(data):
    search_terms = []

    if data.get("language"):
        search_terms.append(f"language:{data['language']}")
    if data.get("projectName"):
        search_terms.append(data["projectName"])
    if data.get("followers"):
        search_terms.append(f"followers:>={data['followers']}")
    if data.get("repoCount"):
        search_terms.append(f"repos:>={data['repoCount']}")
    if data.get("createdAfter"):
        search_terms.append(f"created:>{data['createdAfter']}")
    if data.get("size"):
        search_terms.append(f"size:>={data['size']}")
    if data.get("license"):
        search_terms.append(f"license:{data['license']}")

    github_query = "+".join(search_terms)
    github_url = f"https://github.com/search?q={github_query}&type=Users"
    return github_url


if __name__ == "__main__":
   pass