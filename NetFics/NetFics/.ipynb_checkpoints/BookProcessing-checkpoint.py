#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urlparse


class Book:
    def __init__(self, name, nofeatures):
        self.name = name
        self.webpage = ""
        self.title = ""
        self.coverlink = ""
        self.unikeywords = []
        self.bikeywords = []
        self.nofeatures = nofeatures

        self.get_webpage()
        self.get_keywords()
        self.unikeywords.extend(self.bikeywords)
        self.df = pd.DataFrame({'Name': [self.name], 'Keywords': [self.unikeywords]})

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
            k = i.get('href')
            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if (re.search('google.com', domain.netloc)):
                    continue
                else:
                    g_clean.append(rul)
            except:
                continue
        self.webpage = g_clean[0]

    def get_keywords(self):
        # get stopwords
        stop_nltk = set(stopwords.words("english"))
        stop_custom = {'and', 'best', 'book', 'books', 'character', 'characters', 'did', 'end', 'ending', 'film',
                       'films', 'great', 'just', 'like', 'make', 'movie', 'movies', 'novel', 'permalink', 'read',
                       'review', 'story', 'story', 'the', 'when', 'see', 'seen', 'get', 'many', 'one', 'made',
                       'ever', 'every', 'vote', 'much', 'well', 'watch', 'even', 'everything', 'youll', 'would',
                       'makes', 'even', 'ive', 'really', 'say', 'two', 'three', 'really', 'time', 'reading', 'read',
                       'first', 'going', 'good', 'little', 'new', 'things', 'thing', 'yet', 'us', 'want', 'fiction',
                       'science', 'novella', 'people', 'something', 'know', 'though', 'go', 'post', 'back', 'series'
                       'year','years', 'http', 'www'}
        stop_words = stop_nltk.union(stop_custom)

        # get book keywords and title of book, scrape from internet
        r = requests.get(self.webpage)
        html_soup = BeautifulSoup(r.content)
        self.coverlink = html_soup.find('img', id='coverImage')['src']
        self.title = html_soup.find('h1', id='bookTitle').text.strip()

        # Extract reviews and vectorize the text, returning the keywords
        review_containers = html_soup.find_all('div', class_='review')
        for i, review in enumerate(review_containers):
            review_containers[i] = review.find('span', class_='readable').text.encode("ascii","ignore").strip()
        if len(review_containers) < 2:
            return
        uniVect = TfidfVectorizer(max_features=self.nofeatures, ngram_range=(1,1), stop_words=stop_words, max_df=0.80)
        uniBook_Vect = uniVect.fit_transform(review_containers)
        uniBook_feature_names = list(uniVect.get_feature_names())
        biVect = TfidfVectorizer(max_features=self.nofeatures, ngram_range=(2,2), stop_words=stop_words, max_df=0.80)
        biBook_Vect = biVect.fit_transform(review_containers)
        biBook_feature_names = list(biVect.get_feature_names())
        self.unikeywords = uniBook_feature_names
        self.bikeywords = biBook_feature_names
