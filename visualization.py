# +  Label Encoding
# +  Linear Interpolation -> bu kodda yapılıyor
# +  Data Split -> 80-20 yapılıyor
# +  Normalization -> ayrı dosyada yapılacak
# +  Segmentation -> ayrı dosyada yapılacak
# +  One-Hot Encoding
#   Data Augmentation

import pandas as pd
import os
import random
import numpy as np

columns = ["user_id", "activity", "timestamp", "x", "y", "z"]


def clean_data(input_csv):
    """Veri temizleme ve düzenleme."""
    data = pd.read_csv(input_csv, on_bad_lines="skip", header=None, names=columns)
    # data = data.dropna()
    # data = data.drop_duplicates()
    # Fazladan `;` karakterlerini temizle
    data = data.replace(";", "", regex=True)
    # Tüm sayısal kolonları float64'e çevir
    data[["timestamp", "x", "y", "z"]] = data[["timestamp", "x", "y", "z"]].astype(float)

    # timestamp, x, y ve z aynı anda 0.0 ise hepsini NaN yap
    mask = (data["timestamp"] == 0.0) & (data["x"] == 0.0) & (data["y"] == 0.0) & (data["z"] == 0.0)
    data.loc[mask, ["timestamp", "x", "y", "z"]] = np.nan

    # Linear interpolation
    # Kullanıcı + Aktivite bazlı grup ve interpolate
    data[["timestamp", "x", "y", "z"]] = data.groupby(["user_id", "activity"])[["timestamp", "x", "y", "z"]].transform(lambda group: group.interpolate(method="linear"))
    # Hâlâ kalan nan varsa sil (başta veya sonda olabilir)
    data = data.dropna()
    return data


def split_and_save_data(df, test_user_id: int, output_dir=".") -> tuple:

    # timestamp'ı int yap
    df["timestamp"] = df["timestamp"].astype(np.int64)

    loso_test_df = pd.DataFrame(df[df["user_id"] == test_user_id], columns=columns)
    loso_train_df = pd.DataFrame(df[df["user_id"] != test_user_id], columns=columns)
    train80, test20 = split_80_20(df, test_user_id)

    os.makedirs(output_dir, exist_ok=True)

    # Leave-one-subject-out için dosya isimlendirme
    loso_train_filename = os.path.join(output_dir, f"{test_user_id}_loso_train.csv")
    loso_test_filename = os.path.join(output_dir, f"{test_user_id}_loso_test.csv")

    # 80-20 bölme için dosya isimlendirme
    split_train_filename = os.path.join(output_dir, f"{test_user_id}_train80.csv")
    split_test_filename = os.path.join(output_dir, f"{test_user_id}_test20.csv")

    loso_test_df.to_csv(loso_test_filename, index=False, header=False, encoding="utf-8")
    loso_train_df.to_csv(loso_train_filename, index=False, header=False, encoding="utf-8")

    train80.to_csv(split_train_filename, index=False, header=False, encoding="utf-8")
    test20.to_csv(split_test_filename, index=False, header=False, encoding="utf-8")


def split_80_20(data, user_id):

    data = data[data["user_id"] == user_id]
    data = data.sort_values("timestamp")

    # Divide data into chunks of 20 samples
    chunk_size = 20
    chunks = [data.iloc[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Randomly shuffle the chunks
    random.shuffle(chunks)

    # Calculate split point (80% of chunks)
    split_index = int(len(chunks) * 0.8)

    # Split chunks into train and test sets
    train_chunks = chunks[:split_index]
    test_chunks = chunks[split_index:]

    # Concatenate chunks back into DataFrames
    train_data = pd.concat(train_chunks) if train_chunks else pd.DataFrame(columns=data.columns)
    test_data = pd.concat(test_chunks) if test_chunks else pd.DataFrame(columns=data.columns)

    return train_data, test_data


if __name__ == "__main__":
    data_path = "WISDM_ar_v1.1_raw.csv"
    output_dir = "split_data_diff_2"
    os.makedirs(output_dir, exist_ok=True)
    data = clean_data(data_path)
    for i in range(1, 37):
        print(f"Processing User {i}")
        split_and_save_data(data, i, output_dir)
