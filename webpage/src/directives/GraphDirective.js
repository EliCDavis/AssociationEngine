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

            GraphService.Nodes$.subscribe(function(nodes) {
                nodes.forEach(function(nodeRenderData) {
                    graph.createNode(nodeRenderData);
                });
            });


        }
    };
}