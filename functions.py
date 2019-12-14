import pymongo

mongo = pymongo.MongoClient("mongodb+srv://admin:lgV3ugTp2Rttw6Dz@corpus-fzvdf.mongodb.net/test?retryWrites=true&w=majority")
corpus = client['Corpus']

def getDocTitleURLS(docIDS):
    titleURLPairs = []
    for docID in docIDS:
        d = corpus.test.find_one({"_id": docID})
        titleURLPairs.append((d['title'], d['url']))

    return titleURLPairs

def getDocAuthors(docIDS):
    docAuthors = []
    for docID in docIDS:
        d = corpus.test2.find_one({"_id": docID})
        docAuthors.append(d['authors'])
    
    return docAuthors

