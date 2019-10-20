from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import logging
from logging import handlers
import os

app = Flask(__name__)
fileIDX = open('files.txt', 'r').readlines()

# logging config
logger = logging.getLogger('relevance_judgements')
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler('relevance-judgements.log', backupCount=5)
logger.addHandler(handler)


def logRelevance(query, idx, R):
    logger.debug("({}, {}, {})".format(query, idx, R))
    

def createLink(fileName):
    return "https://www.aclweb.org/anthology/{}.pdf".format(fileName.split('.tei.xml')[0])


def getSearchResults(query):
    searchResultsFile = open('searchResults.txt', 'r')
    rawSearchResults = searchResultsFile.readlines()
    searchResults = []
    for rawSearchResult in rawSearchResults:
        idx, content = rawSearchResult.strip().split('\t')
        idx = int(idx)
        splitted = fileIDX[idx].strip().split('\t') + [""]
        fileName, title = splitted[:2]
        link = createLink(fileName)
        title = link if len(title) == 0 else title
        searchResults.append((title, content, idx))
        logRelevance(query, idx, 0)
    searchResultsFile.close()
    os.remove('searchResults.txt')
    return searchResults


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
    os.system('python3 search.py \"{}\" {} -f'.format(query, str(10)))
    searchResults = getSearchResults(query)
    return render_template('home.html', 
                            searchResults=searchResults, 
                            query=query,
                            logRelevance=logRelevance)


@app.route("/query=<string:query>,paper=<int:paperIdx>")
def goToPaper(query, paperIdx):
    logRelevance(query, paperIdx, 1)
    fileName = fileIDX[paperIdx].strip().split('\t')[0]
    link = createLink(fileName)
    return redirect(link)


if __name__ == "__main__":
    app.run(debug=True)
