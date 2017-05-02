var SocketMessageType = require('../shared/SocketMessageType');
var Rx = require('rx');

module.exports = SocketConnectionService;

/*
 * @ngInject
 */
function SocketConnectionService() {

    var self = this;

    var _socket = io.connect();

    self.server$ = {};
    /*
        _socket.on('event name', (data) => {
            console.log(data);
        })*/

    new Rx.Observable.interval(1000).subscribe((x) => {
        _socket.emit('pinggg', 'fuck');
    });

    var _addClientMessageStream = function(messageType) {

        var newStream = new Rx.ReplaySubject(1);

        _socket.on(messageType, function(message) {
            newStream.onNext(message);
        });

        self.server$[messageType] = newStream;
    };

    for (var messageType in SocketMessageType) {
        _addClientMessageStream(SocketMessageType[messageType]);
    }

}