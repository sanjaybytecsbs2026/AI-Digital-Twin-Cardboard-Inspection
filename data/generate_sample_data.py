
import csv
import random
from pathlib import Path

random.seed(42)

number_of_samples = 100

output_file = Path(__file__).with_name("sample_sensor_data.csv")

with open(output_file, "w", newline="") as file:

    writer = csv.writer(file)

    # CSV column headings
    writer.writerow([
        "sample_id",
        "acceleration_x",
        "acceleration_y",
        "acceleration_z",
        "sound_level",
        "piezo_response"
    ])

    # Generate simulated sensor readings
    for sample_id in range(1, number_of_samples + 1):

        acceleration_x = random.gauss(0, 0.2)
        acceleration_y = random.gauss(0, 0.2)
        acceleration_z = random.gauss(9.8, 0.2)

        sound_level = random.gauss(50, 3)
        piezo_response = random.gauss(1.5, 0.1)

        writer.writerow([
            sample_id,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            sound_level,
            piezo_response
        ])

print("BOX INSPECTION SENSOR SIMULATOR")
print("--------------------------------")
print("Total readings generated:", number_of_samples)
print("CSV file created successfully!")
print("File location:", output_file)

