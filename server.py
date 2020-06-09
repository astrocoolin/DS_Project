#!/usr/bin/env python3
from DblPlusBooks import DblPlusBooks as DPBooks
from flask import Flask, render_template, request

# Create the application object
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=["GET", "POST"])  # we are now using these methods to get user input
def dynamic_page():
    output = ""
    if request.method == 'POST':
        book = 'The Hobbit'
        try:
            book = str(request.form['Book_Name'])
        except:
            errors += "I don't have any exceptions at this point"
        #book_title, book_cover,movie_suggestion= DPBooks.rec_movie(book)
        output = DPBooks.rec_movie(book)
        return render_template('index.html',book_title=output[0],book_cover = output[1],movie_title=output[2],movie_cover=output[3])
        
    return render_template('index.html',output=result)

if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
