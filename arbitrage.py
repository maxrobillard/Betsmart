import pandas as pd
import pymongo
from datetime import datetime, date


df = pd.read_csv('data.txt',sep='\t')
df.columns = ['Site', 'equipe_domicile', 'cote_domicile', 'equipe_exterieur', 'cote_exterieur', 'cote_nul']


d = {'Heure du scraping':[datetime.now()]*8,'Championat':["Première League"]*8,'Date du match':[datetime.now().strftime("%d/%m/%Y")]*8}

df_add = pd.DataFrame(d)
df = df.join(df_add)
df = df[['Heure du scraping', 'Date du match', 'Site', 'Championat', 'equipe_domicile', 'cote_domicile', 'equipe_exterieur', 'cote_exterieur', 'cote_nul']]

def data_cleaning(data):
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].replace(',','.',regex=True).astype(float)
    data[['Site', 'equipe_domicile', 'equipe_exterieur']] = data[['Site', 'equipe_domicile', 'equipe_exterieur']].astype(str)
    return data

def by_match(data):
    
    return bets

print(df.head())
df = data_cleaning(df)
print(df)
