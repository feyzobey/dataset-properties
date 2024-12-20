import struct
import pandas as pd

STRUCT_FORMAT = "lfffB"

activity_map = {"Jogging": 1, "Walking": 2, "Sitting": 3, "Downstairs": 4, "Standing": 5, "Upstairs": 6}


def clean_data(input_csv):
    data = pd.read_csv(input_csv, on_bad_lines="skip", header=None)
    data = data.dropna()
    data = data.drop_duplicates()

    data = data.replace(";", "", regex=True)
    return data


def filter_by_id(data, selected_id):
    filtered_data = data[data[0] == selected_id]
    return filtered_data


def process_csv(filtered_data, output_bin, output_c):
    c_data = []

    with open(output_bin, "wb") as bin_file, open(output_c, "w") as c_file:
        for index, row in filtered_data.iterrows():
            try:
                timestamp = int(int(row[2]) // 1000000)
                x = float(row[3])
                y = float(row[4])
                z = float(row[5])
                activity = activity_map.get(row[1], 255)

                packed_data = struct.pack(STRUCT_FORMAT, timestamp, x, y, z, activity)
                bin_file.write(packed_data)

                c_data.extend(packed_data)

            except ValueError as ve:
                print(f"Değer hatası (satır {index + 1}): {row} -> {ve}")
            except Exception as e:
                print(f"Beklenmeyen hata (satır {index + 1}): {row} -> {e}")

        # C array dosyası yaz
        c_array = ", ".join(f"0x{byte:02X}" for byte in c_data)
        c_file.write("const uint8_t data_array[] = {\n")
        c_file.write(f"    {c_array}\n")
        c_file.write("};\n")


if __name__ == "__main__":
    input_csv = "dataset.csv"
    output_bin = "data.bin"
    output_c = "data_array.c"

    selected_id = int(input("İşlenecek ID'yi girin: "))

    cleaned_data = clean_data(input_csv)

    filtered_data = filter_by_id(cleaned_data, selected_id)

    process_csv(filtered_data, output_bin, output_c)
    print("İşlem tamamlandı.")
