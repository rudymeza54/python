import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import yaml
from sqlalchemy import create_engine
import colorama
from colorama import Fore, Style, Back


# DEFINE SCRAPING FUNCTION FOR WEBSITE URL

def scrape(url):
    
    url = url

    response = requests.get(url)

    content = response.content

    soup = BeautifulSoup(content,'html.parser')

    return soup

# DEFINE URL AND INTIALIZE SCRAPING URL'S FIRST 10 PAGES

main_url = []
pages = [num for num in range(1,50)]

for num in pages:
    urls = f'https://catalog.data.gov/dataset?q=&sort=views_recent+desc&page={num}'
    main_url.append(urls)

    


# PULL ALL DATASETS IN H3 TAG

links = []

for url in main_url:
    
    soup = scrape(url) 

    page = soup.find_all('h3')

    for i in page:
        a_tag = i.find('a')
        if a_tag:
            h = a_tag.get('href')
            if h:
                x ='https://catalog.data.gov/'+''.join(h)
                links.append(x)


# APPLY CRAWLER TO DIFFERENT URL'S AND EXTRACT DATA INTO DICTIONARIES, LISTED DF'S, AND MASTER DF

list_dict = []
list_df = []

print(f'Running Crawler...')

for i in links:
    x= scrape(i)
    title = x.find('h1',{'itemprop':'name'}).text.strip()
    description = x.find('div',{'itemprop': 'description'}).text.strip()
    date = x.find('span',{'itemprop':'dateModified'}).text.strip()
    file_extension = [item.text.strip() for item in x.find_all('a',{'itemprop':'contentUrl'})]
    file_extension = [re.findall(r'File(\w+)', item) for item in file_extension]
    file_extension = [''.join(item) for item in file_extension]
    link = i
    out={
        "title":title,
        "link": link,
        "description": description,
        "date": date,
        "ext": file_extension
    }
    list_dict.append(out)


for i in list_dict:
    x = pd.DataFrame(i,  index=None)
    list_df.append(x)

print(f'Binding list if df....')
master = pd.concat(list_df)



# LOAD INTO MSSQL DB

db = yaml.safe_load(open('pw_mssql.yaml'))


SERVER = db['SERVER']
DATABASE = db['DATABASE']
USERNAME = db['USERNAME']
PASSWORD = db['PASSWORD']
DRIVER = 'ODBC Driver 17 for SQL Server'

connectionString = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?&driver={DRIVER}'

engine = create_engine(connectionString)

tb = "data_gov"

print(f'writing df to sql server...')

master.to_sql(tb,engine, if_exists = 'replace', index = False)

print(f'done')