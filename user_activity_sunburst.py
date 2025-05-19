import pandas as pd
import plotly.express as px
from clean_wisdm import clean_data


def plot_sunburst_user_activity(data, output_path=None):
    count = data.groupby(["user_id", "activity"]).size().reset_index(name="count")
    fig = px.sunburst(
        count, path=["user_id", "activity"], values="count", color="activity", color_discrete_sequence=px.colors.qualitative.Pastel, title="User & Activity Distribution (Sunburst Chart)"
    )
    fig.update_traces(textinfo="label+percent entry")
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
    fig.write_html(output_path)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_sunburst_user_activity(data, "user_activity_sunburst.html")
