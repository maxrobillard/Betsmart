import pandas as pd
import numpy as np
import pymongo
from datetime import datetime, date


df = pd.read_csv('data.txt',sep='\t')
df.columns = ['Site', 'Date du scraping', 'Championat','equipe_domicile', 'cote_domicile', 'equipe_exterieur', 'cote_exterieur', 'cote_nul', 'date du match']


def data_cleaning(data):
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].replace(',','.',regex=True).astype(float)
    data[['Site', 'equipe_domicile', 'equipe_exterieur']] = data[['Site', 'equipe_domicile', 'equipe_exterieur']].astype(str)
    data[['Date du scraping']] = pd.to_datetime(data[['Date du scraping']].stack()).unstack()
    #dftemp = data[data['Site']=='zebet']['date du match'].str.split(' ', n=1, expand=True)
    #print(dftemp)
    #data['heure du match'] = np.NaN
    #data['date du match'] = dftemp[0]
    #data['heure du match'] = dftemp[1]
    return data

def what_matches(data):
    data = data[data['Date du scraping']<datetime.now()][['equipe_domicile','equipe_exterieur']].drop_duplicates()
    return data

def is_a_surebet(data,equipe_1,equipe_2):
    data = data[(data['equipe_domicile']==equipe_1)&( data['equipe_exterieur']==equipe_2)]
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].apply(lambda x : 1/x)
    #data[['somme']] = data[['cote_domicile','cote_exterieur','cote_nul']].sum(axis=1)
    mini = 1
    a, b = 0, 0
    for k in range(data.shape[0]):
        for i in range(data.shape[0]):
            if k!=i:
                S = data['cote_domicile'].iloc[k] + data['cote_exterieur'].iloc[i] + data['cote_nul'].iloc[i]
                if S < mini:
                    mini = S
                    a,b = k, i
    if mini == 1:
        return 1,None,None
    return mini,data['Site'].iloc[a],data['Site'].iloc[b]

def best_surebet(data):
    df_matches = what_matches(data)
    list_S = []
    list_s1 = []
    list_s2 = []
    liste_e1 = []
    liste_e2 = []
    for k in range(df_matches.shape[0]):
        S, site_1, site_2 = is_a_surebet(data,data['equipe_domicile'].iloc[k],data['equipe_exterieur'].iloc[k])
        list_S.append(S)
        list_s1.append(site_1)
        list_s2.append(site_2)
        liste_e1.append(data['equipe_domicile'].iloc[k])
        liste_e2.append(data['equipe_exterieur'].iloc[k])
    df = pd.DataFrame({'rate':list_S,'site_1':list_s1,'site_2':list_s2,'e1':liste_e1,'e2':liste_e2})
    df = df.sort_values(by=['rate'])
    return df


df = data_cleaning(df)
#print(df.head())
df1 = df[df['equipe_domicile']==df['equipe_domicile'][0]]

#print(is_a_surebet(df,df['equipe_domicile'][0],df['equipe_exterieur'][0]))

print(best_surebet(df))
