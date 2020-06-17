#!/usr/bin/env python3
from flask import Flask, render_template, request
from Books2Films import Movie_Scrape, BookProcessing

def makeapp():
    app = Flask(__name__,template_folder='/home/colin/Insight_Project/templates')
    return app
app = makeapp()

@app.route('/')
@app.route('/index')
def my_form():
    return render_template('index.html')

@app.route('/', methods=["GET", "POST"])  # we are now using these methods to get user input
def dynamic_page():
    output = ""
    if request.method == 'POST':
        book_name = str(request.form['Book_Name'])
        book = BookProcessing.Book(book_name)
        movies = Movie_Scrape.Movies(book)
        #book_title, book_cover,movie_suggestion= DPBooks.rec_movie(book)
        #output = DPBooks.rec_movie(book)
        print(movies.next_best)
        return render_template('results_2.html',
                               book_title = book.title,
                               book_cover = book.coverlink,
                               movie_title_1 = movies.title,
                               movie_title_2 = movies.next_best[0],
                               movie_title_3 = movies.next_best[1],
                               movie_title_4 = movies.next_best[2],
                               movie_cover_1 = movies.grab_movie_img(movies.title_code),
                               movie_cover_2 = movies.grab_movie_img(movies.next_best_code[0]),
                               movie_cover_3 = movies.grab_movie_img(movies.next_best_code[1]),
                               movie_cover_4 = movies.grab_movie_img(movies.next_best_code[2]),
                               keywords=', '.join(list(movies.keywords)))
        
#app.run(host='0.0.0.0', debug = True)

if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
