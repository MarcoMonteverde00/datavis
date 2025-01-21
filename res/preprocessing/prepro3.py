#preprocess

import pandas as pd
import numpy as np

df = pd.read_csv('../data/NEET_FamilyRole.csv')


dfNEETfr = df[df['Territorio']=='Italia']
dfNEETfr = dfNEETfr[dfNEETfr['Classe di età']=='15-29 anni']

NEETfinal = dfNEETfr[['Sesso', 'Cittadinanza', 'Ruolo in famiglia', 'Seleziona periodo', 'Value']] 

years = ['2021', '2022', '2023', '2018', '2019', '2020']
NEETyears = NEETfinal[np.isin(NEETfinal['Seleziona periodo'],years)]

#print(NEETfinal['Seleziona periodo'].unique())

NEETyears.rename(columns={'Sesso':'Sex', 'Cittadinanza':'Citizenship', 'Ruolo in famiglia':'Family Role', 'Seleziona periodo':'Year'}, inplace=True)

pd.DataFrame(NEETyears).replace({'femmine':"Female", 'maschi':"Male", 'totale':"Total"}, inplace=True)
pd.DataFrame(NEETyears).replace({'italiano-a': "Italian", 'straniero-a': "Foreigner", 'totale':"Total"}, inplace=True)
pd.DataFrame(NEETyears).replace({'figlio/a':"Son/Daughter", 'genitore': "Parent", 'single, partner senza figli, altro ruolo': "Single/Partner without children/Other", 'Total':"Total"}, inplace=True)

NEETyears = NEETyears[NEETyears['Sex']!='Total']
NEETyears = NEETyears[NEETyears['Family Role']!='Total']
NEETyears = NEETyears[NEETyears['Citizenship']!='Total']

NEETsex = NEETyears[['Sex', 'Family Role', 'Year', 'Value']] 
NEETsex['Factor'] = 'Sex'

NEETcit = NEETyears[['Citizenship', 'Family Role', 'Year', 'Value']] 
NEETcit['Factor'] = 'Citizenship'

NEETfinal = pd.concat([NEETsex,NEETcit])
#print(NEETyears)

NEETyears['Value'] = NEETyears['Value'].astype(float)

group1 = NEETyears[NEETyears['Sex']=='Male']
group1 = group1[group1['Family Role']=="Son/Daughter"]
group1 = group1[group1['Year']=="2021"]
group1['Sum1'] = group1['Value'].sum()
group1['Index'] = 'Sex'

group2 = NEETyears[NEETyears['Sex']=='Female']
group2 = group2[group2['Family Role']=="Son/Daughter"]
group2 = group2[group2['Year']=="2021"]
group2['Sum1'] = group2['Value'].sum()
group2['Index'] = 'Sex'

group3 = NEETyears[NEETyears['Sex']=='Male']
group3 = group3[group3['Family Role']=="Son/Daughter"]
group3 = group3[group3['Year']=="2022"]
group3['Sum1'] = group3['Value'].sum()
group3['Index'] = 'Sex'

group4 = NEETyears[NEETyears['Sex']=='Female']
group4 = group4[group4['Family Role']=="Son/Daughter"]
group4 = group4[group4['Year']=="2022"]
group4['Sum1'] = group4['Value'].sum()
group4['Index'] = 'Sex'

group5 = NEETyears[NEETyears['Sex']=='Male']
group5 = group5[group5['Family Role']=="Son/Daughter"]
group5 = group5[group5['Year']=="2023"]
group5['Sum1'] = group5['Value'].sum()
group5['Index'] = 'Sex'

group6 = NEETyears[NEETyears['Sex']=='Female']
group6 = group6[group6['Family Role']=="Son/Daughter"]
group6 = group6[group6['Year']=="2023"]
group6['Sum1'] = group6['Value'].sum()
group6['Index'] = 'Sex'

group7 = NEETyears[NEETyears['Sex']=='Male']
group7 = group7[group7['Family Role']=="Parent"]
group7 = group7[group7['Year']=="2021"]
group7['Sum1'] = group7['Value'].sum()
group7['Index'] = 'Sex'

group8 = NEETyears[NEETyears['Sex']=='Female']
group8 = group8[group8['Family Role']=="Parent"]
group8 = group8[group8['Year']=="2021"]
group8['Sum1'] = group8['Value'].sum()
group8['Index'] = 'Sex'

group9 = NEETyears[NEETyears['Sex']=='Male']
group9 = group9[group9['Family Role']=="Parent"]
group9 = group9[group9['Year']=="2022"]
group9['Sum1'] = group9['Value'].sum()
group9['Index'] = 'Sex'

group10 = NEETyears[NEETyears['Sex']=='Female']
group10 = group10[group10['Family Role']=="Parent"]
group10 = group10[group10['Year']=="2022"]
group10['Sum1'] = group10['Value'].sum()
group10['Index'] = 'Sex'

