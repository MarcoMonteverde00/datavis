import pandas as pd
df = pd.read_csv('./sample_data/owid-co2-data.csv')
df2022 = df[df['year'] == 2022]
percorso = 'co2_2022.csv'

# Salva il DataFrame come CSV
df2022.to_csv(percorso, index=False)

# Controlla i valori mancanti nella colonna 'variabile'
missing_values = df2022['co2_per_capita'].isnull().sum()
print(f"Valori mancanti in 'variabile': {missing_values}")

# Rimuovi le righe con valori mancanti nella colonna 'variabile'
df_cleaned = df2022.dropna(subset=['co2_per_capita'])

percorso = 'co2_2022_cleaned.csv'

# Salva il DataFrame come CSV
df_cleaned.to_csv(percorso, index=False)
