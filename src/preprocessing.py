import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import pickle
from config import config

print("Loading dataset...")
# Load dataset from processed data directory
data_path = config.get_path('paths', 'data', 'processed') / 'esp32_data.csv'
df = pd.read_csv(str(data_path))

print(f"Dataset shape: {df.shape}")
print("\nClass distribution before preprocessing:")
print(df['label'].value_counts())

print("\nChecking for missing values...")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

print("\nDropping unnecessary columns...")
df = df.drop(['Unnamed: 0', 'DATE', 'TIME'], axis=1)

print("\nEncoding target variable...")
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['label'])
y = np.array(y)  # Ensure y is numpy array

label_classes = label_encoder.classes_
print(f"Classes: {label_classes}")
print(f"Encoded as: {np.unique(y)}")

X = df.drop('label', axis=1)

print("\nHandling missing values...")
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

print("\nScaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

print("\nSplitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

print("\nApplying SMOTE to handle class imbalance...")
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("\nClass distribution after SMOTE:")
unique_labels, label_counts = np.unique(y_train_smote, return_counts=True)
for i, label in enumerate(unique_labels):
    print(f"{label_classes[label]}: {label_counts[i]}")

print(f"Training set shape after SMOTE: {X_train_smote.shape}")

print("\nSaving preprocessed data...")
# Save formatted data using config paths
formatted_data_path = config.get_path('paths', 'data', 'formatted_data')
np.save(str(formatted_data_path / 'X_train.npy'), X_train_smote)
np.save(str(formatted_data_path / 'y_train.npy'), y_train_smote)
np.save(str(formatted_data_path / 'X_test.npy'), X_test)
np.save(str(formatted_data_path / 'y_test.npy'), y_test)

# Save preprocessing objects using config paths
with open(str(config.get_preprocessing_path('scaler')), 'wb') as f:
    pickle.dump(scaler, f)
with open(str(config.get_preprocessing_path('label_encoder')), 'wb') as f:
    pickle.dump(label_encoder, f)
with open(str(config.get_preprocessing_path('imputer')), 'wb') as f:
    pickle.dump(imputer, f)

print("\nPreprocessing complete. Files saved.")
