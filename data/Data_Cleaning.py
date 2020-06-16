#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from nltk.corpus import stopwords


class movie_reviews:
    def __init__(self):
        # stopwords
        stop_nltk = set(stopwords.words("english"))
        stop_custom = set(pd.read_csv('stop_custom.csv')['0'])
        self.stop_words = stop_nltk.union(stop_custom)

        # ngrams for keyword definitions
        self.unikeywords = []
        self.bikeywords = []
        self.trikeywords = []
        self.name = ""
        self.index = 0
        self.text = ""
        # number of features for uni, ngrams
        self.nofeatures = 30
        self.nofeatures_bitri = 10
        self.df = pd.DataFrame(columns=['Name', "Keywords", "BiKeywords", "TriKeywords"])

    def set_index(self, i):
        self.index = i

    def process_df(self, ngram, maxdf):
        # tfidf vectorize text
        movie_vec_uni = TfidfVectorizer(max_features=self.nofeatures, stop_words=self.stop_words, max_df=maxdf,
                                        ngram_range=(ngram, ngram))
        movie_vec_uni.fit_transform(self.text[1:])
        return list(movie_vec_uni.get_feature_names())

    def get_keywords(self, genre):
        self.text = list(np.load('./raw/' + genre + '/Movie_' + str(self.index) + '.npy'))

        if len(self.text) > 10:
            for j, review in enumerate(self.text):
                if j > 0:
                    # clean up text
                    self.text[j] = review.encode("ascii", "ignore").strip().decode("ascii").split('\n')
                    self.text[j] = self.text[j][0].replace('Permalink', '').replace(
                        'Was this review helpful?  Sign in to vote.', '').replace('out of', '').replace(
                        'found this helpful', '').strip().replace('  ', '')
                    self.text[j] = ''.join([k for k in self.text[j] if not k.isdigit()])
            self.name = self.text[0]

            self.unikeywords = self.process_df(1, 0.70)
            self.bikeywords = self.process_df(2, 0.90)
            self.trikeywords = self.process_df(3, 0.95)
            self.df = self.df.append(pd.DataFrame(
                {'Name': self.name, 'Keywords': [self.unikeywords], 'BiKeywords': [self.bikeywords],
                 'TriKeywords': [self.trikeywords]}))

    def make_dataframe(self, genre, lim):
        for i in range(0, lim):
            print(i, genre)
            self.set_index(i)
            self.get_keywords(genre)

    def save_dataframe(self, lim):
        self.make_dataframe('action', lim)
        self.make_dataframe('adventure', lim)
        self.make_dataframe('biography', lim)
        self.make_dataframe('comedy', lim)
        self.make_dataframe('crime', lim)
        self.make_dataframe('documentary', lim)
        self.make_dataframe('drama', lim)
        self.make_dataframe('family', lim)
        # self.make_dataframe('fantasy',325)
        self.make_dataframe('fantasy', lim)
        self.make_dataframe('horror', lim)
        self.make_dataframe('romance', lim)
        self.make_dataframe('scifi', lim)
        self.make_dataframe('thriller', lim)
        self.make_dataframe('western', lim)

        self.df = self.df.reset_index().drop(columns=['index'])
        return self.df


reviews = movie_reviews()
data = reviews.save_dataframe(100)
data.drop_duplicates('Name', inplace=True)
data.reset_index(inplace=True)
data.drop(columns=['index'], inplace=True)
data.to_pickle('Data.pkl', protocol=2)