group11 = NEETyears[NEETyears['Sex']=='Male']
group11 = group11[group11['Family Role']=="Parent"]
group11 = group11[group11['Year']=="2023"]
group11['Sum1'] = group11['Value'].sum()
group11['Index'] = 'Sex'

group12 = NEETyears[NEETyears['Sex']=='Female']
group12 = group12[group12['Family Role']=="Parent"]
group12 = group12[group12['Year']=="2023"]
group12['Sum1'] = group12['Value'].sum()
group12['Index'] = 'Sex'

group13 = NEETyears[NEETyears['Sex']=='Male']
group13 = group13[group13['Family Role']=="Single/Partner without children/Other"]
group13 = group13[group13['Year']=="2021"]
group13['Sum1'] = group13['Value'].sum()
group13['Index'] = 'Sex'

group14 = NEETyears[NEETyears['Sex']=='Female']
group14 = group14[group14['Family Role']=="Single/Partner without children/Other"]
group14 = group14[group14['Year']=="2021"]
group14['Sum1'] = group14['Value'].sum()
group14['Index'] = 'Sex'

group15 = NEETyears[NEETyears['Sex']=='Male']
group15 = group15[group15['Family Role']=="Single/Partner without children/Other"]
group15 = group15[group15['Year']=="2022"]
group15['Sum1'] = group15['Value'].sum()
group15['Index'] = 'Sex'

group16 = NEETyears[NEETyears['Sex']=='Female']
group16 = group16[group16['Family Role']=="Single/Partner without children/Other"]
group16 = group16[group16['Year']=="2022"]
group16['Sum1'] = group16['Value'].sum()
group16['Index'] = 'Sex'

group17 = NEETyears[NEETyears['Sex']=='Male']
group17 = group17[group17['Family Role']=="Single/Partner without children/Other"]
group17 = group17[group17['Year']=="2023"]
group17['Sum1'] = group17['Value'].sum()
group17['Index'] = 'Sex'

group18 = NEETyears[NEETyears['Sex']=='Female']
group18 = group18[group18['Family Role']=="Single/Partner without children/Other"]
group18 = group18[group18['Year']=="2023"]
group18['Sum1'] = group18['Value'].sum()
group18['Index'] = 'Sex'

groupb1 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb1 = groupb1[groupb1['Family Role']=="Son/Daughter"]
groupb1 = groupb1[groupb1['Year']=="2021"]
groupb1['Sum1'] = groupb1['Value'].sum()
groupb1['Index'] = 'Citizenship'

groupb2 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb2 = groupb2[groupb2['Family Role']=="Son/Daughter"]
groupb2 = groupb2[groupb2['Year']=="2021"]
groupb2['Sum1'] = groupb2['Value'].sum()
groupb2['Index'] = 'Citizenship'

groupb3 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb3 = groupb3[groupb3['Family Role']=="Son/Daughter"]
groupb3 = groupb3[groupb3['Year']=="2022"]
groupb3['Sum1'] = groupb3['Value'].sum()
groupb3['Index'] = 'Citizenship'

groupb4 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb4 = groupb4[groupb4['Family Role']=="Son/Daughter"]
groupb4 = groupb4[groupb4['Year']=="2022"]
groupb4['Sum1'] = groupb4['Value'].sum()
groupb4['Index'] = 'Citizenship'

groupb5 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb5 = groupb5[groupb5['Family Role']=="Son/Daughter"]
groupb5 = groupb5[groupb5['Year']=="2023"]
groupb5['Sum1'] = groupb5['Value'].sum()
groupb5['Index'] = 'Citizenship'

groupb6 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb6 = groupb6[groupb6['Family Role']=="Son/Daughter"]
groupb6 = groupb6[groupb6['Year']=="2023"]
groupb6['Sum1'] = groupb6['Value'].sum()
groupb6['Index'] = 'Citizenship'

groupb7 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb7 = groupb7[groupb7['Family Role']=="Parent"]
groupb7 = groupb7[groupb7['Year']=="2021"]
groupb7['Sum1'] = groupb7['Value'].sum()
groupb7['Index'] = 'Citizenship'

groupb8 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb8 = groupb8[groupb8['Family Role']=="Parent"]
groupb8 = groupb8[groupb8['Year']=="2021"]
groupb8['Sum1'] = groupb8['Value'].sum()
groupb8['Index'] = 'Citizenship'

groupb9 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb9 = groupb9[groupb9['Family Role']=="Parent"]
groupb9 = groupb9[groupb9['Year']=="2022"]
groupb9['Sum1'] = groupb9['Value'].sum()
groupb9['Index'] = 'Citizenship'

groupb10 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb10 = groupb10[groupb10['Family Role']=="Parent"]
groupb10 = groupb10[groupb10['Year']=="2022"]
groupb10['Sum1'] = groupb10['Value'].sum()
groupb10['Index'] = 'Citizenship'

