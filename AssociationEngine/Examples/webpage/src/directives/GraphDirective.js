module.exports = GraphDirective;

var NodeView = require('NodeView');
var Rx = require('rx');

function GraphDirective() {
    return {
        'restrict': 'E',
        'templateUrl': 'partial/directives/graph.html',
        'controller': /*@ngInject*/ function($element, GraphService) {

            var self = this;
            var canvas = $element.find('canvas')[0];
            var graph = new NodeView(canvas);

            graph.setOption('applyGravity', false);
            //graph.setOption('centerOnNodes', false);

            // Render most recent data.
            GraphService.Nodes$.combineLatest(GraphService.RelationValue$).subscribe(function(data) {

                graph.clearNodes();
                graph.clearLinks();

                var nodesRendered = {};

                // Add nodes
                data[0].forEach(function(nodeRenderData) {
                    nodesRendered[nodeRenderData.renderData.id] = graph.createNode(nodeRenderData);
                });


                // Add connections between them
                if (data[1].length > 0) {
                    data[1].forEach(function(line) {

                        if (!nodesRendered[line.ids[0]] || !nodesRendered[line.ids[1]]) {
                            console.log("error: ", line, nodesRendered);
                            //return;
                        }


                        graph.linkNodes(nodesRendered[line.ids[0]], nodesRendered[line.ids[1]], {
                            relationship: line.value
                        });
                    });
                }

            });

            // Override line renderer to make lines thicker with stronger relationships
            graph.setLinkRenderMethod(function(graph, point1, point2, link) {

                if (link.linkData.relationship <= 0.1) {
                    return;
                }

                var ctx = graph.getContext();
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 25 * graph.getScale() * link.linkData.relationship;
                ctx.beginPath();
                ctx.moveTo(point1[0], point1[1]);
                ctx.lineTo(point2[0], point2[1]);
                ctx.stroke();
            });


        }
    };
}