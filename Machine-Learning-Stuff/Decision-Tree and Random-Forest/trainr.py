from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from RandomForest import RandomForest


# Load dataset
data = datasets.load_breast_cancer()

X = data.data
y = data.target


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=1234
)


# Create Random Forest
clf = RandomForest(
    n_trees=10,
    max_depth=10,
    min_samples_split=2
)


# Train the model
clf.fit(X_train, y_train)


# Make predictions
predictions = clf.predict(X_test)


# Accuracy function
def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy


# Calculate accuracy
acc = accuracy(y_test, predictions)

print(acc)