import pandas as pd

from functii_online import nan_replace_df

# CERINTA 1
df=pd.read_csv("winequality-red.csv", sep=";")
# afisez nr de randuri si coloane
print(df.shape)
# afisez primele 5 randuri
print(df.head())
# afisez tipurile coloanelor
print(df.dtypes)

# CERINTA 2
df=nan_replace_df(df)

# verific daca mai exista vreun Nan in tabel
nr_nan=df.isna().sum().sum()
print(f"Nr total de valori lipsa ramase in tabel sunt: {nr_nan}")

# CERINTA 3
df_calitate_minima=df[df["quality"]>=7]
# salvez noul tabel filtrat
df_calitate_minima.to_csv("data_out/top50_alcool.csv", index=False)
print(f"Nr vinurilor cu calitate >=7 este: {len(df_calitate_minima)}")
print(df_calitate_minima.head())
print(df_calitate_minima.shape)

# CERINTA 4




