import numpy as np
import pandas as pd

def calcul_medie_ponderata(t:pd.DataFrame):
    x = t.values
    mp = np.average(x[:,:-1],axis=0,weights=x[:,-1])
    return pd.Series(mp,t.columns[:-1])

# CERINTA 1
industria_alim = pd.read_csv("data_in/IndustriaAlimentara.csv",index_col=0)
# [1:] -de la poziția 1 până la final, sar peste Localitate
industrii = list(industria_alim)[1:]

# calc total ang pt fiecare localitate
angajati = industria_alim[industrii].apply(func=lambda x:x.sum(),axis=1)
# pastrez localitatile cu mai mult de 0 ang
cerinta1 = industria_alim[angajati>0]
cerinta1.to_csv("data_out/Cerinta1.csv")
print("\nRezolvare cerinta 1")
print(cerinta1.head())


# CERINTA 2
# procentul de angajați pe fiecare activitate la nivel de localitate
cerinta2 = industria_alim[industrii].apply(func=lambda x: x*100/x.sum(),axis=1)
# verific ca rezultatul din cerinta2 a ramas un df
assert isinstance(cerinta2,pd.DataFrame)
cerinta2.insert(0,"Localitate",industria_alim["Localitate"])
cerinta2.to_csv("data_out/Cerinta2.csv")
print("\nRezolvare cerinta 2")
print(cerinta2.head())

# CERINTA 3
# județele sortate descrescător după ponderea angajaților din industria alimentară în Pop
populatie = pd.read_csv("data_in/PopulatieLocalitati.csv",index_col=0)
populatie["TotalAngajati"] = angajati
judete = populatie.groupby("Judet")[["Populatie", "TotalAngajati"]].sum().reset_index()
judete["Pondere"] = (judete["TotalAngajati"] / judete["Populatie"]) * 100
cerinta3 = judete.sort_values(by="Pondere", ascending=False)
cerinta3.to_csv("data_out/Cerinta3.csv", index=False)
print("\nRezolvare cerinta 3")
print(cerinta3.head())


# CERINTA 4
# afisarea activiatii cu cei mai multi ang la nivel de judet
industria_alim_loc = industria_alim.merge(populatie, left_index=True, right_index=True)
# pandas va potrivi randurile din cele 2 tabele folosind indexul
industria_alim_judet = industria_alim_loc[industrii + ["Populatie", "Judet"]].groupby("Judet").sum()
cerinta4 = industria_alim_judet[industrii].idxmax(axis=1).to_frame(name="Activitate")
cerinta4.to_csv("data_out/Cerinta4.csv")
print("\nRezolvare cerinta 4")
print(cerinta4.head())


# CERINTA 5
# nr mediu de angajați pe fiecare activitate la nivel de regiune
coduri_judete= pd.read_csv("data_in/Coduri_Judete.csv",index_col=0)
# print(industria_alim_loc)
industria_alim_loc_ = industria_alim_loc[industrii+["Judet","Populatie"]].merge(
    coduri_judete["Regiune"],
    left_on="Judet",
    right_index=True
)

cerinta5 = industria_alim_loc_[industrii+["Populatie","Regiune"]].groupby(by="Regiune").apply(
    func=calcul_medie_ponderata,
    include_groups=False
)
cerinta5.to_csv("data_out/Cerinta5.csv")
print("\nRezolvare cerinta 5")
print(cerinta5)

# # Cerinta 6
# # print(industria_alim_judet)
# total_national = industria_alim_judet.sum(axis=0)
# # print(total_national)
# cerinta6 = industria_alim_judet.apply(
#     lambda x: (x[industrii]/total_national[industrii]) /(x["Populatie"]/total_national["Populatie"]) ,
#     axis=1
# )
# # print(cerinta6)
# cerinta6.round(3).to_csv("data_out/Cerinta6.csv")
