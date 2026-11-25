
import csv
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest

# Project location
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "sample_sensor_data.csv"

# Read sensor data
readings = []

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        readings.append([
            float(row["acceleration_x"]),
            float(row["acceleration_y"]),
            float(row["acceleration_z"]),
            float(row["sound_level"]),
            float(row["piezo_response"])
        ])

X = np.array(readings)

print("Dataset loaded:", X.shape)

# Create AI model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# Train AI
model.fit(X)

# Save trained model
model_path = Path(__file__).with_name("box_anomaly_model.pkl")
joblib.dump(model, model_path)

print("\nAI MODEL TRAINED SUCCESSFULLY!")

# Test the model
normal_sample = X[0].reshape(1, -1)

unusual_sample = np.array([[
    2.5, 2.0, 13.0, 85.0, 3.5
]])

normal_result = model.predict(normal_sample)[0]
unusual_result = model.predict(unusual_sample)[0]

print("\nNORMAL SAMPLE:")
print("Normal response" if normal_result == 1 else "Unusual response")

print("\nUNUSUAL DEMO SAMPLE:")
print("Normal response" if unusual_result == 1 else "Unusual response")

print("\nModel saved at:", model_path)
