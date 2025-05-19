import numpy as np
import matplotlib.pyplot as plt
from clean_wisdm import clean_data


def plot_activity_radar(data, output_path=None):
    means = data.groupby("activity")[["x", "y", "z"]].mean()
    categories = list(means.columns)
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    for i, (act, row) in enumerate(means.iterrows()):
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, label=act, linewidth=2)
        ax.fill(angles, values, alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_yticklabels([])
    plt.title("Mean Sensor Values by Activity (Radar Chart)", fontsize=16)
    plt.legend(bbox_to_anchor=(1.2, 1.05), loc="upper right")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_activity_radar(data, "activity_radar.png")
