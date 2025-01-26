#preprocess

import pandas as pd
import numpy as np

dfNotitolo = pd.read_excel('../../res/data/NEET_NessunTitolo.xlsx',sheet_name = 0)
dfDropped = dfNotitolo.drop(dfNotitolo.index[[0,1,2,3,4]])
dfDropped.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione) - Condizione professionale europea, titolo di studio  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2021 Q3', 'Unnamed: 3': '2021 Q4', 'Unnamed: 4': '2022 Q1', 'Unnamed: 5': '2022 Q2', 'Unnamed: 6': '2022 Q3', 'Unnamed: 7': '2022 Q4'
                            , 'Unnamed: 8': '2023 Q1' , 'Unnamed: 9': '2023 Q2', 'Unnamed: 10': '2023 Q3', 'Unnamed: 11': '2023 Q4', 'Unnamed: 12': '2024 Q1', 'Unnamed: 13': '2024 Q2' , 'Unnamed: 14': '2024 Q3'}, inplace=True)
df = dfDropped.drop(dfDropped.index[[0,1,2]])
df = df[df['Condizione Lavorativa']=='Totale  ']
df['Degree'] = 'None'

dfDiploma = pd.read_excel('../../res/data/NEET_Diploma.xlsx',sheet_name = 0)
dfDropped2 = dfDiploma.drop(dfDiploma.index[[0,1,2,3,4]])
dfDropped2.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione) - Condizione professionale europea, titolo di studio  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2021 Q3', 'Unnamed: 3': '2021 Q4', 'Unnamed: 4': '2022 Q1', 'Unnamed: 5': '2022 Q2', 'Unnamed: 6': '2022 Q3', 'Unnamed: 7': '2022 Q4'
                            , 'Unnamed: 8': '2023 Q1' , 'Unnamed: 9': '2023 Q2', 'Unnamed: 10': '2023 Q3', 'Unnamed: 11': '2023 Q4', 'Unnamed: 12': '2024 Q1', 'Unnamed: 13': '2024 Q2' , 'Unnamed: 14': '2024 Q3'}, inplace=True)
df2 = dfDropped2.drop(dfDropped2.index[[0,1,2]])
df2 = df2[df2['Condizione Lavorativa']=='Totale  ']
df2['Degree'] = 'High School Diploma'

dfLaurea = pd.read_excel('../../res/data/NEET_Laurea.xlsx',sheet_name = 0)
dfDropped3 = dfLaurea.drop(dfLaurea.index[[0,1,2,3,4]])
dfDropped3.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione) - Condizione professionale europea, titolo di studio  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2021 Q3', 'Unnamed: 3': '2021 Q4', 'Unnamed: 4': '2022 Q1', 'Unnamed: 5': '2022 Q2', 'Unnamed: 6': '2022 Q3', 'Unnamed: 7': '2022 Q4'
                            , 'Unnamed: 8': '2023 Q1' , 'Unnamed: 9': '2023 Q2', 'Unnamed: 10': '2023 Q3', 'Unnamed: 11': '2023 Q4', 'Unnamed: 12': '2024 Q1', 'Unnamed: 13': '2024 Q2' , 'Unnamed: 14': '2024 Q3'}, inplace=True)
df3 = dfDropped3.drop(dfDropped3.index[[0,1,2]])
df3 = df3[df3['Condizione Lavorativa']=='Totale  ']
df3['Degree'] = 'Degree/Post-degree'

frames = [df, df2, df3]
NEET_degree = pd.concat(frames)
NEET_degree.rename(columns={'Sesso':'Sex'}, inplace=True)

pd.DataFrame(NEET_degree).replace({'Femmine  ':"Female", 'Maschi  ':"Male", 'Totale  ':"Total"}, inplace=True)

#print(NEET_degree)

df2021Q3 = NEET_degree[['Sex', '2021 Q3', 'Degree']] 
df2021Q3['Year'] = '2021 Q3'
df2021Q3.rename(columns={'2021 Q3':'Value'}, inplace=True)

df2021Q4 = NEET_degree[['Sex', '2021 Q4', 'Degree']] 
df2021Q4['Year'] = '2021 Q4'
df2021Q4.rename(columns={'2021 Q4':'Value'}, inplace=True)

df2022Q1 = NEET_degree[['Sex', '2022 Q1', 'Degree']] 
df2022Q1['Year'] = '2022 Q1'
df2022Q1.rename(columns={'2022 Q1':'Value'}, inplace=True)

df2022Q2 = NEET_degree[['Sex', '2022 Q2', 'Degree']] 
df2022Q2['Year'] = '2022 Q2'
df2022Q2.rename(columns={'2022 Q2':'Value'}, inplace=True)

df2022Q3 = NEET_degree[['Sex', '2022 Q3', 'Degree']] 
df2022Q3['Year'] = '2022 Q3'
df2022Q3.rename(columns={'2022 Q3':'Value'}, inplace=True)

df2022Q4 = NEET_degree[['Sex', '2022 Q4', 'Degree']] 
df2022Q4['Year'] = '2022 Q4'
df2022Q4.rename(columns={'2022 Q4':'Value'}, inplace=True)

df2023Q1 = NEET_degree[['Sex', '2023 Q1', 'Degree']] 
df2023Q1['Year'] = '2023 Q1'
df2023Q1.rename(columns={'2023 Q1':'Value'}, inplace=True)

