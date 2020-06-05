import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse

def googleSearch(query):
    query = query+' site:Goodreads.com'
    g_clean = [ ] #this is the list we store the search results
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)#this is the actual query we are going to scrape
    html = requests.get(url)
    soup = BeautifulSoup(html.text,features="html5lib")
    a = soup.find_all('a') # a is a list
    a[0].get('href')
    for i in a:
        k = i.get('href')
        try:
            m = re.search("(?P<url>https?://[^\s]+)", k)
            n = m.group(0)
            rul = n.split('&')[0]
            domain = urlparse(rul)
            if(re.search('google.com', domain.netloc)):
                continue
            else:
                g_clean.append(rul)
        except:
            continue
    return g_clean[0]
