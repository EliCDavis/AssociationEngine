import csv
from datetime import datetime
from operator import itemgetter

# Each field will turn into an individual sensor for each station
FIELDS = [
    "HOURLYDRYBULBTEMPF",
    "HOURLYWETBULBTEMPF",
    "HOURLYDewPointTempF"
]


def main():
    station_data = {}
    with open("noaa_weather_data.csv", newline='') as inCSV:
        reader = csv.DictReader(inCSV)

        for row in reader:
            if row["REPORTTPYE"] != "FM-15":  # This misspelling is intentional
                continue

            station_name = row["STATION_NAME"]

            if station_name not in station_data:
                station_data[station_name] = []

            data = tuple(map(lambda f: row[f], FIELDS))

            station_data[station_name].append(
                (datetime.strptime(row["DATE"], "%Y-%m-%d %H:%M"),
                 *data)
            )

    # A likely unnecessary sorting step if all the data in the file is in order
    for station_name in station_data:
        print(station_name)
        station_data[station_name].sort()

    with open("processed_noaa_weather_data.csv", 'w', newline='') as outCSV:
        writer = csv.writer(outCSV)

        for station_name in station_data:
            for i in range(1, len(FIELDS) + 1):
                writer.writerow(list(
                    map(itemgetter(i), station_data[station_name])
                ))


if __name__ == '__main__':
    main()
