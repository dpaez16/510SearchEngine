from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        query = request.form['query']
        if len(query) != 0:
            return redirect(url_for('search', query=query), code=307) # POST request
    return render_template('home.html')


@app.route("/query=<string:query>", methods=["GET", "POST"])
def search(query):
    if request.method == "POST":
        query = request.form["query"]
        if len(query) == 0:
            return redirect(url_for('home_page'))
        return redirect(url_for('search', query=query)) # GET request
    # process query here
    return render_template('home.html', query=query)


if __name__ == "__main__":
    app.run(debug=True)
