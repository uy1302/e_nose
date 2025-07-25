import pandas as pd
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier           # thêm KNN
from sklearn.neural_network import MLPClassifier
import joblib

# 1. Load dữ liệu
df = pd.read_csv('processed_data.csv')
df = df.drop(columns=['DATE', 'TIME', 'Start Time'])
X = df.drop(columns=['Label'])
y = df['Label']

# 2. Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# --- RandomForest --- 
print("Training RandomForest…")
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['sqrt', 'log2'],
    'random_state': [42]
}
rf_grid_search = GridSearchCV(
    RandomForestClassifier(),
    rf_param_grid,
    cv=5, n_jobs=-1, verbose=1
)
rf_grid_search.fit(X_train, y_train)
print("Best RandomForest parameters:", rf_grid_search.best_params_)
print("Best RandomForest accuracy:", rf_grid_search.best_score_)

# --- XGBoost --- 
print("Training XGBoost…")
xgb_param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'random_state': [42]
}
xgb_grid_search = GridSearchCV(
    XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    xgb_param_grid,
    cv=5, n_jobs=-1, verbose=1
)
xgb_grid_search.fit(X_train, y_train)
print("Best XGBoost parameters:", xgb_grid_search.best_params_)
print("Best XGBoost accuracy:", xgb_grid_search.best_score_)

# --- KNN (thay cho SVM) --- 
print("Training KNN…")
knn_param_grid = {
    'n_neighbors': [3, 5, 7, 9],      # số láng giềng
    'weights': ['uniform', 'distance'],  # cách cho trọng số
    'metric': ['euclidean', 'manhattan']
}
knn_grid_search = GridSearchCV(
    KNeighborsClassifier(),
    knn_param_grid,
    cv=5, n_jobs=-1, verbose=1
)
knn_grid_search.fit(X_train, y_train)
print("Best KNN parameters:", knn_grid_search.best_params_)
print("Best KNN accuracy:", knn_grid_search.best_score_)

# --- ANN (MLPClassifier) --- 
print("Training ANN…")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
ann_param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (50, 50)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam', 'sgd'],
    'max_iter': [200, 300]
}
ann_grid_search = GridSearchCV(
    MLPClassifier(random_state=42),
    ann_param_grid,
    cv=kf, n_jobs=-1, verbose=1
)
ann_grid_search.fit(X_train, y_train)
print("Best ANN parameters:", ann_grid_search.best_params_)
print("Best ANN accuracy:", ann_grid_search.best_score_)

# 4. Lưu model và scaler
joblib.dump(rf_grid_search.best_estimator_, 'random_forest_model.pkl')
joblib.dump(xgb_grid_search.best_estimator_, 'xgboost_model.pkl')
joblib.dump(knn_grid_search.best_estimator_, 'knn_model.pkl')   
joblib.dump(ann_grid_search.best_estimator_, 'ann_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Tất cả mô hình đã được huấn luyện và lưu.")
