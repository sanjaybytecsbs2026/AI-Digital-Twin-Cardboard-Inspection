
import csv
import json
import joblib
import numpy as np

from pathlib import Path
from datetime import datetime

# Project paths
PROJECT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT / "data" / "sample_sensor_data.csv"
MODEL_FILE = PROJECT / "ai_model" / "box_anomaly_model.pkl"

STATE_FILE = Path(__file__).with_name("twin_state.json")

# Load the trained AI model
model = joblib.load(MODEL_FILE)

# Read sensor data
with open(DATA_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)
    readings = list(reader)

# Select the latest sample
sample = readings[-1]

# Prepare sensor values
sensor_values = [
    float(sample["acceleration_x"]),
    float(sample["acceleration_y"]),
    float(sample["acceleration_z"]),
    float(sample["sound_level"]),
    float(sample["piezo_response"])
]

# Ask AI to analyse the sample
prediction = model.predict(
    np.array(sensor_values).reshape(1, -1)
)[0]

status = "Normal response" if prediction == 1 else "Unusual response"

# Create virtual inspection station state
digital_twin = {
    "system_name": "AI Box Inspection Digital Twin",
    "sample_id": int(sample["sample_id"]),
    "last_updated": datetime.now().isoformat(timespec="seconds"),

    "physical_system": {
        "accelerometer": {
            "x": sensor_values[0],
            "y": sensor_values[1],
            "z": sensor_values[2]
        },

        "sound_level": sensor_values[3],
        "piezo_response": sensor_values[4]
    },

    "ai_analysis": {
        "prediction": int(prediction),
        "status": status
    }
}

# Save the virtual system state
with open(STATE_FILE, "w") as file:
    json.dump(digital_twin, file, indent=4)

# Display Digital Twin information
print("======================================")
print("     DIGITAL TWIN INSPECTION SYSTEM")
print("======================================")

print("\nSample ID:", digital_twin["sample_id"])

print("\nSENSOR READINGS")
print("Acceleration:", sensor_values[:3])
print("Sound level:", sensor_values[3])
print("Piezo response:", sensor_values[4])

print("\nAI ANALYSIS")
print("Inspection result:", status)

print("\nDigital Twin state saved successfully!")
print("File:", STATE_FILE)

