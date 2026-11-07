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
# primele 50 de vinuri sortate descrescator in functie de alcolemie
df_top50=df.sort_values(by="alcohol", ascending=False).head(50)
df_top50.to_csv("data_out/top50_alcohol.csv", index=False)
print("Primele 50 de vinuri ordonate descrescator in functie de alcolemie: ")
print({len(df_top50)})
print(df_top50.head())

# CERINTA 5
# vrea media coloanelor alcohol și pH pentru fiecare valoare a coloanei quality
# grupez datele dupa quality
df.groupby("quality")
# ma intereseaza doar pH si alcohol
df.groupby("quality")[["alcohol", "pH"]].mean()
df_medii=df.groupby("quality")[["alcohol", "pH"]].mean().reset_index()
df_medii.to_csv("data_out/medii_pe_calitate.csv", index=False)
print("\nRezultate cerinta 5")
print(df_medii)





