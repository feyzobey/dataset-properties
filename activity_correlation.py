import matplotlib.pyplot as plt
import seaborn as sns
from clean_wisdm import clean_data


def plot_activity_correlation(data, output_path=None):
    counts = data.groupby(["user_id", "activity"]).size().unstack(fill_value=0)
    corr = counts.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Activity Pairwise Correlation (by User Counts)")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_activity_correlation(data, "activity_correlation.png")
