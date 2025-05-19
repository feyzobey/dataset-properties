import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from clean_wisdm import clean_data


def facet_user_activity(data, output_path=None):
    # Kullanıcı-Aktivite bazında kayıt sayısı
    summary = data.groupby(["activity", "user_id"]).size().reset_index(name="count")
    g = sns.FacetGrid(summary, col="activity", col_wrap=3, height=4, sharex=False, sharey=False)
    g.map_dataframe(sns.barplot, x="user_id", y="count", palette="crest", edgecolor=".6")
    g.set_titles(col_template="{col_name}")
    g.set_axis_labels("User ID", "Record Count")
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(90)
    plt.subplots_adjust(top=0.85)
    g.fig.suptitle("User Distribution per Activity", fontsize=18)
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    facet_user_activity(data, "facet_user_activity.png")
