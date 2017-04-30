import json
from threading import Thread
from time import sleep, time

from flask import Flask, send_file
from flask_socketio import SocketIO

from AssociationEngine.Sensor.Cosine import Cosine
from AssociationEngine.Sensor.Sine import Sine
from AssociationEngine.Snapper.Manager import Manager
from AssociationEngine.Examples.webpage.Subscriber import RelationshipSubscriber


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
        for sensor_x, sensor_y in AEManager.get_all_relationships():
            subscriber = RelationshipSubscriber(sensor_x,
                                                sensor_y,
                                                lambda x: io.emit('update relationship',
                                                                  x,
                                                                  broadcast=True))
            subscribers.append(subscriber)
            AEManager.matrix.relationships[frozenset((sensor_x, sensor_y))].subscribe(subscriber)



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
    subscribe_sensors()
    unfreeze_dictionary(AEManager.get_value_matrix())


def send_sensors(new_connection=False):
    global current_sensors
    for uuid in map(lambda sensor: sensor.uuid, AEManager.sensors):
        if uuid not in current_sensors or new_connection:
            io.emit("sensor added", json.dumps(str(uuid)), broadcast=True)
    current_sensors = list(map(lambda sensor: sensor.uuid, AEManager.sensors))


def update_relationship(sensor_x, sensor_y, value, socket):
    socket.emit('update relationship', {"sensor_x": str(sensor_x),
                                    "sensor_y": str(sensor_y),
                                    "value": value}, broadcast=True)


def tick_loop():
    sin = Sine()
    cos = Cosine()
    sin.tick(time())
    cos.tick(time())
    AEManager.add_sensor(sin)
    AEManager.add_sensor(cos)
    while 1:
        sin.tick(time())
        cos.tick(time())
        sleep(1)


def unfreeze_dictionary(dictionary):
    for val1, val2 in dictionary:
        unfrozen_dictionary = {"sensor_x": str(val1),
                               "sensor_y": str(val2),
                               "value": dictionary[frozenset((val1, val2))]}
        io.emit("update relationship", unfrozen_dictionary)


if __name__ == '__main__':
    io.run(app)
