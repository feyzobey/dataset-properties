import csv
import struct

ACTIVITY_MAPPING = {"Jogging": 1, "Walking": 2, "Upstairs": 3, "Downstairs": 4, "Sitting": 5, "Standing": 6}


def parse_line(line):
    fields: list = line.split(",")

    activity_label: str = fields[1].strip()
    timestamp_str: str = fields[2].strip()
    x_str: str = fields[3].strip()
    y_str: str = fields[4].strip()
    z_str: str = fields[5].strip()

    if not x_str or not y_str or not z_str:
        return None

    timestamp = int(timestamp_str.rstrip("00")) if (timestamp_str and timestamp_str.endswith("00")) else int(timestamp_str)
    x = float(x_str)
    y = float(y_str)
    z = float(z_str)

    activity = ACTIVITY_MAPPING.get(activity_label, 0)

    if timestamp == 0 and x == 0 and y == 0 and z == 0:
        return None

    return (timestamp, x, y, z, activity)


def write_to_binary(input_file, output_file):
    with open(input_file, "r") as csv_file, open(output_file, "wb") as bin_file:
        reader = csv.reader(csv_file)

        for line in reader:
            if len(line) < 6:
                continue

            try:
                result = parse_line(",".join(line))
                if result is None:
                    continue

                timestamp, x, y, z, activity = result

                packed_data = struct.pack("lfffB", timestamp, x, y, z, activity)
                bin_file.write(packed_data)
            except Exception as e:
                print(f"Error processing line {line}: {e}")


input_file = "dataset.csv"
output_file = "output.bin"

write_to_binary(input_file, output_file)
