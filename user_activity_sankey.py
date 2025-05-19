import pandas as pd
import plotly.graph_objects as go
from clean_wisdm import clean_data


def plot_sankey_user_activity(data, output_path=None, users=None):
    # Min_user: çok kalabalıkta sadece ilk N kullanıcıyı göster (örn: 10)
    user_counts = data["user_id"].value_counts().sort_index()
    if users:
        selected_users = user_counts.index[:users]
        df = data[data["user_id"].isin(selected_users)]
    else:
        df = data

    user_list = sorted(df["user_id"].unique())
    activity_list = sorted(df["activity"].unique())
    user_nodes = [f"User {u}" for u in user_list]
    activity_nodes = activity_list
    nodes = user_nodes + activity_nodes

    node_indices = {name: idx for idx, name in enumerate(nodes)}
    links = []
    for user in user_list:
        for act in activity_list:
            count = len(df[(df["user_id"] == user) & (df["activity"] == act)])
            if count > 0:
                links.append({"source": node_indices[f"User {user}"], "target": node_indices[act], "value": count})

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(pad=15, thickness=18, line=dict(color="black", width=0.5), label=nodes, color=["#98d7e4"] * len(user_nodes) + ["#f6c7b6"] * len(activity_nodes)),
                link=dict(source=[l["source"] for l in links], target=[l["target"] for l in links], value=[l["value"] for l in links], color="rgba(160,160,240,0.4)"),
            )
        ]
    )
    fig.update_layout(title_text="Sankey: User to Activity Flow", font_size=14)
    fig.write_html(output_path)


if __name__ == "__main__":
    data = clean_data("WISDM_ar_v1.1_raw.csv")
    plot_sankey_user_activity(data, output_path="user_activity_sankey.html", users=36)
