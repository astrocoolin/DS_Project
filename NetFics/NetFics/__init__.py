from flask import Flask
app = Flask(__name__,template_folder='templates')

__all__ = [
        'NetFics',
        'Book_Process',
        'Movie_Process',
]
