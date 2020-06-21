#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urlparse
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

class Book:
    def __init__(self):
        # get stopwords
        stop_nltk = set(stopwords.words("english"))
        stop_custom = pd.read_csv('/home/colin/Insight_Project/data/stop_custom.csv')['0']
        self.stop_words = stop_nltk.union(stop_custom)
        self.title = ""
        self.coverlink = ""
        self.unikeywords = []
        self.bikeywords = []
        self.trikeywords = []
        self.nofeatures = 30
        self.nofeatures_bitri = 10

    def get(self,name):
        self.name = name
        self.get_webpage()
        self.get_keywords()
        self.df = pd.DataFrame({'Name': [self.name], 'Keywords': [self.unikeywords],
                                'BiKeywords': [self.bikeywords], 'TriKeywords': [self.trikeywords]})

    def get_webpage(self):
        url = 'https://www.goodreads.com/search?q='+self.name
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        page = soup.find(class_='tableList')
        tempurl = page.a['href']
        url = 'https://www.goodreads.com/'+tempurl
        #print(url)
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content)

    def process_df(self, ngram, maxdf,text):
        # tfidf vectorize text
        mindf = 0.1
        try:
            keys = self.vectorize(ngram,maxdf,mindf,text)
        except:
            mindf =0.05
            try:
                keys = self.vectorize(ngram, maxdf, mindf,text)
            except:
                mindf = 1
                keys = self.vectorize(ngram, maxdf, mindf,text)
        return keys

    def vectorize(self,ngram,maxdf,mindf,text):
        Vect = TfidfVectorizer(max_features=self.nofeatures, stop_words=self.stop_words, max_df=maxdf,
                                        ngram_range=(ngram, ngram), min_df=mindf)
        Vect.fit_transform(text)
        return list(Vect.get_feature_names())

    def process_df_old(self, ngrams, maxdf, review_containers,mindf):
        # tfidf vectorize dataframe
        Vect = TfidfVectorizer(max_features=self.nofeatures, ngram_range=(ngrams, ngrams), stop_words=self.stop_words,
                               max_df=maxdf,min_df = mindf,tokenizer=LemmaTokenizer())
        Book_Vect = Vect.fit_transform(review_containers)
        Book_feature_names = list(Vect.get_feature_names())
        return Book_feature_names

    def get_keywords(self):

        # get book keywords and title of book, scrape from internet
        self.coverlink = self.soup.find('img', id='coverImage')['src']
        self.title = self.soup.find('h1', id='bookTitle').text.strip()

        # Extract reviews and vectorize the text, returning the keywords
        review_containers = self.soup.find_all('div', class_='review')
        for i, review in enumerate(review_containers):
            review_containers[i] = review.find('span', class_='readable').text.encode("ascii", "ignore").strip()
            review_containers[i] = str(review_containers[i]).translate(str.maketrans('', '', string.punctuation))
            # make sure there are actual reviews
        if len(review_containers) < 2:
            return

        self.unikeywords = self.process_df(1, 0.65, review_containers)
        self.bikeywords = self.process_df(2, 0.80, review_containers)
        self.trikeywords = self.process_df(3, 0.95, review_containers)
