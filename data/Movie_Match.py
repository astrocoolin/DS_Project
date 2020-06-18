from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import time
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
import numpy as np

def top250():
    name_list = []
    code_list = []
    for i in range(0, 250, 50):
        time.sleep(10)
        IMDB_database = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
        r = requests.get(IMDB_database)
        soup = BeautifulSoup(r.content, features="html5lib")
        codesoup = soup.find_all(class_="ribbonize")
        namesoup = soup.find_all(class_='lister-item-header')
        print(len(codesoup))
        print(len(namesoup))
        for j in range(0, len(codesoup)):
            name = namesoup[j].a.text + ' ' + namesoup[j].find(class_='lister-item-year').text
            code = codesoup[j]['data-tconst']

            name_list.append(name)
            code_list.append(code)
    return name_list, code_list


def movie_list_generator(genre):
    name_list = []
    code_list = []
    for i in range(0, 100, 50):
        time.sleep(10)
        IMDB_database = 'https://www.imdb.com/search/title/?title_type=movie&genres=' + genre + '&sort=num_votes,desc&start=' + str(
            i + 1) + '&explore=title_type,genres&ref_=adv_nxt'
        r = requests.get(IMDB_database)
        soup = BeautifulSoup(r.content, features="html5lib")
        codesoup = soup.find_all(class_="ribbonize")
        namesoup = soup.find_all(class_='lister-item-header')
        print(len(codesoup))
        print(len(namesoup))
        for j in range(0, len(codesoup)):
            name = namesoup[j].a.text + ' ' + namesoup[j].find(class_='lister-item-year').text
            code = codesoup[j]['data-tconst']

            name_list.append(name)
            code_list.append(code)
    return name_list, code_list

def full_collection():
    full_names_list = []
    full_codes_list = []
    names_list = ['action', 'adventure', 'comedy', 'drama','horror', 'thriller', 'crime', 'family',
                  'romance', 'biography', 'documentary', 'fantasy', 'scifi', 'western']
    for name in names_list:
        print(name)
        names,codes = movie_list_generator(name)
        full_names_list.extend(names)
        full_codes_list.extend(codes)
    names,codes = top250()
    full_names_list.extend(names)
    full_codes_list.extend(codes)
    return full_names_list, full_codes_list

names , codes = full_collection()
df_codes = pd.DataFrame({'Name':names,'Codes':codes})
df_keys = pd.read_pickle('Data.pkl')
df = df_keys.join(df_codes.set_index('Name'), on='Name')
df = df.drop_duplicates('Codes')
df.to_pickle('Data_id.pkl')