from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace these with your actual API key and search engine ID
API_KEY = 'AIzaSyAfx71S85qKinRvt_JxGy8uOdoQS67kfB0'
SEARCH_ENGINE_ID = 'c21367a6f49c0497b'

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        language = request.form.get('language')
        project_name = request.form.get('project_name')
        creation_date = request.form.get('creation_date')  # format: yyyy-mm-dd

        # Build the GitHub search query
        search_query = f'site:github.com "{project_name}" language:{language} created:>{creation_date}'

        # Prepare API call
        api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

        response = requests.get(api_url)
        data = response.json()

        if 'items' in data:
            results = data['items']

    return render_template('github_form.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
