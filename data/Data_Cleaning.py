from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.corpus import stopwords


class movie_reviews:
    def __init__(self):
        self.keywords = ""
        self.name = ""
        self.index = 0
    def set_index(self,i):
        self.index = i
    def get_keywords(self,genre):
        stop_nltk = set(stopwords.words("english"))
        np.load('./raw/'+genre+'/Movie_1.npy')






