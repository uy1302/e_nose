import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.regularizers import l2
import matplotlib.pyplot as plt
import pickle
import json
from config import config

print("Loading preprocessed data...")
# Load data using config paths
formatted_data_path = config.get_path('paths', 'data', 'formatted_data')
X_train = np.load(formatted_data_path / 'X_train.npy')
y_train = np.load(formatted_data_path / 'y_train.npy')
X_test = np.load(formatted_data_path / 'X_test.npy')
y_test = np.load(formatted_data_path / 'y_test.npy')

# Load label encoder using config path
with open(config.get_preprocessing_path('label_encoder'), 'rb') as f:
    label_encoder = pickle.load(f)
    
num_classes = len(label_encoder.classes_)
print(f"Number of classes: {num_classes}")
print(f"Classes: {label_encoder.classes_}")

print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")

y_train_onehot = keras.utils.to_categorical(y_train, num_classes)
y_test_onehot = keras.utils.to_categorical(y_test, num_classes)

np.random.seed(42)
tf.random.set_seed(42)

print("\nBuilding ANN model with regularization...")
model = Sequential([
    Dense(64, activation='relu', kernel_regularizer=l2(0.001), input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.3),
    
    Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.4),
    
    Dense(64, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.3),
    
    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True,
    verbose=1
)

model_checkpoint = ModelCheckpoint(
    filepath=str(config.get_model_path('ann_best')),
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

print("\nTraining ANN model...")
history = model.fit(
    X_train, y_train_onehot,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint],
    verbose="auto"
)

print("\nEvaluating ANN model on test data...")
test_loss, test_accuracy = model.evaluate(X_test, y_test_onehot, verbose="auto")
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Test loss: {test_loss:.4f}")

model.save(str(config.get_model_path('ann')))
print(f"ANN model saved to {config.get_model_path('ann')}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.tight_layout()
plot_path = config.get_path('paths', 'docs') / 'ann_training_history.png'
plt.savefig(str(plot_path))
print(f"Training history plot saved to {plot_path}")

y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)

from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

report_path = config.get_path('paths', 'data', 'processed') / 'ann_classification_report.json'
with open(str(report_path), 'w') as f:
    json.dump(report, f)
print(f"Classification report saved to {report_path}")

print("ANN training and evaluation complete.")
