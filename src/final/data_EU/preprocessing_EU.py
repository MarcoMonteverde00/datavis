#preprocess
import pandas as pd
import numpy as np

############################################################################################################
### EU NEET (percentage) dataset
df = pd.read_csv('./EU_NEET_PERC.csv')
df15_29 = df[df['age']=="Y15-29"]

areasToBeExcluded = [] #['Euro area – 20 countries (from 2023)', 'European Union - 27 countries (from 2020)']
dfCountries = df15_29[~np.isin(df15_29['Geopolitical entity (reporting)'],areasToBeExcluded)]
dfCountries = dfCountries.drop(['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'freq', 'Time frequency', 'Sex', 'Age class', 'Unit of measure', 'Time', 'Observation value', 'OBS_FLAG', 'Observation status (Flag)'], axis=1)

dfCountries['Geopolitical entity (reporting)'].replace("Türkiye", "Turkey", inplace=True)
dfCountries['Geopolitical entity (reporting)'].replace("Bosnia and Herzegovina", "Bosnia", inplace=True)
dfCountries['Geopolitical entity (reporting)'].replace("North Macedonia", "Macedonia", inplace=True)

print("\n\nPreprocessed: EU NEET (percentage) dataset:\n")
print(dfCountries['Geopolitical entity (reporting)'].unique()) 

path = './preprocessed/EU_NEET_PERC_preproc.csv'
dfCountries.to_csv(path, index=False)

dfAustria = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Austria']
#dfAustria = dfAustria.drop(['Geopolitical entity (reporting)'], axis=1)
dfAustria.to_csv('./preprocessed/EU_NEET_PERC_Austria_preproc.csv', index=False)

dfBelgium = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Belgium']
#dfBelgium = dfBelgium.drop(['Geopolitical entity (reporting)'], axis=1)
dfBelgium.to_csv('./preprocessed/EU_NEET_PERC_Belgium_preproc.csv', index=False)

dfBulgaria = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Bulgaria']
#dfBulgaria = dfBulgaria.drop(['Geopolitical entity (reporting)'], axis=1)
dfBulgaria.to_csv('./preprocessed/EU_NEET_PERC_Bulgaria_preproc.csv', index=False)

dfCroatia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Croatia']
#dfCroatia = dfCroatia.drop(['Geopolitical entity (reporting)'], axis=1)
dfCroatia.to_csv('./preprocessed/EU_NEET_PERC_Croatia_preproc.csv', index=False)

dfCyprus = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Cyprus']
#dfCyprus = dfCyprus.drop(['Geopolitical entity (reporting)'], axis=1)
dfCyprus.to_csv('./preprocessed/EU_NEET_PERC_Cyprus_preproc.csv', index=False)

dfCzechia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Czechia']
#dfCzechia = dfCzechia.drop(['Geopolitical entity (reporting)'], axis=1)
dfCzechia.to_csv('./preprocessed/EU_NEET_PERC_Czechia_preproc.csv', index=False)

dfDenmark = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Denmark']
#dfDenmark = dfDenmark.drop(['Geopolitical entity (reporting)'], axis=1)
dfDenmark.to_csv('./preprocessed/EU_NEET_PERC_Denmark_preproc.csv', index=False)

dfEstonia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Estonia']
#dfEstonia = dfEstonia.drop(['Geopolitical entity (reporting)'], axis=1)
dfEstonia.to_csv('./preprocessed/EU_NEET_PERC_Estonia_preproc.csv', index=False)

dfFinland = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Finland']
#dfFinland = dfFinland.drop(['Geopolitical entity (reporting)'], axis=1)
dfFinland.to_csv('./preprocessed/EU_NEET_PERC_Finland_preproc.csv', index=False)

dfFrance = dfCountries[dfCountries['Geopolitical entity (reporting)']=='France']
#dfFrance = dfFrance.drop(['Geopolitical entity (reporting)'], axis=1)
dfFrance.to_csv('./preprocessed/EU_NEET_PERC_France_preproc.csv', index=False)

dfGermany = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Germany']
#dfGermany = dfGermany.drop(['Geopolitical entity (reporting)'], axis=1)
dfGermany.to_csv('./preprocessed/EU_NEET_PERC_Germany_preproc.csv', index=False)

dfGreece = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Greece']
#dfGreece = dfGreece.drop(['Geopolitical entity (reporting)'], axis=1)
dfGreece.to_csv('./preprocessed/EU_NEET_PERC_Greece_preproc.csv', index=False)

dfHungary = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Hungary']
#dfHungary = dfHungary.drop(['Geopolitical entity (reporting)'], axis=1)
dfHungary.to_csv('./preprocessed/EU_NEET_PERC_Hungary_preproc.csv', index=False)

dfIreland = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Ireland']
#dfIreland = dfIreland.drop(['Geopolitical entity (reporting)'], axis=1)
dfIreland.to_csv('./preprocessed/EU_NEET_PERC_Ireland_preproc.csv', index=False)

dfItaly = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Italy']
#dfItaly = dfItaly.drop(['Geopolitical entity (reporting)'], axis=1)
dfItaly.to_csv('./preprocessed/EU_NEET_PERC_Italy_preproc.csv', index=False)

dfLatvia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Latvia']
#dfLatvia = dfLatvia.drop(['Geopolitical entity (reporting)'], axis=1)
dfLatvia.to_csv('./preprocessed/EU_NEET_PERC_Latvia_preproc.csv', index=False)

dfLithuania = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Lithuania']
#dfLithuania = dfLithuania.drop(['Geopolitical entity (reporting)'], axis=1)
dfLithuania.to_csv('./preprocessed/EU_NEET_PERC_Lithuania_preproc.csv', index=False)

dfLuxembourg = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Luxembourg']
#dfLuxembourg = dfLuxembourg.drop(['Geopolitical entity (reporting)'], axis=1)
dfLuxembourg.to_csv('./preprocessed/EU_NEET_PERC_Luxembourg_preproc.csv', index=False)

dfMalta = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Malta']
#dfMalta = dfMalta.drop(['Geopolitical entity (reporting)'], axis=1)
dfMalta.to_csv('./preprocessed/EU_NEET_PERC_Malta_preproc.csv', index=False)

dfNetherlands = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Netherlands']
#dfNetherlands = dfNetherlands.drop(['Geopolitical entity (reporting)'], axis=1)
dfNetherlands.to_csv('./preprocessed/EU_NEET_PERC_Netherlands_preproc.csv', index=False)

dfPoland = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Poland']
#dfPoland = dfPoland.drop(['Geopolitical entity (reporting)'], axis=1)
dfPoland.to_csv('./preprocessed/EU_NEET_PERC_Poland_preproc.csv', index=False)

dfPortugal = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Portugal']
#dfPortugal = dfPortugal.drop(['Geopolitical entity (reporting)'], axis=1)
dfPortugal.to_csv('./preprocessed/EU_NEET_PERC_Portugal_preproc.csv', index=False)

dfRomania = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Romania']
#dfRomania = dfRomania.drop(['Geopolitical entity (reporting)'], axis=1)
dfRomania.to_csv('./preprocessed/EU_NEET_PERC_Romania_preproc.csv', index=False)

dfSlovakia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Slovakia']
#dfSlovakia = dfSlovakia.drop(['Geopolitical entity (reporting)'], axis=1)
dfSlovakia.to_csv('./preprocessed/EU_NEET_PERC_Slovakia_preproc.csv', index=False)

dfSlovenia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Slovenia']
#dfSlovenia = dfSlovenia.drop(['Geopolitical entity (reporting)'], axis=1)
dfSlovenia.to_csv('./preprocessed/EU_NEET_PERC_Slovenia_preproc.csv', index=False)

dfSpain = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Spain']
#dfSpain = dfSpain.drop(['Geopolitical entity (reporting)'], axis=1)
dfSpain.to_csv('./preprocessed/EU_NEET_PERC_Spain_preproc.csv', index=False)

dfSweden = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Sweden']
#dfSweden = dfSweden.drop(['Geopolitical entity (reporting)'], axis=1)
dfSweden.to_csv('./preprocessed/EU_NEET_PERC_Sweden_preproc.csv', index=False)

dfTürkiye = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Turkey']
#dfTürkiye = dfTürkiye.drop(['Geopolitical entity (reporting)'], axis=1)
dfTürkiye.to_csv('./preprocessed/EU_NEET_PERC_Türkiye_preproc.csv', index=False)

dfBosnia_and_Herzegovina = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Bosnia']
#dfBosnia_and_Herzegovina = dfBosnia_and_Herzegovina.drop(['Geopolitical entity (reporting)'], axis=1)
dfBosnia_and_Herzegovina.to_csv('./preprocessed/EU_NEET_PERC_Bosnia_and_Herzegovina_preproc.csv', index=False)

dfSwitzerland = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Switzerland']
#dfSwitzerland = dfSwitzerland.drop(['Geopolitical entity (reporting)'], axis=1)
dfSwitzerland.to_csv('./preprocessed/EU_NEET_PERC_Switzerland_preproc.csv', index=False)

dfIceland = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Iceland']
#dfIceland = dfIceland.drop(['Geopolitical entity (reporting)'], axis=1)
dfIceland.to_csv('./preprocessed/EU_NEET_PERC_Iceland_preproc.csv', index=False)

dfMontenegro = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Montenegro']
#dfMontenegro = dfMontenegro.drop(['Geopolitical entity (reporting)'], axis=1)
dfMontenegro.to_csv('./preprocessed/EU_NEET_PERC_Montenegro_preproc.csv', index=False)

dfNorth_Macedonia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Macedonia']
#dfNorth_Macedonia = dfNorth_Macedonia.drop(['Geopolitical entity (reporting)'], axis=1)
dfNorth_Macedonia.to_csv('./preprocessed/EU_NEET_PERC_North_Macedonia_preproc.csv', index=False)

dfNorway = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Norway']
#dfNorway = dfNorway.drop(['Geopolitical entity (reporting)'], axis=1)
dfNorway.to_csv('./preprocessed/EU_NEET_PERC_Norway_preproc.csv', index=False)

dfSerbia = dfCountries[dfCountries['Geopolitical entity (reporting)']=='Serbia']
#dfSerbia = dfSerbia.drop(['Geopolitical entity (reporting)'], axis=1)
dfSerbia.to_csv('./preprocessed/EU_NEET_PERC_Serbia_preproc.csv', index=False)

df2014 = dfCountries[dfCountries['TIME_PERIOD']==2014]
df2014 = df2014.drop(['TIME_PERIOD'], axis=1)
df2014.to_csv('./preprocessed/EU_NEET_PERC_2014_preproc.csv', index=False)

df2015 = dfCountries[dfCountries['TIME_PERIOD']==2015]
df2015 = df2015.drop(['TIME_PERIOD'], axis=1)
df2015.to_csv('./preprocessed/EU_NEET_PERC_2015_preproc.csv', index=False)

df2016 = dfCountries[dfCountries['TIME_PERIOD']==2016]
df2016 = df2016.drop(['TIME_PERIOD'], axis=1)
df2016.to_csv('./preprocessed/EU_NEET_PERC_2016_preproc.csv', index=False)

df2017 = dfCountries[dfCountries['TIME_PERIOD']==2017]
df2017 = df2017.drop(['TIME_PERIOD'], axis=1)
df2017.to_csv('./preprocessed/EU_NEET_PERC_2017_preproc.csv', index=False)

df2018 = dfCountries[dfCountries['TIME_PERIOD']==2018]
df2018 = df2018.drop(['TIME_PERIOD'], axis=1)
df2018.to_csv('./preprocessed/EU_NEET_PERC_2018_preproc.csv', index=False)

df2019 = dfCountries[dfCountries['TIME_PERIOD']==2019]
df2019 = df2019.drop(['TIME_PERIOD'], axis=1)
df2019.to_csv('./preprocessed/EU_NEET_PERC_2019_preproc.csv', index=False)

df2020 = dfCountries[dfCountries['TIME_PERIOD']==2020]
df2020 = df2020.drop(['TIME_PERIOD'], axis=1)
df2020.to_csv('./preprocessed/EU_NEET_PERC_2020_preproc.csv', index=False)

df2021 = dfCountries[dfCountries['TIME_PERIOD']==2021]
df2021 = df2021.drop(['TIME_PERIOD'], axis=1)
df2021.to_csv('./preprocessed/EU_NEET_PERC_2021_preproc.csv', index=False)

df2022 = dfCountries[dfCountries['TIME_PERIOD']==2022]
df2022 = df2022.drop(['TIME_PERIOD'], axis=1)
df2022.to_csv('./preprocessed/EU_NEET_PERC_2022_preproc.csv', index=False)

df2023 = dfCountries[dfCountries['TIME_PERIOD']==2023]
df2023 = df2023.drop(['TIME_PERIOD'], axis=1)
df2023.to_csv('./preprocessed/EU_NEET_PERC_2023_preproc.csv', index=False)

############################################################################################################
### EU poverty risk (percentage) dataset
df = pd.read_csv('./EU_poverty_risk_total_PERC.csv')

areasToBeExcluded = []
dfCountries = df[~np.isin(df['Geopolitical entity (reporting)'],areasToBeExcluded)]
dfCountries = dfCountries.drop(['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'freq', 'Time frequency', 'indic_il', 'Income and living conditions indicator', 'Sex', 'Age class', 'Unit of measure', 'Time', 'Observation value', 'OBS_FLAG', 'Observation status (Flag)'], axis=1)

print("\n\nPreprocessed: EU poverty risk (percentage) dataset:\n")
print(dfCountries['Geopolitical entity (reporting)'].unique())

path = './preprocessed/EU_poverty_risk_total_PERC_preproc.csv'
dfCountries.to_csv(path, index=False)

############################################################################################################
### EU fatal accidents (incidence rate) dataset
df = pd.read_csv('./EU_fatal_accidents_total_IR.csv')

areasToBeExcluded = []
dfCountries = df[~np.isin(df['Geopolitical entity (reporting)'],areasToBeExcluded)]
dfCountries = dfCountries.drop(['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'freq', 'Time frequency', 'nace_r2', 'Statistical classification of economic activities in the European Community (NACE Rev. 2)', 'severity', 'Severity (days lost)', 'Sex', 'Unit of measure', 'Time', 'Observation value', 'OBS_FLAG', 'Observation status (Flag) V2 structure', 'CONF_STATUS', 'Confidentiality status (flag)'], axis=1)

print("\n\nPreprocessed: EU fatal accidents (incidence rate) dataset:\n")
print(dfCountries['Geopolitical entity (reporting)'].unique())

path = './preprocessed/EU_fatal_accidents_total_IR_preproc.csv'
dfCountries.to_csv(path, index=False)

############################################################################################################
### EU outside labour for caring total (percentage) dataset
df = pd.read_csv('./EU_outside_labour_4_caring_total_PERC.csv')

areasToBeExcluded = []
dfCountries = df[~np.isin(df['Geopolitical entity (reporting)'],areasToBeExcluded)]
dfCountries = dfCountries.drop(['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'freq', 'Time frequency', 'reason', 'Reason', 'Sex', 'Age class', 'Unit of measure', 'Time', 'Observation value', 'OBS_FLAG', 'Observation status (Flag) V2 structure', 'CONF_STATUS', 'Confidentiality status (flag)'], axis=1)

print("\n\nPreprocessed: EU outside labour for caring total (percentage) dataset:\n")
print(dfCountries['Geopolitical entity (reporting)'].unique())

path = './preprocessed/EU_outside_labour_4_caring_total_PERC_preproc.csv'
dfCountries.to_csv(path, index=False)
