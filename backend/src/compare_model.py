import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import pickle
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns


print("Loading model results...")
with open('tree_models_results.json', 'r') as f:
    tree_results = json.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
    
class_names = label_encoder.classes_

models = ['Artificial Neural Network', 'Random Forest', 'XGBoost']
accuracies = [1.0, tree_results['random_forest']['accuracy'], tree_results['xgboost']['accuracy']]

plt.figure(figsize=(10, 6))
plt.bar(models, accuracies, color=['blue', 'green', 'orange'])
plt.ylim(0.9, 1.01)  
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, acc in enumerate(accuracies):
    plt.text(i, acc + 0.001, f'{acc:.4f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('model_comparison.png')
print("Model comparison chart saved to model_comparison.png")

print("\nAnalyzing feature importance across models...")
feature_names = ['MQ2', 'MQ3', 'MQ4', 'MQ6', 'MQ7', 'MQ135', 'TEMP', 'HUMI']

with open('random_forest_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)
    
rf_importance = rf_model.feature_importances_

import xgboost as xgb
xgb_model = xgb.XGBClassifier()
xgb_model.load_model('xgboost_model.json')
xgb_importance = xgb_model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Random Forest': rf_importance,
    'XGBoost': xgb_importance
})

importance_df['Average'] = importance_df[['Random Forest', 'XGBoost']].mean(axis=1)
importance_df = importance_df.sort_values('Average', ascending=False)

plt.figure(figsize=(12, 8))
importance_df[['Random Forest', 'XGBoost']].plot(
    kind='barh', 
    figsize=(12, 8),
    width=0.8
)
plt.yticks(range(len(importance_df)), importance_df['Feature'].tolist())
plt.title('Feature Importance Comparison: Random Forest vs XGBoost')
plt.xlabel('Importance Score')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('feature_importance_comparison.png')
print("Feature importance comparison saved to feature_importance_comparison.png")

print("\nTop 3 most important features:")
for i, row in importance_df.head(3).iterrows():
    print(f"{row['Feature']}: RF={row['Random Forest']:.4f}, XGB={row['XGBoost']:.4f}, Avg={row['Average']:.4f}")

print("\nCreating evaluation summary...")
summary = {
    'models': {
        'ann': {
            'name': 'Artificial Neural Network',
            'accuracy': 1.0,
            'regularization': 'Dropout, L2, BatchNormalization',
            'file': 'ann_model.h5'
        },
        'random_forest': {
            'name': 'Random Forest',
            'accuracy': tree_results['random_forest']['accuracy'],
            'parameters': {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'max_features': 'sqrt',
                'class_weight': 'balanced'
            },
            'file': 'random_forest_model.pkl'
        },
        'xgboost': {
            'name': 'XGBoost',
            'accuracy': tree_results['xgboost']['accuracy'],
            'parameters': {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            },
            'file': 'xgboost_model.json'
        }
    },
    'feature_importance': importance_df.to_dict(orient='records'),
    'class_distribution': {
        'original': {'fish_sauce': 815, 'garlic': 739, 'lemon': 712, 'milk': 341},
        'after_smote': {'fish_sauce': 652, 'garlic': 652, 'lemon': 652, 'milk': 652}
    },
    'preprocessing': {
        'missing_values': 'Imputed with mean',
        'scaling': 'StandardScaler',
        'class_balancing': 'SMOTE'
    }
}

with open('evaluation_summary.json', 'w') as f:
    json.dump(summary, f, indent=4)
print("Evaluation summary saved to evaluation_summary.json")

print("\nModel evaluation and comparison complete.")
