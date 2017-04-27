var SocketMessageType = require('../shared/SocketMessageType');

module.exports = SocketConnectionService;

/*
 * @ngInject
 */
function SocketConnectionService() {

    var self = this;
    var sensors = [];

    var _socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    self.server$ = {};


    var _addClientMessageStream = function(messageType) {

        var newStream = new Rx.ReplaySubject(1);

        _socket.on(messageType, function(message) {
            newStream.onNext(message);
        });

        self.server$[messageType] = newStream;
    }

    for (var messageType in SocketMessageType) {
        _addClientMessageStream(SocketMessageType[messageType]);
    }


    _socket.on("sensor added", function(sensor) {
       console.log(sensors.indexOf(sensor));
       if (sensors.indexOf(sensor)==-1){
           console.log("Sensor added " + sensor);
           sensors.push(sensor);
       }
    });

    _socket.on("update relationship", function(data){
       console.log("Updataing relationship \n" +
                    "Sensor_x: "+ data.sensor_x +"\n" +
                    "Sensor_y: "+ data.sensor_y +"\n" +
                    "Value: " + data.value);
    });

}