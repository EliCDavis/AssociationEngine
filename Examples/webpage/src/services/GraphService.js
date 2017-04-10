var Rx = require('rx');
var SocketMessageType = require('../shared/SocketMessageType');

module.exports = GraphService;

/*
 * @ngInject
 */
function GraphService(SocketConnectionService) {

    var self = this;

    // Publically exposed function
    self.exampleCall = function() {
        console.log('Example Service has been Called!');
    }

    self.Nodes$ = new Rx.ReplaySubject();

    self.RelationValue$ = new Rx.ReplaySubject();

    SocketConnectionService.server$[SocketMessageType.SensorAdded]
        .scan(function(allNodes, newNode) {

            console.log(newNode);

            allNodes.push({
                renderData: {
                    id: newNode,
                    color: "#" + parseInt(Math.random() * 16777214).toString(16),
                    description: 'hey',
                    name: 'whyd i do a name'
                }
            });

            return allNodes;
        }, [])
        .startWith([])
        .subscribe(self.Nodes$);

    SocketConnectionService.server$[SocketMessageType.UpdateRelationship]
        .scan(function(relationships, rel) {
            relationships.push(rel)
        }, [])
        .startWith([])
        .subscribe(self.RelationValue$);

    /*self.RelationValue$.onNext([{
        ids: ['a', 'b'],
        value: 0.7
    }, {
        ids: ['a', 'c'],
        value: 0.1
    }, {
        ids: ['c', 'd'],
        value: 0.4
    }]);*/

    /**
     [{
        renderData: {
            color: 'red',
            name: 'sensor a',
            description: 'Sensor A Description',
            id: 'a'
        },
    }, {
        renderData: {
            color: 'green',
            name: 'sensor b',
            description: 'Sensor B Description',
            id: 'b'
        },
    }, {
        renderData: {
            color: 'blue',
            name: 'sensor c',
            description: 'Sensor C Description',
            id: 'c'
        },
    }, {
        renderData: {
            color: 'purple',
            name: 'sensor d',
            description: 'Sensor D Description',
            id: 'd'
        },
    }]
     */

}