import pandas as pd
import matplotlib.pyplot as plt

# Türkçe karakter desteği için
plt.rcParams["font.family"] = "DejaVu Sans"

# Renk paleti tanımlama
colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99CC", "#99CCFF"]

# Read the dataset
columns = ["user", "activity", "timestamp", "x-acceleration", "y-accel", "z-accel"]
data = pd.read_csv("dataset.csv", names=columns)

# Create figure with two subplots
plt.figure(figsize=(20, 8))

# 1. Bar plot for total records
plt.subplot(1, 2, 1)
activity_counts = data["activity"].value_counts()
bars = plt.bar(activity_counts.index, activity_counts.values, color=colors)
plt.title("Activity Distribution (Record Count)", size=14, pad=20, weight="bold")
plt.xlabel("Activity", size=12, labelpad=10)
plt.ylabel("Record Count", size=12, labelpad=10)
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height:,}", ha="center", va="bottom", size=10, weight="bold")

# 2. Pie chart for percentage distribution
plt.subplot(1, 2, 2)
wedges, texts, autotexts = plt.pie(activity_counts.values, labels=activity_counts.index, colors=colors, autopct="%1.1f%%", pctdistance=0.85)

# Enhance text properties
plt.setp(autotexts, size=10, weight="bold")
plt.setp(texts, size=10)
plt.title("Activity Distribution (Percentage)", size=14, pad=20, weight="bold")

# Add a circle at the center to create a donut chart
centre_circle = plt.Circle((0, 0), 0.70, fc="white")
plt.gca().add_artist(centre_circle)

# Add overall title
plt.suptitle("Overall Activity Distribution", size=16, weight="bold", y=0.95)

plt.tight_layout()
plt.savefig("overall_activity_distribution1.png", dpi=300, bbox_inches="tight")
plt.close()

# Print overall summary
print("\nOverall Summary:")
print(f"Total record count: {len(data):,}")
print("\nActivity distribution:")
for activity, count in activity_counts.items():
    percentage = (count / len(data)) * 100
    print(f"{activity}: {count:,} ({percentage:.1f}%)")
