import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from arbitrage import df

fig_evol_cote = px.line(df[df['Site']=='zebet'], x='Date du scraping', y=['cote_domicile','cote_exterieur','cote_nul'],color='equipe_domicile')


def evol_cote(df,equipe_dom,equipe_ext,site):
    df = df[(df['Site']==site)&(df['equipe_domicile']==equipe_dom)]
    print(df['date du match'])
    shapes = [{
        'type': 'line',
        'xref': df['Date du scraping'],
        'yref': df['cote_domicile'],
        'x0': df['date du match'][0],
        'y0': 0,
        'x1': df['date du match'][0],
        'y1': 10,
    }]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_domicile'],name='Cote Domicile'))
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_exterieur'],name='Cote Extérieur'))
    fig.add_trace(go.Scatter(x=df['Date du scraping'],y=df['cote_nul'],name='Cote Nul'))
    layout = go.Layout(shapes=shapes)
    fig.update_layout(title = dict(text="Evolution de des cotes du match "+equipe_dom+" VS "+equipe_ext,
                                font = {"size":30},
                                y=0.97,
                                x=0.5,
                                xanchor = 'center',
                                yanchor  = 'top'),
                    xaxis_title = 'Jours',
                    yaxis_title = 'Cote',
                    #paper_bgcolor=colors['background'],
                    #font_color=colors['text']
                    )
    return fig

fig_cote = evol_cote(df,'Leicester','Liverpool','zebet')
fig_cote.show()
