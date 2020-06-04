#!/usr/bin/env python3
import CineBook.CinebBook
from flask import Flask, render_template, request

# Create the application object
app = Flask(__name__)

#@app.route('/parse_data', methods=['GET', 'POST'])
#def parse_data(data):
#    if request.method == "POST":
@app.route('/', methods=["GET", "POST"])  # we are now using these methods to get user input
def dynamic_page():
    return project()
#def home_page():
#    return render_template('index.html')  # render a template


#@app.route('/output')
#def recommendation_output():
#    #
#    # Pull input
#    some_input = request.args.get('user_input')
#
#    # Case if empty
#    if some_input == "'":
#        return render_template("index.html",
#                               my_input=some_input,
#                               my_form_result="Empty")
#    else:
#        some_output = "yeay!"
#        some_number = 3
#        some_image = "giphy.gif"
#        return render_template("index.html",
#                               my_input=some_input,
#                               my_output=some_output,
#                               my_number=some_number,
#                               my_img_name=some_image,
#                               my_form_result="NotEmpty")
#

# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
