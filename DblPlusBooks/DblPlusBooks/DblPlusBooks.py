#!/usr/bin/env python3
from DblPlusBooks import Book_Scrape, Book_Extract
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


def rec_movie(book):
    book_page = Book_Scrape.googleSearch(book)
    no_features = 50
    book_titles, book_labels = Book_Extract.get_book_labels(book_page, no_features)
    df = pd.read_pickle('/home/colin/Data_Science/Insight/DS_Project/data/Moviedb.pkl')

    One_book = pd.DataFrame({'Name': [book_titles], 'Keywords': [book_labels]})
    df2 = One_book.append(df).reset_index(drop=True)
    df = One_book.append(df).reset_index(drop=True)
    mlb = MultiLabelBinarizer()
    df1 = df.join(pd.DataFrame(mlb.fit_transform(df.pop('Keywords')),
                               columns=mlb.classes_,
                               index=df.index))
    df2 = df1.drop(columns='Name')
    H = cosine_similarity(df2, df2)
    H2 = pd.DataFrame(H).join(df1['Name'])
    max_index = np.argmax(H[0][1:]) + 1
    return 'You might enjoy: \n' + df1['Name'][max_index]
