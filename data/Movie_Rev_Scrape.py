from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import time
import requests
import pandas as pd
import csv

def movie_list_generator():
    no_features = 25
    filename = 'Movie_list.html'
    f = open(filename)
    html_soup = BeautifulSoup(f, 'html.parser')
    top_250 = html_soup.find_all('h3')
    Name_list= []
    Keyword_list = []
    for i, film in enumerate(top_250):
        if i < 50:
            top_250[i] = film.a['href']
            #print(i)
            tempname, tempkeys = get_movie_labels(top_250[i],no_features)
            #print(tempname,tempkeys,i)
            Name_list.append(tempname)
            Keyword_list.append(tempkeys)
            time.sleep(10.0)
    return Name_list, Keyword_list

def get_movie_labels(url,no_features):
    # temporarily working with an html file
    r = requests.get(url.replace('?','reviews?'))
    html_soup = BeautifulSoup(r.content, features="html5lib")
    Title = html_soup.find('meta',property='og:title')['content'][:-7]
    review_containers = html_soup.find_all('div', class_='content')
    for i, review in enumerate(review_containers):
        review_containers[i] = review.text.replace('\n',' ').replace("\'",'')
        #print(review)

    CV = CountVectorizer(max_features=no_features, stop_words='english')
    Movie_CV = CV.fit_transform(review_containers)
    Movie_feature_names = CV.get_feature_names()
    Movie_labels = Movie_feature_names
    return Title, Movie_labels

movie_titles, movie_labels = movie_list_generator()
df = pd.DataFrame({'Name':movie_titles, 'Keywords':movie_labels})
df.to_pickle('Moviedb.pkl')

