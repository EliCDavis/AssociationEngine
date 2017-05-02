import csv
from datetime import datetime
from itertools import zip_longest


def formatted_csv_reader():
    with open('processed_noaa_weather_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data_sorted_by_date = []
        sensors = []
        for i, row in enumerate(reader):
            sensors.append(row[0])
            for timestamp, value in grouper(row[1:], 2):
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                value = int(value)
                data_sorted_by_date.append((timestamp, i, value))
    data_sorted_by_date.sort()
    return sensors, data_sorted_by_date


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


if __name__ == '__main__':
    print(formatted_csv_reader()[0])
