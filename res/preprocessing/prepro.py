#preprocess

import pandas as pd
import numpy as np

df1519 = pd.read_excel('../../res/data/Neet1519.xlsx',sheet_name = 0)
dfDropped = df1519.drop(df1519.index[[0,1,2,3,4]])
dfDropped.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione)- Condizione professionale europea, età  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2018', 'Unnamed: 3': '2019', 'Unnamed: 4': '2020', 'Unnamed: 5': '2021', 'Unnamed: 6': '2022', 'Unnamed: 7': '2023'}, inplace=True)
df = dfDropped.drop(dfDropped.index[[0,1]])
dfNEET = df[df['Condizione Lavorativa']=='Totale  ']
dfNEET['Age'] = '15-19 y.o.'

df2024 = pd.read_excel('../../res/data/Neet2024.xlsx',sheet_name = 0)
dfDropped2 = df2024.drop(df2024.index[[0,1,2,3,4]])
dfDropped2.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione)- Condizione professionale europea, età  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2018', 'Unnamed: 3': '2019', 'Unnamed: 4': '2020', 'Unnamed: 5': '2021', 'Unnamed: 6': '2022', 'Unnamed: 7': '2023'}, inplace=True)
df2 = dfDropped2.drop(dfDropped2.index[[0,1]])
dfNEET2 = df2[df2['Condizione Lavorativa']=='Totale  ']
dfNEET2['Age'] = '20-24 y.o.'

df2529 = pd.read_excel('../../res/data/Neet2529.xlsx',sheet_name = 0)
dfDropped3 = df2529.drop(df2024.index[[0,1,2,3,4]])
dfDropped3.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione)- Condizione professionale europea, età  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2018', 'Unnamed: 3': '2019', 'Unnamed: 4': '2020', 'Unnamed: 5': '2021', 'Unnamed: 6': '2022', 'Unnamed: 7': '2023'}, inplace=True)
df3 = dfDropped3.drop(dfDropped3.index[[0,1]])
dfNEET3 = df3[df3['Condizione Lavorativa']=='Totale  ']
dfNEET3['Age'] = '25-29 y.o.'

frames = [dfNEET, dfNEET2, dfNEET3]
NEET = pd.concat(frames)
NEET.rename(columns={'Sesso':'Sex'}, inplace=True)

pd.DataFrame(NEET).replace({'Femmine  ':"Female", 'Maschi  ':"Male", 'Totale  ':"Total"}, inplace=True)

print(NEET)
df2018 = NEET[['Sex', '2018', 'Age']] 
df2018['Year'] = 2018
df2018.rename(columns={'2018':'Value'}, inplace=True)

df2019 = NEET[['Sex', '2019', 'Age']] 
df2019['Year'] = 2019
df2019.rename(columns={'2019':'Value'}, inplace=True)

df2020 = NEET[['Sex', '2020', 'Age']] 
df2020['Year'] = 2020
df2020.rename(columns={'2020':'Value'}, inplace=True)

df2021 = NEET[['Sex', '2021', 'Age']] 
df2021['Year'] = 2021
df2021.rename(columns={'2021':'Value'}, inplace=True)

df2022 = NEET[['Sex', '2022', 'Age']] 
df2022['Year'] = 2022
df2022.rename(columns={'2022':'Value'}, inplace=True)

df2023 = NEET[['Sex', '2023', 'Age']] 
df2023['Year'] = 2023
df2023.rename(columns={'2023':'Value'}, inplace=True)

NEETcorr = pd.concat([df2018,df2019,df2020,df2021,df2022,df2023])
print(type(NEETcorr['Value']))

NEETcorr = NEETcorr[NEETcorr['Sex']!='Total']

IncidenzaDF = pd.read_csv('../data/IncidenzaMaschi.csv')
IncidenzaDF = IncidenzaDF[IncidenzaDF['Territorio']=='Italia']
#IncidenzaDF = IncidenzaDF[dfNEETfr['Classe di età']=='15-29 anni']

IncidenzaDF = IncidenzaDF[['Sesso','Classe di età', 'Seleziona periodo', 'Value']] 

years = [2021, 2022, 2023, 2018, 2019, 2020]
ages = ['15-19 anni','20-24 anni','25-29 anni']
IncidenzaDF = IncidenzaDF[np.isin(IncidenzaDF['Classe di età'],ages)]
IncidenzaDF = IncidenzaDF[np.isin(IncidenzaDF['Seleziona periodo'],years)]

IncidenzaDF.rename(columns={'Sesso':'Sex', 'Classe di età':'Age', 'Value':'Prop', 'Seleziona periodo':'Year'}, inplace=True)

pd.DataFrame(IncidenzaDF).replace({'femmine':"Female", 'maschi':"Male", 'totale':"Total"}, inplace=True)
pd.DataFrame(IncidenzaDF).replace({'15-19 anni':"15-19 y.o.", '20-24 anni':"20-24 y.o.", '25-29 anni':"25-29 y.o."}, inplace=True)
IncidenzaDF['Prop'] = IncidenzaDF['Prop'].round(2)

res = pd.merge(NEETcorr, IncidenzaDF, on=['Sex','Age', 'Year'])

print(res)

#NEETcorr['Prop'] = []
#print(IncidenzaDF)

percorso = '../../src/data/Neet_age_sex.csv'
res.to_csv(percorso, index=False)