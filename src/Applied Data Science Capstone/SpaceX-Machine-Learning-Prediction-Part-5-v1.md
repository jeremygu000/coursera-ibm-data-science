### Model Training and Evaluation Report

This report documents the steps from Task 1 to Task 12, describing the purpose of each step and the methods used.

#### Task 1: Extract Labels

We extracted the target variable Class from the dataset and converted it into a NumPy array.

```py
Y = X['Class'].to_numpy()
```

#### Task 2: Standardize Features

We standardized the feature dataset X using StandardScaler to normalize the data (zero mean and unit variance).

```py
X = transform.fit_transform(X)
```

#### Task 3: Split Data

We split the dataset into training and testing sets using an 80/20 split.

```py
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
```

#### Task 4: Logistic Regression with Grid Search

We created a Logistic Regression model and tuned hyperparameters using GridSearchCV with 10-fold cross-validation.

```py
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)
```

#### Task 5: Logistic Regression Test Accuracy

We calculated the accuracy of the Logistic Regression model on the test set.

```py
logreg_cv.score(X_test, Y_test)
```

#### Task 6: Support Vector Machine with Grid Search

We trained an SVM classifier and tuned its hyperparameters using GridSearchCV with 10-fold cross-validation.

```py
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, Y_train)
```

#### Task 7: SVM Test Accuracy

We calculated the accuracy of the tuned SVM model on the test set.

```py
svm_cv.score(X_test, Y_test)
```

#### Task 8: Decision Tree with Grid Search

We created a Decision Tree classifier and tuned hyperparameters using GridSearchCV with 10-fold cross-validation.

```py
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, Y_train)
```

#### Task 9: Decision Tree Test Accuracy

We calculated the accuracy of the tuned Decision Tree model on the test set.

```py
tree_cv.score(X_test, Y_test)
```

#### Task 10: K Nearest Neighbors with Grid Search

We trained a KNN classifier and tuned hyperparameters using GridSearchCV with 10-fold cross-validation.

```py
knn_cv = GridSearchCV(KNN, parameters, cv=10)
knn_cv.fit(X_train, Y_train)
```

#### Task 11: KNN Test Accuracy

We calculated the accuracy of the tuned KNN model on the test set.

```py
knn_cv.score(X_test, Y_test)
```

#### Task 12: Model Comparison

We compared all four models (Logistic Regression, SVM, Decision Tree, KNN) and identified which one performed best on the test set.

```py
results = {
"Logistic Regression": logreg_cv.score(X_test, Y_test),
"SVM": svm_cv.score(X_test, Y_test),
"Decision Tree": tree_cv.score(X_test, Y_test),
"KNN": knn_cv.score(X_test, Y_test)
}
best_model = max(results, key=results.get)

✨ In summary:
```

- Tasks 1–3: Data preparation (label extraction, scaling, splitting).
- Tasks 4–11: Training and evaluation of Logistic Regression, SVM, Decision Tree, and KNN.
- Task 12: Comparison of test accuracies to find the best-performing model.

#### Final Model Performance Comparison

| Model               | CV Accuracy (`best_score_`) | Test Accuracy (`.score()`)        |
| ------------------- | --------------------------- | --------------------------------- |
| Logistic Regression | `logreg_cv.best_score_`     | `logreg_cv.score(X_test, Y_test)` |
| SVM                 | `svm_cv.best_score_`        | `svm_cv.score(X_test, Y_test)`    |
| Decision Tree       | `tree_cv.best_score_`       | `tree_cv.score(X_test, Y_test)`   |
| KNN                 | `knn_cv.best_score_`        | `knn_cv.score(X_test, Y_test)`    |
