from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import time
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
import numpy as np

def movie_list_generator():
    #nltk.download('stopwords')
    stop_nltk=set(stopwords.words("english"))
    stop_custom = {'and', 'best', 'book', 'books', 'character', 'characters', 'did', 'end', 'ending', 'film', 'films', 'great',
                   'just', 'like', 'make', 'movie', 'movies', 'novel', 'permalink', 'read', 'review', 'story', 'story', 'the',
                   'when','see','seen', 'get', 'many', 'one', 'made', 'ever', 'every', 'vote', 'much', 'well', 'watch', 'even',
                   'everything', 'youll', 'would', 'makes', 'even', 'ive', 'really', 'say', 'two', 'three', 'really', 'time',
                   'going', 'acting', 'actor', 'actors','also', 'dont', 'good', 'great', 'greatest','thing', 'things', 'way',
                   'never','could','first','found','performance','perfect','hollywood','us','think','10','action','new','oscar'
                   'academy','original','amazing','better','part','parts','scenes','sequel'}
    stop_words = stop_nltk.union(stop_custom)
    no_features = 50

    #get the list of best movies
    top_250 = []
    for i in range(0,2000,50):
        #IMDB_database = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=%i&ref_=adv_nxt'%(i+1)
        IMDB_database = 'https://www.imdb.com/search/title/?title_type=movie&genres=action&sort=num_votes,desc&start=%i&explore=title_type,genres&ref_=adv_nxt'%(i+1)
        r = requests.get(IMDB_database)
        html_soup = BeautifulSoup(r.content, features="html5lib")
        temp_50 = html_soup.find_all('h3')[:50]
        top_250.extend(temp_50)
        time.sleep(10.0)
    Name_list = []
    Keyword_list = []

    #scrape the reviews from the webpages
    for i, film in enumerate(top_250):
        if i < 2000:
            top_250[i] = 'https://www.imdb.com'+film.a['href']+'?ref_=adv_li_tt'
            print(top_250[i], i)
            tempname, tempkeys = get_movie_labels(top_250[i], no_features, stop_words,i+0)
            Name_list.append(tempname)
            Keyword_list.append(tempkeys)
            time.sleep(10.0)

    return Name_list, Keyword_list


def get_movie_labels(url, no_features, stop_words,j):
    r = requests.get(url.replace('?', 'reviews?'))
    html_soup = BeautifulSoup(r.content, features="html5lib")
    Title = html_soup.find('meta', property='og:title')['content'][:-7]
    review_containers = html_soup.find_all('div', class_='content')

    raw_data = np.array([Title])

    #extract the text from the reviews
    for i, review in enumerate(review_containers):
        review_containers[i] = review.text.replace('\n', ' ').replace("\'", '').replace("*",'')
        raw_data = np.append(raw_data, review_containers[i])
    np.save('./raw/Movie_' + str(j) + '.npy', raw_data)

    # get keywords
    CV = CountVectorizer(max_features=no_features, stop_words=list(stop_words))
    Movie_CV = CV.fit_transform(review_containers)
    Movie_feature_names = CV.get_feature_names()
    Movie_labels = Movie_feature_names
    return Title, Movie_labels


movie_titles, movie_labels = movie_list_generator()
df = pd.DataFrame({'Name': movie_titles, 'Keywords': movie_labels})
df.to_pickle('Moviedb.pkl')
