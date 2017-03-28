from flask import Flask, send_file
from flask_socketio import SocketIO
from Snapper.Manager import Manager


app = Flask(__name__, static_folder='dist', static_url_path='')
io = SocketIO(app)

AEManager = Manager()


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/python/socket.io.js")
def socketio():
    return send_file("python_static/socket.io.1.7.3.min.js")


@io.on('message')
def handle_message(message):
    print("received message:", message)
    io.send(message)


@io.on('add sensor')
def add_sensor(sensor):
    print("received call to add:", sensor)
    io.send(sensor)


@io.on('remove sensor')
def remove_sensor(sensor):
    print("received call to remove:", sensor)
    io.send(sensor)


if __name__ == '__main__':
    io.run(app)
