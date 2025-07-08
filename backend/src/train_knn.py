import numpy as np
import pandas as pd
import pickle
import json
import matplotlib.pyplot as plt
import seaborn as sns
from config import config
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import time

print("="*60)
print("KNN MODEL TRAINING PIPELINE")
print("="*60)

print("Loading preprocessed data...")
# Load data using config paths
formatted_data_path = config.get_path('paths', 'data', 'formatted_data')
X_train = np.load(formatted_data_path / 'X_train.npy')
y_train = np.load(formatted_data_path / 'y_train.npy')
X_test = np.load(formatted_data_path / 'X_test.npy')
y_test = np.load(formatted_data_path / 'y_test.npy')

# Load label encoder using config path
label_encoder_path = config.get_path('paths', 'data', 'decoder_scaler') / 'label_encoder.pkl'
with open(label_encoder_path, 'rb') as f:   
    label_encoder = pickle.load(f)

print(f"Data loaded successfully!")
print(f"   X_train shape: {X_train.shape}")
print(f"   y_train shape: {y_train.shape}")
print(f"   X_test shape: {X_test.shape}")
print(f"   y_test shape: {y_test.shape}")
print(f"   Classes: {label_encoder.classes_}")
print(f"   Number of classes: {len(label_encoder.classes_)}")

print("\n" + "="*60)
print("KNN HYPERPARAMETER TUNING")
print("="*60)

# Define parameter grid for hyperparameter tuning
param_grid = {
    'n_neighbors': [21, 23, 25, 27, 29, 31, 33, 35],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'metric': ['euclidean', 'manhattan', 'minkowski']
}

print("Parameter grid:")
for key, values in param_grid.items():
    print(f"   {key}: {values}")

# Create KNN classifier
knn = KNeighborsClassifier()

print("\nStarting GridSearchCV...")
start_time = time.time()

# Perform grid search with cross-validation
grid_search = GridSearchCV(
    estimator=knn,
    param_grid=param_grid,
    cv=5,  # 5-fold cross validation
    scoring='accuracy',
    n_jobs=-1,  # Use all available processors
    verbose=1
)

grid_search.fit(X_train, y_train)

tuning_time = time.time() - start_time
print(f"Hyperparameter tuning completed in {tuning_time:.2f} seconds")

print("\nBest parameters found:")
for key, value in grid_search.best_params_.items():
    print(f"   {key}: {value}")
print(f"Best cross-validation score: {grid_search.best_score_:.4f}")

print("\n" + "="*60)
print("TRAINING FINAL KNN MODEL")
print("="*60)

# Train the final model with best parameters
best_knn = grid_search.best_estimator_
print("Using best parameters from grid search")



print("\nEvaluating KNN model on test data...")
y_pred_knn = best_knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)

print(f"KNN Test Accuracy: {accuracy_knn:.4f} ({accuracy_knn*100:.2f}%)")

# Confusion Matrix
cm_knn = confusion_matrix(y_test, y_pred_knn)
print("\nKNN Confusion Matrix:")
print(cm_knn)

# Classification Report
report_knn = classification_report(y_test, y_pred_knn, target_names=label_encoder.classes_, output_dict=True)
print("\nKNN Classification Report:")
print(classification_report(y_test, y_pred_knn, target_names=label_encoder.classes_))

print("\n" + "="*60)
print("SAVING MODEL AND RESULTS")
print("="*60)

# Save the trained model
knn_model_path = config.get_model_path('knn')
with open(knn_model_path, 'wb') as f:
    pickle.dump(best_knn, f)
print(f"KNN model saved to: {knn_model_path}")

# Save detailed results
results = {
    'model_info': {
        'name': 'K-Nearest Neighbors',
        'type': 'instance_based',
        'algorithm': 'KNN'
    },
    'hyperparameters': {
        'best_params': grid_search.best_params_,
        'cv_score': float(grid_search.best_score_),
        'param_grid': param_grid
    },
    'performance': {
        'test_accuracy': float(accuracy_knn),
        'confusion_matrix': cm_knn.tolist(),
        'classification_report': report_knn
    },
    'training_info': {
        'training_time': float(tuning_time),
        'cv_folds': 5,
        'data_shapes': {
            'X_train': list(X_train.shape),
            'X_test': list(X_test.shape),
            'y_train': list(y_train.shape),
            'y_test': list(y_test.shape)
        }
    }
}

# Save results to JSON
results_path = config.get_path('paths', 'data', 'processed') / 'knn_results.json'
with open(str(results_path), 'w') as f:
    json.dump(results, f, indent=4)
print(f"Results saved to: {results_path}")

print("\n" + "="*60)
print("GENERATING VISUALIZATIONS")
print("="*60)

# Create visualization directory path
docs_path = config.get_path('paths', 'docs')

# 1. Confusion Matrix Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Blues', 
            xticklabels=label_encoder.classes_, 
            yticklabels=label_encoder.classes_)
