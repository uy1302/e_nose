import streamlit as st
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
import xgboost as xgb
import requests
import json
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import keras
from config import config
import adapter

# Set page configuration
st.set_page_config(
    page_title="E-Nose MVP",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-bottom: 1rem;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .prediction-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Function to load models and preprocessing objects
@st.cache_resource
def load_models():
    # Load preprocessing objects using config paths
    with open(str(config.get_preprocessing_path('scaler')), 'rb') as f:
        scaler = pickle.load(f)
    
    with open(str(config.get_preprocessing_path('label_encoder')), 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Load models using config paths
    ann_model = keras.models.load_model(str(config.get_model_path('ann')))
    
    with open(str(config.get_model_path('random_forest')), 'rb') as f:
        rf_model = pickle.load(f)
    
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(str(config.get_model_path('xgboost')))
    
    return {
        'scaler': scaler,
        'label_encoder': label_encoder,
        'ann_model': ann_model,
        'rf_model': rf_model,
        'xgb_model': xgb_model
    }

# Function to make predictions
def predict_with_models(input_data, models):
    # Convert input to numpy array
    input_array = np.array(input_data).reshape(1, -1)
    
    # Handle missing values
    for i in range(len(input_array[0])):
        if np.isnan(input_array[0, i]):
            # Replace with mean (which will be 0 after scaling)
            input_array[0, i] = 0
    
    # Apply preprocessing
    input_scaled = models['scaler'].transform(input_array)
    
    # Predict with ANN model
    ann_pred_prob = models['ann_model'].predict(input_scaled)
    ann_pred_class = np.argmax(ann_pred_prob, axis=1)[0]
    ann_pred_label = models['label_encoder'].inverse_transform([ann_pred_class])[0]
    
    # Predict with Random Forest model
    rf_pred_class = models['rf_model'].predict(input_scaled)[0]
    rf_pred_label = models['label_encoder'].inverse_transform([rf_pred_class])[0]
    
    # Predict with XGBoost model
    xgb_pred_class = models['xgb_model'].predict(input_scaled)[0]
    xgb_pred_label = models['label_encoder'].inverse_transform([xgb_pred_class])[0]
    
    # Return predictions
    return {
        'input_data': input_data,
        'predictions': {
            'ann': {
                'class_id': int(ann_pred_class),
                'class_label': ann_pred_label
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

# Function to display prediction results
def display_prediction_results(result):
    # Create columns for each model
    col1, col2, col3 = st.columns(3)
    
    # ANN prediction
    with col1:
        st.markdown(f"""
        <div class="prediction-box" style="background-color: rgba(76, 175, 80, 0.1); border: 1px solid #4CAF50;">
            <div class="prediction-header">Artificial Neural Network</div>
            <p><b>Prediction:</b> {result['predictions']['ann']['class_label']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Random Forest prediction
    with col2:
        st.markdown(f"""
        <div class="prediction-box" style="background-color: rgba(33, 150, 243, 0.1); border: 1px solid #2196F3;">
            <div class="prediction-header">Random Forest</div>
            <p><b>Prediction:</b> {result['predictions']['random_forest']['class_label']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # XGBoost prediction
    with col3:
        st.markdown(f"""
        <div class="prediction-box" style="background-color: rgba(255, 152, 0, 0.1); border: 1px solid #FF9800;">
            <div class="prediction-header">XGBoost</div>
            <p><b>Prediction:</b> {result['predictions']['xgboost']['class_label']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if all models agree
    predictions = [
        result['predictions']['ann']['class_label'],
        result['predictions']['random_forest']['class_label'],
        result['predictions']['xgboost']['class_label']
    ]
    
    if len(set(predictions)) == 1:
        st.success(f"All models agree: The sensor readings indicate **{predictions[0]}**")
    else:
        st.warning("Models have different predictions. Consider collecting more data.")

# Function to display input data
def display_input_data(input_data):
    # Create a DataFrame for better display
    sensor_names = config.sensor_features
    df = pd.DataFrame([input_data])
    df.columns = sensor_names
    
    # Display as a table
    st.subheader("Input Sensor Data")
    st.dataframe(df, use_container_width=True)
    
    # Create a bar chart for sensor values
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Separate temperature and humidity for a different scale
    gas_sensors = df.iloc[0, :6].values
    temp_humi = df.iloc[0, 6:].values
    
    # Plot gas sensors
    ax.bar(sensor_names[:6], gas_sensors, color='skyblue')
    ax.set_ylabel('Gas Sensor Values')
    
    # Create a second y-axis for temperature and humidity
    ax2 = ax.twinx()
    ax2.bar(sensor_names[6:], temp_humi, color=['red', 'green'])
    ax2.set_ylabel('Temperature (°C) / Humidity (%)')
    
    plt.title('Sensor Readings')
    plt.tight_layout()
    
    # Display the chart
    st.pyplot(fig)

# Main function
def main():
    # Load models
    models = load_models()
    
    # Header
    st.markdown('<h1 class="main-header">E-Nose MVP</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Input Options")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Manual Input", "ThingSpeak API"]
    )
    
    # Initialize input_data
    input_data = None
    
    # Manual Input
    if input_method == "Manual Input":
        st.markdown('<h2 class="sub-header">Manual Sensor Input</h2>', unsafe_allow_html=True)
        
        # Create two rows of 4 inputs each
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mq2 = st.number_input("MQ2 Sensor", value=815.0)
        with col2:
            mq3 = st.number_input("MQ3 Sensor", value=2530.0)
        with col3:
            mq4 = st.number_input("MQ4 Sensor", value=1075.0)
        with col4:
            mq6 = st.number_input("MQ6 Sensor", value=2510.0)
            
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            mq7 = st.number_input("MQ7 Sensor", value=1435.0)
        with col6:
            mq135 = st.number_input("MQ135 Sensor", value=2160.0)
        with col7:
            temp = st.number_input("Temperature (°C)", value=37.0)
        with col8:
            humi = st.number_input("Humidity (%)", value=72.0)
        
        input_data = [mq2, mq3, mq4, mq6, mq7, mq135, temp, humi]
        
        if st.button("Predict with Manual Input", type="primary"):
            # Display input data
            display_input_data(input_data)
            
            # Make prediction
            result = predict_with_models(input_data, models)
            
            # Display results
            st.markdown('<h2 class="sub-header">Prediction Results</h2>', unsafe_allow_html=True)
            display_prediction_results(result)
    
    # ThingSpeak API
    else:
        st.markdown('<h2 class="sub-header">ThingSpeak API Data</h2>', unsafe_allow_html=True)
        
        api_key = st.text_input("ThingSpeak API Key", value="RJNVLFM0O88JP765")
        
        if st.button("Fetch Latest Data", type="primary"):
            with st.spinner("Fetching data from ThingSpeak..."):
                data = adapter.fetch_thingspeak_data(api_key)
                
                if data:
                    st.success(f"Successfully fetched {len(data)} records from ThingSpeak")
                    
                    # Process the data to get the averaged sensor values
                    input_data = adapter.process_thingspeak_data(data)
                    
                    if input_data:
                        # Display input data
                        display_input_data(input_data)
                        
                        # Make prediction
                        result = predict_with_models(input_data, models)
                        
                        # Display results
                        st.markdown('<h2 class="sub-header">Prediction Results</h2>', unsafe_allow_html=True)
                        display_prediction_results(result)
                    else:
                        st.error("Could not process sensor data from ThingSpeak")
    
    # About section
    with st.expander("About this App"):
        st.markdown("""
        This application classifies ESP32 sensor data into four categories:
        - fish_sauce
        - garlic
        - lemon
        - milk
        
        The app uses three machine learning models:
        1. **Artificial Neural Network**: A deep learning model with regularization
        2. **Random Forest**: An ensemble of decision trees
        3. **XGBoost**: A gradient boosting algorithm
        
        All models were trained on ESP32 sensor data and achieved 100% accuracy on the test set.
        
        The most important sensors for classification are:
        - MQ6
        - MQ2
        - MQ4
        """)

if __name__ == "__main__":
    main()
