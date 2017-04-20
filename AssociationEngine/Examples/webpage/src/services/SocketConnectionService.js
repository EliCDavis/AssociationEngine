var SocketMessageType = require('../shared/SocketMessageType');

module.exports = SocketConnectionService;

/*
 * @ngInject
 */
function SocketConnectionService() {

    var self = this;

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

}