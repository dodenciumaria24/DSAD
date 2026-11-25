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
print(firme.NrFirme.describe() )
print(firme.DenLocalitate.unique() )
print(firme.shape)
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
# print(filtrare.head())

# 2
# Să se calculeze la nivel de județ rata pierderii raportată la cifra de afaceri si diferența netă dintre profit și pierdere
# Datele vor fi salvate în Train2.csv în ordinea crescătoare a ratei pierderii, afișând Judet, Rata_Pierdere_Procent și Rezultat_Net.
df_unit2=pd.merge(populatiiLocalitati,firme,on="Siruta")
c5=df_unit2.groupby("Judet")[["TotalPierdere","TotalProfit", "TotalCifraAfaceri"]].sum().reset_index()
c5["Rata pierderii"]=(c5["TotalPierdere"]/c5["TotalCifraAfaceri"])*100
c5["Diferenta neta"]=c5["TotalProfit"]-c5["TotalPierdere"]
c5=c5.sort_values(by=["Rata pierderii"],ascending=True)
c5=c5[["Judet", "Rata pierderii", "Diferenta neta"]]
c5.to_csv("data_out/Train2.csv", index=False)
# print(c5.head(10))

# 3
# determinarea pt fiecare judet, a localitatii cu densitatea cea mai mica de firme la 1000 loc,luand in calcul NrFirme>0
filtrare1=df_unit[df_unit["NrFirme"]>0].copy()
# densitatea pt fiecare localitate
filtrare1["Firme_la_1000_loc"]=(filtrare1["NrFirme"]/filtrare1["Populatie"])*1000
# pt fiecare jd, caut indexul randului unde Firme_la_1000_loc-minim
indecsi_min=filtrare1.groupby("Judet")["Firme_la_1000_loc"].idxmin()
# extrag randurile din df indecsi_min
# loc comes fom 'locate'
filtrare1_min=filtrare1.loc[indecsi_min]
# sortez alfabetic dupa judet
filtrare1_min=filtrare1_min.sort_values(by=["Judet"],ascending=True)
# selectez col cerute
out5=filtrare1_min[["Judet", "Localitate", "Firme_la_1000_loc"]]
# salvez in Train3.csv
out5.to_csv("data_out/Train3.csv", index=False)
# print(out5.head(10))

# 4
# Calcularea mediei ponderate la nivel de judet pt indicatorii  TotalCifraAfaceri, TotalProfit, TotalPierdere,
# folosind ca pondere NrFirme din fiecare loc.Salvez in Train4.csv indicativul de judet, cele 3 medii ponderate, rotunjite la 3 zecimale

# creez lista cu indicatorii
indicatorii=["TotalCifraAfaceri", "TotalProfit", "TotalPierdere"]
df=df_unit.copy()
# inmultesc fiecare indicator cu ponderea
for i in indicatorii:
    df[i]=df[i]*df["NrFirme"]

# grupam pe Judet si adunam atat produsele de sus, cat si ponderea (NrFirme), fac 2 sume
df=df.groupby("Judet")[indicatorii+["NrFirme"]].sum().reset_index()
for i in indicatorii:
    df[i]=df[i]/df["NrFirme"]

df=df[["Judet"]+indicatorii].round(3)
df.to_csv("data_out/Train4.csv", index=False)
print(df.head(10))













