from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import MultiLabelBinarizer

def get_book_labels(filename,no_features):
    #get stopwords
    stop_nltk=set(stopwords.words("english"))
    stop_custom = {'and', 'best', 'book', 'books', 'character', 'characters', 'did', 'end', 'ending', 'film', 'films', 'great',
                   'just', 'like', 'make', 'movie', 'movies', 'novel', 'permalink', 'read', 'review', 'story', 'story', 'the',
                   'when','see','seen', 'get', 'many', 'one', 'made', 'ever', 'every', 'vote', 'much', 'well', 'watch', 'even',
                   'everything', 'youll', 'would', 'makes', 'even', 'ive', 'really', 'say', 'two', 'three', 'really', 'time'}
    stop_words = stop_nltk.union(stop_custom)

    # get book keywords and title of book, scrape from internet
    r = requests.get(filename)
    html_soup = BeautifulSoup(r.content,features="html5lib")
    coverurl = html_soup.find('img',id='coverImage')['src']
    Title = html_soup.find('h1',id='bookTitle').text.strip()

    # Extract reviews and vectorize the text, returning the keywords
    review_containers = html_soup.find_all('div',class_ ='review')
    for i, review in enumerate(review_containers):
        review_containers[i] = review.find('span', class_ = 'readable').text
    if len(review_containers) < 2:
        return
    Vect = TfidfVectorizer(max_features=no_features, stop_words=stop_words,max_df=0.65)
    Book_Vect = Vect.fit_transform(review_containers)
    Book_feature_names = Vect.get_feature_names()
    book_labels = Book_feature_names
    return Title, book_labels, coverurl
