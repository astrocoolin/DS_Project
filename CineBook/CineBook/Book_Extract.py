from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import requests
from sklearn.preprocessing import MultiLabelBinarizer

def get_book_labels(filename,no_features):
    #temporarily working with an html file
    #f = open(filename)
    #html_soup = BeautifulSoup(f, 'html.parser')
    r = requests.get(filename)
    html_soup = BeautifulSoup(r.content,features="html5lib")
    Title = html_soup.title.text[:-12]
    review_containers = html_soup.find_all('div',class_ ='review')
    for i, review in enumerate(review_containers):
        review_containers[i] = review.find('span', class_ = 'readable').text

    CV = CountVectorizer(max_features=no_features, stop_words='english')
    Book_CV = CV.fit_transform(review_containers)
    Book_feature_names = CV.get_feature_names()
    book_labels = Book_feature_names
    return Title, book_labels