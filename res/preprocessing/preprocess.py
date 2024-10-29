import pandas as pd
df = pd.read_csv('co-emissions-per-capita.csv')
colname = 'Annual CO₂ emissions (per capita)'

missing_values = df[colname].isnull().sum()

print(f"Valori mancanti in 'variabile': {missing_values}")


# Rimuovi le righe con valori mancanti nella colonna 'variabile'
df_cleaned = df.dropna(subset=[colname])

df_useful = df_cleaned[df_cleaned['Year'] >= 2012]
df_useful = df_useful[df_useful['Year'] <= 2022]

df_mean = df_useful.groupby('Entity')[colname].mean()

df_2022 = df_cleaned[df_cleaned['Year'] == 2022]


# Salva il DataFrame come CSV
#df2022.to_csv(percorso, index=False)

# Controlla i valori mancanti nella colonna 'variabile'





df_sorted_2022 = df_2022.sort_values(by=[colname], ascending=False)

percorso = '../../src/data/co2_2022.csv'
per2 = '../../src/data/co2_2022_mean.csv'

# Salva il DataFrame come CSV
df_sorted_2022.to_csv(percorso, index=False)
df_mean.to_csv(per2, index=False )