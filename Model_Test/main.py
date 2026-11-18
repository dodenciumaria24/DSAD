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
c1["Raport intre CA si NrSal"]=c1["TotalCifraAfaceri"]/c1["NrSal"]
# operatie vectorizata
# sortez descrescator dupa raport
c1=c1.sort_values(by=["Raport intre CA si NrSal"],ascending=False)
# selectez doar coloanele dorite de cerinta
out1=c1[["Siruta", "DenLocalitate", "Raport intre CA si NrSal"]]
# salvare in Output1.csv
out1.to_csv("data_in/Output1.csv", index=False)
print(out1.head(20))



