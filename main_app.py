from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import sys

sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')
from database_scripts import db_execution_objs as postsql_db_funcs

app = Flask(__name__)
api = Api(app)

class comment_word (Resource):
    def get (self):
        cursor = postsql_db_funcs.get_db_funct_object()[0] #returns both a cursor and connection