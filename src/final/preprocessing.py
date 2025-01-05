#preprocess

import pandas as pd
import numpy as np

df = pd.read_csv('../../src/final/Neet20182023region.csv')

print(df)

#selection of age 15-29 to be coherent with eurostat

df15_29 = df[df['ETA1']=="Y15-29"]
print(df15_29)

print(df15_29['Territorio'].unique())

areasToBeExcluded = ['Nord' ,'Nord-ovest' ,'Nord-est','Centro','Mezzogiorno','Provincia Autonoma Bolzano / Bozen','Provincia Autonoma Trento']

dfRegions = df15_29[~np.isin(df15_29['Territorio'],areasToBeExcluded)]

dfRegions = dfRegions.drop(['TIPO_DATO_FOL','Tipo dato', 'Classe di età', 'Flag Codes', 'Flags', 'Seleziona periodo'], axis=1)
 
dfRegions['Territorio'].replace("Valle d'Aosta / Vallée d'Aoste", "Valle d'Aosta/Vallée d'Aoste", inplace=True)
dfRegions['Territorio'].replace("Trentino Alto Adige / Südtirol", "Trentino-Alto Adige/Südtirol", inplace=True)
#dfRegions['Territorio'].replace("Friuli-Venezia Giulia", "Friuli Venezia Giulia", inplace=True)

print(dfRegions['Territorio'].unique()) 

percorso = '../../src/final/Neet_1529_regions.csv'
dfRegions.to_csv(percorso, index=False)