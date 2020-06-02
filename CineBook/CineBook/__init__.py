#!/usr/bin/env python3

import matplotlib
from Book_Extract import get_book_labels
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from Book_Scrape import googleSearch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('tkAgg')
book = input()
book_page = googleSearch(book)
print(book_page,'this is book')
no_features = 15
#book_titles,book_labels = get_book_labels('../../data/Book_page.html',no_features)
book_titles,book_labels = get_book_labels(book_page,no_features)
df = pd.read_pickle('../../data/Moviedb.pkl')
#df['Keywords'] = df['Keywords'].str.replace("'",'')

One_book = pd.DataFrame({'Name':[book_titles], 'Keywords':[book_labels]})
df2 =One_book.append(df).reset_index(drop=True)
df =One_book.append(df).reset_index(drop=True)
#df = df.append(One_book)
mlb = MultiLabelBinarizer()
df1 = df.join(pd.DataFrame(mlb.fit_transform(df.pop('Keywords')),
                          columns=mlb.classes_,
                          index=df.index))
df2 = df1.drop(columns='Name')
H = cosine_similarity(df2,df2)
H2 = pd.DataFrame(H).join(df1['Name'])
max_index = np.argmax(H[0][1:])+1
print('You might enjoy', df1['Name'][max_index])
#print(H2)
#plt.imshow(H, cmap='bwr')
#plt.colorbar()
#plt.show()

