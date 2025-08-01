import numpy as np
import pickle
import joblib
import xgboost as xgb
import sys
from config import config


def create_security_mapping():
    """
    Create mapping between real names and security names for API responses
    """
    sensor_mapping = {
        'MQ136': 'sensor_1',
        'MQ137': 'sensor_2', 
        'TEMP': 'sensor_3',
        'HUMI': 'sensor_4'
    }
    
    model_mapping = {
        'ann': 'base_1',
        'random_forest': 'base_2',
        'xgboost': 'base_3',
        'knn': 'base_4',
        'meta': 'meta'
    }
    
    return sensor_mapping, model_mapping


def mask_sensor_names(sensor_list):
    """Convert real sensor names to security names"""
    sensor_mapping, _ = create_security_mapping()
    return [sensor_mapping.get(sensor, sensor) for sensor in sensor_list]


def mask_model_predictions(predictions):
    """Convert real model names to security names in predictions"""
    _, model_mapping = create_security_mapping()
    masked_predictions = {}
    
    for model_name, prediction_data in predictions.items():
        masked_name = model_mapping.get(model_name, model_name)
        masked_predictions[masked_name] = prediction_data
    
    return masked_predictions


def map_label_to_meat_type(label):
    """
    Map numeric label to meat type name
    
    Args:
        label: Numeric label (0-4) or string representation
    
    Returns:
        String: Meat type name
    """
    # Convert to int if it's string representation of number
    try:
        if isinstance(label, str):
            # Handle string numbers like "0.0", "1", etc.
            numeric_label = int(float(label))
        else:
            numeric_label = int(label)
    except (ValueError, TypeError):
        return str(label)  # Return as-is if conversion fails
    
    label_map = {
        0: "Thịt loại 1",
        1: "Thịt loại 2", 
        2: "Thịt loại 3",
        3: "Thịt loại 4",
        4: "Thịt hỏng"
    }
    
    return label_map.get(numeric_label, f"Unknown_{numeric_label}")


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
    input_data (list or array): List of sensor readings [MQ136, MQ137, TEMP, HUMI]

    Returns:
    dict: Predictions from all models including meta-model with class labels and probabilities
    """
    input_array = np.array(input_data).reshape(1, -1)

    # Load scaler only
    scaler = joblib.load('../models/scaler.pkl')

    # Scale input
    input_scaled = scaler.transform(input_array)

    # Load base models
    rf_model  = joblib.load('../models/random_forest_model.pkl')
    xgb_model = joblib.load('../models/xgboost_model.pkl')
    knn_model = joblib.load('../models/knn_model.pkl')
    ann_model = joblib.load('../models/ann_model.pkl')  # MLPClassifier

    base_models = {'rf': rf_model, 'xgb': xgb_model, 'knn': knn_model, 'ann': ann_model}

    # ANN prediction
    ann_prob  = ann_model.predict_proba(input_scaled)
    ann_index = np.argmax(ann_prob, axis=1)[0]
    ann_label = ann_model.classes_[ann_index]
    ann_conf  = float(ann_prob[0, ann_index])

    # Random Forest prediction
    rf_pred  = rf_model.predict(input_scaled)[0]
    rf_label = str(rf_pred) if hasattr(rf_pred, 'dtype') else rf_pred

    # XGBoost prediction
    xgb_pred  = xgb_model.predict(input_scaled)[0]
    xgb_label = str(xgb_pred) if hasattr(xgb_pred, 'dtype') else xgb_pred

    # KNN prediction
    knn_pred  = knn_model.predict(input_scaled)[0]
    knn_label = str(knn_pred) if hasattr(knn_pred, 'dtype') else knn_pred

    # Meta-model prediction
    meta_X      = get_meta_features(base_models, input_scaled)
    meta_model  = joblib.load('../models/meta_model.pkl')
    meta_prob   = meta_model.predict_proba(meta_X)
    meta_index  = np.argmax(meta_prob, axis=1)[0]
    meta_label  = str(meta_model.classes_[meta_index])
    meta_conf   = float(meta_prob[0, meta_index])

    # Create original predictions
    original_predictions = {
        'ann':   {'class_label': map_label_to_meat_type(ann_label),  'probability': round(ann_conf, 4)},
        'random_forest': {'class_label': map_label_to_meat_type(rf_label)},
        'xgboost':      {'class_label': map_label_to_meat_type(xgb_label)},
        'knn':          {'class_label': map_label_to_meat_type(knn_label)},
        'meta':         {'class_label': map_label_to_meat_type(meta_label), 'probability': round(meta_conf, 4)}
    }
    
    # Mask model names for security
    masked_predictions = mask_model_predictions(original_predictions)
    
    return {
        'input_data': input_data,
        'predictions': masked_predictions
    }

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try:
            sensor_readings = [float(arg) for arg in sys.argv[1:5]]
        except ValueError:
            print("All sensor readings must be numeric.")
            sys.exit(1)
    else:
        print("Usage: python predict.py MQ136 MQ137 TEMP HUMI")
        sys.exit(1)

    result = predict_with_models(sensor_readings)
    print("\nInput data:", result['input_data'])
    print("\nPredictions (with security masking):")
    predictions = result['predictions']
    for model_name, pred_data in predictions.items():
        if 'probability' in pred_data:
            print(f"{model_name.upper()}: {pred_data['class_label']} (Prob: {pred_data['probability']:.4f})")
        else:
            print(f"{model_name.upper()}: {pred_data['class_label']}")
