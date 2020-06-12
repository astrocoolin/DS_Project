import requests
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import pandas as pd
import numpy as np


class Movies:
    def __init__(self,book,nofeatures):
        self.df = pd.read_pickle(
            '/home/colin/Insight_Project/data/smallset.pkl')
        self.keywords = []
        self.webpage = ""
        self.title = ""
        self.coverlink = ""
        self.nofeatures = nofeatures
        self.second_best = ""
        self.third_best = ""
        self.combine_frames(book)
        self.best_movie()
        self.grab_movie_img()

    def combine_frames(self,book):
        Book_df = book.df
        self.df = Book_df.append(self.df).reset_index(drop=True)

    def best_movie(self):
        # Determine which movie has the most features in common with the book
        mlb = MultiLabelBinarizer()
        temp_df = self.df.copy()
        print('b4 mlb')
        clean_df = temp_df.join(pd.DataFrame(mlb.fit_transform(temp_df.pop('Keywords')),
                                   columns=mlb.classes_,
                                   index=temp_df.index))
        print('post mlb')
        sparse_df = clean_df.drop(columns='Name')
        print('pre NN')
        print(sparse_df.shape)
        nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(sparse_df.iloc[1:])
        distances, top_three = nbrs.kneighbors(pd.DataFrame(sparse_df.iloc[0]).T)
        print('post NN',top_three)
        self.keywords = self.df['Keywords'][top_three[0][0]+1]
        self.title = clean_df['Name'][top_three[0][0]+1]
        self.second_best =clean_df['Name'][top_three[0][1]+1]
        self.third_best = clean_df['Name'][top_three[0][2]+1]
        #return H, clean_df['Name']
        #return sparse_df

    def grab_movie_img(self):
        query = self.title + ' site:imdb.com'
        g_clean = []
        self.webpage = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
            query)  # this is the actual query we are going to scrape
        html = requests.get(self.webpage)
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
                if re.search("google.com", domain.netloc):
                    continue
                else:
                    g_clean.append(rul)
            except:
                continue
        url = g_clean[0]
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        self.coverlink = soup.find(class_='poster').img['src']
