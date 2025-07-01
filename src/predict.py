import numpy as np
import pickle
import tensorflow as tf
import xgboost as xgb
import sys
from config import config

def predict_with_models(input_data):
    """
    Make predictions using all three trained models
    
    Parameters:
    input_data (list or array): List of sensor readings [MQ2, MQ3, MQ4, MQ6, MQ7, MQ135, TEMP, HUMI]
    
    Returns:
    dict: Predictions from all models with class labels
    """
    input_array = np.array(input_data).reshape(1, -1)
    
    # Load preprocessing objects using config paths
    with open(config.get_preprocessing_path('imputer'), 'rb') as f:
        imputer = pickle.load(f)
    
    with open(config.get_preprocessing_path('scaler'), 'rb') as f:
        scaler = pickle.load(f)
        
    with open(config.get_preprocessing_path('label_encoder'), 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Preprocess input data
    input_imputed = imputer.transform(input_array)
    input_scaled = scaler.transform(input_imputed)
    
    # Load models using config paths and make predictions
    ann_model = tf.keras.models.load_model(config.get_model_path('ann'))
    ann_pred_prob = ann_model.predict(input_scaled)
    ann_pred_class = np.argmax(ann_pred_prob, axis=1)[0]
    ann_pred_label = label_encoder.inverse_transform([ann_pred_class])[0]
    ann_confidence = float(np.max(ann_pred_prob))
    
    with open(config.get_model_path('random_forest'), 'rb') as f:
        rf_model = pickle.load(f)
    rf_pred_class = rf_model.predict(input_scaled)[0]
    rf_pred_label = label_encoder.inverse_transform([rf_pred_class])[0]
    
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(config.get_model_path('xgboost'))
    xgb_pred_class = xgb_model.predict(input_scaled)[0]
    xgb_pred_label = label_encoder.inverse_transform([xgb_pred_class])[0]
    
    return {
        'input_data': input_data,
        'predictions': {
            'ann': {
                'class_id': int(ann_pred_class),
                'class_label': ann_pred_label,
                'probability': ann_confidence
            },
            'random_forest': {
                'class_id': int(rf_pred_class),
                'class_label': rf_pred_label
            },
            'xgboost': {
                'class_id': int(xgb_pred_class),
                'class_label': xgb_pred_label
            }
        }
    }

if __name__ == "__main__":
    if len(sys.argv) > 8:

        sensor_readings = [float(arg) for arg in sys.argv[1:9]]
        result = predict_with_models(sensor_readings)
        print("\nInput data:", result['input_data'])
        print("\nPredictions:")
        print("ANN:", result['predictions']['ann']['class_label'], 
              f"(Probability: {result['predictions']['ann']['probability']:.4f})")
        print("Random Forest:", result['predictions']['random_forest']['class_label'])
        print("XGBoost:", result['predictions']['xgboost']['class_label'])
    else:
        example_data = [815, 2530, 1075, 2510, 1435, 2160, 37.0, 72.0] 
        result = predict_with_models(example_data)
        print("\nExample prediction with sample data:", example_data)
        print("\nPredictions:")
        print("ANN:", result['predictions']['ann']['class_label'], 
              f"(Probability: {result['predictions']['ann']['probability']:.4f})")
        print("Random Forest:", result['predictions']['random_forest']['class_label'])
        print("XGBoost:", result['predictions']['xgboost']['class_label'])
        
        print("\nUsage:")
        print("python predict.py MQ2 MQ3 MQ4 MQ6 MQ7 MQ135 TEMP HUMI")
        print("Example: python predict.py 815 2530 1075 2510 1435 2160 37.0 72.0")