plt.title('KNN Model - Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
cm_plot_path = docs_path / 'knn_confusion_matrix.png'
plt.savefig(str(cm_plot_path), dpi=300, bbox_inches='tight')
print(f"Confusion matrix plot saved to: {cm_plot_path}")
plt.close()

# 2. Hyperparameter tuning results
if hasattr(grid_search, 'cv_results_'):
    cv_results = pd.DataFrame(grid_search.cv_results_)
    
    # Plot parameter sensitivity
    plt.figure(figsize=(15, 10))
    
    # K-neighbors sensitivity
    plt.subplot(2, 2, 1)
    k_results = cv_results.groupby('param_n_neighbors')['mean_test_score'].mean()
    plt.plot(k_results.index.values, k_results.values, 'o-')
    plt.title('Accuracy vs Number of Neighbors (k)')
    plt.xlabel('k (Number of Neighbors)')
    plt.ylabel('Cross-Validation Accuracy')
    plt.grid(True, alpha=0.3)
    
    # Weights comparison
    plt.subplot(2, 2, 2)
    weights_results = cv_results.groupby('param_weights')['mean_test_score'].mean()
    plt.bar(weights_results.index.values, weights_results.values)
    plt.title('Accuracy vs Weight Function')
    plt.xlabel('Weight Function')
    plt.ylabel('Cross-Validation Accuracy')
    plt.grid(True, alpha=0.3)
    
    # Algorithm comparison
    plt.subplot(2, 2, 3)
    algo_results = cv_results.groupby('param_algorithm')['mean_test_score'].mean()
    plt.bar(range(len(algo_results)), algo_results.values)
    plt.xticks(range(len(algo_results)), list(algo_results.index), rotation=45)
    plt.title('Accuracy vs Algorithm')
    plt.xlabel('Algorithm')
    plt.ylabel('Cross-Validation Accuracy')
    plt.grid(True, alpha=0.3)
    
    # Metric comparison
    plt.subplot(2, 2, 4)
    metric_results = cv_results.groupby('param_metric')['mean_test_score'].mean()
    plt.bar(range(len(metric_results)), metric_results.values)
    plt.xticks(range(len(metric_results)), list(metric_results.index), rotation=45)
    plt.title('Accuracy vs Distance Metric')
    plt.xlabel('Distance Metric')
    plt.ylabel('Cross-Validation Accuracy')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    hyperparam_plot_path = docs_path / 'knn_hyperparameter_analysis.png'
    plt.savefig(str(hyperparam_plot_path), dpi=300, bbox_inches='tight')
    print(f"Hyperparameter analysis plot saved to: {hyperparam_plot_path}")
    plt.close()

# 3. Performance metrics visualization
plt.figure(figsize=(12, 6))

# Accuracy by class
plt.subplot(1, 2, 1)
class_accuracies = []
for i, class_name in enumerate(label_encoder.classes_):
    if class_name in report_knn and 'f1-score' in report_knn[class_name]:
        class_acc = report_knn[class_name]['f1-score']
        class_accuracies.append(class_acc)
    else:
        class_accuracies.append(0.0)

plt.bar(range(len(label_encoder.classes_)), class_accuracies)
plt.xticks(range(len(label_encoder.classes_)), label_encoder.classes_, rotation=45)
plt.title('F1-Score by Class')
plt.xlabel('Class')
plt.ylabel('F1-Score')
plt.grid(True, alpha=0.3)

# Overall metrics
plt.subplot(1, 2, 2)
metrics = ['precision', 'recall', 'f1-score']
macro_scores = []
for metric in metrics:
    if 'macro avg' in report_knn and metric in report_knn['macro avg']:
        macro_scores.append(report_knn['macro avg'][metric])
    else:
        macro_scores.append(0.0)

plt.bar(metrics, macro_scores)
plt.title('Overall Performance Metrics (Macro Average)')
plt.ylabel('Score')
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)

plt.tight_layout()
performance_plot_path = docs_path / 'knn_performance_metrics.png'
plt.savefig(str(performance_plot_path), dpi=300, bbox_inches='tight')
print(f"Performance metrics plot saved to: {performance_plot_path}")
plt.close()

print("\n" + "="*60)
print("KNN TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)

print(f"""
FINAL RESULTS:
   Test Accuracy: {accuracy_knn:.4f} ({accuracy_knn*100:.2f}%)
   Best k: {grid_search.best_params_['n_neighbors']}
   Best weights: {grid_search.best_params_['weights']}
   Best algorithm: {grid_search.best_params_['algorithm']}
   Best metric: {grid_search.best_params_['metric']}
   
FILES SAVED:
   Model: {knn_model_path}
   Results: {results_path}
   Confusion Matrix: {cm_plot_path}
   Hyperparameter Analysis: {hyperparam_plot_path}
   Performance Metrics: {performance_plot_path}
""")

print("KNN model is now ready for inference!")
print("You can use this model in the prediction pipeline alongside ANN, RF, and XGB.") 