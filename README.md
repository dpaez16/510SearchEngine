# 510SearchEngine

To run locally, first download the following files (after cloning the repo):  
https://drive.google.com/open?id=1srX0nqtbKLFYHhDyaPHTP1GhnslJ3lst  

Extract their contents, then run:
```
python3 create_data_files.py
```
The above script will create all necessary files (including the inverted index) for the search engine to work.  
Finally, run the web app with:
```
sudo python3 app.py
```
It should run on ```localhost:80```.  


Note: ```relevance_judgements.log``` is what the web app will use to log user clicks/doesn't click to (as relevance judgements).

# Deployment
We have depoyed the search engine, and it can be accessed by going to [3.19.232.111](3.19.232.111).

# System Description
For our project, we used the meTaPy toolkit. To format the data so we could use the toolkit, we created a .dat file where each file in the dataset is represented as a line. We then use meTaPy to create an inverted index for the data. We used a unigram language model with the stopwords listed in ```stopwords.txt```.

For our actual search engine, we used the BM25 algorithm (which was implemented by meTaPy) with ```k1 = 1.2```, ```b = 0.75```, and ```k2=500``` as we found this parameter set to yield the best results of the ones we tried.
