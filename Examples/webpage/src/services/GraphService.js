var Rx = require('rx');
module.exports = GraphService;

/*
 * @ngInject
 */
function GraphService() {

    var self = this;

    // Publically exposed function
    self.exampleCall = function() {
        console.log('Example Service has been Called!');
    }

    self.Nodes$ = new Rx.ReplaySubject();

    self.Nodes$.onNext([{
        renderData: {
            color: 'red',
            name: 'sensor a',
            description: 'Sensor A Description'
        },
    }, {
        renderData: {
            color: 'green',
            name: 'sensor b',
            description: 'Sensor B Description'
        },
    }, {
        renderData: {
            color: 'blue',
            name: 'sensor c',
            description: 'Sensor C Description'
        },
    }, {
        renderData: {
            color: 'purple',
            name: 'sensor d',
            description: 'Sensor D Description'
        },
    }]);

}