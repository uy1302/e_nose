# E-Nose Flask API Documentation

## Tổng Quan

Flask API backend cho hệ thống E-Nose, cung cấp các endpoint để dự đoán mùi từ dữ liệu cảm biến.

## Cài Đặt

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Cấu hình môi trường (tùy chọn)
cp config.env .env
# Chỉnh sửa .env theo nhu cầu

# 3. Chạy API server
python src/api.py
# Hoặc
python src/run_api.py
```

## API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-01-06T21:00:00.000Z",
    "service": "e-nose-api",
    "version": "1.0.0"
}
```

### 2. Dự Đoán với Dữ Liệu Thủ Công
```http
POST /predict
Content-Type: application/json

{
    "sensor_data": [815.0, 2530.0, 1075.0, 2510.0, 1435.0, 2160.0, 37.0, 72.0]
}
```

**Response:**
```json
{
    "input_data": [815.0, 2530.0, 1075.0, 2510.0, 1435.0, 2160.0, 37.0, 72.0],
    "predictions": {
        "ann": {
            "class_id": 0,
            "class_label": "fish_sauce",
            "probability": 0.95
        },
        "random_forest": {
            "class_id": 0,
            "class_label": "fish_sauce"
        },
        "xgboost": {
            "class_id": 0,
            "class_label": "fish_sauce"
        }
    },
    "metadata": {
        "timestamp": "2025-01-06T21:00:00.000Z",
        "sensor_names": ["MQ2", "MQ3", "MQ4", "MQ6", "MQ7", "MQ135", "TEMP", "HUMI"],
        "model_versions": {
            "ann": "v1.0",
            "random_forest": "v1.0",
            "xgboost": "v1.0"
        }
    }
}
```

### 3. Dự Đoán với Dữ Liệu ThingSpeak
```http
POST /predict/thingspeak
Content-Type: application/json

{
    "api_key": "RJNVLFM0O88JP765"
}
```

**Response:** Tương tự `/predict` nhưng có thêm metadata ThingSpeak.

### 4. Thông Tin Cảm Biến
```http
GET /sensors
```

**Response:**
```json
{
    "sensor_features": ["MQ2", "MQ3", "MQ4", "MQ6", "MQ7", "MQ135", "TEMP", "HUMI"],
    "sensor_count": 8,
    "sensor_types": {
        "gas_sensors": ["MQ2", "MQ3", "MQ4", "MQ6", "MQ7", "MQ135"],
        "environmental_sensors": ["TEMP", "HUMI"]
    },
    "sensor_descriptions": {
        "MQ2": "Smoke, Propane, Hydrogen",
        "MQ3": "Alcohol, Ethanol",
        "MQ4": "Methane, CNG Gas",
        "MQ6": "LPG, Propane Gas",
        "MQ7": "Carbon Monoxide",
        "MQ135": "Air Quality (Ammonia, Sulfide)",
        "TEMP": "Temperature (°C)",
        "HUMI": "Humidity (%)"
    }
}
```

### 5. Thông Tin Mô Hình
```http
GET /models
```

**Response:**
```json
{
    "models": {
        "ann": {
            "name": "Artificial Neural Network",
            "type": "deep_learning",
            "accuracy": "100%",
            "description": "Deep neural network with regularization"
        },
        "random_forest": {
            "name": "Random Forest",
            "type": "ensemble",
            "accuracy": "100%",
            "description": "Ensemble of decision trees"
        },
        "xgboost": {
            "name": "XGBoost",
            "type": "gradient_boosting",
            "accuracy": "100%",
            "description": "Gradient boosting algorithm"
        }
    },
    "classes": ["fish_sauce", "garlic", "lemon", "milk"],
    "ensemble_method": "majority_vote"
}
```

### 6. Lấy Dữ Liệu ThingSpeak
```http
POST /thingspeak/data
Content-Type: application/json

{
    "api_key": "RJNVLFM0O88JP765",
    "results": 10
}
```

## Error Handling

API trả về các mã lỗi HTTP chuẩn:

- `200`: Thành công
- `400`: Bad Request (dữ liệu đầu vào không hợp lệ)
- `404`: Not Found (endpoint không tồn tại)
- `422`: Unprocessable Entity (dữ liệu không thể xử lý)
- `500`: Internal Server Error
- `503`: Service Unavailable (ThingSpeak không khả dụng)

**Định dạng lỗi:**
```json
{
    "error": "Mô tả lỗi",
    "details": "Chi tiết lỗi (nếu có)"
}
```

## Cấu Hình Môi Trường

Các biến môi trường có thể thiết lập:

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `API_HOST` | `0.0.0.0` | Host để bind API |
| `API_PORT` | `5000` | Port cho API |
| `API_DEBUG` | `False` | Chế độ debug |
| `LOG_LEVEL` | `INFO` | Mức độ logging |

## Ví Dụ Sử Dụng

### Python
```python
import requests

# Dự đoán với dữ liệu thủ công
response = requests.post('http://localhost:5000/predict', json={
    'sensor_data': [815.0, 2530.0, 1075.0, 2510.0, 1435.0, 2160.0, 37.0, 72.0]
})
result = response.json()
print(f"Prediction: {result['predictions']['ann']['class_label']}")
```

### JavaScript
```javascript
// Dự đoán với ThingSpeak
fetch('http://localhost:5000/predict/thingspeak', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        api_key: 'RJNVLFM0O88JP765'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Prediction:', data.predictions);
});
```

### curl
```bash
# Health check
curl -X GET http://localhost:5000/health

# Dự đoán
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": [815.0, 2530.0, 1075.0, 2510.0, 1435.0, 2160.0, 37.0, 72.0]}'
```

## Deployment

### Docker (Tùy chọn)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY models/ ./models/
COPY configs/ ./configs/
EXPOSE 5000
CMD ["python", "src/run_api.py"]
```

### Production
- Sử dụng WSGI server như Gunicorn
- Thiết lập reverse proxy với Nginx
- Cấu hình HTTPS
- Monitoring và logging 