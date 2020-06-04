#!/usr/bin/env python3
from flask import Flask,request
from CineBook import CineBook as CB

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    if request.method == "POST":
        book = 'Oryx and Crake'
        try:
            book = str(request.form["Book_Name"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["Book_Name"])
        result = CB.rec_movie(book)
        return '''
                <html>
                    <body>
                        <p>{result}</p>
                        <p><a href="/">Click here to try again!</a>
                    </body>
                </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
                <p>Enter your numbers:</p>
                <form method="post" action=".">
                    <p><input name="Book_Name" /></p>
                    <p><input type="submit" value="Find Film" /></p>
                </form>
            </body>
        </html>
    '''


if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/

