import os
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def load_data():
    """
    Loads Wine Quality data from a CSV file.
    Returns:
        DataFrame: Raw wine quality data.
    """
    data = pd.read_csv("/home/mlops_fall_2024/wine_quality.csv", sep=";")
    return data


def data_preprocessing(data):
    """
    Preprocess: drop nulls, scale features, train/test split.
    """
    X = data.drop("quality", axis=1)
    y = data["quality"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    num_columns = list(X.columns)

    ct = make_column_transformer(
        (MinMaxScaler(), num_columns),
        (StandardScaler(), num_columns),
        remainder='passthrough',
    )

    X_train = ct.fit_transform(X_train)
    X_test = ct.transform(X_test)

    return X_train, X_test, y_train.values, y_test.values


def build_model(data, filename):
    """
    Train Random Forest model and save it.
    """
    X_train, X_test, y_train, y_test = data

    rf_clf = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
    )
    rf_clf.fit(X_train, y_train)

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, filename)

    pickle.dump(rf_clf, open(output_path, 'wb'))


def load_model(data, filename):
    """
    Load saved model, evaluate on test set, return first prediction.
    """
    X_train, X_test, y_train, y_test = data

    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)

    loaded_model = pickle.load(open(output_path, 'rb'))

    predictions = loaded_model.predict(X_test)
    print(f"Model score on test data: {loaded_model.score(X_test, y_test)}")

    return predictions[0]


if __name__ == '__main__':
    x = load_data()
    x = data_preprocessing(x)
    build_model(x, 'model.sav')
