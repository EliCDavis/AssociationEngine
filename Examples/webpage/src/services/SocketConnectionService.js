module.exports = SocketConnectionService;

/*
 * @ngInject
 */
function SocketConnectionService() {
    var self = this;

    var socket = io.connect('http://localhost:5000/');
    socket.on('connect', function () {
        socket.on('message', function (msg) {
            console.log('Got Message: ' + msg);
        });

        socket.on('sensor added', function (sensor) {
            console.log("sensor added: " + sensor);
        });
    });
}
