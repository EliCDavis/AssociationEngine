import datetime
import json
from threading import Thread
from time import sleep

from flask import Flask, send_file
from flask_socketio import SocketIO

from AssociationEngine.Examples.webpage.ReadFromCSV import formatted_csv_reader
from AssociationEngine.Examples.webpage.Subscriber import \
    RelationshipSubscriber
from AssociationEngine.Sensor.Sensor import Sensor
from AssociationEngine.Snapper.Manager import Manager

AEManager = Manager()
AEManager.set_window_size(20000)
app = Flask(__name__, static_folder='dist', static_url_path='')
app.debug = True
io = SocketIO(app, logger=True, debug=True, async_mode="eventlet")
ticker = None
subscribers = []


def subscribe_sensors():
    if subscribers == []:
        relationships = AEManager.get_all_relationships()
        print(relationships)
        for sensor_x, sensor_y in relationships:
            subscriber = RelationshipSubscriber(str(AEManager.reverse_route_map[str(sensor_x)]),
                                                str(AEManager.reverse_route_map[str(sensor_y)]),
                                                lambda x: io.emit('update relationship',
                                                                  x,
                                                                  broadcast=True))
            subscribers.append(subscriber)
            relationships[frozenset((sensor_x, sensor_y))].subscribe(subscriber)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/python/socket.io.js")
def get_socketio_js():
    return send_file("python_static/socket.io.1.7.3.min.js")


@io.on("connect_failed")
def failed_connect():
    print("The connection failed, idk what to do now.")


@io.on('error')
def fucked_up():
    print('\nyou fucked up.\n')


@io.on("connect")
def client_connected():
    print("New Connection")
    global ticker

    if ticker is None:
        ticker = io.start_background_task(target=tick_loop)
        io.sleep(2)
    send_sensors()
    unfreeze_dictionary(AEManager.get_value_matrix())


@io.on("disconnect")
def client_disconnected():
    print("Client Disconnected")


def send_sensors():
    for sensor in AEManager.sensors:
        io.emit("sensor added", {
            "uuid": str(sensor.uuid),
            "name": str(sensor)
        }, broadcast=True)


def tick_loop():
    sensors, sensor_data = formatted_csv_reader()

    for sensor_name in sensors:
        AEManager.add_sensor(Sensor(name=sensor_name))

    subscribe_sensors()

    simtimestamp = sensor_data[0][0]
    lastTimestamp = sensor_data[-1][0]
    print("Starting at timestamp", simtimestamp)
    print("Ending at timestamp", lastTimestamp)
    print("Length of", lastTimestamp-simtimestamp)
    print("Starting Simulation")

    i = 0  # I'm indexing sensor_data instead of popping to save the rams
    while i < len(sensor_data):
        while simtimestamp > sensor_data[i][0]:
            timestamp, sensorIndex, value = sensor_data[i]
            #print("Publishing", value, "on sensor", sensorIndex, "at time",
             #     timestamp)
            AEManager.sensors[sensorIndex].publish(
                value, timestamp=timestamp.timestamp()
            )

            i += 1
            if i >= len(sensor_data):
                break

        simtimestamp += datetime.timedelta(hours=1)
        print("stepping to:", simtimestamp)
        io.sleep(.5)

    print("Simulation Complete")


def unfreeze_dictionary(dictionary):
    for val1, val2 in dictionary:
        unfrozen_dictionary = {"sensor_x": str(AEManager.reverse_route_map[str(val1)]),
                               "sensor_y": str(AEManager.reverse_route_map[str(val2)]),
                               "value": dictionary[frozenset((val1, val2))]}
        io.emit("update relationship", unfrozen_dictionary)


if __name__ == '__main__':
    io.run(app, host="0.0.0.0")
