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
            GraphService.Nodes$.combineLatest(GraphService.RelationValue$, GraphService.ObfuscateMode$).subscribe(function(data) {

                graph.clearNodes();
                graph.clearLinks();

                var nodesRendered = {};
                var nodesToRemove = {};

                data[0].forEach(function(nodeRenderData) {
                    nodesToRemove[nodeRenderData.renderData.id] = data[2] === "weak";
                });

                if (data[1].length > 0) {
                    data[1].forEach(function(line) {
                        if (line.value > 0.3) {
                            nodesToRemove[line.ids[0]] = false;
                            nodesToRemove[line.ids[0]] = false;
                        }
                    });
                }

                // Add nodes
                data[0].forEach(function(nodeRenderData) {
                    if (!nodesToRemove[nodeRenderData.renderData.id]) {
                        nodesRendered[nodeRenderData.renderData.id] = graph.createNode(nodeRenderData);
                    }
                });

                // Add connections between them
                if (data[1].length > 0) {
                    data[1].forEach(function(line) {

                        if (!nodesRendered[line.ids[0]] || !nodesRendered[line.ids[1]]) {
                            //console.log("error: ", line, nodesRendered);
                            return;
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

            graph.setDefaultNodeRenderAndMouseDetection(function(node, nodeCanvasPos, graph) {

                var mainColor = node.getRenderData()["color"];

                if (!mainColor) {
                    mainColor = "rgb(197, 23, 23)";
                }

                var ctx = graph.getContext();
                ctx.fillStyle = mainColor;
                ctx.beginPath();
                ctx.arc(nodeCanvasPos[0],
                    nodeCanvasPos[1],
                    node.getRadius() * graph.getScale() * 0.8,
                    0,
                    2 * Math.PI);
                ctx.fill();

                if (node.getRenderData()['$mouseOver']) {
                    ctx.fillStyle = "black";
                    ctx.beginPath();
                    ctx.arc(nodeCanvasPos[0],
                        nodeCanvasPos[1],
                        node.getRadius() * graph.getScale() * 0.8 * 0.5,
                        0,
                        2 * Math.PI);
                    ctx.fill();
                }

                if (node.getRenderData()['$beingDragged']) {
                    ctx.fillStyle = "white";
                    ctx.beginPath();
                    ctx.arc(nodeCanvasPos[0],
                        nodeCanvasPos[1],
                        node.getRadius() * graph.getScale() * 0.8 * 0.3,
                        0,
                        2 * Math.PI);
                    ctx.fill();
                }

                if (node.getRenderData().$mouseOver) {

                    // Make sure the mouse over box is always on top of everything.
                    graph.postRender(function() {

                        ctx.font = "16px Monospace";
                        var textDimensions = ctx.measureText(node.getRenderData()["name"]);

                        // Draw a rectangle for text.
                        ctx.fillStyle = mainColor;
                        ctx.lineWidth = 2;
                        ctx.fillRect(nodeCanvasPos[0] - 70 - textDimensions.width,
                            nodeCanvasPos[1] - 95 - 20,
                            textDimensions.width + 40, 40);

                        // Draw a line coming from the node to the rectangle
                        ctx.strokeStyle = mainColor;
                        ctx.beginPath();
                        ctx.moveTo(nodeCanvasPos[0], nodeCanvasPos[1]);
                        ctx.lineTo(nodeCanvasPos[0], nodeCanvasPos[1] - 95);
                        ctx.lineTo(nodeCanvasPos[0] - 50, nodeCanvasPos[1] - 95);
                        ctx.stroke();

                        // display the text
                        ctx.fillStyle = "black";
                        ctx.fillText(node.getRenderData()["name"], nodeCanvasPos[0] - 50 - textDimensions.width, nodeCanvasPos[1] - 95);

                    });
                }

            }, function(node, graph, mousePos) {
                return (node.distanceFrom(mousePos) <= node.getRadius() * .6);
            });

        }
    };
}