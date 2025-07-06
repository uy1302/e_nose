import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from config import config
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("Loading preprocessed data...")
formatted_data_path = config.get_path('paths', 'data', 'formatted_data')
X_train = np.load(formatted_data_path / 'X_train.npy')
y_train = np.load(formatted_data_path / 'y_train.npy')
X_test = np.load(formatted_data_path / 'X_test.npy')
y_test = np.load(formatted_data_path / 'y_test.npy')

label_encoder_path = config.get_path('paths', 'data', 'decoder_scaler') / 'label_encoder.pkl'
with open(label_encoder_path, 'rb') as f:   
    label_encoder = pickle.load(f)

print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")
print(f"Classes: {label_encoder.classes_}")

print("\n=== Training Random Forest model ===")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    class_weight='balanced',
    random_state=69,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
print("Random Forest model trained.")

y_pred_rf = rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Test Accuracy: {accuracy_rf:.4f}")

cm_rf = confusion_matrix(y_test, y_pred_rf)
print("\nRandom Forest Confusion Matrix:")
print(cm_rf)

report_rf = classification_report(y_test, y_pred_rf, target_names=label_encoder.classes_, output_dict=True)
print("\nRandom Forest Classification Report:")
print(classification_report(y_test, y_pred_rf, target_names=label_encoder.classes_))

rf_model_path = config.get_model_path('random_forest')
with open(rf_model_path, 'wb') as f:
    pickle.dump(rf_model, f)
print(f"Random Forest model saved to {rf_model_path}")

feature_importances_rf = rf_model.feature_importances_
feature_names = ['MQ2', 'MQ3', 'MQ4', 'MQ6', 'MQ7', 'MQ135', 'TEMP', 'HUMI']

plt.figure(figsize=(10, 6))
sorted_idx = np.argsort(feature_importances_rf)
plt.barh(range(len(sorted_idx)), feature_importances_rf[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance')
plt.tight_layout()
docs_path = config.get_path('paths', 'docs')
plt.savefig(str(docs_path / 'random_forest_feature_importance.png'))
print(f"Feature importance plot saved to {docs_path / 'random_forest_feature_importance.png'}")

print("\n=== Training XGBoost model ===")
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='multi:softmax',
    num_class=len(label_encoder.classes_),
    random_state=69,
    use_label_encoder=False,
    eval_metric='mlogloss'
)

xgb_model.fit(X_train, y_train)
print("XGBoost model trained.")

y_pred_xgb = xgb_model.predict(X_test)
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
print(f"XGBoost Test Accuracy: {accuracy_xgb:.4f}")

cm_xgb = confusion_matrix(y_test, y_pred_xgb)
print("\nXGBoost Confusion Matrix:")
print(cm_xgb)

report_xgb = classification_report(y_test, y_pred_xgb, target_names=label_encoder.classes_, output_dict=True)
print("\nXGBoost Classification Report:")
print(classification_report(y_test, y_pred_xgb, target_names=label_encoder.classes_))

xgb_model_path = config.get_model_path('xgboost')
xgb_model.save_model(str(xgb_model_path))
print(f"XGBoost model saved to {xgb_model_path}")

feature_importances_xgb = xgb_model.feature_importances_

plt.figure(figsize=(10, 6))
sorted_idx = np.argsort(feature_importances_xgb)
plt.barh(range(len(sorted_idx)), feature_importances_xgb[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance')
plt.tight_layout()
plt.savefig(str(docs_path / 'xgboost_feature_importance.png'))
print(f"Feature importance plot saved to {docs_path / 'xgboost_feature_importance.png'}")

import json
results = {
    'random_forest': {
        'accuracy': float(accuracy_rf),
        'classification_report': report_rf
    },
    'xgboost': {
        'accuracy': float(accuracy_xgb),
        'classification_report': report_xgb
    }
}

output_path = config.get_path('paths', 'output') / 'tree_models_results.json'
with open(output_path, 'w') as f:
    json.dump(results, f, indent=4)
print(f"Results saved to {output_path}")

print("\nTraining and evaluation of tree-based models complete.")
