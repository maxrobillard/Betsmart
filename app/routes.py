
from flask import render_template, request
from datetime import datetime
import os
from elasticsearch import Elasticsearch,ElasticsearchException
import requests
import pandas as pd
import json

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from flask_bootstrap import Bootstrap

from . import dashapp,mongo,client,MONGO_URI,db,dbbet,server,es_client

@server.route("/")
def index():
    ping=es_client.ping()
    m=client.database_names()
    df=read_mongo()
    return render_template("index.html",ping=ping,mongo=m,df=df)

@server.route("/scrape")
def scrape():
    response = requests.get("http://scraper:9080/crawl.json?spider_name=zebet&url=https://www.zebet.fr/fr/competition/94-premier_league")
    output_json = json.loads(response.text)
    response2 = requests.get("http://scraper:9080/crawl.json?spider_name=netbet&url=https://www.netbet.fr/football/angleterre/premier-league?tab=matchs")
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
    try :
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
    except :
        return render_template("index.html",error="Veuillez scraper avant de faire une recherche")
    return render_template('results.html', res=res )


def read_mongo(no_id=True):
    cursor = dbbet.find()
    df = pd.DataFrame(list(cursor))
    if no_id:
        del df['_id']
    return df

body = dbc.Container(
    [

        html.H1('Page 1')

    ],
    className="mt-4",
)

dashapp.layout = html.Div([body])
