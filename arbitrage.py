import pandas as pd
import pymongo
from datetime import datetime, date


df = pd.read_csv('data.txt',sep='\t')
df.columns = ['Site', 'Date du scraping', 'Championat','equipe_domicile', 'cote_domicile', 'equipe_exterieur', 'cote_exterieur', 'cote_nul', 'date du match']


def data_cleaning(data):
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].replace(',','.',regex=True).astype(float)
    data[['Site', 'equipe_domicile', 'equipe_exterieur']] = data[['Site', 'equipe_domicile', 'equipe_exterieur']].astype(str)
    return data



def by_match(data):
    return bets


df = data_cleaning(df)

df1 = df[df['equipe_domicile']==df['equipe_domicile'][0]]
