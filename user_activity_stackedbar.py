import matplotlib.pyplot as plt
from clean_wisdm import clean_data


def plot_stacked_user_activity(data, output_path=None):
    pivot = data.groupby(["user_id", "activity"]).size().unstack(fill_value=0)
    percent = pivot.div(pivot.sum(axis=1), axis=0) * 100

    percent.plot(kind="bar", stacked=True, colormap="Set2", figsize=(16, 8), edgecolor="black", linewidth=0.3)
    plt.title("User Activity Distribution (Stacked Percentage)")
    plt.ylabel("Percentage (%)")
    plt.xlabel("User ID")
    plt.legend(title="Activity", bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=200)
    plt.show()


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_stacked_user_activity(data, "user_activity_stackedbar.png")