df2023Q2 = NEET_degree[['Sex', '2023 Q2', 'Degree']] 
df2023Q2['Year'] = '2023 Q2'
df2023Q2.rename(columns={'2023 Q2':'Value'}, inplace=True)

df2023Q3 = NEET_degree[['Sex', '2023 Q3', 'Degree']] 
df2023Q3['Year'] = '2023 Q3'
df2023Q3.rename(columns={'2023 Q3':'Value'}, inplace=True)

df2023Q4 = NEET_degree[['Sex', '2023 Q4', 'Degree']] 
df2023Q4['Year'] = '2023 Q4'
df2023Q4.rename(columns={'2023 Q4':'Value'}, inplace=True)

df2024Q1 = NEET_degree[['Sex', '2024 Q1', 'Degree']] 
df2024Q1['Year'] = '2024 Q1'
df2024Q1.rename(columns={'2024 Q1':'Value'}, inplace=True)

df2024Q2 = NEET_degree[['Sex', '2024 Q2', 'Degree']] 
df2024Q2['Year'] = '2024 Q2'
df2024Q2.rename(columns={'2024 Q2':'Value'}, inplace=True)

df2024Q3 = NEET_degree[['Sex', '2024 Q3', 'Degree']] 
df2024Q3['Year'] = '2024 Q3'
df2024Q3.rename(columns={'2024 Q3':'Value'}, inplace=True)

NEETcorr = pd.concat([df2021Q3,df2021Q4,df2022Q1,df2022Q2, df2023Q3, df2022Q4,df2023Q1,df2023Q2, df2023Q3, df2023Q4,df2024Q1,df2024Q2, df2024Q3])

percorso = '../../src/data/Neet_degree.csv'
NEETcorr.to_csv(percorso, index=False)

df2021mean = NEET_degree[['Sex', '2021 Q3','2021 Q4', 'Degree']] 
df2021mean['Year'] = '2021'
df2021mean['Value'] = ((NEET_degree['2021 Q3']+NEET_degree['2021 Q4'])/2)
df2021mean = df2021mean.drop(['2021 Q3','2021 Q4'],axis=1)

df2022mean = NEET_degree[['Sex', '2022 Q1', '2022 Q2','2022 Q3','2022 Q4', 'Degree']] 
df2022mean['Year'] = '2022'
df2022mean['Value'] = ((NEET_degree['2022 Q1']+NEET_degree['2022 Q2']+NEET_degree['2022 Q3']+NEET_degree['2022 Q4'])/4)
df2022mean = df2022mean.drop(['2022 Q1','2022 Q2','2022 Q3','2022 Q4'],axis=1)

df2023mean = NEET_degree[['Sex', '2023 Q1', '2023 Q2','2023 Q3','2023 Q4', 'Degree']] 
df2023mean['Year'] = '2023'
df2023mean['Value'] = ((NEET_degree['2023 Q1']+NEET_degree['2023 Q2']+NEET_degree['2023 Q3']+NEET_degree['2023 Q4'])/4)
df2023mean = df2023mean.drop(['2023 Q1','2023 Q2','2023 Q3','2023 Q4'],axis=1)

df2024mean = NEET_degree[['Sex', '2024 Q1', '2024 Q2','2024 Q3', 'Degree']] 
df2024mean['Year'] = '2024'
df2024mean['Value'] = ((NEET_degree['2024 Q1']+NEET_degree['2024 Q2']+NEET_degree['2024 Q3'])/3)
df2024mean = df2024mean.drop(['2024 Q1','2024 Q2','2024 Q3'],axis=1)

NEETmean = pd.concat([df2021mean,df2022mean,df2023mean,df2024mean])
NEETmean2 = pd.DataFrame(NEETmean)
NEETmean2['Value'] = NEETmean2['Value'].astype(float)


NEETmean2['Value'] = NEETmean2['Value'].round(2)

NEETmean2 = NEETmean2[NEETmean2['Sex']!='Total']



IncidenzaDF = pd.read_csv('../data/IncidenzaTitolo.csv')
IncidenzaDF = IncidenzaDF[IncidenzaDF['Territorio']=='Italia']
#IncidenzaDF = IncidenzaDF[dfNEETfr['Classe di età']=='15-29 anni']

IncidenzaDF = IncidenzaDF[['Sesso', 'Seleziona periodo', 'Value','Titolo di studio']] 
#print(IncidenzaDF['Seleziona periodo'].unique()) 


years = ['2021', '2022', '2023']
IncidenzaDF = IncidenzaDF[np.isin(IncidenzaDF['Seleziona periodo'],years)]


IncidenzaDF.rename(columns={'Sesso':'Sex', 'Value':'Prop', 'Seleziona periodo':'Year', 'Titolo di studio':'Degree'}, inplace=True)

pd.DataFrame(IncidenzaDF).replace({'femmine':"Female", 'maschi':"Male", 'totale':"Total"}, inplace=True)
IncidenzaDF = IncidenzaDF[IncidenzaDF['Degree']!='Total']

pd.DataFrame(IncidenzaDF).replace({'diploma':'High School Diploma', 'laurea e post-laurea':'Degree/Post-degree', 
 'nessun titolo di studio, licenza di scuola elementare e media':'None'}, inplace=True)


IncidenzaDF['Prop'] = IncidenzaDF['Prop'].round(2)
res = pd.merge(NEETmean2, IncidenzaDF, on=['Sex','Degree', 'Year'])
print(res) 


percorsomean = '../../src/data/Neet_degree_mean.csv'
res.to_csv(percorsomean, index=False)


