import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score

# load dataset
iris=load_iris()
X=iris.data
Y=iris.target

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

# train LDA
lda=LinearDiscriminantAnalysis(n_components=2)
lda.fit(X_train, y_train)

# classification
predictions=lda.predict(X_test)
print("Accuracy:",accuracy_score(y_test, predictions))

# dimensionality reduction for visualization
x_lda=lda.transform(X)
plt.figure(figsize=(8,5))
for i, name in enumerate(iris.target_names):
    plt.scatter(
        x_lda[Y== i, 0],
        x_lda[Y== i, 1],
        label=name
    )
plt.xlabel("Linear Discriminant 1")
plt.ylabel("Linear Discriminant 2")
plt.title("Linear Discriminant Analysis-Iris Dataset")
plt.legend()
plt.show()

