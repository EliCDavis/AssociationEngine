var Rx = require('rx');
var SocketMessageType = require('../shared/SocketMessageType');

module.exports = GraphService;

/*
 * @ngInject
 */
function GraphService(SocketConnectionService) {

    var self = this;

    self.Nodes$ = new Rx.ReplaySubject();

    self.RelationValue$ = new Rx.ReplaySubject();

    SocketConnectionService.server$[SocketMessageType.SensorAdded]
        .scan(function(allNodes, newNode) {

            console.log(newNode);

            for (var i = 0; i < allNodes.length; i++) {
                if (allNodes[i].renderData.id === newNode) {
                    return allNodes;
                }
            }

            var name = newNode.name.split(":")[0]
            var description = newNode.name.split(":")[1]

            allNodes.push({
                renderData: {
                    id: newNode.uuid,
                    color: "#" + parseInt(Math.random() * 16777214).toString(16),
                    description: description,
                    name: name
                }
            });

            return allNodes;
        }, [])
        .startWith([])
        .subscribe(self.Nodes$);

    SocketConnectionService.server$[SocketMessageType.UpdateRelationship]
        .scan(function(relationships, rel) {

            var updated = false;

            for (var relIndex = 0; relIndex < relationships.length; relIndex++) {
                var curRel = relationships[relIndex];
                if (curRel.ids[0] === rel.sensor_x && curRel.ids[1] === rel.sensor_y) {
                    updated = true;
                    console.log("update rel from: " + curRel.value + " to " + rel.value);
                    relationships[relIndex].value = rel.value;
                }
            }

            if (updated === false) {
                relationships.push({
                    ids: [rel.sensor_x, rel.sensor_y],
                    value: rel.value
                });
                console.log("new relationship: " + rel.value);
            }

            return relationships;
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