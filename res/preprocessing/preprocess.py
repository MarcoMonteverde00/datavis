from iso3166 import countries
import pandas as pd
import numpy as np
import pycountry_convert as pc


df = pd.read_csv('co-emissions-per-capita.csv')
colname = 'Annual CO₂ emissions (per capita)'

missing_values = df[colname].isnull().sum()

print(f"Valori mancanti in 'variabile': {missing_values}")


# Rimuovi le righe con valori mancanti nella colonna 'variabile'
df_cleaned = df.dropna(subset=[colname])

df_useful = df_cleaned[df_cleaned['Year'] >= 2012]
df_useful = df_useful[df_useful['Year'] <= 2022]

df_2022 = df_cleaned[df_cleaned['Year'] == 2022]
df_sorted_2022 = df_2022.sort_values(by=[colname], ascending=False)

df_mean = df_useful.groupby('Entity')[colname].mean().reset_index()
df_sorted_mean = df_mean.sort_values(by=[colname], ascending=False)

percorso = '../../src/data/co2_2022.csv'
percorso_medie = '../../src/data/co2_2022_mean.csv'

# Salva il DataFrame come CSV
df_sorted_2022.to_csv(percorso, index=False)
df_sorted_mean.to_csv(percorso_medie, index=False )

continent_mapping = {
    "EU": "Europe",
    "AS": "Asia",
    "AF": "Africa",
    "NA": "North America",
    "SA": "South America",
    "OC": "Oceania",
    "AN": "Antarctica"
}

def get_continent(country_name):
    try:
        #print(country_name)
        country_code = countries.get(country_name).alpha2
        # Map ISO codes to continent
        # Example: 'IT' (Italy) would map to 'EU' in this context
        #print(country_name, " ", country_code)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        #print(country_name, " ", country_code, " ", continent_code)
        return continent_mapping.get(continent_code, None)
    except KeyError:
        return None
    

continents = list(map(get_continent, df_mean['Entity']))
df_mean['Continent'] = continents

df_continents = df_mean.dropna(subset=['Continent'])

#df_continents_sorted = df_continents.sort_values(by=['Continent', colname], ascending=False)

df_stacked = pd.DataFrame()

for continent in ['Europe', 'Asia', 'Africa', 'North America', 'South America', 'Oceania', 'Antarctica']:
    df_continent = df_continents[df_continents['Continent'] == continent].sort_values(by=[colname], ascending=False)
    df_others = df_continent[5:].groupby('Continent')[colname].sum().reset_index()
    df_others['Entity'] = continent + ' Others'
    df_sum = df_continent.groupby('Continent')[colname].sum().reset_index()
    df_sum['Entity'] = continent + ' Sum'
    df_continent = pd.concat([df_continent[0:5], df_others, df_sum])
    df_stacked = pd.concat([df_stacked, df_continent])

percorso_stacked = '../../src/data/co2_2022_stacked.csv'

tmp1 = df_stacked.to_numpy()

tmp2 = np.concat([tmp1[i::7] for i in range(7)])

df_reordered = pd.DataFrame(tmp2, columns=['Entity','Annual CO₂ emissions (per capita)','Continent'])
#print(df_reordered)
df_reordered.insert(3, 'Rank', ["1st"] * 6 + ["2nd"] * 6 + ["3rd"] * 6 + ["4th"] * 6 + ["5th"] * 6 + ["Others"] * 6 + ["Total"] * 6 , True)

df_reordered.to_csv(percorso_stacked, index=False)
#print(df_stacked)