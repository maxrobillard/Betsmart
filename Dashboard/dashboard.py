import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
from arb_fig import evol_cote, fig_profit
from arbitrage import what_matches, df, match_dd, colors, best_surebet, all_bets, surebet_dd, all_profits, profit

import plotly_express as px
import plotly.graph_objects as go

import numpy as np


df_matches = what_matches(df)
list_surebets = all_bets(best_surebet(df),100)


app = dash.Dash(__name__,title='Sure Bet',external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(style={'backgroundColor': colors['background']},
                    children=[
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
                        html.Div(
                            children=[
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            dcc.Dropdown(
                                                id='match_dropdown',
                                                options=match_dd(df),
                                                value=df_matches['equipe_domicile'].iloc[0]+'/'+df_matches['equipe_exterieur'].iloc[0],
                                                #disabled=True,
                                                multi = True,
                                                placeholder="Choisissez une match"
                                            )
                                        ),width=11
                                    ),justify='center'
                                ),
                                dbc.Row([
                                    dbc.Col(
                                        html.Div(
                                            dcc.Graph(
                                                id = 'fig_cotes',
                                                figure = evol_cote(df,'Paris','Marseille','zebet')
                                            )
                                        ),width=8
                                    ),
                                    dbc.Col(
                                        html.Div(children=[
                                            dbc.Card([
                                                dbc.CardHeader([
                                                    'Surebet'
                                                ]),
                                                dbc.CardBody([


                                                ])
                                            ],color="dark")
                                        ]),width=3
                                    )
                                ],align='center',justify='center'),


                            ]
                        ),
                        html.Div(
                            children=[
                                dbc.Row([
                                    dbc.Col(
                                        html.Div(children=[
                                            dbc.Card([
                                                dbc.CardHeader([
                                                    dcc.Dropdown(
                                                        id='surebet_dropdown',
                                                        options=surebet_dd(df),
                                                        value='0',
                                                        #disabled=True,
                                                        multi = False,
                                                        placeholder="Choisissez un paris sur"
                                                    )
                                                ]),
                                                dbc.CardBody([
                                                    dt.DataTable(
                                                        id='table',
                                                        columns=[{"name":i, "id":i} for i in list_surebets[0].columns],
                                                        data = list_surebets[0].to_dict('records')
                                                    )

                                                ])
                                            ],color="dark")
                                        ]),width=5

                                    ),
                                    dbc.Col(
                                        html.Div(children=[
                                            dcc.Graph(id="Profit",
                                                        figure=fig_profit(all_profits(all_bets(best_surebet(df))))

                                            )
                                        ]),width=5

                                    )
                                ],align='center',justify='center'),
                            ]
                        )
                    ]
)


###################### CALLBACKS ######################


@app.callback(
        Output('fig_cotes','figure'),
        [Input('match_dropdown', 'value')]
)

def update_fig_evo(match_dropdown,df=df):
    if isinstance(match_dropdown, str):
        l = match_dropdown.split('/')
        fig = evol_cote(df,l[0],l[1],'zebet')
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
        fig = evol_cote(df,l[0],l[1],'zebet')
        for i in range(2,len(l),2):
            df = df[(df['Site']=='zebet')&(df['equipe_domicile']==l[i])]
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_domicile'],name='Cote Domicile ('+l[i]+')'))
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_exterieur'],name='Cote Extérieur ('+l[i+1]+')'))
            fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_nul'],name='Cote Nul ('+l[i]+')'))
    return fig

@app.callback(
        [Output('table','data'),
        Output('Profit','figure')],
        [Input('surebet_dropdown', 'value')]
)
def update_table(surebet_dropdown):
    i = int(surebet_dropdown)
    return [list_surebets[i].to_dict('records'),
            fig_profit([profit(list_surebets[i]),0])]
