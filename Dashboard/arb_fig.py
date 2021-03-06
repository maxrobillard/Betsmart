import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from arbitrage import df, colors

fig_evol_cote = px.line(df[df['Site']=='zebet'], x='Date du scraping', y=['cote_domicile','cote_exterieur','cote_nul'],color='equipe_domicile')


def evol_cote(df,equipe_dom,equipe_ext,site):
    df = df[(df['Site']==site)&(df['equipe_domicile']==equipe_dom)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_domicile'],name='Cote Domicile'))
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_exterieur'],name='Cote Extérieur'))
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_nul'],name='Cote Nul'))
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
    return fig

fig_cote = evol_cote(df,'Leicester','Liverpool','zebet')


def fig_profit(profits):
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = profits[0],                                      #DATA A METTRE --------------------------
        delta = {'position': "top", 'reference': profits[1]},
        #domain = {'x': [0, 1], 'y': [0, 1]}
        ))

    fig.update_layout(title="Profit réalisé",paper_bgcolor = "#212121",font={"color":"#fff"})
    return fig
