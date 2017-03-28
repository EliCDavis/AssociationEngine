module.exports = SocketConnectionService;

/*
 * @ngInject
 */
function SocketConnectionService() {
    var self = this;

    var socket = io.connect('http://localhost:5000/');
    socket.on('connect', function () {
        socket.send('hi');

        socket.on('message', function (msg) {
            console.log('Got Message: ' + msg);
        });

        self.add_sensor = function (sensor) {
            socket.emit("add sensor", sensor);
        }

        self.remove_sensor = function (sensor) {
            socket.emit("remove sensor", sensor);
        }
    });
}
