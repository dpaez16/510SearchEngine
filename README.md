# 510SearchEngine

To run locally, first download the following files (after cloning the repo):  
https://drive.google.com/uc?export=download&id=10UBBDPJ37u6JvVPMK1OkGfEWGM-GwEOz  
https://drive.google.com/uc?export=download&id=1zuYvx4JCKencCXore4Yxo6HXUuBKFjm3  
  
Extract their contents, then run:
```
python3 create_data_files.py
```
The above script will create all necessary files (including the inverted index) for the search engine to work.  
Finally, run the web app with:
```
python3 app.py
```
It should run on ```localhost:5000```.
