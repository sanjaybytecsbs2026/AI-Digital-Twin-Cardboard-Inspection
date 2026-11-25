
import csv
import statistics
from pathlib import Path

# Locate the CSV file
project_folder = Path(__file__).resolve().parent.parent
input_file = project_folder / "data" / "sample_sensor_data.csv"

# Store sensor readings
acceleration_x = []
acceleration_y = []
acceleration_z = []
sound_levels = []
piezo_responses = []

# Read the CSV file
with open(input_file, "r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:
        acceleration_x.append(float(row["acceleration_x"]))
        acceleration_y.append(float(row["acceleration_y"]))
        acceleration_z.append(float(row["acceleration_z"]))
        sound_levels.append(float(row["sound_level"]))
        piezo_responses.append(float(row["piezo_response"]))

# Calculate sensor statistics
print("===================================")
print(" BOX INSPECTION - DATA ANALYSIS")
print("===================================")

print("\nTotal samples:", len(acceleration_x))

print("\nACCELEROMETER ANALYSIS")
print("Average X:", round(statistics.mean(acceleration_x), 3))
print("Average Y:", round(statistics.mean(acceleration_y), 3))
print("Average Z:", round(statistics.mean(acceleration_z), 3))

print("\nSOUND ANALYSIS")
print("Average sound level:", round(statistics.mean(sound_levels), 3))
print("Maximum sound level:", round(max(sound_levels), 3))

print("\nPIEZO SENSOR ANALYSIS")
print("Average piezo response:", round(statistics.mean(piezo_responses), 3))
print("Maximum piezo response:", round(max(piezo_responses), 3))

print("\nData analysis completed successfully!")
