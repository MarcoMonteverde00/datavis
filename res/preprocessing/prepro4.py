#preprocess

import pandas as pd
import numpy as np

ds = pd.read_excel('../../res/data/NEET_Sex.xlsx',sheet_name = 0)
dfDropped = ds.drop(ds.index[[0,1,2,3,4]])
dfDropped.rename(columns={'NEET (giovani non occupati e non in istruzione e formazione)- Condizione professionale europea, età  ': 'Sesso','Unnamed: 1': 'Condizione Lavorativa', 'Unnamed: 2': '2018', 'Unnamed: 3': '2019', 'Unnamed: 4': '2020', 'Unnamed: 5': '2021', 'Unnamed: 6': '2022', 'Unnamed: 7': '2023'}, inplace=True)
df = dfDropped.drop(dfDropped.index[[0,1]])
NEET = df[df['Condizione Lavorativa']=='Totale  ']

NEET.rename(columns={'Sesso':'Sex'}, inplace=True)

df2018 = NEET[['Sex', '2018']] 
df2018['Year'] = 2018
df2018.rename(columns={'2018':'Value'}, inplace=True)

df2019 = NEET[['Sex', '2019']] 
df2019['Year'] = 2019
df2019.rename(columns={'2019':'Value'}, inplace=True)

df2020 = NEET[['Sex', '2020']] 
df2020['Year'] = 2020
df2020.rename(columns={'2020':'Value'}, inplace=True)

df2021 = NEET[['Sex', '2021']] 
df2021['Year'] = 2021
df2021.rename(columns={'2021':'Value'}, inplace=True)

df2022 = NEET[['Sex', '2022']] 
df2022['Year'] = 2022
df2022.rename(columns={'2022':'Value'}, inplace=True)

df2023 = NEET[['Sex', '2023']] 
df2023['Year'] = 2023
df2023.rename(columns={'2023':'Value'}, inplace=True)

NEETcorr = pd.concat([df2018,df2019,df2020,df2021,df2022,df2023])
pd.DataFrame(NEETcorr).replace({'Femmine  ':"Female", 'Maschi  ':"Male", 'Totale  ':"Total"}, inplace=True)

NEETcorr = NEETcorr[NEETcorr['Sex']!='Total']

NEETcorr['Prop']= [21.3,25.2,20.1,24.1,21.8,25.8,21.2,25.0,17.7,20.5,14.4,17.8]

percorso = '../../src/data/Neet_sex.csv'
NEETcorr.to_csv(percorso, index=False)