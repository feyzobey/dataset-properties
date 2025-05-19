import pandas as pd
import plotly.graph_objs as go
from clean_wisdm import clean_data


def plot_chord_user_activity(data, users):
    user_counts = data["user_id"].value_counts().sort_index()
    selected_users = user_counts.index[:users]
    df = data[data["user_id"].isin(selected_users)]
    activity_list = sorted(df["activity"].unique())
    user_list = sorted(selected_users)
    # Matrix: rows=user, cols=activity, value=count
    matrix = pd.crosstab(df["user_id"], df["activity"]).reindex(index=user_list, columns=activity_list, fill_value=0)
    # Chord için özel paketler de var, ama Plotly'nin heatmap'iyle benzer sunum:
    fig = go.Figure(data=go.Heatmap(z=matrix.values, x=matrix.columns, y=[f"User {u}" for u in matrix.index], colorscale="blues", hoverongaps=False))
    fig.update_layout(title="Chord-like Matrix: User vs Activity Connections", xaxis_title="Activity", yaxis_title="User ID", autosize=False, width=1440, height=900)
    fig.write_html("user_activity_chord.html")


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_chord_user_activity(data, users=36)
