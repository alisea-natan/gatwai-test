import pandas as pd
from os.path import join
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def determine_left(data):
    employees_left = data[data['left'] == 1].shape[0]
    employees_working = data[data['left'] == 0].shape[0]

    print(f"Number of employees who left the company: {employees_left}")
    print(f"Number of employees who are still working: {employees_working}\n")


def features_import(X_encoded, rf_classifier):
    feature_importances = pd.DataFrame(
        {'feature': X_encoded.columns, 'importance': rf_classifier.feature_importances_})
    feature_importances = feature_importances.sort_values('importance', ascending=False)

    print("Higher Feature Importances:")
    print(feature_importances.head(5))
    print()


def predict_next(X_encoded, y, rf_classifier):
    y_probabilities = rf_classifier.predict_proba(X_encoded)
    prediction_results = pd.DataFrame({'True Labels': y, 'Predicted Labels': y})
    prediction_results['Probabilities'] = y_probabilities[:, 1]  # Probability of belonging to class 1

    misclassified_instances = prediction_results[(prediction_results['True Labels'] == 0)]
    misclassified_instances = misclassified_instances.sort_values('Probabilities', ascending=False).head(10)

    print("Higher probabilities to leave:")
    print(misclassified_instances[['Probabilities']])


def receive_hr_prediction():

    data = pd.read_csv(join('data', 'HR.csv'))

    determine_left(data)

    X = data.drop('left', axis=1)
    y = data['left']

    # Convert categorical variables into numerical using one-hot encoding
    X_encoded = pd.get_dummies(X)

    np.random.seed(42)  # To make this model give same result each time

    # Here was check of the model work, last report is: Accuracy: 0.987

    # X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    # rf_classifier = RandomForestClassifier()
    # rf_classifier.fit(X_train, y_train)
    # y_pred = rf_classifier.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # clas_report = classification_report(y_test, y_pred)
    # print("Accuracy:", accuracy)
    # print("Classification Report:")
    # print(clas_report)

    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(X_encoded, y)

    features_import(X_encoded, rf_classifier)
    predict_next(X_encoded, y, rf_classifier)


if __name__ == "__main__":
    receive_hr_prediction()
