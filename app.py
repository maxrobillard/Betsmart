
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

from flask_pymongo import PyMongo,MongoClient
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from pymongo import MongoClient

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from flask_bootstrap import Bootstrap

LOCAL = False

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

server = Flask(__name__,instance_relative_config= True)
dash = Dash(__name__, server = server, routes_pathname_prefix='/dash/',
				external_stylesheets=[dbc.themes.BOOTSTRAP])

server.config.from_object(Config)
server.config.from_pyfile('config.py')

MONGO_URI = server.config["MONGO_URI"]

admin = Admin(server)
client =  MongoClient(MONGO_URI)
mongo = PyMongo(server)

db=client["mongodb"]
dbbet = db["Bet"]

@server.route("/")
def index():
    ping=es_client.ping()
    m=client.database_names()
    return render_template("index.html",ping=ping,mongo=m)

@server.route("/scrape")
def scrape():
    response = requests.get("http://scraper:9080/crawl.json?spider_name=zebet&url=https://www.zebet.fr/fr/competition/94-premier_league")
    output_json = json.loads(response.text)
    response2 = requests.get("http://scraper:9080/crawl.json?spider_name=netbet&url=https://www.netbet.fr/football/angleterre/premier-league")
    output_json1 = json.loads(response2.text)

    for doc in output_json["items"]:
        try:
            res = es_client.index(index='bet', id=None, body=doc)
            print(res["result"])

        except ElasticsearchException as es1:
            print("Error: ",es1)

    for doc in output_json1["items"]:
        try:
            res = es_client.index(index='bet', id=None, body=doc)
            print(res["result"])

        except ElasticsearchException as es1:
            print("Error: ",es1)
    return render_template('search.html')


@server.route("/search")
def search():
    return render_template('search.html')

@server.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es_client.search(
        index="bet",
        size=50,
        body={
            "query": {
                "multi_match" : {
                    "query": search_term,
                    "fields": [
                        "site",
                        "championnat",
                        "equipe1",
                        "cote1",
                        "equipe2",
                        "cote2",
                        "cote3"
                    ]
                }
            }
        }
    )
    return render_template('results.html', res=res )

body = dbc.Container(
    [

        html.H1('Page 1')

    ],
    className="mt-4",
)

dash.layout = html.Div([body])


if __name__ == "__main__":
    server.run(port=5000, debug=True, host="127.0.0.1")
