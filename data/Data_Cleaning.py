from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
class movie_reviews:
    def __init__(self):
        self.keywords = ""
        self.name = ""
        self.index = 0
        self.text = ""
        self.nofeatures = 25
        self.df= pd.DataFrame(columns = ['Name',"Keywords"])

    def set_index(self,i):
        self.index = i
    def get_keywords(self,genre):
        stop_nltk = set(stopwords.words("english"))
        stop_custom = {'and', 'best', 'book', 'books', 'character', 'characters', 'did', 'end', 'ending', 'film',
               'films', 'great', 'just', 'like', 'make', 'movie', 'movies', 'novel', 'permalink', 'read',
               'review', 'story', 'story', 'the', 'when', 'see', 'seen', 'get', 'many', 'one', 'made',
               'ever', 'every', 'vote', 'much', 'well', 'watch', 'even', 'everything', 'youll', 'would',
               'makes', 'even', 'ive', 'really', 'say', 'two', 'three', 'really', 'time', 'reading', 'read',
               'first', 'going', 'good', 'little', 'new', 'things', 'thing', 'yet', 'us', 'want', 'fiction',
               'science', 'novella', 'people', 'something', 'know'}
        stop_custom2 = {'and', 'best', 'book', 'books', 'character', 'characters', 'did', 'end', 'ending', 'film', 'films', 'great',
               'just', 'like', 'make', 'movie', 'movies', 'novel', 'permalink', 'read', 'review', 'story', 'story', 'the',
               'when','see','seen', 'get', 'many', 'one', 'made', 'ever', 'every', 'vote', 'much', 'well', 'watch', 'even',
               'everything', 'youll', 'would', 'makes', 'even', 'ive', 'really', 'say', 'two', 'three', 'really', 'time',
               'going', 'acting', 'actor', 'actors','also', 'dont', 'good', 'great', 'greatest','thing', 'things', 'way',
               'never','could','first','found','performance','perfect','hollywood','us','think','10','action','new','oscar'
               'academy','original','amazing','better','part','parts','scenes','sequel','im','plot'}
        stop_words_temp = stop_nltk.union(stop_custom)
        stop_words = stop_words_temp.union(stop_custom2)
        self.text = list(np.load('./raw/'+genre+'/Movie_'+str(self.index)+'.npy'))
        if len(self.text) > 10:
            for j, review in enumerate(self.text):
                if j > 0:
                    self.text[j] = review.encode("ascii","ignore").strip()
            self.name =  self.text[0]
            movie_vec= TfidfVectorizer(max_features=self.nofeatures, stop_words=stop_words, max_df=0.65)
            movie_vec.fit_transform(self.text[1:])
            self.keywords = movie_vec.get_feature_names()
            self.df = self.df.append(pd.DataFrame({'Name':self.name, 'Keywords':[self.keywords]}))

    def make_dataframe(self,genre):
        for i in range(0,2000):
            print(i,genre)
            self.set_index(i)
            self.get_keywords(genre)

    def save_dataframe(self):
        self.make_dataframe('action')
        self.make_dataframe('comedy')
        self.make_dataframe('drama')
        self.make_dataframe('horror')
        self.make_dataframe('romance')
        self.make_dataframe('scifi')
        self.make_dataframe('thriller')
        self.df = self.df.reset_index().drop(columns = ['index'])
        return self.df






