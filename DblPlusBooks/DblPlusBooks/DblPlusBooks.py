#!/usr/bin/env python3
from DblPlusBooks import BookProcessing, Movie_Scrape

# for webpage I/O
def rec_movie(bookname):
    nofeatures = 50
    book = Book(bookname,nofeatures)
    movies = Movies(book,nofeatures)
    return book, movies
    #return book_titles, bookimg, movie_sugg, Movie_Scrape.grab_movie_img(movie_sugg)

def print_rec(bookname):
    print(rec_movie(bookname))
