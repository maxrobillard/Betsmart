from flask import Flask, render_template, request
import subprocess
from datetime import datetime
import os
from elasticsearch import Elasticsearch,ElasticsearchException
from elasticsearch.helpers import bulk
import requests
import pandas as pd
import json

from config import Config

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
#import dash_bootstrap_components as dbc

from flask_pymongo import PyMongo,MongoClient
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from pymongo import MongoClient


server = Flask(__name__, instance_relative_config = True)

#app_dash = Dash(__name__, server = server, routes_pathname_prefix='/dash/',
				#external_stylesheets=[dbc.themes.BOOTSTRAP]
#                )

LOCAL = False

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])


server.config.from_object(Config)
server.config.from_pyfile('config.py')

MONGO_URI = server.config["MONGO_URI"]

admin = Admin(server)
client =  MongoClient(MONGO_URI)
mongo = PyMongo(server)

db=client["mongodb"]
dbbet = db["Bet"]
