import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import random

columns = ["user_id", "activity", "timestamp", "x", "y", "z"]


def clean_data(input_csv):
    data = pd.read_csv(input_csv, on_bad_lines="skip", header=None, names=columns)
    data = data.replace(";", "", regex=True)
    data[["timestamp", "x", "y", "z"]] = data[["timestamp", "x", "y", "z"]].astype(float)

    mask = (data["timestamp"] == 0.0) & (data["x"] == 0.0) & (data["y"] == 0.0) & (data["z"] == 0.0)
    data.loc[mask, ["timestamp", "x", "y", "z"]] = np.nan

    data[["timestamp", "x", "y", "z"]] = data.groupby(["user_id", "activity"])[["timestamp", "x", "y", "z"]].transform(lambda group: group.interpolate(method="linear"))

    return data.dropna()


def split_80_20(data, user_id):
    user_data = data[data["user_id"] == user_id].sort_values("timestamp")
    chunk_size = 20
    chunks = [user_data.iloc[i : i + chunk_size] for i in range(0, len(user_data), chunk_size)]
    random.shuffle(chunks)
    split_index = int(len(chunks) * 0.8)
    train_chunks = chunks[:split_index]
    return pd.concat(train_chunks) if train_chunks else pd.DataFrame(columns=data.columns)


def plot_activity_distribution(df_group, user_range):
    pivot_count = df_group.pivot_table(index="user_id", columns="activity", aggfunc="size", fill_value=0)
    pivot_percent = pivot_count.div(pivot_count.sum(axis=1), axis=0) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 12))

    sns.heatmap(pivot_count, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5, ax=ax1, cbar_kws={"label": "Number of Records"})
    ax1.set_title(f"Activity Distribution (Users {user_range}) - Count")
    ax1.set_xlabel("Activity Type")
    ax1.set_ylabel("User ID")

    sns.heatmap(pivot_percent, cmap="YlOrRd", annot=True, fmt=".1f", linewidths=0.5, ax=ax2, cbar_kws={"label": "Percentage (%)"})
    ax2.set_title(f"Activity Distribution (Users {user_range}) - Percentage")
    ax2.set_xlabel("Activity Type")
    ax2.set_ylabel("User ID")

    plt.suptitle(f"User Activity Distribution Heatmap – Users {user_range}", fontsize=18)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


# Ana çalışma akışı
def main():
    data_path = "WISDM_ar_v1.1_raw.csv"  # CSV dosya adı
    data = clean_data(data_path)

    # Kullanıcıları 3 gruba ayır
    for group_start in [1, 13, 25]:
        group_end = group_start + 11
        user_data = []

        for user_id in range(group_start, group_end + 1):
            train80 = split_80_20(data, user_id)
            train80["user_id"] = user_id
            user_data.append(train80)

        df_group = pd.concat(user_data, ignore_index=True)
        plot_activity_distribution(df_group, f"{group_start}–{group_end}")


if __name__ == "__main__":
    main()
