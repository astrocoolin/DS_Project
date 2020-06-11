#!/usr/bin/env python3
from flask import Flask, render_template, request
from DblPlusBooks import Movie_Scrape, BookProcessing

app = Flask(__name__)
app.run(host='0.0.0.0', debug = True)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=["GET", "POST"])  # we are now using these methods to get user input
def dynamic_page():
    output = ""
    if request.method == 'POST':
        nofeatures = 25
        try:
            book_name = str(request.form['Book_Name'])
            book = BookProcessing.Book(book_name,nofeatures)
            movies = Movie_Scrape.Movies(book,nofeatures)
        except:
            errors += "I don't have any exceptions at this point"
        #book_title, book_cover,movie_suggestion= DPBooks.rec_movie(book)
        #output = DPBooks.rec_movie(book)
        return render_template('index.html',book_title=book.title,book_cover = book.coverlink,movie_title=movies.title,
                               movie_cover=movies.coverlink,sugg_two=movies.second_best,sugg_three=movies.third_best,
                               keywords=', '.join(list(set(book.keywords).intersection(movies.keywords))))
        
    return render_template('index.html',output=result)

if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
