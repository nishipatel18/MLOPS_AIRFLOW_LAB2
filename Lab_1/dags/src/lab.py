import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
import base64


def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("Loading Wine Quality data...")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"), sep=";")
    serialized_data = pickle.dumps(df)
    return base64.b64encode(serialized_data).decode("ascii")


def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled processed data.
    """
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()

    # Separate features and target
    X = df.drop("quality", axis=1)
    y = df["quality"]

    # Scale features using MinMaxScaler
    min_max_scaler = MinMaxScaler()
    X_scaled = min_max_scaler.fit_transform(X)

    # Pack X_scaled and y together
    processed_data = (X_scaled, y.values)
    serialized_data = pickle.dumps(processed_data)
    return base64.b64encode(serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a Random Forest model on the preprocessed data and saves it.
    Returns accuracy scores for different n_estimators (like SSE in original).
    """
    data_bytes = base64.b64decode(data_b64)
    X_scaled, y = pickle.loads(data_bytes)

    # Try different n_estimators and record accuracy (similar to elbow method)
    accuracy_scores = []
    for n in range(10, 210, 10):
        rf = RandomForestClassifier(n_estimators=n, max_depth=10, random_state=42, n_jobs=-1)
        rf.fit(X_scaled, y)
        train_acc = accuracy_score(y, rf.predict(X_scaled))
        accuracy_scores.append(train_acc)

    # Save the last model (n=200)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "wb") as f:
        pickle.dump(rf, f)

    print(f"Model saved to {output_path}")
    return accuracy_scores


def load_model_elbow(filename: str, accuracy_scores: list):
    """
    Loads the saved model and finds the optimal n_estimators
    based on accuracy convergence (like elbow method).
    Returns the first prediction on test.csv.
    """
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(output_path, "rb"))

    # Find where accuracy stabilizes (similar to elbow)
    n_estimators_range = list(range(10, 210, 10))
    best_idx = 0
    for i in range(1, len(accuracy_scores)):
        if abs(accuracy_scores[i] - accuracy_scores[i-1]) < 0.001:
            best_idx = i
            break
    print(f"Optimal n_estimators: {n_estimators_range[best_idx]}")

    # Predict on test data
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"), sep=";")
    pred = loaded_model.predict(df)[0]

    try:
        return int(pred)
    except Exception:
        return pred.item() if hasattr(pred, "item") else pred
