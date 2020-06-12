from flask import Flask
app = Flask(__name__,template_folder='templates')

__all__ = [
        'Books2Films',
        'BookProcessing',
        'Movie_Scrape',
]
