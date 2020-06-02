import matplotlib
from Book_Extract import get_book_labels
from sklearn.preprocessing import MultiLabelBinarizer
from Book_Scrape import googleSearch
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

matplotlib.use('tkAgg')

no_features = 15
book = input()
googleSearch(book)
book_titles,book_labels = get_book_labels('Book_page.html',no_features)
df = pd.read_pickle('Moviedb.pkl')
#df['Keywords'] = df['Keywords'].str.replace("'",'')

One_book = pd.DataFrame({'Name':[book_titles], 'Keywords':[book_labels]})
df2 =One_book.append(df).reset_index(drop=True)
df =One_book.append(df).reset_index(drop=True)
#df = df.append(One_book)
mlb = MultiLabelBinarizer()
df1 = df.join(pd.DataFrame(mlb.fit_transform(df.pop('Keywords')),
                          columns=mlb.classes_,
                          index=df.index))
#print(book_labels)
#print(movie_labels)
