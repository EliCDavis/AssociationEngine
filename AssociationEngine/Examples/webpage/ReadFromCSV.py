from datetime import datetime
import csv

def formatted_csv_reader():
    epoch = datetime.utcfromtimestamp(0)
    with open('processed_noaa_weather_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        grouped_data = []
        row_count = 0
        for row in reader:
            item = 0
            grouped_data.append([])
            while item < len(row):
                grouped_data[row_count].append({"Time": str((datetime.strptime(row[item], '%Y-%m-%d %H:%M:%S')-epoch).total_seconds()), "Value": row[item+1]})
                item += 2
            row_count += 1

    return grouped_data

formatted_csv_reader()