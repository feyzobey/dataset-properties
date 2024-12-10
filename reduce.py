import pandas as pd
import os
import gzip
import pickle


# Function to format file size
def format_size(bytes):
    units = ["Bytes", "KB", "MB", "GB"]
    size = bytes
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


# Load the dataset
file_path = "dataset.csv"
columns = ["user", "activity", "timestamp", "x-acceleration", "y-accel", "z-accel"]
data = pd.read_csv(file_path, names=columns)

# Calculate original file size
original_size = os.path.getsize(file_path)
print(f"Original file size: {format_size(original_size)}")

# Compress using pickle and gzip
pickle_file_path = "user33_dataset.pkl.gz"
with gzip.open(pickle_file_path, "wb") as f:
    pickle.dump(data, f)
pickle_size = os.path.getsize(pickle_file_path)
print(f"Pickle gzip compressed file size: {format_size(pickle_size)}")

# Summary of sizes
sizes = [original_size, pickle_size]
labels = ["Original", "Pickle"]

# Visualize compression results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(labels, sizes, color="skyblue")
plt.ylabel("File Size (Bytes)")
plt.title("File Size Comparison Across Compression Methods")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
