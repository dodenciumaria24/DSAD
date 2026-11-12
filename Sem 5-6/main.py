import sys

import numpy as np
import pandas as pd

from functii import nan_replace_df, acp, tabelare_varianta, salvare_ndarray
from grafice import plot_varianta, corelograma, f_scatterplot


pd.set_option("display.max_columns",None)
np.set_printoptions(3,sys.maxsize,suppress=True)

# citirea setului de date
set_date=pd.read_csv("data_in/Wholesale customers data.csv")
nume_variabile="Categorii de produse"
# verific daca exista valori lipsa
nan_replace_df(set_date)
# sar primele 2 col
variabile_observate=list(set_date)[2:]
x=set_date[variabile_observate].values
# x- matricea datelor standardizate
# print(x)
x_,r_v,alpha,a = acp(x)
# r_v- matricea de corelație dintre cele 6 var
# alpha: vectorul cu valorile proprii (eigenvalues),
# care reprezintă varianța explicată de fiecare componentă principală în parte.
# a- matricea vectorilor proprii (eigenvectors), care arată cum contribuie fiecare produs la formarea noilor componente.
t_r = salvare_ndarray(r_v, variabile_observate, variabile_observate, nume_variabile, "data_out/R.csv")
# heatmap ul corelatiilor din t_r
corelograma(t_r)

# Analiza variabilitatii
t_varianta = tabelare_varianta(alpha)
t_varianta.round(3).to_csv("data_out/Varianta.csv")

k = plot_varianta(alpha)
nr_min_comp = min([v for v in k if v is not None])

# Analiza corelatiilor factoriale
c = x_@a
s = c/np.sqrt(alpha)
etichete_componente = list(t_varianta.index)
t_c = salvare_ndarray(
    c,
    set_date.index,
    etichete_componente,
    set_date.index.name,
    "data_out/C.csv"
)
t_s = salvare_ndarray(
    s,
    set_date.index,
    etichete_componente,
    set_date.index.name,
    "data_out/S.csv"
)
n,m = x.shape
r_xc = np.corrcoef(x,c,rowvar=False)[:m,m:]
t_r_xc = salvare_ndarray(
    r_xc,
    variabile_observate,
    etichete_componente,
    nume_variabile,
    "data_out/R_xc.csv"
)
corelograma(t_r_xc,"Corelatii factoriale")
# Cercul corelatiilor
for i in range(2,nr_min_comp+1):
    f_scatterplot(
        t_r_xc,
        titlu="Corelatii factoriale C1xC"+str(i),
        y="c"+str(i),
        corelatii=True
    )

# Analiza scorurilor
for i in range(2,nr_min_comp+1):
    f_scatterplot(t_c,titlu="Plot componente (C1,C"+str(i)+")",y="c"+str(i))

# Calcul metrici
# Valorile cosinus
c2 = c*c
cosin = (c2.T/np.sum(c2,axis=1)).T
t_cosin=salvare_ndarray(
    cosin,
    set_date.index,
    etichete_componente,
    set_date.index.name,
    "data_out/Cosin.csv"
)
if n<50:
    corelograma(
        t_cosin,
        "Valori cosinus",
        0,
        "Reds",
        m<15
    )

# Calcul contributii
contrib = c2/np.sum(c2,axis=0)
t_contrib = salvare_ndarray(
    contrib,
    set_date.index,
    etichete_componente,
    set_date.index.name,
    "data_out/Contrib.csv"
)
corelograma(
    t_contrib,
    "Contributii instante la variantele axelor",
    0, "Blues",False
)
# Calcul comunalitati
r2 = r_xc*r_xc
comm = np.cumsum(r2,axis=1)
t_comm = salvare_ndarray(
    comm,
    variabile_observate,
    etichete_componente,
    nume_variabile,
    "data_out/Comm.csv"
)
corelograma(
    t_comm,
    "Comunalitati",
    0,
    "Greens",
    False
)

# # Trasare harta scoruri
# gdf = GeoDataFrame.from_file("Europa/Europa.shp")
# print(gdf)

# show()
