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

current_sensors = []
sensors = []
sensor_pairs = []
AEManager = Manager()
AEManager.set_window_size(60000)
app = Flask(__name__, static_folder='dist', static_url_path='')
app.debug = True
io = SocketIO(app, logger=True, debug=True)
ticker = None
subscribers = []


def subscribe_sensors():
    if subscribers == []:
        relationships = AEManager.get_all_relationships()
        for sensor_x, sensor_y in relationships:
            subscriber = RelationshipSubscriber(sensor_x,
                                                sensor_y,
                                                lambda x: io.emit('update relationship',
                                                                  x,
                                                                  broadcast=True))
            subscribers.append(subscriber)
            relationships[frozenset((sensor_x, sensor_y))].subscribe(subscriber)



@app.route("/")
def index():
    global ticker

    if ticker is None:
        ticker = Thread(target=tick_loop)
        ticker.daemon = True
        ticker.start()
        sleep(2)
        subscribe_sensors()
    return app.send_static_file('index.html')


@app.route("/python/socket.io.js")
def socketio():
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
    send_sensors(new_connection=True)

    unfreeze_dictionary(AEManager.get_value_matrix())


@io.on("disconnect")
def client_disconnected():
    print("Client Disconnected")


def send_sensors(new_connection=False):
    global current_sensors
    for uuid in map(lambda sensor: sensor.uuid, AEManager.sensors):
        if uuid not in current_sensors or new_connection:
            io.emit("sensor added", json.dumps(str(uuid)), broadcast=True)
    current_sensors = list(map(lambda sensor: sensor.uuid, AEManager.sensors))


def tick_loop():
    numSensors, sensor_data = formatted_csv_reader()
    print(numSensors)

    for _ in range(numSensors):
        AEManager.add_sensor(Sensor())

    timestamp = sensor_data[0][0]
    lastTimestamp = sensor_data[-1][0]
    print("Starting at timestamp", timestamp)
    print("Ending at timestamp", lastTimestamp)
    print("Length of", lastTimestamp-timestamp)
    print("Starting Simulation")

    i = 0  # I'm indexing sensor_data instead of popping to save the rams
    while i < len(sensor_data):
        while timestamp <= sensor_data[i][0]:
            timestamp, sensorIndex, value = sensor_data[i]
            print("Publishing", value, "on sensor", sensorIndex, "at time",
                  timestamp)
            AEManager.sensors[sensorIndex].publish(
                value, timestamp=timestamp.timestamp()
            )

            i += 1
            if i > len(sensor_data):
                break

        timestamp += datetime.timedelta(hours=1)

    print("Simulation Complete")


def unfreeze_dictionary(dictionary):
    for val1, val2 in dictionary:
        unfrozen_dictionary = {"sensor_x": str(val1),
                               "sensor_y": str(val2),
                               "value": dictionary[frozenset((val1, val2))]}
        io.emit("update relationship", unfrozen_dictionary)


if __name__ == '__main__':
    io.run(app)
