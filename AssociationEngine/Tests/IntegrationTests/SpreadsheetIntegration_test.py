import csv
from _datetime import datetime

from AssociationEngine.Sensor.Sensor import Sensor
from AssociationEngine.Snapper.Manager import Manager


def get_manager_and_sensor_data_from_cvs(filename):
    # List of (datetime, value) but datetime is still a string
    sensors_data = []

    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            sensors_data.append(row)

    manager = Manager()
    for _ in range(len(sensors_data)):
        sensor = Sensor()
        manager.add_sensor(sensor)

    return manager, sensors_data


def publish_all_sensors(manager, sensors_data):
    for i, sensor in enumerate(manager.sensors):
        datetimeStr, valueStr = sensors_data[i].pop(0)
        data = int(valueStr)
        timestamp = datetime.strptime(datetimeStr, "%Y-%m-%d %H:%M:%S")\
            .timestamp()
        sensor.publish(data, timestamp=timestamp)


if __name__ == '__main__':
    manager, sensors_data = get_manager_and_sensor_data_from_cvs("test.csv")
    while True:
        try:
            print(manager.get_value_matrix())
            publish_all_sensors(manager, sensors_data)
        except IndexError:
            break
