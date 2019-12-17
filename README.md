# 510SearchEngine

To run locally, first download the dataset file (after cloning the repo):  
https://drive.google.com/open?id=1srX0nqtbKLFYHhDyaPHTP1GhnslJ3lst  

If its zipped, extract the file and move ```citeseer.dat``` in the citeseer folder and run:
```
python3 create_indexes.py
```
The above script will create all necessary files (including the inverted and forward indexes) for the search engine to work.  
Finally, run the web app with:
```
sudo python3 app.py
```
```sudo``` is needed to run on port 80 (i.e. on AWS). The web app should run on ```localhost:80```.  


Note: ```relevance_judgements.log``` is what the web app will use to log user clicks/doesn't click to (as relevance judgements).

# Deployment
We have depoyed the search engine, and it can be accessed by going to [3.19.232.111](3.19.232.111).