groupb11 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb11 = groupb11[groupb11['Family Role']=="Parent"]
groupb11 = groupb11[groupb11['Year']=="2023"]
groupb11['Sum1'] = groupb11['Value'].sum()
groupb11['Index'] = 'Citizenship'

groupb12 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb12 = groupb12[groupb12['Family Role']=="Parent"]
groupb12 = groupb12[groupb12['Year']=="2023"]
groupb12['Sum1'] = groupb12['Value'].sum()
groupb12['Index'] = 'Citizenship'

groupb13 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb13 = groupb13[groupb13['Family Role']=="Single/Partner without children/Other"]
groupb13 = groupb13[groupb13['Year']=="2021"]
groupb13['Sum1'] = groupb13['Value'].sum()
groupb13['Index'] = 'Citizenship'

groupb14 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb14 = groupb14[groupb14['Family Role']=="Single/Partner without children/Other"]
groupb14 = groupb14[groupb14['Year']=="2021"]
groupb14['Sum1'] = groupb14['Value'].sum()
groupb14['Index'] = 'Citizenship'

groupb15 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb15 = groupb15[groupb15['Family Role']=="Single/Partner without children/Other"]
groupb15 = groupb15[groupb15['Year']=="2022"]
groupb15['Sum1'] = groupb15['Value'].sum()
groupb15['Index'] = 'Citizenship'

groupb16 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb16 = groupb16[groupb16['Family Role']=="Single/Partner without children/Other"]
groupb16 = groupb16[groupb16['Year']=="2022"]
groupb16['Sum1'] = groupb16['Value'].sum()
groupb16['Index'] = 'Citizenship'

groupb17 = NEETyears[NEETyears['Citizenship']=='Italian']
groupb17 = groupb17[groupb17['Family Role']=="Single/Partner without children/Other"]
groupb17 = groupb17[groupb17['Year']=="2023"]
groupb17['Sum1'] = groupb17['Value'].sum()
groupb17['Index'] = 'Citizenship'

groupb18 = NEETyears[NEETyears['Citizenship']=='Foreigner']
groupb18 = groupb18[groupb18['Family Role']=="Single/Partner without children/Other"]
groupb18 = groupb18[groupb18['Year']=="2023"]
groupb18['Sum1'] = groupb18['Value'].sum()
groupb18['Index'] = 'Citizenship'


GROUPS = pd.concat([group1,group2,group3,group4,group5,group6,group7,group8,group9,group10,group11,group12,group13,group14,group15,group16,group17,group18,
groupb1,groupb2,groupb3,groupb4,groupb5,groupb6,groupb7,groupb8,groupb9,groupb10,groupb11,groupb12,groupb13,groupb14,groupb15,groupb16,groupb17,groupb18])

GROUPS['Sum1'] = GROUPS['Sum1'].round(2)

percorso2 = '../../src/data/Neet_FR_TEXT.csv'
GROUPS.to_csv(percorso2, index=False)

GROUPS_Sex = GROUPS[GROUPS['Index']=="Sex"]
percorso3 = '../../src/data/Neet_FR_TEXT_Sex.csv'
GROUPS_Sex.to_csv(percorso3, index=False)


##incidence
IncidenzaDF = pd.read_csv('../data/IncidenzaRole.csv')
IncidenzaDF = IncidenzaDF[IncidenzaDF['Territorio']=='Italia']
print(IncidenzaDF.columns)
IncidenzaDF = IncidenzaDF[['Sesso', 'Seleziona periodo', 'Value','Ruolo in famiglia']] 
years = ['2021', '2022', '2023']
IncidenzaDF = IncidenzaDF[np.isin(IncidenzaDF['Seleziona periodo'],years)]


IncidenzaDF.rename(columns={'Sesso':'Sex', 'Value':'Prop', 'Seleziona periodo':'Year', 'Ruolo in famiglia':'Family Role'}, inplace=True)

pd.DataFrame(IncidenzaDF).replace({'femmine':"Female", 'maschi':"Male", 'totale':"Total"}, inplace=True)
pd.DataFrame(IncidenzaDF).replace({'figlio/a':"Son/Daughter", 'genitore': "Parent", 'single, partner senza figli, altro ruolo': "Single/Partner without children/Other", 'Total':"Total"}, inplace=True)
IncidenzaDF['Prop'] = IncidenzaDF['Prop'].round(2)
IncidenzaDF = IncidenzaDF[IncidenzaDF['Family Role']!='Total']
IncidenzaDF = IncidenzaDF[IncidenzaDF['Sex']!='Total']

res = pd.merge(NEETyears, IncidenzaDF, on=['Sex','Family Role', 'Year'])
percorso = '../../src/data/Neet_FR.csv'
res.to_csv(percorso, index=False)

res2 = pd.merge(GROUPS_Sex, IncidenzaDF, on=['Sex','Family Role', 'Year'])
percorso4 = '../../src/data/Neet_FR_Incidenza.csv'
res2.to_csv(percorso4, index=False)