import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn as sk

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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
df.to_csv("data_out/cerinta2.csv")
print(df.head())

# ACP
# 1. import instrumente sklearn
# 2. aleg doar indicatorii pt analiza
lista_val_numerice=['FR','IM','LE','LEF','LEM','MMR','RS']
df=df_miscareNaturala.loc[:, lista_val_numerice]
# Standardizare date
scaler=StandardScaler()
df=scaler.fit_transform(df)
# Aplicare PCA si afisare variante (B.1)
pca=PCA()
pca.fit(df)
variante=pca.explained_variance_
print("\nVariantele componentelor principale:\n", variante)

# Scorurile asociate instanțelor. Scorurile vor fi salvate în fișierul scoruri.csv.
scoruri=pca.transform(df).round(3)
col_PCA=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
etichete_tari=df_miscareNaturala['Three_Letter_Country_Code']
df_scoruri=pd.DataFrame(scoruri,index=etichete_tari,columns=col_PCA)
df_scoruri.to_csv("data_out/cerinta3.csv")

# Graficul scorurilor în primele două axe principale.
# gf scorurilor in primele doua axe principale
plt.figure(figsize=(10,10))
# desenez punctele
plt.scatter(df_scoruri['C1'],df_scoruri['C2'], color='blue')
# pun codul tarii langa fiecare punct
for i in range(len(df_scoruri)):
    plt.text(df_scoruri['C1'].iloc[i], df_scoruri['C2'].iloc[i], df_scoruri.index[i])
# plasarea axelor
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.title('Graficul scorurilor în primele două axe principale.')
plt.xlabel('C1')
plt.ylabel('C2')
plt.show()



