#preprocess

import pandas as pd
import numpy as np

df = pd.read_csv('../data/NEET_cit.csv')

dfNEETcit = df[df['Territorio']=='Italia']
dfNEETcit = dfNEETcit[dfNEETcit['Classe di età']=='15-29 anni']
dfNEETcit = dfNEETcit[dfNEETcit['Condizione professionale europea']=='totale']

dfNEETcit = dfNEETcit[['Sesso', 'Cittadinanza', 'Seleziona periodo', 'Value']] 

dfNEETcit = dfNEETcit[dfNEETcit['Cittadinanza']!='totale']
dfNEETcit = dfNEETcit[dfNEETcit['Sesso']!='totale']

dfNEETcit.rename(columns={'Sesso':'Sex', 'Cittadinanza':'Citizenship', 'Seleziona periodo':'Year'}, inplace=True)

pd.DataFrame(dfNEETcit).replace({'femmine':"Female", 'maschi':"Male"}, inplace=True)
pd.DataFrame(dfNEETcit).replace({'italiano-a': "Italian", 'straniero-a': "Foreigner"}, inplace=True)

Incidenza = pd.read_csv('../data/IncidenzaCit.csv')

IncidenzaCit = Incidenza[Incidenza['Territorio']=='Italia']
IncidenzaCit = IncidenzaCit[IncidenzaCit['Classe di età']=='15-29 anni']
IncidenzaCit = IncidenzaCit[['Sesso', 'Cittadinanza', 'Seleziona periodo', 'Value']] 

years = ['2021', '2022', '2023']
IncidenzaCit = IncidenzaCit[np.isin(IncidenzaCit['Seleziona periodo'],years)]


IncidenzaCit = IncidenzaCit[IncidenzaCit['Cittadinanza']!='totale']
IncidenzaCit = IncidenzaCit[IncidenzaCit['Sesso']!='totale']

IncidenzaCit.rename(columns={'Sesso':'Sex', 'Cittadinanza':'Citizenship', 'Seleziona periodo':'Year', 'Value': 'Prop'}, inplace=True)

pd.DataFrame(IncidenzaCit).replace({'femmine':"Female", 'maschi':"Male"}, inplace=True)
pd.DataFrame(IncidenzaCit).replace({'italiano-a': "Italian", 'straniero-a': "Foreigner"}, inplace=True)

IncidenzaCit['Prop'] = IncidenzaCit['Prop'].round(2)
res = pd.merge(dfNEETcit, IncidenzaCit, on=['Sex','Citizenship', 'Year'])

res['POPcategorica']=(res['Value']/res['Prop'])*100

group1 = res[res['Sex']=='Male']
group1 = group1[group1['Year']=='2021']
group1['POPtot'] = group1['POPcategorica'].sum()

group2 = res[res['Sex']=='Male']
group2 = group2[group2['Year']=='2022']
group2['POPtot'] = group2['POPcategorica'].sum()

group3 = res[res['Sex']=='Male']
group3 = group3[group3['Year']=='2023']
group3['POPtot'] = group3['POPcategorica'].sum()

group1a = res[res['Sex']=='Female']
group1a = group1a[group1a['Year']=='2021']
group1a['POPtot'] = group1a['POPcategorica'].sum()

group2a = res[res['Sex']=='Female']
group2a = group2a[group2a['Year']=='2022']
group2a['POPtot'] = group2a['POPcategorica'].sum()

group3a = res[res['Sex']=='Female']
group3a = group3a[group3a['Year']=='2023']
group3a['POPtot'] = group3a['POPcategorica'].sum()

GROUPS = pd.concat([group1, group2, group3, group1a, group2a, group3a])

GROUPS['PropPop'] = (GROUPS['POPcategorica']/GROUPS['POPtot'])*100
GROUPS['PropPop'] = GROUPS['PropPop'].round(2)
GROUPS['Value'] = GROUPS['Value'].round(2)

print(GROUPS)

percorso = '../../src/data/Neet_CIT.csv'
GROUPS.to_csv(percorso, index=False)