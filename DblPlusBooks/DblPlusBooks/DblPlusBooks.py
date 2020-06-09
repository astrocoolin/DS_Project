#!/usr/bin/env python3
from DblPlusBooks import Book_Scrape, Book_Extract, Movie_Scrape
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
#import matplotlib
#matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# for webpage I/O
def rec_movie(book):
    # Get the features from the book and load up the movie database
    book_page = Book_Scrape.googleSearch(book)
    no_features = 50
    book_titles, book_labels, bookimg = Book_Extract.get_book_labels(book_page, no_features)
    df = pd.read_pickle('/home/colin/Data_Science/Insight/DS_Project/data/raw/top_250_movies/Moviedb.pkl')
    One_book = pd.DataFrame({'Name': [book_titles], 'Keywords': [book_labels]})

    # Determine which movie has the most features in common with the book
    df = One_book.append(df).reset_index(drop=True)
    mlb = MultiLabelBinarizer()
    df1 = df.join(pd.DataFrame(mlb.fit_transform(df.pop('Keywords')),
                               columns=mlb.classes_,
                               index=df.index))
    df2 = df1.drop(columns='Name')
    H = cosine_similarity(df2, df2)
    max_index = np.argmax(H[0][1:]) + 1
    movie_sugg = df1['Name'][max_index]

    return book_titles, bookimg, movie_sugg, Movie_Scrape.grab_movie_img(movie_sugg)

# for terminal I/O
def print_rec(bookname):
    print(rec_movie(bookname))
