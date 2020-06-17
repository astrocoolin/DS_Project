from typing import Set, Any

import requests
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import jaccard_score
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import pandas as pd
import numpy as np


class Movies:
    keywords: Set[Any]

    def __init__(self):
        self.df = pd.read_pickle(
            '/home/colin/Insight_Project/data/Data_id.pkl')
        self.keywords = []
        self.webpage = ""
        self.title = ""
        self.title_code = ""
        self.next_best = ""
        self.next_best_code = ''
        # self.grab_movie_img()

    def compare_book(self,book):
        self.combine_frames(book)
        self.poop = self.process_df('Keywords')
        self.best_movie()

    def combine_frames(self, book):
        Book_df = book.df
        self.df = Book_df.append(self.df).reset_index(drop=True)

    def process_df(self, keywordtype):
        mlb = MultiLabelBinarizer()
        temp_df = self.df.copy()
        sparse_df = pd.DataFrame(mlb.fit_transform(temp_df.pop(keywordtype)),
                                 columns=mlb.classes_,
                                 index=temp_df.index)
        keyscore = []
        for i in range(0, len(sparse_df) - 1):
            keyscore.append(jaccard_score(sparse_df.iloc[0], sparse_df.iloc[i]))
        return np.array(keyscore)

    def best_movie(self):
        # Determine which movie has the most features in common with the book
        WGT = [0.3, 0.4, 0.6]
        JS1 = WGT[0] * self.process_df('Keywords')
        JS2 = WGT[1] * self.process_df('BiKeywords')
        JS3 = WGT[2] * self.process_df('TriKeywords')
        total_score = (JS1 + JS2 + JS3)/np.sum(WGT)

        top = np.argsort(total_score)[-5:-1]
        print(total_score[top])

        # get shared keywords
        self.keywords = set(self.df['Keywords'][top[2]]).intersection(self.df['Keywords'][0])
        self.keywords = self.keywords.union(set(self.df['BiKeywords'][top[2]]).intersection(self.df['BiKeywords'][0]))
        self.keywords = self.keywords.union(set(self.df['TriKeywords'][top[2]]).intersection(self.df['TriKeywords'][0]))
        print(self.keywords)
        self.title = self.df['names'][top[3]]
        self.title_code = self.df['codes'][top[3]]
        self.next_best = list(self.df['names'][top[0:3]])
        self.next_best_code = list(self.df['codes'][top[0:3]])

    def grab_movie_img(self, code):
        url = 'https://www.imdb.com/title/'+str(code)
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        return soup.find(class_='poster').img['src']
