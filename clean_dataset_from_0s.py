import pandas as pd

# CSV'yi oku
df = pd.read_csv("dataset.csv", header=None)
names = ["user_id", "activity", "timestamp", "x", "y", "z"]
df.columns = names

# Timestamp'i 0 olan satırları filtrele
df = df[df["timestamp"] != 0]

# Temizlenmiş veriyi kaydet
df.to_csv("dataset_cleaned.csv", index=False)
