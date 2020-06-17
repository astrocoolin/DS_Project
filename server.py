#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from Books2Films import Movie_Scrape, BookProcessing


def makeapp():
    app = Flask(__name__,template_folder='/home/colin/Insight_Project/templates')
    return app
app = makeapp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading')
def intermediate():
    #movies.compare_book(book)
    return render_template('intermediate.html')#, book_title=book.title, book_cover=book.coverlink)

@app.route('/results')
def delivery():
    #movies.compare_book(book)
    return render_template('results_2.html')#,
                       #book_title = book.title,
                       #movie_title_1=movies.title,
                       #movie_title_2=movies.next_best[0],
                       #movie_title_3=movies.next_best[1],
                       #movie_title_4=movies.next_best[2],
                       #movie_cover_1=movies.grab_movie_img(movies.title_code),
                       #movie_cover_2=movies.grab_movie_img(movies.next_best_code[0]),
                       #movie_cover_3=movies.grab_movie_img(movies.next_best_code[1]),
                       #movie_cover_4=movies.grab_movie_img(movies.next_best_code[2]),
                       #keywords=', '.join(list(movies.keywords)))


@app.route('/', methods=["POST"])  # we are now using these methods to get user input
def dynamic_page():
    #book = BookProcessing.Book()
    #movies = Movie_Scrape.Movies()
    if request.method == 'POST':
        book_name = str(request.form['Book_Name'])
        #book.get(book_name)
        return redirect('/results')

#app.run(host='0.0.0.0', debug = True)

if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
