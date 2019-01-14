
# Marco Remane

# # idealista HTML Selenium Scrapping to MongoDB

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint
import datetime
import time
from selenium.webdriver.firefox.options import Options

client = MongoClient('') # MongoDB instance URL
db = client['ub-ads'] # DB name
collection = db['idealistaAPI'] # Collection Name

#result = db.collection.create_index([('url', 1)],unique=True) #Create unique index

df = pd.read_csv('idealistaAPI-2018-Oct-30-1713.csv') #Read CSV with all URLs to scrape

for url in df.url:
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = Options()
    options.headless = False
    options.add_argument('user-agent={"user_agent"}')
    wd = webdriver.Firefox('/Users/marcoremane/Desktop/chromedriver', options=options)
    wd.get(url);
    html = wd.page_source
    parser = BeautifulSoup(html, "html.parser")
    all_features = []
    try:
        #Try to find our divs
        parser_HTML = parser.findAll('div', attrs={'class':'details-property_features'})
    except AttributeError as error:
        #Can't find them? Feature list will be empty.
        pass
    #Found something? One div only?
    if len(parser_HTML) == 1:
        x = parser_HTML[0].findAll('li')
        basic_features = [item.get_text() for item in x]
        all_features = basic_features
    #Found something? Two divs?
    if len(parser_HTML) == 2:
        x = parser_HTML[0].findAll('li')
        y = parser_HTML[1].findAll('li')
        basic_features = [item.get_text() for item in x]
        extras = [item.get_text() for item in y]
        all_features = basic_features + extras
    #try:
        #Try to create our mongo db doc
    #    doc = {
    #        "url" : url,
    #        "feautures" : all_features,
    #        "scrape_date" : datetime.datetime.utcnow()
    #    }
    #    document_id = db.collection.insert_one(doc).inserted_id
    #    print(" #{0} - URL scrapped: {1} with features: {2}".format(document_id, url, all_features))
    #except pymongo.errors.DuplicateKeyError as error:
        #Document already exists? It's ok. Go to next document.
        #print(url, " record already exists on DB.")
        #pass
    doc = {
        "url" : url,
        "feautures" : all_features,
        "scrape_date" : datetime.datetime.utcnow()
    }
    document_id = db.collection.insert_one(doc).inserted_id
    print(" #{0} - URL scrapped: {1} with features: {2}".format(document_id, 'https://www.idealista.com/inmueble/82895714/', all_features))
    time.sleep(60)
    wd.quit()
