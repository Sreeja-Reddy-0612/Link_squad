from flask import Flask, render_template, request
from git_linkedin import generate_linkedin_url, generate_github_url

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # optional landing page

@app.route('/linkedin', methods=['GET', 'POST'])
def linkedin():
    if request.method == 'POST':
        data = request.form.to_dict()
        url = generate_linkedin_url(data)
        return render_template('result.html', url=url, platform='LinkedIn')
    return render_template('linkedin_form.html')

@app.route('/github', methods=['GET', 'POST'])
def github():
    if request.method == 'POST':
        data = request.form.to_dict()
        url = generate_github_url(data)
        return render_template('result.html', url=url, platform='GitHub')
    return render_template('github_form.html')

if __name__ == '__main__':
    app.run(debug=True)
