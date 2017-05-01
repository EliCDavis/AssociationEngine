import json
from threading import Thread
from time import sleep, time

from flask import Flask, send_file
from flask_socketio import SocketIO


from AssociationEngine.Sensor.Sensor import Sensor
from AssociationEngine.Snapper.Manager import Manager
from AssociationEngine.Examples.webpage.Subscriber import RelationshipSubscriber
from AssociationEngine.Examples.webpage.ReadFromCSV import formatted_csv_reader

current_sensors = []
sensors = []
sensor_pairs = []
AEManager = Manager()
app = Flask(__name__, static_folder='dist', static_url_path='')
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
        ticker.start()

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
    data = formatted_csv_reader()
    for x in range(len(data)):
        sensors.append(Sensor())
        AEManager.add_sensor(sensors[x])
    timestamp = 0
    for i in range(min([len(n) for n in data])):
        for sensor in range(len(sensors)):
            sensors[sensor].publish(data[sensor][timestamp]['date'],
                                    data[sensor][timestamp]['value'])
        timestamp += 1
        sleep(10)


def unfreeze_dictionary(dictionary):
    for val1, val2 in dictionary:
        unfrozen_dictionary = {"sensor_x": str(val1),
                               "sensor_y": str(val2),
                               "value": dictionary[frozenset((val1, val2))]}
        io.emit("update relationship", unfrozen_dictionary)


if __name__ == '__main__':
    subscribe_sensors()
    io.run(app)
