from flask import Flask

app = Flask(__name__)

from . import server
from NetFics.NetFics import Book_Process
from NetFics.NetFics import Movie_Process
