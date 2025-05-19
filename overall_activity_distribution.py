import pandas as pd
import matplotlib.pyplot as plt
from clean_wisdm import clean_data

# Türkçe karakter desteği için
plt.rcParams["font.family"] = "DejaVu Sans"

# Modern ve soft renk paleti
colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99CC", "#99CCFF", "#D4A5A5", "#A5D4B5"]

data = clean_data("WISDM_ar_v1.1_raw.csv")

# Aktivite isimleri ve toplamları
activity_counts = data["activity"].value_counts()

plt.figure(figsize=(20, 8))

# 1. Bar plot (adet bazında dağılım)
plt.subplot(1, 2, 1)
bars = plt.bar(activity_counts.index, activity_counts.values, color=colors)
plt.title("Activity Distribution (Record Count)", size=14, pad=20, weight="bold")
plt.xlabel("Activity", size=12, labelpad=10)
plt.ylabel("Record Count", size=12, labelpad=10)
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Bar üstüne değerleri ekle
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{int(height):,}", ha="center", va="bottom", size=10, weight="bold")

# 2. Pie-Donut chart (yüzde bazında dağılım)
plt.subplot(1, 2, 2)
wedges, texts, autotexts = plt.pie(activity_counts.values, labels=activity_counts.index, colors=colors[: len(activity_counts)], autopct="%1.1f%%", pctdistance=0.85)
plt.setp(autotexts, size=10, weight="bold")
plt.setp(texts, size=10)
plt.title("Activity Distribution (Percentage)", size=14, pad=20, weight="bold")
# Donut görünümü için merkez çember
centre_circle = plt.Circle((0, 0), 0.70, fc="white")
plt.gca().add_artist(centre_circle)

plt.suptitle("Overall Activity Distribution", size=16, weight="bold", y=0.95)
plt.tight_layout()
plt.savefig("overall_activity_distribution1.png", dpi=300, bbox_inches="tight")
plt.close()

# Konsol özeti
print("\nOverall Summary:")
print(f"Total record count: {len(data):,}")
print("\nActivity distribution:")
for activity, count in activity_counts.items():
    percentage = (count / len(data)) * 100
    print(f"{activity}: {count:,} ({percentage:.1f}%)")
