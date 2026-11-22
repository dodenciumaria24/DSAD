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
medii_clase.to_csv("data_out/medii_predictori_pe_clasa.csv")

# One plot (e.g. degree_spondylolisthesis) by class.
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="class", y="degree_spondylolisthesis", palette="Set2")
plt.title("Distributia degree_spondylolisthesis pe clase")
plt.xlabel("Clasa (Diagnostic)")
plt.ylabel("degree_spondylolisthesis")
plt.savefig("plot_degree_spondylolisthesis.png")
plt.show()

# train_test_split(0.3, stratify, random_state=42).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# Fit LinearDiscriminantAnalysis on train; print classes_, priors_.
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
print("Clasele modelului (classes_):", lda.classes_)
print("Probabilitatile a priori (priors_):", lda.priors_)

# Predict on test → Predictii_test.csv.

# Accuracy + confusion matrix → Acuratete_lda.csv, CM_lda.csv.

# transform() on train → z.csv (Z1, Z2).

# Scatter Z1 vs Z2, coloured by class + group centres.

# Distributions of predictors by class (as in f_distributii).

# Short interpretation: which predictor “looks” most discriminative?