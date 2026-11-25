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

