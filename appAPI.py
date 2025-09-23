from flask import Flask, render_template, request
from LinkedIn_API import build_search_query, search_linkedin_profiles

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def partner_search():
    profiles = []
    user_input = {}

    if request.method == "POST":
        user_input = request.form.to_dict()
        query = build_search_query(user_input)
        profiles = search_linkedin_profiles(query, user_input)

    return render_template("linkedin_form.html", profiles=profiles, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)
