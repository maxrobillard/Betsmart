from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from flask_bootstrap import Bootstrap

from flask import Flask
from datetime import datetime
import os
from elasticsearch import Elasticsearch,ElasticsearchException
from elasticsearch.helpers import bulk
import requests
import pandas as pd
import json

from config import Config

from flask_pymongo import PyMongo,MongoClient
from flask_admin import Admin
from pymongo import MongoClient



LOCAL = False

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

server = Flask(__name__,instance_relative_config= True)
dashapp = Dash(__name__,title='Dashboard', server = server, routes_pathname_prefix='/dash/')

Bootstrap(server)

server.config.from_object(Config)
server.config.from_pyfile('config.py')

MONGO_URI = server.config["MONGO_URI"]

admin = Admin(server)
client =  MongoClient(MONGO_URI)
mongo = PyMongo(server)

db=client["mongodb"]
dbbet = db["Bet"]
from . import routes
