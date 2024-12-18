import pandas as pd
import numpy as np
from decimal import Decimal

dfMin = pd.read_csv('../../src/data/countriesMinTemperatures.csv')
dfMax = pd.read_csv('../../src/data/countriesMaxTemperatures.csv')

dfMin['Index'] = 'Min'
dfMax['Index'] = 'Max'

frames = [dfMin, dfMax]

res = pd.concat(frames)
res2 = res[res['State']=='Alabama']
res3 = res2[(res2['Year']==2023 or res2['Year']==2018)]

print (res2['Index'].unique())
print (res3)

percorso_res = '../../src/data/dataRidgeLine.csv'
res2.to_csv(percorso_res, index=False)