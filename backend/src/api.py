from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adapter import fetch_thingspeak_data, process_thingspeak_data
from predict import predict_with_models, mask_sensor_names

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

# Predict endpoint with ThingSpeak data
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict smell category from ThingSpeak averaged data
    
    Expected JSON payload:
    {
        "api_key": "P91SEPV5ZZG00Y4S"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'error': 'Missing api_key in request body',
                'expected_format': {
                    'api_key': 'P91SEPV5ZZG00Y4S'
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
        
        # Add ThingSpeak metadata with masked sensor names
        original_sensor_names = ['MQ136', 'MQ137', 'TEMP', 'HUMI']
        masked_sensor_names = mask_sensor_names(original_sensor_names)
        
        result['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'sensor_names': masked_sensor_names,
            'thingspeak': {
                'records_fetched': len(thingspeak_data),
                'latest_entry_time': thingspeak_data[-1].get('created_at'),
                'api_key': api_key
            },
            'model_versions': {
                'base_1': 'v1.0',
                'base_2': 'v1.0',
                'base_3': 'v1.0',
                'base_4': 'v1.0',
                'meta': 'v1.0'
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

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': {
            'GET /health': 'Health check',
            'POST /predict': 'Predict with ThingSpeak data'
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