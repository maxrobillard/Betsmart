
from flask import Flask, render_template, request
import subprocess
from datetime import datetime
import os
from elasticsearch import Elasticsearch,ElasticsearchException
from elasticsearch.helpers import bulk
import requests
import pandas as pd
import json

from flask_pymongo import PyMongo,MongoClient
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView

LOCAL = False

es_client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])

app = Flask(__name__)


@app.route("/")
def index():
    ping=es_client.ping()
    return render_template("index.html",ping=ping)

@app.route("/scrape")
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


@app.route("/search")
def search():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="127.0.0.1")
