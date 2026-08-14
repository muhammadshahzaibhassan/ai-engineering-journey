from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from DecisionTree import DecisionTree


# Load dataset
data = datasets.load_breast_cancer()

X, y = data.data, data.target


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=1234
)


# Create model
clf = DecisionTree()

# Train model
clf.fit(X_train, y_train)

# Make predictions
predictions = clf.predict(X_test)


# Accuracy function
def accuracy(y_test, y_pred):
    return np.sum(y_test == y_pred) / len(y_test)


# Calculate accuracy
acc = accuracy(y_test, predictions)

print(acc)