#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urlparse


class Book:
    def __init__(self, name):
        # get stopwords
        stop_nltk = set(stopwords.words("english"))
        stop_custom = pd.read_csv('/home/colin/Insight_Project/data/stop_custom.csv')['0']
        self.stop_words = stop_nltk.union(stop_custom)

        self.name = name
        self.webpage = ""
        self.title = ""
        self.coverlink = ""
        self.unikeywords = []
        self.bikeywords = []
        self.trikeywords = []
        self.nofeatures = 30
        self.nofeatures_bitri = 10

        self.get_webpage()
        self.get_keywords()
        self.df = pd.DataFrame({'Name': [self.name], 'Keywords': [self.unikeywords],
                                'BiKeywords': [self.bikeywords], 'TriKeywords': [self.trikeywords]})

    def get_webpage(self):
        query = self.name + ' site:Goodreads.com'
        g_clean = []  # this is the list we store the search results
        url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
            query)  # this is the actual query we are going to scrape

        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        a = soup.find_all('a')  # a is a list
        a[0].get('href')
        for i in a:
            try:
                k = i.get('href')
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n  = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if re.search('google.com', domain.netloc):
                    continue
                else:
                    g_clean.append(rul)
            except:
                continue
        self.webpage = g_clean[0]

    def process_df(self, ngrams, maxdf, review_containers):
        # tfidf vectorize dataframe
        Vect = TfidfVectorizer(max_features=self.nofeatures, ngram_range=(ngrams, ngrams), stop_words=self.stop_words,
                               max_df=maxdf)
        Book_Vect = Vect.fit_transform(review_containers)
        Book_feature_names = list(Vect.get_feature_names())
        return Book_feature_names

    def get_keywords(self):

        # get book keywords and title of book, scrape from internet
        r = requests.get(self.webpage)
        html_soup = BeautifulSoup(r.content)
        self.coverlink = html_soup.find('img', id='coverImage')['src']
        self.title = html_soup.find('h1', id='bookTitle').text.strip()

        # Extract reviews and vectorize the text, returning the keywords
        review_containers = html_soup.find_all('div', class_='review')
        for i, review in enumerate(review_containers):
            review_containers[i] = review.find('span', class_='readable').text.encode("ascii", "ignore").strip()
            # make sure there are actual reviews
        if len(review_containers) < 2:
            return

        self.unikeywords = self.process_df(1, 0.70, review_containers)
        self.bikeywords = self.process_df(2, 0.90, review_containers)
        self.trikeywords = self.process_df(3, 0.95, review_containers)
