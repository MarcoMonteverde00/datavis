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

ds2022 = pd.read_csv('2022pop.csv')

for year in range(2019,2023):
    df_year = df_cleaned[df_cleaned['Year'] == year]
    df_sorted_year = df_year.sort_values(by=[colname], ascending=False)
    
    population = pd.read_csv(str(year)+'pop.csv')
    population = population.drop(["Code", "Year"], axis=1)
    
    population.rename(columns = {'Population - Sex: all - Age: all - Variant: estimates':'Population'}, inplace = True)
    
    if year != 2022:
        population = pd.merge(population, ds2022.drop(["Code", "Year", "Population"],axis=1), on = 'Entity') 
    
    dsComplete = pd.merge(df_year, population, on='Entity')
    dsComplete = dsComplete.drop(["Year", "Code"], axis=1)
    
    df_continents = dsComplete.dropna(subset=['Continent'])
    df_continents.insert(4, 'Total CO2', df_continents[colname]*df_continents['Population'])
      
    df_stacked = pd.DataFrame()
      
    for continent in ['Europe', 'Asia', 'Africa', 'North America', 'South America', 'Oceania', 'Antarctica']:
        df_continent = df_continents[df_continents['Continent'] == continent].sort_values(by=['Total CO2'], ascending=False)
        df_others = df_continent[5:].groupby('Continent')[colname].sum().reset_index()
        df_others['Entity'] = continent + ' Others'
        df_others_total = df_continent[5:].groupby('Continent')['Total CO2'].sum().reset_index()
        df_others['Total CO2'] = df_others_total['Total CO2']
        df_others_pop = df_continent[5:].groupby('Continent')['Population'].sum().reset_index()
        df_others['Population'] = df_others_pop['Population']
        df_others[colname] = df_others['Total CO2']/df_others['Population']
        df_sum = df_continent.groupby('Continent')[colname].sum().reset_index()
        df_sum['Entity'] = continent + ' Sum'    
        df_sum_total = df_continent.groupby('Continent')['Total CO2'].sum().reset_index()
        df_sum['Total CO2'] = df_sum_total['Total CO2']
        df_sum_pop = df_continent.groupby('Continent')['Population'].sum().reset_index()
        df_sum['Population'] = df_sum_pop['Population']
        df_sum[colname] = df_sum['Total CO2']/df_sum['Population']
        df_continent = pd.concat([df_continent[0:5], df_others, df_sum])
        df_stacked = pd.concat([df_stacked, df_continent])

    percorso_stacked = '../../src/data/co2_'+str(year)+'_stacked.csv'

    tmp1 = df_stacked.to_numpy()

    tmp2 = np.concat([tmp1[i::7] for i in range(7)])

    df_reordered = pd.DataFrame(tmp2, columns=['Entity','Annual CO₂ emissions (per capita)','Population','Continent','Total CO2'])

    #df_reordered = pd.DataFrame(tmp2, columns=['Entity','Annual CO₂ emissions (per capita)','Continent','Total CO2','Population'])

    df_reordered.insert(5, 'Rank', ["1st"] * 6 + ["2nd"] * 6 + ["3rd"] * 6 + ["4th"] * 6 + ["5th"] * 6 + ["Others"] * 6 + ["Total"] * 6 , True)

    df_reordered.to_csv(percorso_stacked, index=False)
        
    percorso = f"../../src/data/co2_{year}.csv"
    df_sorted_year.to_csv(percorso, index=False)

df_mean = df_useful.groupby('Entity')[colname].mean().reset_index()
df_sorted_mean = df_mean.sort_values(by=[colname], ascending=False)


percorso_medie = '../../src/data/co2_2022_mean.csv'

# Salva il DataFrame come CSV

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

'''
def get_continent(country_code):

    try:
        #print(country_name)
        #country_code = countries.get(country_name).alpha2
        # Map ISO codes to continent
        # Example: 'IT' (Italy) would map to 'EU' in this context
        #print(country_name, " ", country_code)

        continent_code = pc.country_alpha2_to_continent_code(country_code[0:2])
        #print(country_name, " ", country_code, " ", continent_code)
        return continent_mapping.get(continent_code, None)
    except Exception:
        print("error for ", country_code)
        return None
    
'''

df2 = pd.read_csv('co2-fossil-plus-land-use.csv')

df2_noNA = df2.dropna()
df2_noWorld = df2_noNA[df2_noNA['Entity']!= 'World']
df2_useful = df2_noWorld[df2_noWorld['Year'] >= 2012]
df2_useful = df2_noWorld[df2_noWorld['Year'] <= 2022]

df2_useful= df2_useful.groupby('Entity').agg(Total=('Annual CO2 emissions including land-use change', 'mean'), Land_Use=('Annual CO2 emissions from land-use change', 'mean'),Fossils=('Annual CO2 emissions','mean')).reset_index()
df2_useful = df2_useful.sort_values(by=['Total'], ascending=False)
df2_useful = df2_useful[0:10]

df_Total= (df2_useful[['Entity', 'Total']].copy()).rename(columns= {'Total':'Value'})
df_Total.insert(2, "Type", 'Total', True)

df_Fossil= (df2_useful[['Entity', 'Fossils']].copy()).rename(columns= {'Fossils':'Value'})
df_Fossil.insert(2, "Type", 'Fossils', True)

df_LandUse= (df2_useful[['Entity', 'Land_Use']].copy()).rename(columns= {'Land_Use':'Value'})
df_LandUse.insert(2, "Type", 'Land_Use', True)

dfHeatmap = pd.concat([df_Total, df_Fossil, df_LandUse])

percorso_ds2 = '../../src/data/co2_by_type_Heatmap.csv'

# Salva il DataFrame come CSV
dfHeatmap.to_csv(percorso_ds2, index=False)


# alluvial preprocess


