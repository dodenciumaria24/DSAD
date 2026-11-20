import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, confusion_matrix

# load .csv
df=pd.read_csv("data_in/hernia.csv", index_col=0)
print(df.head())
# separate predictors vs class
print("\nColoanele tabelului: ", df.columns.tolist())
X=df.drop(columns=["class"])
y=df["class"]

# counts per class
clase_count=y.value_counts()
print("\nNr observatii pe clasa: ", clase_count)
clase_count.to_csv("clase_count.csv", header=["Count"])

# Group means of predictors by class → medii_predictori_pe_clasa.csv.
medii_clase=df.groupby("class").mean()
print("\nMedii predictori pe clasa:\n", medii_clase)
medii_clase.to_csv("medii_predictori_pe_clasa.csv")
