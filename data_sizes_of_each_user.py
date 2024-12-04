import pandas as pd
import matplotlib.pyplot as plt


def format_size(bytes):
    units = ["Bytes", "KB", "MB", "GB"]
    size = bytes
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


file_path = "clean_dataset.csv"
columns = ["user", "activity", "timestamp", "x-acceleration", "y-accel", "z-accel"]
data = pd.read_csv(file_path, names=columns)

# group by user and calculate the memory usage of each user's data
user_sizes = data.groupby("user").apply(lambda x: x.memory_usage(deep=True).sum())

# convert sizes to the most significant unit
user_sizes = user_sizes.reset_index()
user_sizes.columns = ["user", "size_in_bytes"]
user_sizes["formatted_size"] = user_sizes["size_in_bytes"].apply(format_size)

print(user_sizes[["user", "formatted_size"]])

plt.figure(figsize=(10, 6))
plt.bar(user_sizes["user"].astype(str), user_sizes["size_in_bytes"], color="skyblue")
plt.xlabel("User")
plt.ylabel("Data Size (MB)")
plt.title("Data Size by User")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
