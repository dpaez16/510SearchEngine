from flask import Flask, request, render_template, redirect, url_for
import logging
from logging import handlers
from create_sentences import split_into_sentences
import pymongo
import os

app = Flask(__name__)

USING_SENTENCES = True

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://admin:lgV3ugTp2Rttw6Dz@corpus-fzvdf.mongodb.net/test?retryWrites=true&w=majority")
corpus = client['Corpus']

# logging config
logger = logging.getLogger('relevance_judgements')
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler('relevance-judgements.log', backupCount=5)
logger.addHandler(handler)


def logRelevance(query, idx, R):
    logger.debug("({}, {}, {})".format(query, idx, R))


def processInput(text_input):
    doc = text_input.replace('\r', '')
    doc = doc.replace('\n', ' ')
    if doc[-1] not in ['.', '!', '?']:
        doc = doc + '.'
    sentences = split_into_sentences(doc)
    return sentences


def getDocTitleURL(db, docID):
    d = db.find_one({"_id": docID})
    if d is None:
        return None, None
    else:
        return d['title'], d['url']


def getDocAuthors(db, docID):
    d = db.find_one({"_id": docID})
    if d is None:
        return None
    else:
        return d['authors']


def getSearchResults(query):
    searchResultsFile = open('searchResults.txt', 'r')
    rawSearchResults = searchResultsFile.readlines()
    searchResults = []
    for rawSearchResult in rawSearchResults:
        docIdx, doc, score = rawSearchResult.strip().split('----------')
        docIdx = int(docIdx)
        score = float(score)
        title, url = getDocTitleURL(corpus.test, docIdx)
        if title is None or url is None:
            continue
        else:
            title = " ".join(map(lambda s: s.capitalize(), title.split()))
            searchResults.append((title, doc, docIdx, score))
            logRelevance(query, docIdx, 0)
    
    searchResultsFile.close()
    os.remove('searchResults.txt')
    return searchResults


@app.route("/query=<string:query>,paper=<int:paperIdx>")
def goToPaper(query, paperIdx):
    logRelevance(query, paperIdx, 1)
    title, url = getDocTitleURL(corpus.test, paperIdx)
    authors = getDocAuthors(corpus.test2, paperIdx)
    if title is None or url is None or authors is None:
        error = "Page does not exist!"
        return render_template('error.html', error=error)
    else:
        title = " ".join(map(lambda s: s.capitalize(), title.split()))
        return render_template('paper.html',
                                title=title,
                                url=url,
                                authors=authors)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text_input = request.form['text_input']
        if len(text_input) == 0:
            return redirect(url_for('home'))
        if USING_SENTENCES:
            # splitting into sentences
            sentences = processInput(text_input)
            results = []
            for sentence in sentences:
                os.system('python3 search.py \"{}\" {} -f'.format(sentence, str(10)))
                searchResults = getSearchResults(sentence)
                results += searchResults
        else:
            # using entire doc as query
            os.system('python3 search.py \"{}\" {} -f'.format(text_input, str(10)))
            results = getSearchResults(text_input)
        results = sorted(results, key=lambda x: x[-1])
        return render_template('home.html', 
                                searchResults=results,
                                text_input=text_input,
                                query=text_input)
    else:
        return render_template('home.html',
                                searchResults=None,
                                text_input='')


if __name__ == "__main__":
    app.run(debug=True)
