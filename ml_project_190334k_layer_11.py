# -*- coding: utf-8 -*-
"""ML_Project_190334K_Layer_11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kBwwBUEN2l_inYO1wqwSUCUxzaJv0-SQ

Define label names and feature names
"""

import pandas as pd
import numpy as np

LABELS = ['label_1','label_2', 'label_3', 'label_4']
FEATURES = [f'feature_{i}' for i in range(1, 769)]

"""Read training,validation and test data"""

from google.colab import drive
drive.mount('/content/drive')


train_df = pd.read_csv("/content/drive/MyDrive/ML_Project_11/train.csv")
valid_df = pd.read_csv("/content/drive/MyDrive/ML_Project_11/valid.csv")
test_df = pd.read_csv("/content/drive/MyDrive/ML_Project_11/test.csv")

"""Initialize dictionaries to store data"""

train_x = {}
valid_x = {}
test_x = {}
train_y = {}
valid_y = {}
test_y = {}

"""Prepare and preprocess the data. Here, rows with missing values for each label are dropped when train and validation dataframes are created.

"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
for LBL in LABELS:
  train_df_new = train_df[train_df[LBL].notna()]# dropping rows with miising values for label 2 column.
  valid_df_new = valid_df[valid_df[LBL].notna()]# dropping rows with miising values for label 2 column.
  train_x[LBL] = pd.DataFrame(scaler.fit_transform(train_df_new.drop(LABELS, axis=1)), columns = FEATURES)
  train_y[LBL] = train_df_new[LBL]
  valid_x[LBL] = pd.DataFrame(scaler.transform(valid_df_new.drop(LABELS, axis=1)), columns = FEATURES)
  valid_y[LBL] = valid_df_new[LBL]
  test_x[LBL] = pd.DataFrame(scaler.transform(test_df.drop(['ID'], axis=1)), columns=FEATURES)

"""Imports"""

from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

"""# For Label 1"""

LBL = 'label_1'

"""## Applying Feature Engineering techniques

### Using Principal Component Analysis(PCA)

Apply PCA on original features
"""

pca = PCA(n_components=0.99, svd_solver='full')
pca.fit(train_x[LBL])

train_x_trans = pd.DataFrame(pca.transform(train_x[LBL]))
valid_x_trans = pd.DataFrame(pca.transform(valid_x[LBL]))
test_x_trans = pd.DataFrame(pca.transform(test_x[LBL]))

print("Shape after feature reduction:", train_x_trans.shape)
print("Shape after feature reduction:", valid_x_trans.shape)
print("Shape after feature reduction:", test_x_trans.shape)

"""## Model Selection

### Cross Validation

For Support Vector Machine(SVM) classifier
"""

svm_classifier = SVC(kernel='rbf')

