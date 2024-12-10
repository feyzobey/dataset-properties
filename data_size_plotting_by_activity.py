import pickle
import gzip
import matplotlib.pyplot as plt
import pandas as pd

file_path = "user33_dataset.pkl.gz"
with gzip.open(file_path, "rb") as f:
    data = pickle.load(f)

activity_stats = data.groupby("activity").apply(
    lambda x: {"row_count": len(x), "size_in_bytes": x.memory_usage(deep=True).sum()}
)
activity_stats = pd.DataFrame(activity_stats.tolist(), index=activity_stats.index)

activity_stats["size_in_kb"] = activity_stats["size_in_bytes"] / 1024

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.bar(
    activity_stats.index,
    activity_stats["row_count"],
    color="skyblue",
    label="Row Count",
    alpha=0.7,
)
ax1.set_xlabel("Activity")
ax1.set_ylabel("Number of Rows", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()
ax2.plot(
    activity_stats.index,
    activity_stats["size_in_kb"],
    color="orange",
    marker="o",
    label="Size (KB)",
    linewidth=2,
)
ax2.set_ylabel("Size (KB)", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")

plt.title("Data Size and Row Count by Activity")
fig.tight_layout()
plt.grid(axis="x", linestyle="--", alpha=0.7)

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.show()
