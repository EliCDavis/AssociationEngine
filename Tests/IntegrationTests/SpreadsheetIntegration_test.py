import csv

from Sensor.Sensor import Sensor
from Snapper.Manager import Manager


def get_manager_and_sensor_data_from_cvs(filename):
    sensors_data = []

    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            sensors_data.append(list(map(int, row)))

    manager = Manager()
    for _ in range(len(sensors_data)):
        sensor = Sensor()
        manager.add_sensor(sensor)

    return manager, sensors_data


def publish_all_sensors(manager, sensors_data):
    for i, sensor in enumerate(manager.sensors):
        data = sensors_data[i].pop(0)
        sensor.publish(data)


if __name__ == '__main__':
    manager, sensors_data = get_manager_and_sensor_data_from_cvs("test.csv")
    while True:
        try:
            print(manager.get_value_matrix())
            publish_all_sensors(manager, sensors_data)
        except IndexError:
            break
