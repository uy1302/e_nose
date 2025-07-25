import numpy as np
import pickle
import joblib
import xgboost as xgb
import sys
from config import config


def get_meta_features(models: dict, X: np.ndarray) -> np.ndarray:
    """
    Generate meta-features by concatenating each base model's probability outputs or decision scores.
    """
    preds = []
    for model in models.values():
        if hasattr(model, 'predict_proba'):
            p = model.predict_proba(X)
        else:
            p = model.decision_function(X)
        preds.append(p)
    return np.hstack(preds)


def predict_with_models(input_data):
    """
    Make predictions using all base models and a meta-model

    Parameters:
    input_data (list or array): List of sensor readings [MQ2, MQ3, MQ4, MQ6, MQ7, MQ135, TEMP, HUMI]

    Returns:
    dict: Predictions from all models including meta-model with class labels and probabilities
    """
    input_array = np.array(input_data).reshape(1, -1)

    # Load scaler only
    scaler = joblib.load(config.get_preprocessing_path('scaler'))

    # Scale input
    input_scaled = scaler.transform(input_array)

    # Load base models
    rf_model  = joblib.load(config.get_model_path('random_forest'))
    xgb_model = joblib.load(config.get_model_path('xgboost'))
    knn_model = joblib.load(config.get_model_path('knn'))
    ann_model = joblib.load(config.get_model_path('ann'))  # MLPClassifier

    base_models = {'rf': rf_model, 'xgb': xgb_model, 'knn': knn_model, 'ann': ann_model}

    # ANN prediction
    ann_prob  = ann_model.predict_proba(input_scaled)
    ann_index = np.argmax(ann_prob, axis=1)[0]
    ann_label = ann_model.classes_[ann_index]
    ann_conf  = float(ann_prob[0, ann_index])

    # Random Forest prediction
    rf_pred  = rf_model.predict(input_scaled)[0]
    rf_label = rf_pred if rf_pred in rf_model.classes_ else str(rf_pred)

    # XGBoost prediction
    xgb_pred  = xgb_model.predict(input_scaled)[0]
    xgb_label = xgb_pred if xgb_pred in xgb_model.classes_ else str(xgb_pred)

    # KNN prediction
    knn_pred  = knn_model.predict(input_scaled)[0]
    knn_label = knn_pred if knn_pred in knn_model.classes_ else str(knn_pred)

    # Meta-model prediction
    meta_X      = get_meta_features(base_models, input_scaled)
    meta_model  = joblib.load(config.get_model_path('meta_model'))
    meta_prob   = meta_model.predict_proba(meta_X)
    meta_index  = np.argmax(meta_prob, axis=1)[0]
    meta_label  = meta_model.classes_[meta_index]
    meta_conf   = float(meta_prob[0, meta_index])

    return {
        'input_data': input_data,
        'predictions': {
            'ann':   {'class_label': ann_label,  'probability': round(ann_conf, 4)},
            'random_forest': {'class_label': rf_label},
            'xgboost':      {'class_label': xgb_label},
            'knn':          {'class_label': knn_label},
            'meta':         {'class_label': meta_label, 'probability': round(meta_conf, 4)}
        }
    }

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try:
            sensor_readings = [float(arg) for arg in sys.argv[1:5]]
        except ValueError:
            print("All sensor readings must be numeric.")
            sys.exit(1)
    else:
        print("Usage: python predict.py MQ7 MQ135 TEMP HUMI")
        sys.exit(1)

    result = predict_with_models(sensor_readings)
    print("\nInput data:", result['input_data'])
    print("\nPredictions:")
    print(f"ANN: {result['predictions']['ann']['class_label']} (Prob: {result['predictions']['ann']['probability']:.4f})")
    print(f"RF: {result['predictions']['random_forest']['class_label']}")
    print(f"XGB: {result['predictions']['xgboost']['class_label']}")
    print(f"KNN: {result['predictions']['knn']['class_label']}")
    print(f"META: {result['predictions']['meta']['class_label']} (Prob: {result['predictions']['meta']['probability']:.4f})")
