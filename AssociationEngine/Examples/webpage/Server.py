import json
from threading import Thread

from flask import Flask, send_file
from flask_socketio import SocketIO

from AssociationEngine.Sensor.Cosine import Cosine
from AssociationEngine.Sensor.Sine import Sine
from AssociationEngine.Snapper.Manager import Manager

app = Flask(__name__, static_folder='dist', static_url_path='')
io = SocketIO(app)
AEManager = Manager()
thread = None


@app.route("/")
def index():
    global thread
    if thread is None:
        thread = Thread(target=setup_Manager)
        thread.start()
        
    return app.send_static_file('index.html')


@app.route("/python/socket.io.js")
def socketio():
    return send_file("python_static/socket.io.1.7.3.min.js")


@io.on("connect")
def client_connected():
    print("New Connection")
    for uuid in map(lambda sensor: sensor.uuid, AEManager.sensors):
        io.emit("sensor added", json.dumps(str(uuid)), broadcast=False)
    io.emit("relationships", json.dumps(AEManager.get_value_matrix()), broadcast=False)

def update_relationship(sensor_x, sensor_y, value):
    io.emit('update relationship', {"sensor_x": sensor_x,
                                    "sensor_y": sensor_y,
                                    "value": value})


def setup_Manager():
    global AEManager
    AEManager.add_sensor(Sine())
    AEManager.add_sensor(Cosine())
    print("setup done")


if __name__ == '__main__':
    io.run(app)
    setup_Manager()
