import pandas as pd
import numpy as np
import pymongo
from datetime import datetime, date

colors = {
  'background': '#5D6D7E',
  'text' : 'white',
  'PN': '#2874A6',
  'GN': '#A93226'
}

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
    return data

def what_matches(data):
    data = data[data['Date du match']>datetime.now()][['equipe_domicile','equipe_exterieur']].drop_duplicates()
    return data

def match_dd(data):
    l_dic = []
    data = what_matches(data)
    for i in range(data.shape[0]):
        l_dic.append({'label':df_matches['equipe_domicile'].iloc[i] +' vs '+df_matches['equipe_exterieur'].iloc[i],'value':df_matches['equipe_domicile'].iloc[i]+'/'+df_matches['equipe_exterieur'].iloc[i]})
    return l_dic

def is_a_surebet(data,equipe_1,equipe_2):
    data = data[(data['equipe_domicile']==equipe_1)&( data['equipe_exterieur']==equipe_2)]
    #data[['somme']] = data[['cote_domicile','cote_exterieur','cote_nul']].sum(axis=1)
    mini = data['cote_domicile'].iloc[0] + data['cote_exterieur'].iloc[0] + data['cote_nul'].iloc[0]
    a, b, c = 0, 0, 0
    for k in range(data.shape[0]):
        for i in range(data.shape[0]):
            if k!=i:
                for j in range(data.shape[0]):
                    S = 1/data['cote_domicile'].iloc[k] + 1/data['cote_exterieur'].iloc[i] + 1/data['cote_nul'].iloc[j]
                    if S < mini:
                        mini = S
                        a,b,c = k,i,j
    return mini,data['Site'].iloc[a],data['Site'].iloc[b],data['Site'].iloc[c],data['cote_domicile'].iloc[a],data['cote_exterieur'].iloc[b],data['cote_nul'].iloc[c]

def best_surebet(data):
    df_matches = what_matches(data)
    #comments
    [list_S, list_s1, list_s2, list_s3, liste_e1, liste_e2, list_cote_dom, list_cote_ext, list_cote_nul] = [[] for k in range(9)]
    for k in range(df_matches.shape[0]):
        S, site_1, site_2, site_3, cote_e1, cote_e2, cote_nul = is_a_surebet(data,data['equipe_domicile'].iloc[k],data['equipe_exterieur'].iloc[k])
        list_S.append(S)
        list_s1.append(site_1)
        list_s2.append(site_2)
        list_s3.append(site_3)
        liste_e1.append(data['equipe_domicile'].iloc[k])
        liste_e2.append(data['equipe_exterieur'].iloc[k])
        list_cote_dom.append(cote_e1)
        list_cote_ext.append(cote_e2)
        list_cote_nul.append(cote_nul)
    df = pd.DataFrame({'rate':list_S,'site_1':list_s1,'site_2':list_s2,'site_3':list_s3,'e1':liste_e1,'e2':liste_e2,'cote_e1':list_cote_dom,'cote_e2':list_cote_ext,'cote_nul':list_cote_nul})
    df = df.sort_values(by=['rate'])
    df = df.reset_index(drop=True).drop_duplicates()
    return df


def how_to_bet(data,mise):
    e1 = data['e1']
    e2 = data['e2']
    B1 = data['site_1']
    B2 = data['site_2']
    B3 = data['site_3']
    me1 = mise/data['cote_e1']
    me2 = mise/data['cote_e2']
    mn = mise/data['cote_nul']
    df = pd.DataFrame({'equipe':[e1,e2,'nul'],'mise':[me1,me2,mn],'bookmaker':[B1,B2,B3],'cotes':[data['cote_e1'],data['cote_e2'],data['cote_nul']]})
    return df


def all_bets(data, mise=100):
    i = 0
    list_bets = []
    while i<data.shape[0] and data['rate'].iloc [i]<1:
        list_bets.append(how_to_bet(data.iloc[i],mise))
        i+=1
    return list_bets


def profit(data):
    p = data['mise'].iloc[0]*(data['cotes'].iloc[0]-1)-data['mise'].iloc[1]-data['mise'].iloc[2]
    return p

def all_profits(liste_bets):
    liste_profits = []
    for bet in liste_bets:
        p = profit(bet)
        liste_profits.append(p)
    return liste_profits

def surebet_dd(data,mise=100):
    l_dic = []
    data = all_bets(best_surebet(data),mise)
    for i in range(len(data)):
        surebet =data[i]
        l_dic.append({'label':surebet['equipe'].iloc[0] +' vs '+surebet['equipe'].iloc[1],'value':str(i)})
    return l_dic



df = data_cleaning(df)

df_matches = what_matches(df)
df_bets = best_surebet(df)
bets = all_bets(df_bets,100)

d = [{'label':df_matches['equipe_domicile'].iloc[i] +' vs '+df_matches['equipe_exterieur'].iloc[i],'value':[df_matches['equipe_domicile'].iloc[i]]} for i in range(df_matches.shape[0])]

print(profit(bets[0]))
print(all_profits(bets))
#print(profit_dd(df))
