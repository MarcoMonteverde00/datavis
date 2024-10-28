import pandas as pd

emissions = pd.read_csv("co-emissions-per-capita.csv")

emissions2022 = emissions[emissions["Year"] == 2022]

emissions_top_20 = emissions2022.sort_values(by="Annual CO₂ emissions (per capita)", ascending=False)[:20]

emissions_top_20.to_csv("../data/top_20.csv", index=False)