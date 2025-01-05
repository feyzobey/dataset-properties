import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
columns = ["user", "activity", "timestamp", "x-acceleration", "y-accel", "z-accel"]
data = pd.read_csv("dataset.csv", names=columns)

# Create a pivot table for the heatmap
pivot_data = pd.pivot_table(data, values="timestamp", index="user", columns="activity", aggfunc="count", fill_value=0)

# Calculate percentages for each user
pivot_data_pct = pivot_data.div(pivot_data.sum(axis=1), axis=0) * 100

# Create a figure with two subplots
plt.figure(figsize=(20, 10))

# 1. Heatmap showing record counts
plt.subplot(1, 2, 1)
sns.heatmap(pivot_data, annot=True, fmt=",d", cmap="YlOrRd", cbar_kws={"label": "Number of Records"})
plt.title("Activity Distribution by User (Record Count)", size=14, pad=20)
plt.xlabel("Activity Type", size=12)
plt.ylabel("User ID", size=12)

# 2. Heatmap showing percentages
plt.subplot(1, 2, 2)
sns.heatmap(pivot_data_pct, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "Percentage (%)"})
plt.title("Activity Distribution by User (Percentage)", size=14, pad=20)
plt.xlabel("Activity Type", size=12)
plt.ylabel("User ID", size=12)

plt.suptitle("User Activity Distribution Analysis", size=16, y=1.02)
plt.tight_layout()
plt.savefig("user_activity_distribution1.png", dpi=300, bbox_inches="tight")
plt.close()

# Print summary for each user
print("\nUser-wise Summary:")
for user in sorted(data["user"].unique()):
    user_data = data[data["user"] == user]
    print(f"\nUser {user}:")
    print(f"Total records: {len(user_data):,}")
    print("Activity distribution:")
    activity_summary = user_data["activity"].value_counts()
    for activity, count in activity_summary.items():
        percentage = (count / len(user_data)) * 100
        print(f"{activity}: {count:,} ({percentage:.1f}%)")
