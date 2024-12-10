import pickle
import gzip
import matplotlib.pyplot as plt

# Load the compressed pickle gzip file
file_path = "user33_dataset.pkl.gz"
with gzip.open(file_path, "rb") as f:
    data = pickle.load(f)

# Check the dataset structure
# print(data.head())

# Plot the data by activities
plt.figure(figsize=(10, 6))
activities = data["activity"].unique()

for activity in activities:
    activity_data = data[data["activity"] == activity]
    plt.scatter(
        activity_data["x-acceleration"],
        activity_data["y-accel"],
        label=activity,
        alpha=0.6,
    )

# Customize the plot
plt.title("Activity Data Plot")
plt.xlabel("X-Acceleration")
plt.ylabel("Y-Acceleration")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
