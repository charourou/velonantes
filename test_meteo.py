
import pandas as pd

meteo = pd.read_csv('/home/charourou/projects/velonantes/meteo_44109012_2022-01-01_au_2022-12-31.csv', sep=';')

print(meteo.head())

print(meteo.columns)

meteo_clean = meteo.dropna(axis = 1)
print(meteo_clean)
