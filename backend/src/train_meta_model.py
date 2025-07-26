import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np


def load_data(path: str):
    df = pd.read_csv(path)
    df = df.drop(columns=['DATE', 'TIME', 'Start Time'])
    X = df.drop(columns=['Label'])
    y = df['Label']
    return X, y

X, y = load_data('processed_data.csv')

# Load scaler and transform features
scaler = joblib.load('../models/scaler.pkl')
X_scaled = scaler.transform(X)

# Split data (same split as base models)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Load base (level-0) models
models = {
    'rf': joblib.load('../models/random_forest_model.pkl'),
    'xgb': joblib.load('../models/xgboost_model.pkl'),
    'knn': joblib.load('../models/knn_model.pkl'),
    'ann': joblib.load('../models/ann_model.pkl'),
}


def get_meta_features(models: dict, X: np.ndarray) -> np.ndarray:
    preds = []
    for name, model in models.items():
        if hasattr(model, 'predict_proba'):
            p = model.predict_proba(X)
        else:
            p = model.decision_function(X)
        preds.append(p)
    return np.hstack(preds)

meta_train = get_meta_features(models, X_train)
meta_test  = get_meta_features(models, X_test)

print("Training Meta-Model (Logistic Regression)...")
meta_model = LogisticRegression(
    solver='liblinear', multi_class='ovr', random_state=42
)
meta_model.fit(meta_train, y_train)

preds = meta_model.predict(meta_test)
acc = accuracy_score(y_test, preds)
print(f"Meta-Model Accuracy on Test Set: {acc:.4f}")

joblib.dump(meta_model, '../models/meta_model.pkl')
print("Meta-model trained and saved as 'meta_model.pkl'.")
