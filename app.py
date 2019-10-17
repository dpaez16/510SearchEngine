from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home_page():
    query = None
    if request.method == "POST":
        query = request.form['query']
    
    return render_template('home.html', query=query)


if __name__ == "__main__":
    app.run(debug=True)
