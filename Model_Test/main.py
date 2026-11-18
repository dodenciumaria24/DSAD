import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CERINTA 1
#  raportul dintre cifra de afaceri și numărul de salariați pentru fiecare localitate unde există salariați
# citire fisiere de intrare
firme=pd.read_csv("data_in/I2014.csv")
populatiiLocalitati=pd.read_csv("data_in/PopulatieLocalitati.csv")
print(firme.head())
# filtrez localitatile (NrSal>0)
c1=firme[firme["NrSal"]>0].copy()
# help(firme.copy)
# raport dintre TotalCifraAfaceri si NrSal
c1["Raport intre CA si NrSal"]=(c1["TotalCifraAfaceri"]/c1["NrSal"]).round(3)
# operatie vectorizata
# sortez descrescator dupa raport
c1=c1.sort_values(by=["Raport intre CA si NrSal"],ascending=False)
# selectez doar coloanele dorite de cerinta
out1=c1[["Siruta", "DenLocalitate", "Raport intre CA si NrSal"]]
# salvare in Output1.csv
out1.to_csv("data_out/Output1.csv", index=False)
# print(out1.head(20))

# CERINTA 2
#  rata ocupării populației ca număr de salariați la 1000 locuitori pentru fiecare județ
print(populatiiLocalitati.head())
# daca am nevoie de date pt o cerinta de la 2 df, le unesc prin merge() folosind col comuna
populatiiLocalitati.columns = populatiiLocalitati.columns.str.strip()
firme.columns = firme.columns.str.strip()

df_unit=pd.merge(populatiiLocalitati,firme,on="Siruta")
# print(df_unit.head())
# gruparea dupa var Judet, adunam sal si pop totala pe fiecare judet
c2=df_unit.groupby("Judet")[["NrSal", "Populatie"]].sum().reset_index()
# calc rata ocuparii la 1000 de locuitori
c2["Rata ocuparii"]=(c2["NrSal"]/c2["Populatie"])*1000
# ordonarea datelor descrescator in functie de rata ocuparii
c2=c2.sort_values(by=["Rata ocuparii"],ascending=False)
# salvez doar col cerute
out2=c2[["Judet", "Rata ocuparii"]]
# salvez rezultatu in Output2.csv
out2.to_csv("data_out/Output2.csv", index=False)
# print(out2.head(20))

# CERINTA 3
# pentru fiecare județ se determina localitatea cu cel mai mare profit pe locuitor
c3=df_unit.copy()
c3["Profit_locuitor"]=c3["TotalProfit"]/c3["Populatie"]
# gasim pentru fiecare judet indexul randului unde Profit_locuitor e maxim
indecsi_max=c3.groupby("Judet")["Profit_locuitor"].idxmax()
# extrag randurile aferenta indexului localitatii care indeplineste conditia
c3_max=c3.loc[indecsi_max]
# selectez col cerute
out3=c3_max[["Judet", "Localitate"]]
# salvez totul in Output3.csv
out3.to_csv("data_out/Output3.csv", index=False)
print(out3.head())

