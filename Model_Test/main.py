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

# CERINTA 4
# valorile medii ale indicatorilor la nivel de județ (media localităților din județ)
# creez o lista cu cei 5 indicatori
indicatori=["NrFirme", "NrSal", "TotalCifraAfaceri", "TotalProfit", "TotalPierdere"]
c4=df_unit.copy()
# inmultesc pentru fiecare indicator, valoarea sa cu populatia, pe fiecare localitate
for i in indicatori:
    c4[i]=c4[i]*c4["Populatie"]
# grupez pe judet si insumez produsele obtinute, plus populatia totala a judetului
c4_grupat=c4.groupby("Judet")[indicatori+["Populatie"]].sum().reset_index()

# impart fiecare suma ponderata la populatia totala a judetului
for j in indicatori:
    c4_grupat[j]=c4_grupat[j]/c4_grupat["Populatie"]

out4=c4_grupat[["Judet"]+indicatori].round(3)
out4.to_csv("data_out/Output4.csv", index=False)
# print(out4.head())

# SUPLEMENTAR

# 1
# Să se salveze în fișierul Train1.csv profitul mediu pe firmă pentru fiecare localitate unde există cel puțin 10 firme și profitul total este strict pozitiv
# Datele vor fi sortate descrescător după acest indicator și rotunjite la 2 zecimale.
filtrare=firme[(firme["NrFirme"]>=10) & (firme["TotalProfit"]>0)].copy()
print(filtrare.head(20))
filtrare["Profit mediu"]=(filtrare["TotalProfit"]/filtrare["NrFirme"]).round(2)
filtrare=filtrare.sort_values(by=["Profit mediu"],ascending=False)
filtrare=filtrare[["Siruta", "DenLocalitate", "Profit mediu"]]
filtrare.to_csv("data_out/Train1.csv", index=False)
print(filtrare.head())



