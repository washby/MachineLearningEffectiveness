import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from Utilities.DB_Utils import DatabaseUtility

TARGET_VARIABLE_NAME = 'FailedCourse'

db_connection = DatabaseUtility('db_config.json')
training_data = db_connection.select_data("TrainingData")
testing_data = db_connection.select_data("TestingData")

# Split data into training and testing sets
x_train = training_data.drop([TARGET_VARIABLE_NAME], axis=1)
y_train = training_data[TARGET_VARIABLE_NAME]

# Define parameter grids for hyperparameter tuning
nb_param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]}
nn_param_grid = {'hidden_layer_sizes': [(50,), (100,), (200,)], 'alpha': [0.0001, 0.001, 0.01]}
dt_param_grid = {'max_depth': [5, 10, 15, None], 'min_samples_split': [2, 5, 10]}
svm_param_grid = {'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1], 'kernel': ['linear', 'rbf']}

# Run Naive Bayes algorithm with hyperparameter tuning
nb = GaussianNB()
nb_grid = GridSearchCV(nb, nb_param_grid, cv=5)
nb_grid.fit(x_train, y_train)
print("Best Naive Bayes parameters:", nb_grid.best_params_)
nb_scores = []
for course_data in testing_data:
    x_test = course_data.drop([TARGET_VARIABLE_NAME], axis=1)
    y_test = course_data[TARGET_VARIABLE_NAME]
    nb_pred = nb_grid.predict(x_test)
    nb_accuracy = f1_score(y_test, nb_pred)
    nb_scores.append(nb_accuracy)
print("Naive Bayes accuracy:", nb_scores)


# Run Neural Network algorithm with hyperparameter tuning
nn = MLPClassifier(max_iter=500, solver='adam', verbose=10, random_state=42)
nn_grid = GridSearchCV(nn, nn_param_grid, cv=5)
nn_grid.fit(x_train, y_train)
print("Best Neural Network parameters:", nn_grid.best_params_)
nn_scores = []
for course_data in testing_data:
    x_test = course_data.drop([TARGET_VARIABLE_NAME], axis=1)
    y_test = course_data[TARGET_VARIABLE_NAME]
    nn_pred = nn_grid.predict(x_test)
    nn_accuracy = f1_score(y_test, nn_pred)
    nn_scores.append(nn_accuracy)
print("Neural Network accuracy:", nn_accuracy)

# Run Decision Tree algorithm with hyperparameter tuning
dt = DecisionTreeClassifier(random_state=42)
dt_grid = GridSearchCV(dt, dt_param_grid, cv=5)
dt_grid.fit(x_train, y_train)
print("Best Decision Tree parameters:", dt_grid.best_params_)
dt_scores = []
for course_data in testing_data:
    x_test = course_data.drop([TARGET_VARIABLE_NAME], axis=1)
    y_test = course_data[TARGET_VARIABLE_NAME]
    dt_pred = dt_grid.predict(x_test)
    dt_accuracy = f1_score(y_test, dt_pred)
    dt_scores.append(dt_accuracy)
print("Decision Tree accuracy:", dt_accuracy)

# Run Support Vector Machine algorithm with hyperparameter tuning
svm = SVC()
svm_grid = GridSearchCV(svm, svm_param_grid, cv=5)
svm_grid.fit(x_train, y_train)
print("Best Support Vector Machine parameters:", svm_grid.best_params_)
svm_scores = []
for course_data in testing_data:
    x_test = course_data.drop([TARGET_VARIABLE_NAME], axis=1)
    y_test = course_data[TARGET_VARIABLE_NAME]
    svm_pred = svm_grid.predict(x_test)
    svm_accuracy = f1_score(y_test, svm_pred)
    svm_scores.append(svm_accuracy)
print("Support Vector Machine accuracy:", svm_accuracy)
