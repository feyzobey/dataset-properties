import pandas as pd
import numpy as np


def clean_data(input_csv):
    columns = ["user_id", "activity", "timestamp", "x", "y", "z"]
    data = pd.read_csv(input_csv, on_bad_lines="skip", header=None, names=columns, sep=",")
    data = data.replace(";", "", regex=True)
    data["user_id"] = data["user_id"].astype(int)
    data["activity"] = data["activity"].astype(str)
    data[["timestamp", "x", "y", "z"]] = data[["timestamp", "x", "y", "z"]].astype(float)
    mask = (data["timestamp"] == 0.0) & (data["x"] == 0.0) & (data["y"] == 0.0) & (data["z"] == 0.0)
    data.loc[mask, ["timestamp", "x", "y", "z"]] = np.nan
    data = data.sort_values(by=["user_id", "timestamp"])
    data[["timestamp", "x", "y", "z"]] = data.groupby("user_id")[["timestamp", "x", "y", "z"]].transform(lambda group: group.interpolate(method="linear"))
    data = data.dropna()
    return data

