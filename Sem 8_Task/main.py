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
print("\nMedii predictori pe clasa:\n", medii_clase.round(3))
medii_clase.to_csv("data_out/medii_predictori_pe_clasa.csv")

# One plot (e.g. degree_spondylolisthesis) by class.
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="class", y="degree_spondylolisthesis", palette="Set2", hue="class")
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
y_pred = lda.predict(X_test)
df_pred = pd.DataFrame({
    "Clasa_Reala": y_test,
    "Clasa_Prezisa": y_pred
}, index=X_test.index)
df_pred.to_csv("data_out/Predictii_test.csv")
# Accuracy + confusion matrix → Acuratete_lda.csv, CM_lda.csv.
acc = accuracy_score(y_test, y_pred)
print("Acuratete LDA pe test:", round(acc, 4))
pd.DataFrame({"Acuratete": [acc]}).to_csv("data_out/Acuratete_lda.csv", index=False)

# transform() on train → z.csv (Z1, Z2).
Z_train = lda.transform(X_train)
df_z = pd.DataFrame(Z_train, columns=["Z1", "Z2"], index=X_train.index)
df_z["class"] = y_train
df_z.to_csv("data_out/z.csv")

# Scatter Z1 vs Z2, coloured by class + group centres.
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df_z, x="Z1", y="Z2", hue="class", palette="Set1", s=60, alpha=0.8)

centre = df_z.groupby("class")[["Z1", "Z2"]].mean()
plt.scatter(centre["Z1"], centre["Z2"], c="black", marker="X", s=200, label="Centre grupuri")
for clasa, rand in centre.iterrows():
    plt.text(rand["Z1"] + 0.1, rand["Z2"] + 0.1, clasa, fontsize=11, fontweight="bold")

plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
plt.title("Spatiul discriminant (Z1 vs Z2) si centrele claselor")
plt.legend()
plt.savefig("data_out/scatter_Z1_Z2.png")
plt.show()
# Distributions of predictors by class (as in f_distributii).

# Short interpretation: which predictor “looks” most discriminative?