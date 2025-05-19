import matplotlib.pyplot as plt
import seaborn as sns
from clean_wisdm import clean_data


def plot_user_total_records(data, output_path=None):
    user_counts = data["user_id"].value_counts().sort_index()
    plt.figure(figsize=(12, 8))
    sns.barplot(y=user_counts.index, x=user_counts.values, orient="h", palette="viridis")
    plt.xlabel("Total Records")
    plt.ylabel("User ID")
    plt.title("Total Records per User")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_user_total_records(data, "bar_chart_row_count.png")
