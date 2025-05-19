import matplotlib.pyplot as plt
import pandas as pd
from clean_wisdm import clean_data


def plot_user_activity_line(data, output_path=None):
    counts = data.groupby(["user_id", "activity"]).size().unstack(fill_value=0)
    plt.figure(figsize=(15, 8))
    for activity in counts.columns:
        plt.plot(counts.index, counts[activity], label=activity)
    plt.xlabel("User ID")
    plt.ylabel("Record Count")
    plt.title("Activity Count per User")
    plt.legend()
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_user_activity_line(data, "line_chart_user_activity_distribution.png")
