import pandas as pd
import os


def split_and_save_data(data_path: str, test_user_id: int, output_dir=".") -> tuple:
    columns = ["user_id", "activity", "timestamp", "x", "y", "z"]

    df = pd.read_csv(data_path, names=columns)

    test_df = pd.DataFrame(df[df["user_id"] == test_user_id], columns=columns)
    train_df = pd.DataFrame(df[df["user_id"] != test_user_id], columns=columns)

    os.makedirs(output_dir, exist_ok=True)

    test_filename = os.path.join(output_dir, f"{test_user_id}_test.csv")
    train_filename = os.path.join(output_dir, f"{test_user_id}_training.csv")

    test_df.to_csv(test_filename, index=False, header=False, encoding="utf-8")

    train_df.to_csv(train_filename, index=False, header=False, encoding="utf-8")


if __name__ == "__main__":
    data_path = "dataset.csv"
    output_dir = "split_data"
    for i in range(1, 37):
        split_and_save_data(data_path, i, output_dir)