# Define the number of splits for k-fold cross-validation
k_folds = 10
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(svm_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For kNN classifier"""

knn_classifier = KNeighborsClassifier(n_neighbors=5)

# Perform k-fold cross-validation
cv_scores = cross_val_score(knn_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""Since SVM has the highest mean accuracy, SVM classifier is selected as the classification model

## Hyperparameter tuning

### Using Grid search
"""

# Define the parameter grid for grid search
param_grid = {
    'C' : [0.1, 1, 10],
    'kernel': ['rbf','linear','poly']
}

# Create the SVM model
svm_model = SVC()

# Create Grid Search object
grid_search = GridSearchCV(svm_model, param_grid, cv=3, scoring='accuracy')

# Fit the model
grid_search.fit(train_x_trans, train_y[LBL])

# Get the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

"""C = 10 and kernel = 'rbf' are used for training the SVM model

## Train, Evaluation and Prediction

Train the SVM classifier
"""

classifier = svm.SVC(kernel='rbf',C=10)
classifier.fit(train_x_trans, train_y[LBL])

"""Prediction and evaluation for valid set."""

y_predict_valid = classifier.predict(valid_x_trans)
print(classification_report(valid_y[LBL], y_predict_valid))

"""Prediction for test dataset"""

test_y[LBL] = classifier.predict(test_x_trans)

"""# For Label 2"""

LBL = 'label_2'

"""## Applying Feature Engineering techniques

### Using Principal Component Analysis(PCA)

Apply PCA on original features
"""

pca = PCA(n_components=0.99, svd_solver='full')
pca.fit(train_x[LBL])

train_x_trans = pd.DataFrame(pca.transform(train_x[LBL]))
valid_x_trans = pd.DataFrame(pca.transform(valid_x[LBL]))
test_x_trans = pd.DataFrame(pca.transform(test_x[LBL]))

print("Shape after feature reduction:", train_x_trans.shape)
print("Shape after feature reduction:", valid_x_trans.shape)
print("Shape after feature reduction:", test_x_trans.shape)

"""## Model Selection

### Cross Validation

For SVM classifier
"""

svm_classifier = SVC(kernel='rbf')

# Define the number of splits for k-fold cross-validation
k_folds = 10
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(svm_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For kNN classifier"""

knn_classifier = KNeighborsClassifier(n_neighbors=10)

# Perform k-fold cross-validation
cv_scores = cross_val_score(knn_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For kNN Regressor"""

knn_Regressor = KNeighborsRegressor(n_neighbors=10)

# Perform k-fold cross-validation
cv_scores = cross_val_score(knn_Regressor, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For Random Forest classifier"""

random_forest_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
k_folds = 10
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
# Perform k-fold cross-validation
cv_scores = cross_val_score(random_forest_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""Since SVM has the highest mean accuracy, SVM classifier is selected as the classification model

## Hyperparameter tuning

### Using Grid search
"""

# Define the parameter grid for grid search
param_grid = {
    'C': [100,1000,10000],
    'kernel': ['rbf','linear']
}

# Create the SVM model
svm_model = SVC()

# Create Grid Search object
grid_search = GridSearchCV(svm_model, param_grid, cv=3, scoring='accuracy')

# Fit the model
grid_search.fit(train_x_trans, train_y[LBL])

# Get the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

"""C = 1000 and kernel = 'rbf' are used for training the SVM model

## Train, Evaluation and Prediction

Train the SVC classifier
"""

train_x_trans = train_x[LBL]
valid_x_trans = valid_x[LBL]
test_x_trans = test_x[LBL]

classifier = svm.SVC(kernel='rbf',C =1000)
classifier.fit(train_x_trans, train_y[LBL])

classifier = svm.SVC(kernel='rbf',C =10)
classifier.fit(train_x_trans, train_y[LBL])

"""Prediction and evaluation for valid set."""

y_predict_valid = classifier.predict(valid_x_trans)
print(classification_report(valid_y[LBL], y_predict_valid))

y_predict_valid = classifier.predict(valid_x_trans)
print(classification_report(valid_y[LBL], y_predict_valid))

"""Prediction for test dataset"""

test_y[LBL] = classifier.predict(test_x_trans)

test_y[LBL] = classifier.predict(test_x_trans)

"""# For Label 3"""

LBL = 'label_3'

"""## Applying Feature Engineering techniques

### Using Principal Component Analysis(PCA)

Apply PCA on original features
"""

pca = PCA(n_components=0.98, svd_solver='full')
pca.fit(train_x[LBL])

train_x_trans = pd.DataFrame(pca.transform(train_x[LBL]))
valid_x_trans = pd.DataFrame(pca.transform(valid_x[LBL]))
test_x_trans = pd.DataFrame(pca.transform(test_x[LBL]))

print("Shape after feature reduction:", train_x_trans.shape)
print("Shape after feature reduction:", valid_x_trans.shape)
print("Shape after feature reduction:", test_x_trans.shape)

"""## Model Selection

### Cross Validation

For SVM classifier
"""

svm_classifier = SVC(kernel='rbf')

# Define the number of splits for k-fold cross-validation
k_folds = 10
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(svm_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For kNN classifier"""

knn_classifier = KNeighborsClassifier(n_neighbors=5)

# Perform k-fold cross-validation
cv_scores = cross_val_score(knn_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For XGBoost classifier"""

xgb_classifier = xgb.XGBClassifier()

cv_scores = cross_val_score(xgb_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""Since SVM has the highest mean accuracy, SVM classifier is selected as the classification model

## Hyperparameter tuning

### Using Grid search
"""

# Define the parameter grid for grid search
param_grid = {
    'C' : [1, 10],
    'kernel': ['rbf','linear','poly']
}

# Create the SVM model
svm_model = SVC()

# Create Grid Search object
grid_search = GridSearchCV(svm_model, param_grid, cv=3, scoring='accuracy')

# Fit the model
grid_search.fit(train_x_trans, train_y[LBL])

# Get the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

"""C = 10 and kernel = 'rbf' are used for training the SVM model

## Train, Evaluation and Prediction

Train the SVM classifier
"""

classifier = svm.SVC(kernel='rbf', C = 10)
classifier.fit(train_x_trans, train_y[LBL])

"""Prediction and evaluation for valid set."""

y_predict_valid = classifier.predict(valid_x_trans)
print(classification_report(valid_y[LBL], y_predict_valid))

"""Prediction for test dataset"""

test_y[LBL] = classifier.predict(test_x_trans)

"""# For Label 4"""

LBL = 'label_4'

"""## Applying Feature Engineering techniques

### Using Principal Component Analysis(PCA)

Apply PCA on original features
"""

pca = PCA(n_components=0.99, svd_solver='full')
pca.fit(train_x[LBL])

train_x_trans = pd.DataFrame(pca.transform(train_x[LBL]))
valid_x_trans = pd.DataFrame(pca.transform(valid_x[LBL]))
test_x_trans = pd.DataFrame(pca.transform(test_x[LBL]))

print("Shape after feature reduction:", train_x_trans.shape)
print("Shape after feature reduction:", valid_x_trans.shape)
print("Shape after feature reduction:", test_x_trans.shape)

"""## Model Selection

### Cross Validation

For SVM classifier
"""

svm_classifier = SVC(kernel='rbf')

# Define the number of splits for k-fold cross-validation
k_folds = 10
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(svm_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For kNN classifier"""

knn_classifier = KNeighborsClassifier(n_neighbors=5)

# Perform k-fold cross-validation
cv_scores = cross_val_score(knn_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""For Random Forest classifier"""

random_forest_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(random_forest_classifier, train_x_trans, train_y[LBL], cv=kf)

# Print the cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean accuracy: {np.mean(cv_scores)}")

"""Since SVM has the highest mean accuracy, SVM classifier is selected as the classification model

## Hyperparameter tuning

### Using Grid search
"""

# Define the parameter grid for grid search
param_grid = {
    'C': [1, 10, 100],
    'kernel': ['rbf','linear','poly']
}

# Create the SVM model
svm_model = SVC()

# Create Grid Search object
grid_search = GridSearchCV(svm_model, param_grid, cv=3, scoring='accuracy')

# Fit the model
grid_search.fit(train_x_trans, train_y[LBL])

# Get the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

"""C = 10 and kernel = 'rbf' are used for training the SVM model

## Train, Evaluation and Prediction

Train the SVM classifier
"""

classifier = svm.SVC(kernel='rbf', C = 10)
classifier.fit(train_x_trans, train_y[LBL])

"""Prediction and evaluation for valid set."""

y_predict_valid = classifier.predict(valid_x_trans)
print(classification_report(valid_y[LBL], y_predict_valid))

"""Prediction for test dataset"""

test_y[LBL] = classifier.predict(test_x_trans)

IDs = [i for i in range(1, 745)]
output_df = pd.DataFrame({
    'ID': IDs,
})
for l in LABELS:
  lbl_df = pd.DataFrame({l : test_y[l]})
  output_df = pd.concat([output_df, lbl_df], axis=1)

output_df.to_csv('/content/drive/MyDrive/ML_Project_11/output.csv', index=False)