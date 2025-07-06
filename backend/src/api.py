from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import logging
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from predict import predict_with_models
from adapter import fetch_thingspeak_data, process_thingspeak_data
from config import config

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'e-nose-api',
        'version': '1.0.0'
    })

# Predict endpoint with manual input
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict smell category from sensor data
    
    Expected JSON payload:
    {
        "sensor_data": [MQ2, MQ3, MQ4, MQ6, MQ7, MQ135, TEMP, HUMI]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({
                'error': 'Missing sensor_data in request body',
                'expected_format': {
                    'sensor_data': [815.0, 2530.0, 1075.0, 2510.0, 1435.0, 2160.0, 37.0, 72.0]
                }
            }), 400
        
        sensor_data = data['sensor_data']
        
        # Validate sensor data
        if len(sensor_data) != 8:
            return jsonify({
                'error': 'sensor_data must contain exactly 8 values',
                'received': len(sensor_data),
                'expected': 8,
                'sensor_names': config.sensor_features
            }), 400
        
        # Convert to float and validate
        try:
            sensor_values = [float(val) for val in sensor_data]
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': 'All sensor values must be numeric',
                'details': str(e)
            }), 400
        
        # Make prediction
        result = predict_with_models(sensor_values)
        
        # Add metadata
        result['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'sensor_names': config.sensor_features,
            'model_versions': {
                'ann': 'v1.0',
                'random_forest': 'v1.0', 
                'xgboost': 'v1.0'
            }
        }
        
        logger.info(f"Prediction successful for input: {sensor_values[:3]}...")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': 'Internal server error during prediction',
            'details': str(e)
        }), 500

# Predict endpoint with ThingSpeak data
@app.route('/predict/thingspeak', methods=['POST'])
def predict_thingspeak():
    """
    Predict smell category from ThingSpeak latest data
    
    Expected JSON payload:
    {
        "api_key": "RJNVLFM0O88JP765"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'error': 'Missing api_key in request body',
                'expected_format': {
                    'api_key': 'RJNVLFM0O88JP765'
                }
            }), 400
        
        api_key = data['api_key']
        
        # Fetch data from ThingSpeak
        thingspeak_data = fetch_thingspeak_data(api_key)
        
        if not thingspeak_data:
            return jsonify({
                'error': 'Failed to fetch data from ThingSpeak',
                'api_key': api_key
            }), 503
        
        # Process data to get sensor values
        sensor_values = process_thingspeak_data(thingspeak_data)
        
        if not sensor_values:
            return jsonify({
                'error': 'Failed to process ThingSpeak data',
                'raw_data_count': len(thingspeak_data)
            }), 422
        
        # Make prediction
        result = predict_with_models(sensor_values)
        
        # Add ThingSpeak metadata
        result['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'sensor_names': config.sensor_features,
            'thingspeak': {
                'records_fetched': len(thingspeak_data),
                'latest_entry_time': thingspeak_data[-1].get('created_at'),
                'api_key': api_key
            },
            'model_versions': {
                'ann': 'v1.0',
                'random_forest': 'v1.0',
                'xgboost': 'v1.0'
            }
        }
        
        logger.info(f"ThingSpeak prediction successful, {len(thingspeak_data)} records fetched")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"ThingSpeak prediction error: {str(e)}")
        return jsonify({
            'error': 'Internal server error during ThingSpeak prediction',
            'details': str(e)
        }), 500

# Get sensor configuration
@app.route('/sensors', methods=['GET'])
def get_sensors():
    """Get sensor configuration and information"""
    return jsonify({
        'sensor_features': config.sensor_features,
        'sensor_count': len(config.sensor_features),
        'sensor_types': {
            'gas_sensors': ['MQ2', 'MQ3', 'MQ4', 'MQ6', 'MQ7', 'MQ135'],
            'environmental_sensors': ['TEMP', 'HUMI']
        },
        'sensor_descriptions': {
            'MQ2': 'Smoke, Propane, Hydrogen',
            'MQ3': 'Alcohol, Ethanol',
            'MQ4': 'Methane, CNG Gas',
            'MQ6': 'LPG, Propane Gas',
            'MQ7': 'Carbon Monoxide',
            'MQ135': 'Air Quality (Ammonia, Sulfide)',
            'TEMP': 'Temperature (°C)',
            'HUMI': 'Humidity (%)'
        }
    })

# Get model information
@app.route('/models', methods=['GET'])
def get_models():
    """Get information about available models"""
    return jsonify({
        'models': {
            'ann': {
                'name': 'Artificial Neural Network',
                'type': 'deep_learning',
                'accuracy': '100%',
                'description': 'Deep neural network with regularization'
            },
            'random_forest': {
                'name': 'Random Forest',
                'type': 'ensemble',
                'accuracy': '100%',
                'description': 'Ensemble of decision trees'
            },
            'xgboost': {
                'name': 'XGBoost',
                'type': 'gradient_boosting',
                'accuracy': '100%',
                'description': 'Gradient boosting algorithm'
            }
        },
        'classes': [
            'fish_sauce',
            'garlic', 
            'lemon',
            'milk'
        ],
        'ensemble_method': 'majority_vote'
    })

# Get ThingSpeak data endpoint
@app.route('/thingspeak/data', methods=['POST'])
def get_thingspeak_data():
    """
    Fetch raw data from ThingSpeak
    
    Expected JSON payload:
    {
        "api_key": "RJNVLFM0O88JP765",
        "results": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'error': 'Missing api_key in request body'
            }), 400
        
        api_key = data['api_key']
        results = data.get('results', 10)
        
        # Fetch data from ThingSpeak
        thingspeak_data = fetch_thingspeak_data(api_key, results)
        
        if not thingspeak_data:
            return jsonify({
                'error': 'Failed to fetch data from ThingSpeak'
            }), 503
        
        return jsonify({
            'data': thingspeak_data,
            'count': len(thingspeak_data),
            'metadata': {
                'api_key': api_key,
                'results_requested': results,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"ThingSpeak data fetch error: {str(e)}")
        return jsonify({
            'error': 'Internal server error during data fetch',
            'details': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': {
            'GET /health': 'Health check',
            'POST /predict': 'Predict with manual sensor data',
            'POST /predict/thingspeak': 'Predict with ThingSpeak data',
            'GET /sensors': 'Get sensor information',
            'GET /models': 'Get model information',
            'POST /thingspeak/data': 'Fetch ThingSpeak data'
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500

# Main entry point
if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting E-Nose API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug) 