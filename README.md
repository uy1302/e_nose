# 🔬 E-Nose - Electronic Nose System

Hệ thống mũi điện tử (E-Nose) sử dụng Machine Learning để phân loại và nhận diện các loại mùi khác nhau thông qua dữ liệu cảm biến.

## 📁 Cấu trúc dự án

```
e_nose/
├── src/                    # Source code chính
│   ├── config.py          # Configuration management
│   ├── preprocessing.py   # Data preprocessing
│   ├── train_ann.py      # ANN model training
│   ├── train_tree_model.py # Tree models training
│   ├── predict.py        # Prediction module
│   ├── compare_model.py  # Model comparison
│   ├── visual_gen.py     # Visualization generation
│   └── app.py            # Web application (Flask/Streamlit)
├── models/                # Trained models
│   ├── ann_model.h5      # ANN model (best)
│   ├── ann_model_best.h5 # ANN model checkpoint
│   ├── random_forest_model.pkl # Random Forest model
│   └── xgboost_model.json # XGBoost model
├── data/                  # Data files
│   ├── raw/              # Raw sensor data
│   │   ├── fw_2_0_1/     # Firmware v2.0.1 data
│   │   ├── fw_3_0_1/     # Firmware v3.0.1 data
│   │   └── mvp/          # MVP data
│   └── processed/        # Processed data
│       ├── formatted_data/ # Formatted training data
│       ├── decoder_scaler/ # Preprocessing objects
│       ├── *.csv         # Processed CSV files
│       └── *.json        # Model evaluation results
├── configs/               # Configuration files
│   └── config.yaml       # Main configuration
├── scripts/               # Utility scripts
│   └── setup.py          # Project setup script
├── docs/                  # Documentation & visualizations
│   ├── *.png             # Generated plots
│   └── images/           # Project images
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Cài đặt và thiết lập

### 1. Clone repository
```bash
git clone <repository-url>
cd e_nose
```

### 2. Chạy setup tự động
```bash
python scripts/setup.py
```

### 3. Hoặc cài đặt thủ công
```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

## 🔧 Sử dụng

### 1. Preprocessing data
```bash
cd src
python preprocessing.py
```

### 2. Huấn luyện mô hình

#### Huấn luyện ANN:
```bash
python train_ann.py
```

#### Huấn luyện Tree models (Random Forest & XGBoost):
```bash
python train_tree_model.py
```

### 3. So sánh mô hình
```bash
python compare_model.py
```

### 4. Dự đoán
```bash
# Dự đoán với dữ liệu mẫu
python predict.py

# Dự đoán với dữ liệu tùy chỉnh
python predict.py 815 2530 1075 2510 1435 2160 37.0 72.0
```

### 5. Tạo visualizations
```bash
python visual_gen.py
```

### 6. Chạy web application
```bash
python app.py
```

## 📊 Mô hình và độ chính xác

Dự án sử dụng 3 mô hình machine learning:

1. **ANN (Artificial Neural Network)** - `models/ann_model.h5`
   - Kiến trúc: 64 → 128 → 64 → num_classes
   - Regularization: L2, Dropout, BatchNormalization

2. **Random Forest** - `models/random_forest_model.pkl`
   - Ensemble method với multiple decision trees

3. **XGBoost** - `models/xgboost_model.json`
   - Gradient boosting algorithm

## 🔍 Cảm biến được sử dụng

- **MQ2**: Khí dễ cháy, khói
- **MQ3**: Rượu, ethanol
- **MQ4**: Methane, khí thiên nhiên
- **MQ6**: LPG, butane
- **MQ7**: Carbon monoxide
- **MQ135**: Chất lượng không khí
- **TEMP**: Nhiệt độ
- **HUMI**: Độ ẩm

## 🎯 Các loại mùi được phân loại

- Normal (Không khí bình thường)
- Coffee (Cà phê)
- CocaCola
- RedBull  
- Apple_Juice (Nước ép táo)
- Sweet_Tea (Trà ngọt)
- Water (Nước)

## ⚙️ Cấu hình

Tất cả cấu hình được quản lý trong `configs/config.yaml`:

- Đường dẫn files và thư mục
- Tham số huấn luyện mô hình
- Cấu hình cảm biến
- Thiết lập visualization

## 📈 Kết quả và đánh giá

Kết quả đánh giá mô hình được lưu trong:
- `data/processed/ann_classification_report.json`
- `data/processed/tree_models_results.json`
- `data/processed/evaluation_summary.json`

Visualizations được lưu trong `docs/`:
- Training history
- Model comparison
- Feature importance
- Dataset visualization

## 🛠️ Development

### Thêm model mới
1. Tạo script huấn luyện trong `src/`
2. Cập nhật `configs/config.yaml`
3. Cập nhật `src/config.py` nếu cần
4. Cập nhật `src/predict.py` để support model mới

### Thêm loại mũi mới
1. Thu thập data và đặt trong `data/raw/`
2. Cập nhật class names trong `configs/config.yaml`
3. Chạy lại preprocessing và training

## 📝 License

[LICENSE](LICENSE)

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Liên hệ

Nếu có câu hỏi hoặc vấn đề, vui lòng tạo issue trên GitHub repository.