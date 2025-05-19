import matplotlib.pyplot as plt
import seaborn as sns

from clean_wisdm import clean_data


def plot_user_activity_distribution(data, output_path=None):
    # Kullanıcı ve aktiviteye göre kayıt sayısı
    pivot_count = data.groupby(["user_id", "activity"]).size().unstack(fill_value=0)
    # Yüzdelik (her kullanıcı toplamına böl)
    pivot_percent = pivot_count.div(pivot_count.sum(axis=1), axis=0) * 100

    fig, axes = plt.subplots(1, 2, figsize=(24, 12))
    # Adet heatmap
    sns.heatmap(pivot_count, annot=True, fmt="d", cmap="YlOrRd", ax=axes[0], cbar_kws={"label": "Number of Records"})
    axes[0].set_title("Activity Distribution by User (Record Count)")
    axes[0].set_xlabel("Activity Type")
    axes[0].set_ylabel("User ID")
    # Yüzde heatmap
    sns.heatmap(pivot_percent, annot=True, fmt=".1f", cmap="YlOrRd", ax=axes[1], cbar_kws={"label": "Percentage (%)"})
    axes[1].set_title("Activity Distribution by User (Percentage)")
    axes[1].set_xlabel("Activity Type")
    axes[1].set_ylabel("User ID")

    fig.suptitle("User Activity Distribution Analysis", fontsize=18)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    if output_path:
        plt.savefig(output_path, dpi=200)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_user_activity_distribution(data, output_path="heat_map_user_activity_distribution.png")
