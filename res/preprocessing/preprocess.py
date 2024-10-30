from iso3166 import countries
import pandas as pd
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
        print(country_name)
        country_code = countries.get(country_name).alpha2
        # Map ISO codes to continent
        # Example: 'IT' (Italy) would map to 'EU' in this context
        print(country_name, " ", country_code)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        print(country_name, " ", country_code, " ", continent_code)
        return continent_mapping.get(continent_code, None)
    except KeyError:
        return None
    

continents = list(map(get_continent, df_mean['Entity']))
df_mean['Continent'] = continents

df_continents = df_mean.dropna(subset=['Continent'])

#df_continents_sorted = df_continents.sort_values(by=['Continent', colname], ascending=False)

df_europe = df_continents[df_continents['Continent'] == 'Europe'].sort_values(by=[colname], ascending=False)
df_asia = df_continents[df_continents['Continent'] == 'Asia'].sort_values(by=[colname], ascending=False)
df_africa = df_continents[df_continents['Continent'] == 'Africa'].sort_values(by=[colname], ascending=False)
df_northamerica = df_continents[df_continents['Continent'] == 'North America'].sort_values(by=[colname], ascending=False)
df_southamerica = df_continents[df_continents['Continent'] == 'South America'].sort_values(by=[colname], ascending=False)
df_oceania = df_continents[df_continents['Continent'] == 'Oceania'].sort_values(by=[colname], ascending=False)
df_antarctica = df_continents[df_continents['Continent'] == 'Antarctica'].sort_values(by=[colname], ascending=False)

df_europe_others = df_europe[5:].groupby('Continent')[colname].sum().reset_index()
df_europe_others['Entity'] = 'Others'
df_europe_sum = df_europe.groupby('Continent')[colname].sum().reset_index()
df_europe_sum['Entity'] = 'Total'
df_europe = pd.concat([df_europe[0:5], df_europe_others, df_europe_sum])

print(df_europe)