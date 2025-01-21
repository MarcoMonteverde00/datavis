import pandas as pd

df = pd.read_csv('../../src/data/Neet_FR_Incidenza.csv')

res = df[df['Citizenship']=='Italian']
res = res.drop('Citizenship',axis=1)
res = res.drop('Value',axis=1)
res['POPcategorica']=(res['Sum1']/res['Prop'])*100;

group1 = res[res['Sex']=='Male']
group1 = group1[group1['Year']==2021]
group1['POPtot'] = group1['POPcategorica'].sum()

group2 = res[res['Sex']=='Male']
group2 = group2[group2['Year']==2022]
group2['POPtot'] = group2['POPcategorica'].sum()

group3 = res[res['Sex']=='Male']
group3 = group3[group3['Year']==2023]
group3['POPtot'] = group3['POPcategorica'].sum()

group1a = res[res['Sex']=='Female']
group1a = group1a[group1a['Year']==2021]
group1a['POPtot'] = group1a['POPcategorica'].sum()

group2a = res[res['Sex']=='Female']
group2a = group2a[group2a['Year']==2022]
group2a['POPtot'] = group2a['POPcategorica'].sum()

group3a = res[res['Sex']=='Female']
group3a = group3a[group3a['Year']==2023]
group3a['POPtot'] = group3a['POPcategorica'].sum()

GROUPS = pd.concat([group1, group2, group3, group1a, group2a, group3a])

GROUPS['PropPop'] = (GROUPS['POPcategorica']/GROUPS['POPtot'])*100
GROUPS['PropPop'] = GROUPS['PropPop'].round(2)
#GROUPS['Value'] = GROUPS['Value'].round(2)

print(GROUPS)
percorso = '../../src/data/Neet_FR_POP.csv'
GROUPS.to_csv(percorso, index=False)