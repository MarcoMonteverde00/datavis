import pandas as pd
import numpy as np
from decimal import Decimal

stateCodes = {}

with open("statecodes.txt", "r") as file:
    line = file.readline()
    while line:

        codeState = line.strip().split(" ")
        code = codeState[0]
        state = " ".join(codeState[1:])
        stateCodes[code] = state
        line = file.readline()


#header = ["State", "Year", "January", "February", "March", 
#          "April", "May", "June", "July", "August",
#          "September", "October", "November", "December"]

header = ["State", "Year", "Month", "Value"]

maxes = []

with open("maxTempData.txt", "r") as file:
    line = file.readline()
    while line:
        cols = line.split()
        state = stateCodes[cols[0][:3]]
        info = cols[0][3]
        year = int(cols[0][6:10])
        values = map(lambda x: Decimal((float(x) - 32) * 5.0/9).quantize(Decimal('1.00')), cols[1:])
        
        for i, v in enumerate(values):
            maxes.append([state, year, i, v])

        line = file.readline()

    
maxes = pd.DataFrame(maxes, columns=header)
percorso_maxes = '../../src/data/countriesMaxTemperatures.csv'
maxes.to_csv(percorso_maxes, index=False)

mins = []

with open("minTempData.txt", "r") as file:
    line = file.readline()
    while line:
        cols = line.split()
        state = stateCodes[cols[0][:3]]
        info = cols[0][3]
        year = int(cols[0][6:10])
        values = map(lambda x: Decimal((float(x) - 32) * 5.0/9).quantize(Decimal('1.00')), cols[1:]) # fahrenheit to celsius
        
        for i, v in enumerate(values):
            mins.append([state, year, i, v])

        line = file.readline()

    
mins = pd.DataFrame(mins, columns=header)
percorso_mins = '../../src/data/countriesMinTemperatures.csv'
mins.to_csv(percorso_mins, index=False)



avgs = []

with open("avgTempData.txt", "r") as file:
    line = file.readline()
    while line:
        cols = line.split()
        state = stateCodes[cols[0][:3]]
        info = cols[0][3]
        year = int(cols[0][6:10])
        values = map(lambda x: Decimal((float(x) - 32) * 5.0/9).quantize(Decimal('1.00')), cols[1:]) # fahrenheit to celsius
        
        for i, v in enumerate(values):
            avgs.append([state, year, i, v])

        line = file.readline()

    
avgs = pd.DataFrame(avgs, columns=header)
percorso_avgs = '../../src/data/countriesAvgTemperatures.csv'
avgs.to_csv(percorso_avgs, index=False)
