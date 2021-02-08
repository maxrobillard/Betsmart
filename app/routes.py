
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
import dash_table as dt
from flask_bootstrap import Bootstrap

from app.fonctions import arb_fig as fg
from app.fonctions import arbitrage as ar

from app import navbar as nav

import plotly_express as px
import plotly.graph_objects as go


from . import dashapp,mongo,client,MONGO_URI,db,dbbet,server,es_client

colors = {
  'background': 'white',
  'text' : 'white',
  'PN': '#2874A6',
  'GN': '#A93226'
}


@server.route("/")
def index():
    ping=es_client.ping()
    m=client.database_names()
    return render_template("index.html",ping=ping,mongo=m)

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

df = read_mongo()

#df = pd.read_csv('data.txt',sep='\t')
df.columns = ['Date du scraping','Site', 'Championnat','cote_domicile','cote_exterieur', 'cote_nul','equipe_domicile','equipe_exterieur','Date du match']
df = ar.data_cleaning(df)


df_test = pd.read_csv('app/data.txt',sep='\t')
df_test.columns = ['Site','Date du scraping','Championnat','equipe_domicile','cote_domicile','equipe_exterieur','cote_exterieur','cote_nul','Date du match']
df_test = ar.data_cleaning(df_test)
df = pd.concat([df,df_test])

df_matches = ar.what_matches(df)
list_surebets = ar.all_bets(ar.best_surebet(df),100)
df_empty = pd.DataFrame({'Equipe':['Equipe 1', 'Equipe 2', 'Nul'],'Mise':[0,0,0],'Bookmaker':['Netbet','Zebet','Netbet'],'Cote':[0,0,0]})

body = html.Div(style={'backgroundColor': colors['background']},
                            children=[
                                html.Div(nav.Navbar()),
                                html.Div(
                                    className='app-header--title',
                                    children=[
                                        html.H1(className="app-header--title",
                                            id = 'title',
                                            children=f'Dashboard',
                                            style={'textAlign': 'center'}
                                            ),
                                        ],
                                    style={'marginTop':'50px'}
                                ),
                                html.Div(style={'backgroundColor': colors['background']},
                                    children=[
                                        dbc.Row(
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id='match_dropdown',
                                                        options=ar.match_dd(df,df_matches),
                                                        value=df_matches['equipe_domicile'].iloc[0]+'/'+df_matches['equipe_exterieur'].iloc[0],
                                                        #disabled=True,
                                                        multi = True,
                                                        placeholder="Choisissez une match"
                                                    )
                                                ),width=11
                                            ),justify='center',style={'width':'98%','margin-left':'10px'}
                                        ),
                                        dbc.Row([
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Graph(
                                                        id = 'fig_cotes',
                                                        figure = fg.evol_cote(df,'Paris','Marseille','zebet')
                                                    )
                                                ),width=7,style={'width':'98%','margin-left':'20px'}
                                            ),
                                            dbc.Col(
                                                html.Div(children=[
                                                    dbc.Card([
                                                        dbc.CardHeader([
                                                            'Choix du Bookmaker'
                                                        ]),
                                                        dbc.CardBody([
                                                            dbc.RadioItems(
                                                                id='id_radioItems',
                                                                options=[
                                                                    {'label':'Zebet','value':'zebet'},
                                                                    {'label':'Netbet','value':'netbet'},
                                                                ],
                                                                value='zebet'
                                                            )


                                                        ])
                                                    ],)
                                                ]),width=3,style={'width':'98%','margin-left':'15px'}
                                            )
                                        ],align='center',justify='center'),


                                    ]
                                ),
                                html.Div(style={'backgroundColor': colors['background']},
                                    children=[
                                        dbc.Row([
                                            dbc.Col(
                                                html.Div(children=[
                                                    dbc.Card([
                                                        dbc.CardHeader([
                                                            dcc.Dropdown(
                                                                id='surebet_dropdown',
                                                                options=ar.surebet_dd(df),
                                                                value='0',
                                                                #disabled=True,
                                                                multi = False,
                                                                placeholder="Choisissez un paris sur"
                                                            )
                                                        ]),
                                                        dbc.CardBody([
                                                             dt.DataTable(
                                                                 id='table',
                                                                 columns=[{"name":i, "id":i} for i in ['Equipe','Mise','Bookmaker','Cotes']],
                                                                 data = df_empty.to_dict('records')
                                                             )

                                                        ])
                                                    ])
                                                ]),width=5,style={'width':'98%','margin-left':'10px'}

                                            ),
                                            dbc.Col(
                                                html.Div(children=[
                                                    dcc.Graph(id="Profit",
                                                                figure=fg.fig_profit([0,0])

                                                    )
                                                ]),width=5,style={'width':'98%','margin-left':'10px'}

                                            )
                                        ],align='center',justify='center',no_gutters=True),
                                    ]
                                )
                            ]
        )




dashapp.layout = html.Div(children=[body],style={"margin-top":"100px"})


@dashapp.callback(
        Output('fig_cotes','figure'),
        [Input('match_dropdown', 'value'),Input('id_radioItems','value')]
)

def update_fig_evo(match_dropdown,id_radioItems,df=df):
    if isinstance(match_dropdown, str):
        l = match_dropdown.split('/')
        fig = fg.evol_cote(df,l[0],l[1],id_radioItems)
    elif match_dropdown==[]:
        fig = go.Figure()
        fig.update_layout(title = dict(text="Evolution de des cotes du match",
                                font = {"size":30},
                                y=0.97,
                                x=0.5,
                                xanchor = 'center',
                                yanchor  = 'top'),
                    xaxis_title = 'Jours',
                    yaxis_title = 'Cote',
                    paper_bgcolor=colors['background'],
                    font_color=colors['text']
                    )
    else:
        l = []
        for match in match_dropdown:
            e1, e2 = match.split('/')
            l.append(e1)
            l.append(e2)
        fig = fg.evol_cote(df,l[0],l[1],id_radioItems)
        for i in range(2,len(l),2):
            df = df[(df['Site']==id_radioItems)&(df['equipe_domicile']==l[i])]
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_domicile'],name='Cote Domicile ('+l[i]+')'))
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_exterieur'],name='Cote Extérieur ('+l[i]+')'))
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_nul'],name='Cote Nul ('+l[i]+')'))
    return fig

@dashapp.callback(
        [Output('table','data'),
        Output('Profit','figure')],
        [Input('surebet_dropdown', 'value')]
)
def update_table(surebet_dropdown):
    i = int(surebet_dropdown)
    if len(list_surebets) == 0:
        return [df_empty.to_dict('records'),fg.fig_profit([0,0])]
    else:
        return [list_surebets[i].to_dict('records'),
                fg.fig_profit([ar.profit(list_surebets[i]),0])]
