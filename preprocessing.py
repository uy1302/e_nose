import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

print("Loading dataset...")
df = pd.read_csv('/home/luonguy/smell-datasets/esp32_data.csv')

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
unique, counts = np.unique(y_train_smote, return_counts=True)
for i, label in enumerate(unique):
    print(f"{label_classes[label]}: {counts[i]}")

print(f"Training set shape after SMOTE: {X_train_smote.shape}")

print("\nSaving preprocessed data...")
np.save('X_train.npy', X_train_smote)
np.save('y_train.npy', y_train_smote)
np.save('X_test.npy', X_test)
np.save('y_test.npy', y_test)

import pickle
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
with open('imputer.pkl', 'wb') as f:
    pickle.dump(imputer, f)

print("\nPreprocessing complete. Files saved.")
