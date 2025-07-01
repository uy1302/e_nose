import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("Loading preprocessed data...")
X_train = np.load('/formatted_data/X_train.npy')
y_train = np.load('/formatted_data/y_train.npy')
X_test = np.load('/formatted_data/X_test.npy')
y_test = np.load('/formatted_data/y_test.npy')

with open('/decoder_scaler/label_encoder.pkl', 'rb') as f:
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
    random_state=42,
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

with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("Random Forest model saved to random_forest_model.pkl")

feature_importances_rf = rf_model.feature_importances_
feature_names = ['MQ2', 'MQ3', 'MQ4', 'MQ6', 'MQ7', 'MQ135', 'TEMP', 'HUMI']

plt.figure(figsize=(10, 6))
sorted_idx = np.argsort(feature_importances_rf)
plt.barh(range(len(sorted_idx)), feature_importances_rf[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance')
plt.tight_layout()
plt.savefig('random_forest_feature_importance.png')
print("Feature importance plot saved to random_forest_feature_importance.png")

print("\n=== Training XGBoost model ===")
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='multi:softmax',
    num_class=len(label_encoder.classes_),
    random_state=42,
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

xgb_model.save_model('xgboost_model.json')
print("XGBoost model saved to xgboost_model.json")

feature_importances_xgb = xgb_model.feature_importances_

plt.figure(figsize=(10, 6))
sorted_idx = np.argsort(feature_importances_xgb)
plt.barh(range(len(sorted_idx)), feature_importances_xgb[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance')
plt.tight_layout()
plt.savefig('xgboost_feature_importance.png')

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

with open('tree_models_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\nTraining and evaluation of tree-based models complete.")
