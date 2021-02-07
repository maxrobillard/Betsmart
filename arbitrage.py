import pandas as pd
import numpy as np
import pymongo
from datetime import datetime, date


df = pd.read_csv('data.txt',sep='\t')
df.columns = ['Site', 'Date du scraping', 'Championat','equipe_domicile', 'cote_domicile', 'equipe_exterieur', 'cote_exterieur', 'cote_nul', 'Date du match']


def data_cleaning(data):
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].replace(',','.',regex=True).astype(float)
    data[['Site', 'equipe_domicile', 'equipe_exterieur']] = data[['Site', 'equipe_domicile', 'equipe_exterieur']].astype(str)
    data[['Date du scraping']] = pd.to_datetime(data[['Date du scraping']].stack()).unstack()
    dfzebet = data[data['Site']=='zebet']
    dfnetbet = data[data['Site']=='netbet']
    date = dfzebet['Date du match'].str.split(' ', n=1, expand=True)
    dfnetbet['heure du match'] = np.NaN
    dfzebet['Date du match'] = date[0].replace('/','-',regex=True) + '-2021'
    dfzebet['heure du match'] = date[1]
    data = pd.concat([dfnetbet,dfzebet])
    data[['Date du match']] = pd.to_datetime(data[['Date du match']].stack()).unstack()
    print(data)
    return data

def what_matches(data):
    data = data[data['Date du match']>datetime.now()][['equipe_domicile','equipe_exterieur']].drop_duplicates()
    return data

def is_a_surebet(data,equipe_1,equipe_2):
    data = data[(data['equipe_domicile']==equipe_1)&( data['equipe_exterieur']==equipe_2)]
    data[['cote_domicile','cote_exterieur','cote_nul']] = data[['cote_domicile','cote_exterieur','cote_nul']].apply(lambda x : 1/x)
    #data[['somme']] = data[['cote_domicile','cote_exterieur','cote_nul']].sum(axis=1)
    mini = data['cote_domicile'].iloc[0] + data['cote_exterieur'].iloc[0] + data['cote_nul'].iloc[0]
    a, b, c = 0, 0, 0
    for k in range(data.shape[0]):
        for i in range(data.shape[0]):
            if k!=i:
                for j in range(data.shape[0]):
                    S = data['cote_domicile'].iloc[k] + data['cote_exterieur'].iloc[i] + data['cote_nul'].iloc[j]
                    if S < mini:
                        mini = S
                        a,b,c = k,i,j
    return mini,data['Site'].iloc[a],data['Site'].iloc[b],data['Site'].iloc[c]

def best_surebet(data):
    df_matches = what_matches(data)
    list_S = []
    list_s1 = []
    list_s2 = []
    list_s3 = []
    liste_e1 = []
    liste_e2 = []
    liste_e3 = []
    for k in range(df_matches.shape[0]):
        S, site_1, site_2, site_3 = is_a_surebet(data,data['equipe_domicile'].iloc[k],data['equipe_exterieur'].iloc[k])
        list_S.append(S)
        list_s1.append(site_1)
        list_s2.append(site_2)
        list_s3.append(site_3)
        liste_e1.append(data['equipe_domicile'].iloc[k])
        liste_e2.append(data['equipe_exterieur'].iloc[k])
        liste_e3.append(data['equipe_domicile'].iloc[k])
    df = pd.DataFrame({'rate':list_S,'site_1':list_s1,'site_2':list_s2,'e1':liste_e1,'e2':liste_e2})
    df = df.sort_values(by=['rate'])
    return df


df = data_cleaning(df)
#print(df.head())
df1 = df[df['equipe_domicile']==df['equipe_domicile'][0]]

#print(is_a_surebet(df,df['equipe_domicile'][0],df['equipe_exterieur'][0]))

print(best_surebet(df))
