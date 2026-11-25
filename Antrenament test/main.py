import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn as sk

df_miscareNaturala=pd.read_csv("data_in/MiscareaNaturala.csv")
df_coduriTari=pd.read_csv("data_in/CoduriTariExtins.csv")

# A
# CERINTA 1
# 1. Salvarea în fișierul cerinta1.csv a țărilor în care rata sporului natural este pozitivă, în ordinea desc
# a ratei sporului natural. Se va salva codul de țară, numele țării și rata sporului natural.
df=df_miscareNaturala.loc[(df_miscareNaturala.RS>0), :]
df=df.sort_values(by=['RS'], ascending=False)
df=df[['Three_Letter_Country_Code','Country_Name','RS']]
df.to_csv("data_out/cerinta1.csv", index=False)
print(df.head(20))

# CERINTA 2
# Salvarea în fișierul cerinta2.csv a valorilor medii pentru indicatorii de mai sus, la nivel de continent, pentru
# acele continente la care valoarea medie a ratei sporului natural la nivel de continent este mai mare decât
# valoarea medie a ratei sporului natural la nivel mondial.
df=df_miscareNaturala.merge(df_coduriTari[['Three_Letter_Country_Code', 'Continent_Name']],  on='Three_Letter_Country_Code')
lista=['RS', 'FR', 'IM', 'LE', 'LEF', 'LEM', 'MMR']
df=df.groupby('Continent_Name')[lista].mean()
medie_mondiala=df_miscareNaturala.RS.mean()
df=df.loc[(df.RS>medie_mondiala), :]
df.to_csv("data_out/cerinta2.csv", index=False)
print(df.head())

# ACP
